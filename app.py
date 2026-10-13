"""
app.py — Servidor Flask do AcademIA
"""
from estatisticas import calcular_resumo_progresso
import os
import re
from datetime import date
from dotenv import load_dotenv
from flask import (
    Flask, jsonify, render_template,
    request, send_from_directory, session,
)
from werkzeug.utils import secure_filename

from bot import Bot
from database import Database
from exercicios import get_exercicios_por_local

load_dotenv()

app = Flask(__name__, template_folder=".")
# A chave da sessão é uma configuração privada e não deve ficar no código.
app.secret_key = os.getenv("FLASK_SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("Defina FLASK_SECRET_KEY no arquivo .env antes de iniciar o app.")

db = Database()
bot = Bot()

PASTA_FOTOS = "fotos"
os.makedirs(PASTA_FOTOS, exist_ok=True)


def usuario_atual():
    return session.get("usuario_id", "anonimo")


def calcular_nivel(total_treinos):
    """Nível sobe a cada 5 treinos."""
    return max(1, (total_treinos // 5) + 1)


# ── Login ─────────────────────────────────────────────────────────────────────

@app.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    nome_usuario = dados.get("usuario", "").strip().lower().replace(" ", "_")
    nome_exibicao = dados.get("usuario", "").strip()
    if not nome_usuario:
        return jsonify({"erro": "Nome inválido"}), 400
    session["usuario_id"] = nome_usuario
    session["nome_exibicao"] = nome_exibicao

    # O nome digitado na tela de login já entra direto no Perfil (se ainda
    # não houver um nome salvo), assim o chat também já sabe quem é o
    # usuário sem precisar perguntar de novo.
    perfil = db.carregar_perfil(nome_usuario)
    if not perfil.get("nome"):
        perfil["nome"] = nome_exibicao
        db.salvar_perfil(nome_usuario, perfil)

    return jsonify({"status": "ok", "usuario": nome_usuario})


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"status": "ok"})


@app.route("/sessao_atual")
def sessao_atual():
    uid = session.get("usuario_id")
    nome = session.get("nome_exibicao", "")
    return jsonify({"logado": uid is not None, "usuario": uid, "nome": nome})


# ── Página principal ──────────────────────────────────────────────────────────

@app.route("/")
def home():
    return render_template("index.html")


def _grupo_para_interface(grupo):
    """Converte o grupo do catálogo para a categoria exibida na página."""
    grupo = grupo.lower()
    if "peito" in grupo:
        return "💪 Peito"
    if "costas" in grupo or "lombar" in grupo:
        return "🏋️ Costas"
    if any(parte in grupo for parte in ("quadriceps", "gluteos", "posteriores", "adutores", "panturrilha")):
        return "🦵 Pernas"
    if "ombros" in grupo:
        return "🤸 Ombros"
    if "biceps" in grupo or "triceps" in grupo:
        return "💥 Bíceps e Tríceps"
    return "🔥 Abdômen e Core"


@app.route("/catalogo_exercicios")
def catalogo_exercicios():
    """Entrega à página o mesmo catálogo usado pelo bot."""
    local = request.args.get("local", "academia").lower().strip()
    if local not in ("academia", "casa"):
        local = "academia"

    exercicios = []
    for exercicio in get_exercicios_por_local(local):
        video_match = re.search(
            r"(?:[?&]v=|youtu\.be/)([\w-]+)",
            exercicio.get("video", ""),
        )
        exercicios.append({
            "grupo": _grupo_para_interface(exercicio["grupo"]),
            "nome": exercicio["nome"],
            "meta": exercicio["series_reps"],
            "videoId": video_match.group(1) if video_match else "",
        })
    return jsonify({"local": local, "exercicios": exercicios})


# ── Chat ──────────────────────────────────────────────────────────────────────

@app.route("/carregar_historico_chat")
def carregar_historico_chat():
    uid = usuario_atual()
    historico = db.carregar_historico(uid)
    mensagens = [
        {"role": m["role"], "content": m["content"]}
        for m in historico
        if m["role"] in ("user", "assistant") and m.get("content")
    ]
    return jsonify({"mensagens": mensagens})


@app.route("/enviar_mensagem", methods=["POST"])
def enviar_mensagem():
    uid = usuario_atual()
    dados = request.get_json()
    mensagem_usuario = dados.get("mensagem", "")

    historico = db.carregar_historico(uid)
    perfil = db.carregar_perfil(uid)
    resposta_bot = bot.responder(mensagem_usuario, historico, perfil)

    # 1. Tenta extrair a avaliação física
    avaliacao = bot.extrair_avaliacao(resposta_bot)
    if avaliacao:
        if "data" not in avaliacao:
            avaliacao["data"] = str(date.today())
        db.salvar_avaliacao(uid, avaliacao)

    # 2. Captura o plano de treino customizado enviado pela IA
    plano_gerado = bot.extrair_plano(resposta_bot)
    if plano_gerado:
        db.salvar_plano_treino(uid, plano_gerado)

    # 3. Captura dados de perfil que o usuário contou durante a conversa
    #    (chat -> perfil) e mescla com o que já existia no perfil salvo.
    perfil_extraido = bot.extrair_perfil(resposta_bot) or {}
    # Para dados objetivos (idade, peso, altura etc.), a própria mensagem do
    # usuário também é lida. Isso evita perder atualizações se a IA não emitir
    # o marcador de perfil em uma resposta específica.
    perfil_extraido.update(bot.extrair_perfil_da_mensagem(mensagem_usuario))
    if perfil_extraido:
        perfil.update(perfil_extraido)
        db.salvar_perfil(uid, perfil)

    resposta_limpa = bot.limpar_marcador(resposta_bot)
    # O texto visível é montado a partir do plano que acabou de ser validado.
    # Isso garante que o que aparece no chat seja o mesmo que a aba Planos usa.
    if plano_gerado:
        resposta_limpa = bot.formatar_plano_para_usuario(plano_gerado)

    historico.append({"role": "user", "content": mensagem_usuario})
    historico.append({"role": "assistant", "content": resposta_limpa})
    db.salvar_historico(uid, historico)

    return jsonify({
        "resposta": resposta_limpa,
        "plano_gerado": bool(plano_gerado),
        "perfil_atualizado": bool(perfil_extraido)
    })


@app.route("/obter_plano_customizado")
def obter_plano_customizado():
    uid = usuario_atual()
    plano = db.carregar_plano_treino(uid)
    return jsonify({"plano": plano})


# ── Concluir treino ───────────────────────────────────────────────────────────

@app.route("/concluir_treino", methods=["POST"])
def concluir_treino():
    uid = usuario_atual()
    dados = request.get_json()
    treino = dados.get("treino", "A")
    
    # 1. Pega a nota enviada pelo Javascript
    nota = dados.get("nota", 5)

    # Guarda datas no formato ISO, igual ao usado pelos cálculos do gráfico.
    hoje_str = date.today().isoformat()
    hoje_exibicao = date.today().strftime('%d/%m/%Y')

    # 2. Salva a nota real recebida no dicionário de avaliação
    avaliacao = {
        "data": hoje_str,
        "nota": int(nota),
        "treino": treino
    }
    db.salvar_avaliacao(uid, avaliacao)

    # Inserir a confirmação no histórico do chat para manter consistência
    historico = db.carregar_historico(uid)
    historico.append({"role": "user", "content": f"Concluí o Treino {treino} pela aba de Planos com nota {nota}."})
    historico.append({"role": "assistant", "content": f"Sensacional! Registrei seu Treino {treino} de hoje ({hoje_exibicao}) com nota {nota}/5 com sucesso por aqui! 💪 O seu gráfico de progresso já foi atualizado."})
    db.salvar_historico(uid, historico)

    # Calcula novo nível
    avaliacoes = db.carregar_avaliacoes(uid)
    total = len(avaliacoes)
    nivel = calcular_nivel(total)

    return jsonify({
        "status": "ok",
        "totalTreinos": total,
        "nivel": nivel,
        "mensagem": f"Treino {treino} concluído! 💪"
    })


# ── Perfil ────────────────────────────────────────────────────────────────────

@app.route("/carregar_perfil")
def carregar_perfil():
    return jsonify(db.carregar_perfil(usuario_atual()))


@app.route("/salvar_perfil", methods=["POST"])
def salvar_perfil():
    uid = usuario_atual()
    dados = request.get_json()
    perfil_atual = db.carregar_perfil(uid)
    perfil_atual.update(dados)
    db.salvar_perfil(uid, perfil_atual)
    return jsonify({"status": "ok"})


# ── Foto de perfil ────────────────────────────────────────────────────────────

@app.route("/upload_foto", methods=["POST"])
def upload_foto():
    if "foto" not in request.files:
        return jsonify({"erro": "Nenhum arquivo"}), 400
    arquivo = request.files["foto"]
    uid = usuario_atual()
    nome_seguro = f"{uid}_{secure_filename(arquivo.filename)}"
    caminho = os.path.join(PASTA_FOTOS, nome_seguro)
    arquivo.save(caminho)
    perfil = db.carregar_perfil(uid)
    perfil["foto"] = nome_seguro
    db.salvar_perfil(uid, perfil)
    return jsonify({"caminho": nome_seguro})


@app.route("/fotos/<nome_arquivo>")
def servir_foto(nome_arquivo):
    return send_from_directory(PASTA_FOTOS, nome_arquivo)


# ── Progresso ─────────────────────────────────────────────────────────────────

@app.route("/dados_progresso")
def dados_progresso():
    uid = usuario_atual()
    avaliacoes = db.carregar_avaliacoes(uid)
    resumo = calcular_resumo_progresso(avaliacoes)
    resumo["avaliacoes"] = avaliacoes
    resumo["nivel"] = calcular_nivel(resumo["totalTreinos"])
    resumo["proximoNivel"] = calcular_nivel(resumo["totalTreinos"]) * 5
    return jsonify(resumo)


# ── Inicialização ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=5001)
