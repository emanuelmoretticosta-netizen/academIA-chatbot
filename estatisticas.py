from datetime import datetime, timedelta


def converter_data(data_texto):
    """Aceita o padrão atual (AAAA-MM-DD) e registros antigos (DD/MM/AAAA)."""
    if not data_texto:
        return None
    for formato in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(data_texto, formato).date()
        except ValueError:
            continue
    return None


def gerar_dados_grafico_semanal(avaliacoes, dias=7):
    # Pega o dia de hoje
    hoje = datetime.now().date()

    dias_lista = []
    contagem_por_dia = {}

    # Gera os últimos 7 dias (incluindo hoje)
    for i in range(dias - 1, -1, -1):
        dia_especifico = hoje - timedelta(days=i)
        chave_dia = dia_especifico.isoformat()
        rotulo = dia_especifico.strftime("%d/%m")

        dias_lista.append({
            "rotulo": rotulo,
            "dia": dia_especifico,
            "chave": chave_dia
        })

        contagem_por_dia[chave_dia] = 0

    # Contabiliza os treinos no dia exato em que foram feitos
    for avaliacao in avaliacoes:
        data_texto = avaliacao.get("data")
        if not data_texto:
            continue

        data_avaliacao = converter_data(data_texto)
        if not data_avaliacao:
            continue

        chave_avaliacao = data_avaliacao.isoformat()

        if chave_avaliacao in contagem_por_dia:
            contagem_por_dia[chave_avaliacao] += 1

    rotulos = []
    valores = []

    for d in dias_lista:
        rotulos.append(d["rotulo"])
        valores.append(contagem_por_dia[d["chave"]])

    return {
        "semanas": rotulos,
        "valores": valores
    }

def calcular_resumo_progresso(avaliacoes):
    total_treinos = len(avaliacoes)

    if total_treinos == 0:
        return {
            "totalTreinos": 0,
            "semanasAtivas": 0,
            "notaMedia": 0,
            "grafico": gerar_dados_grafico_semanal([])
        }

    notas_validas = []
    semanas_unicas = set()

    for avaliacao in avaliacoes:
        data_texto = avaliacao.get("data")
        nota = avaliacao.get("nota")

        if isinstance(nota, (int, float)):
            notas_validas.append(nota)

        data_avaliacao = converter_data(data_texto)
        if data_avaliacao:
            inicio_semana = data_avaliacao - timedelta(days=data_avaliacao.weekday())
            semanas_unicas.add(inicio_semana.isoformat())

    nota_media = 0
    if notas_validas:
        nota_media = round(sum(notas_validas) / len(notas_validas), 2)

    return {
        "totalTreinos": total_treinos,
        "semanasAtivas": len(semanas_unicas),
        "notaMedia": nota_media,
        "grafico": gerar_dados_grafico_semanal(avaliacoes)
    }
