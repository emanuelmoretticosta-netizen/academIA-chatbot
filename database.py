"""
database.py — A memória do AcademIA
"""

import json
import os

CAMINHO_ARQUIVO = os.path.join("data", "usuarios.json")


class Database:
    def __init__(self, caminho=CAMINHO_ARQUIVO):
        self.caminho = caminho
        self._garantir_arquivo()

    def _garantir_arquivo(self):
        pasta = os.path.dirname(self.caminho)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta)
        if not os.path.exists(self.caminho):
            with open(self.caminho, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def _carregar_tudo(self):
        with open(self.caminho, "r", encoding="utf-8") as f:
            return json.load(f)

    def _salvar_tudo(self, dados):
        with open(self.caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    def carregar_perfil(self, usuario_id):
        dados = self._carregar_tudo()
        return dados.get(usuario_id, {}).get("perfil", {})

    def salvar_perfil(self, usuario_id, perfil):
        dados = self._carregar_tudo()
        dados.setdefault(usuario_id, {})
        dados[usuario_id]["perfil"] = perfil
        self._salvar_tudo(dados)

    def carregar_historico(self, usuario_id):
        dados = self._carregar_tudo()
        return dados.get(usuario_id, {}).get("historico", [])

    def salvar_historico(self, usuario_id, historico):
        dados = self._carregar_tudo()
        dados.setdefault(usuario_id, {})
        dados[usuario_id]["historico"] = historico
        self._salvar_tudo(dados)

    def salvar_avaliacao(self, usuario_id, avaliacao):
        dados = self._carregar_tudo()
        dados.setdefault(usuario_id, {})
        if "avaliacoes" not in dados[usuario_id]:
            dados[usuario_id]["avaliacoes"] = []
        dados[usuario_id]["avaliacoes"].append(avaliacao)
        self._salvar_tudo(dados)

    def carregar_avaliacoes(self, usuario_id):
        dados = self._carregar_tudo()
        return dados.get(usuario_id, {}).get("avaliacoes", [])

    def salvar_peso(self, usuario_id, valor):
        from datetime import date
        dados = self._carregar_tudo()
        dados.setdefault(usuario_id, {})
        if "pesos" not in dados[usuario_id]:
            dados[usuario_id]["pesos"] = []
        dados[usuario_id]["pesos"].append({
            "data": str(date.today()),
            "valor": valor
        })
        self._salvar_tudo(dados)

    def carregar_pesos(self, usuario_id):
        dados = self._carregar_tudo()
        return dados.get(usuario_id, {}).get("pesos", [])

    def salvar_plano_treino(self, usuario_id, plano):
        dados = self._carregar_tudo()
        dados.setdefault(usuario_id, {})
        dados[usuario_id]["plano_customizado"] = plano
        self._salvar_tudo(dados)

    def carregar_plano_treino(self, usuario_id):
        dados = self._carregar_tudo()
        return dados.get(usuario_id, {}).get("plano_customizado", None)