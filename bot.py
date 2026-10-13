"""
bot.py — O cérebro do AcademIA
Usando OpenAI (gpt-4o-mini) com datas dinâmicas no padrão brasileiro (DD-MM-AAAA),
mas salvando internamente em formato universal (AAAA-MM-DD) para não quebrar o gráfico.
"""

import os
import re
import json
from datetime import date, timedelta
from openai import OpenAI
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT
from exercicios import get_contexto_exercicios, get_exercicios_por_local

load_dotenv()


class Bot:
    def __init__(self):
        self.cliente = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.modelo = "gpt-4o-mini"

    def _detectar_local_treino(self, historico: list) -> str:
        for msg in historico:
            if msg.get("role") == "user":
                conteudo = msg.get("content", "").lower()
                if "academia" in conteudo:
                    return "academia"
                if "casa" in conteudo:
                    return "casa"
        return None

    def extrair_perfil_da_mensagem(self, mensagem: str) -> dict:
        """Lê dados objetivos informados diretamente pelo usuário no chat.

        É um complemento ao marcador da IA: cobre frases usuais sem alterar
        campos quando a informação não estiver explícita.
        """
        texto = mensagem.lower().replace(",", ".")
        perfil = {}

        idade = re.search(r"\b(?:tenho|idade(?:\s+é|:)?)[^\d]{0,12}(\d{1,3})\s*anos\b", texto)
        if idade:
            valor = int(idade.group(1))
            if 10 <= valor <= 120:
                perfil["idade"] = valor

        peso = re.search(
            r"\b(?:(?:meu|minha)\s+)?(?:peso(?:\s+(?:é|atual|de))?|estou com|tenho)\s*"
            r"(\d{2,3}(?:\.\d{1,2})?)\s*(?:kg|quilo|quilos)\b",
            texto,
        )
        if peso:
            perfil["peso"] = float(peso.group(1))

        altura = re.search(
            r"\b(?:(?:minha\s+)?altura\s*(?:é|de|:)?\s*(?:de\s*)?|meço|tenho)\s*"
            r"(\d(?:\.\d{1,2})|\d{3})\s*(m|cm)\b",
            texto,
        )
        if altura:
            valor = float(altura.group(1))
            perfil["altura"] = int(valor * 100) if altura.group(2) == "m" else int(valor)

        dias = re.search(
            r"\b(?:trein(?:o|arei|ar)[^\d]{0,20}([2-5])\s*dias?|([2-5])\s*dias?\s+(?:por|na)\s+semana)\b",
            texto,
        )
        if dias:
            perfil["dias"] = int(dias.group(1) or dias.group(2))

        if re.search(r"\b(?:em casa|na minha casa|treinar em casa)\b", texto):
            perfil["local"] = "casa"
        elif re.search(r"\bacademia\b", texto):
            perfil["local"] = "academia"

        if "ganhar massa" in texto or "hipertrofia" in texto:
            perfil["objetivo"] = "ganhar_massa"
        elif "emagrecer" in texto or "perder peso" in texto:
            perfil["objetivo"] = "emagrecer"
        elif "condicionamento" in texto or "resistência" in texto:
            perfil["objetivo"] = "condicionamento"

        if re.search(r"\b(?:sem|não tenho|nao tenho)\s+(?:lesões|lesoes|limitações|limitacoes)\b", texto):
            perfil["limitacoes"] = "Nenhuma"
        else:
            limitacao = re.search(r"\b(?:tenho|sinto)\s+(dor\s+(?:no|na)\s+[a-záéíóúçãõ]+)\b", texto)
            if limitacao:
                perfil["limitacoes"] = limitacao.group(1)

        return perfil

    def _montar_bloco_perfil(self, perfil: dict) -> str:
        """Formata os dados salvos na aba Perfil para injetar no prompt,
        para que a IA sempre 'enxergue' o que o usuário já preencheu lá."""
        if not perfil:
            return ""

        campos = [
            ("nome", "Nome"),
            ("idade", "Idade"),
            ("peso", "Peso (kg)"),
            ("altura", "Altura (cm)"),
            ("objetivo", "Objetivo"),
            ("local", "Local de treino"),
            ("dias", "Dias de treino por semana"),
            ("limitacoes", "Limitações físicas"),
        ]
        linhas = [
            f"- {rotulo}: {perfil[chave]}"
            for chave, rotulo in campos
            if perfil.get(chave) not in (None, "", "None")
        ]
        if not linhas:
            return ""

        return (
            "\n\n════════════════════════════════════════\n"
            "DADOS JÁ PREENCHIDOS PELO USUÁRIO NA ABA 'MEU PERFIL' DO APP:\n"
            + "\n".join(linhas) +
            "\nNÃO peça novamente essas informações se elas já estiverem aqui — use-as diretamente. "
            "Só pergunte o que estiver faltando na lista de coleta de perfil."
        )

    def responder(self, mensagem_usuario, historico, perfil=None):
        try:
            perfil = perfil or {}

            # Prioriza o local salvo na aba Perfil; só usa o que foi dito no
            # chat como fallback (compatibilidade com conversas antigas).
            local = perfil.get("local") or self._detectar_local_treino(historico)

            if local:
                contexto_exercicios = get_contexto_exercicios(local)
                system_completo = SYSTEM_PROMPT + "\n\n" + contexto_exercicios
            else:
                system_completo = SYSTEM_PROMPT

            system_completo += self._montar_bloco_perfil(perfil)

            # Calcula as datas no momento do envio
            hoje = date.today()
            ontem = hoje - timedelta(days=1)
            anteontem = hoje - timedelta(days=2)

            # Formata as datas no padrão brasileiro DD-MM-AAAA
            hoje_br = hoje.strftime('%d-%m-%Y')
            ontem_br = ontem.strftime('%d-%m-%Y')
            anteontem_br = anteontem.strftime('%d-%m-%Y')

            # Regra dinâmica adaptada para o padrão do Brasil
            instrucao_data = (
                f"\n\n════════════════════════════════════════\n"
                f"REGRA CRÍTICA DE REGISTRO DE TREINO:\n"
                f"Sempre que o usuário confirmar um treino, você DEVE incluir obrigatoriamente no FINAL da resposta o marcador oculto:\n"
                f"[AVALIACAO: nota=X treino=Y data=DD-MM-AAAA]\n"
                f"- Considere estritamente que HOJE é {hoje.strftime('%d/%m/%Y')}.\n"
                f"- Se o usuário não citar dia, ou disser 'hoje', use data={hoje_br}.\n"
                f"- Se disser 'ontem', use data={ontem_br}.\n"
                f"- Se disser 'anteontem', use data={anteontem_br}.\n"
                f"- Se disser uma data específica (ex: '02/07/2026'), converta rigidamente para o formato data=DD-MM-AAAA.\n"
            )
            system_completo += instrucao_data

            mensagens = [{"role": "system", "content": system_completo}]
            mensagens.extend(historico)
            
            conteudo_usuario = mensagem_usuario
            palavras_chave = ["treino", "fiz", "conclui", "concluí", "nota", "1", "2", "3", "4", "5", "/", "ontem", "anteontem"]
            
            if any(palavra in mensagem_usuario.lower() for palavra in palavras_chave):
                conteudo_usuario += "\n\n(Lembrete de sistema: Lembre-se de gerar a tag [AVALIACAO: nota=X treino=Y data=DD-MM-AAAA] no final, incluindo a data retroativa no formato brasileiro se eu tiver mencionado uma)."

            mensagens.append({"role": "user", "content": conteudo_usuario})

            print(f"[AcademIA] 🤖 Processando sua mensagem...")
            
            resposta = self.cliente.chat.completions.create(
                model=self.modelo,
                messages=mensagens,
                # O plano possui a lista visível e um JSON técnico para o app.
                # Mantemos espaço suficiente para os dois trechos na resposta.
                max_tokens=1600,
                temperature=0.3
            )

            texto = resposta.choices[0].message.content
            print(f"[AcademIA] 💬 Texto gerado pela IA (incluindo tag oculta):\n{texto}\n")
            return texto

        except Exception as erro:
            print(f"[AcademIA] ❌ Erro na função responder: {erro}")
            return "Desculpe, tive um problema para processar essa resposta. Tente novamente."

    def extrair_avaliacao(self, texto_resposta):
        try:
            padrao_tag = r"\[AVALIA[CÇ][AÃ]O:(.*?)\]"
            tag_match = re.search(padrao_tag, texto_resposta, re.IGNORECASE)
            
            if tag_match:
                conteudo = tag_match.group(1)
                
                nota_match = re.search(r"nota\s*[=:]\s*(\d)", conteudo, re.IGNORECASE)
                treino_match = re.search(r"treino\s*[=:]\s*([a-zA-Z])", conteudo, re.IGNORECASE)
                data_match = re.search(r"data\s*[=:]\s*([\d]{2}-[\d]{2}-[\d]{2,4})", conteudo, re.IGNORECASE)
                
                if nota_match and treino_match:
                    dados = {
                        "nota": int(nota_match.group(1)),
                        "treino": treino_match.group(1).upper()
                    }
                    
                    if data_match:
                        data_br = data_match.group(1)
                        # Traduz DD-MM-AAAA para AAAA-MM-DD para o gráfico funcionar!
                        partes = data_br.split('-')
                        if len(partes) == 3:
                            dados["data"] = f"{partes[2]}-{partes[1]}-{partes[0]}"
                        else:
                            dados["data"] = data_br
                    
                    print(f"[AcademIA] 🎯 TAG LIDA E TRADUZIDA PARA O GRÁFICO: {dados}")
                    return dados
                    
            print("[AcademIA] ⚠️ Nenhuma avaliação capturada no texto.")
            return None
        except Exception as e:
            print(f"[AcademIA] ❌ Erro ao extrair avaliação: {e}")
            return None

    def extrair_perfil(self, texto_resposta):
        """
        Lê o marcador oculto [PERFIL: {...}] que a IA gera sempre que o
        usuário conta/atualiza um dado pessoal durante a conversa (idade,
        peso, altura, objetivo, dias de treino, local, limitações...) e
        devolve um dicionário para ser mesclado no perfil salvo no app,
        fazendo o caminho chat -> perfil funcionar.
        """
        try:
            inicio_tag = texto_resposta.find("[PERFIL:")
            if inicio_tag == -1:
                return None

            inicio_json = texto_resposta.find("{", inicio_tag)
            if inicio_json == -1:
                return None

            decoder = json.JSONDecoder()
            dados_brutos, _fim_json = decoder.raw_decode(texto_resposta, inicio_json)

            campos_validos = {"nome", "idade", "peso", "altura", "objetivo",
                               "local", "dias", "limitacoes"}
            perfil = {
                chave: valor for chave, valor in dados_brutos.items()
                if chave in campos_validos and valor not in (None, "")
            }

            if "local" in perfil:
                perfil["local"] = str(perfil["local"]).lower().strip()

            if not perfil:
                return None

            print(f"[AcademIA] 🙋 PERFIL ATUALIZADO PELO CHAT: {perfil}")
            return perfil
        except Exception as e:
            print(f"[AcademIA] ❌ Erro ao extrair perfil: {e}")
            return None

    def extrair_plano(self, texto_resposta):
        """
        Lê o marcador oculto [PLANO: {...}] gerado pela IA, valida os nomes
        dos exercícios contra o catálogo real (exercicios.py) e devolve um
        dicionário já enriquecido com grupo muscular, séries/reps e o ID do
        vídeo do YouTube — nunca confiamos em dados que a IA "inventou".
        """
        try:
            # A IA pode variar espaços e maiúsculas/minúsculas. Procuramos o
            # marcador de forma tolerante, mas continuamos exigindo o JSON
            # estruturado para não tentar adivinhar exercícios no texto livre.
            marcador = re.search(r"\[\s*PLANO\s*:", texto_resposta, re.IGNORECASE)
            if not marcador:
                return None

            inicio_json = texto_resposta.find("{", marcador.end())
            if inicio_json == -1:
                return None

            # raw_decode lida corretamente com chaves aninhadas (diferente de regex)
            decoder = json.JSONDecoder()
            plano_bruto, _fim_json = decoder.raw_decode(texto_resposta, inicio_json)

            dias = plano_bruto.get("dias")
            local = str(plano_bruto.get("local", "")).lower().strip()
            treinos_nomes = plano_bruto.get("treinos", {})

            if not isinstance(dias, int) or dias not in (2, 3, 4, 5):
                print("[AcademIA] ⚠️ Plano com número de dias inválido, ignorando.")
                return None

            if not isinstance(treinos_nomes, dict) or local not in ("academia", "casa"):
                print("[AcademIA] ⚠️ Plano sem 'local' ou 'treinos' válidos, ignorando.")
                return None

            catalogo = get_exercicios_por_local(local)
            catalogo_por_nome = {e["nome"]: e for e in catalogo}

            treinos_enriquecidos = {}
            for letra, nomes in treinos_nomes.items():
                letra = str(letra).upper().strip()
                if letra not in "ABCDE" or not isinstance(nomes, list):
                    continue
                lista = []
                for nome in nomes:
                    if not isinstance(nome, str):
                        continue
                    exercicio = catalogo_por_nome.get(nome)
                    if not exercicio:
                        # Busca por similaridade: aceita se um nome contém o outro
                        nome_lower = nome.lower().strip()
                        for nome_catalogo, ex_catalogo in catalogo_por_nome.items():
                            nc_lower = nome_catalogo.lower()
                            if nome_lower in nc_lower or nc_lower in nome_lower:
                                exercicio = ex_catalogo
                                print(f"[AcademIA] 🔍 '{nome}' mapeado para '{nome_catalogo}' por similaridade.")
                                break
                    if not exercicio:
                        print(f"[AcademIA] ⚠️ Exercício '{nome}' não encontrado no catálogo de {local}, descartado.")
                        continue
                    # Aceita links completos (youtube.com/watch?v=...) e
                    # links curtos (youtu.be/...), usados no catálogo.
                    video_match = re.search(
                        r"(?:[?&]v=|youtu\.be/)([\w-]+)",
                        exercicio.get("video", ""),
                    )
                    lista.append({
                        "nome": exercicio["nome"],
                        "grupo": exercicio["grupo"],
                        "series_reps": exercicio["series_reps"],
                        "videoId": video_match.group(1) if video_match else "",
                    })
                if lista:
                    treinos_enriquecidos[letra] = lista

            if not treinos_enriquecidos:
                print("[AcademIA] ⚠️ Nenhum exercício válido encontrado no plano, ignorando.")
                return None

            plano_final = {
                "dias": dias,
                "local": local,
                "treinos": treinos_enriquecidos,
            }
            print(f"[AcademIA] 📋 PLANO EXTRAÍDO E VALIDADO: {plano_final}")
            return plano_final

        except Exception as e:
            print(f"[AcademIA] ❌ Erro ao extrair plano: {e}")
            return None

    def _remover_marcador_plano(self, texto_resposta):
        """Remove a tag [PLANO: {...}] do texto, mesmo com JSON aninhado."""
        marcador = re.search(r"\[\s*PLANO\s*:", texto_resposta, re.IGNORECASE)
        if not marcador:
            return texto_resposta
        inicio_tag = marcador.start()

        inicio_json = texto_resposta.find("{", marcador.end())
        if inicio_json == -1:
            return texto_resposta

        try:
            decoder = json.JSONDecoder()
            _plano, fim_json = decoder.raw_decode(texto_resposta, inicio_json)
            fim_colchete = texto_resposta.find("]", fim_json)
            fim_tag = fim_colchete + 1 if fim_colchete != -1 else fim_json
            return texto_resposta[:inicio_tag] + texto_resposta[fim_tag:]
        except Exception:
            return texto_resposta

    def formatar_plano_para_usuario(self, plano):
        """Cria no servidor o texto exibido no chat a partir do plano validado.

        Assim, o chat e a aba Planos usam exatamente os mesmos exercícios,
        sem depender de a IA repetir duas vezes a mesma lista.
        """
        linhas = [
            f"Seu novo plano de {plano['dias']} dias está pronto!",
            "Faça 5 minutos de aquecimento antes de começar.",
            "",
        ]
        for letra in sorted(plano["treinos"]):
            linhas.append(f"Treino {letra}")
            for exercicio in plano["treinos"][letra]:
                linhas.append(f"• {exercicio['nome']} — {exercicio['series_reps']}")
            linhas.append("")
        linhas.append("Seus treinos já estão disponíveis na aba Planos de Treino com os vídeos de execução! 📋")
        return "\n".join(linhas)

    def _remover_marcador_json(self, texto_resposta, tag):
        """Remove marcadores no formato [TAG: {...}], lidando com JSON aninhado."""
        inicio_tag = texto_resposta.find(tag)
        if inicio_tag == -1:
            return texto_resposta

        inicio_json = texto_resposta.find("{", inicio_tag)
        if inicio_json == -1:
            return texto_resposta

        try:
            decoder = json.JSONDecoder()
            _dados, fim_json = decoder.raw_decode(texto_resposta, inicio_json)
            fim_colchete = texto_resposta.find("]", fim_json)
            fim_tag = fim_colchete + 1 if fim_colchete != -1 else fim_json
            return texto_resposta[:inicio_tag] + texto_resposta[fim_tag:]
        except Exception:
            return texto_resposta

    def limpar_marcador(self, texto_resposta):
        texto = re.sub(r"\[AVALIA[CÇ][AÃ]O:.*?\]", "", texto_resposta, flags=re.IGNORECASE)
        texto = self._remover_marcador_plano(texto)
        texto = self._remover_marcador_json(texto, "[PERFIL:")
        return texto.strip()
