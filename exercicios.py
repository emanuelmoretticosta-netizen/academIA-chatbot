"""
Banco de exercícios do AcademIA.

Cada exercício possui: nome, grupo, séries/repetições sugeridas,
equipamento e vídeo de referência no YouTube.
"""

BUSCA_YOUTUBE = "https://www.youtube.com/results?search_query="

# ACADEMIA — 31 exercícios
EXERCICIOS_ACADEMIA = [
    # PEITO
    {"nome": "Supino Reto com Barra", "grupo": "peito", "series_reps": "3x10", "equipamento": ["barra", "banco"], "video": "https://youtu.be/dJfxLn2SAE0?si=QoKQH5cWiHkHOKZC"},
    {"nome": "Supino Inclinado com Halteres", "grupo": "peito", "series_reps": "3x12", "equipamento": ["halteres", "banco inclinado"], "video": "https://youtu.be/F4Q1g2z8MWM?si=5iWgWKDjJEPWTI05"},
    {"nome": "Crucifixo com Halteres", "grupo": "peito", "series_reps": "3x12", "equipamento": ["halteres", "banco"], "video": "https://youtu.be/_kpKlYexyXs?si=FFVyK-8tyKc0hufa"},
    {"nome": "Crossover (polia)", "grupo": "peito", "series_reps": "3x15", "equipamento": ["polia"], "video": "https://youtu.be/sbMJLbVN7So?si=XU7ARxoH09zRsIpc"},
    {"nome": "Supino Fechado com Barra", "grupo": "peito/triceps", "series_reps": "3x10", "equipamento": ["barra", "banco"], "video": "https://youtu.be/c2cCPyRDDYs?si=DnsmpI2L6NdwwQlV"},
    # COSTAS
    {"nome": "Puxada Frontal (pulley)", "grupo": "costas", "series_reps": "3x12", "equipamento": ["pulley"], "video": "https://youtu.be/ecuTSZM1wOQ?si=qp0NL_AtbL0nJ6rm"},
    {"nome": "Remada Curvada com Barra", "grupo": "costas", "series_reps": "3x10", "equipamento": ["barra"], "video": "https://youtu.be/-dQiXndRAJo?si=cyxOf2nIJJeWQT2P"},
    {"nome": "Remada Unilateral com Halter", "grupo": "costas", "series_reps": "3x12 cada lado", "equipamento": ["halter", "banco"], "video": "https://youtu.be/E008-XIJBEk?si=XgacQkGmuqri-PRn"},
    {"nome": "Remada Baixa (cabo)", "grupo": "costas", "series_reps": "3x12", "equipamento": ["cabo"], "video": "https://youtu.be/dUy0chKG-yo?si=IrWneqUqOdDsm6JA"},
    {"nome": "Barra Fixa (pegada pronada)", "grupo": "costas/biceps", "series_reps": "3x ao máximo", "equipamento": ["barra fixa"], "video": "https://youtu.be/pmDEhjDUQeA?si=kCrnUEXL2e-vCeY8"},
    # OMBROS
    {"nome": "Desenvolvimento com Halteres", "grupo": "ombros", "series_reps": "3x12", "equipamento": ["halteres"], "video": "https://youtu.be/MmHTcVK-1tU?si=_lr_mlV-Q8yikzDS"},
    {"nome": "Elevação Lateral com Halteres", "grupo": "ombros", "series_reps": "3x15", "equipamento": ["halteres"], "video": "https://youtu.be/qDAoUOmdbi4?si=DiBVhfudCexNj0-A"},
    {"nome": "Elevação Frontal com Halter", "grupo": "ombros", "series_reps": "3x12", "equipamento": ["halter"], "video": "https://youtu.be/xNiyS3b9ERg?si=VP3SvxeaCkG4Lz2m"},
    {"nome": "Desenvolvimento Arnold", "grupo": "ombros", "series_reps": "3x12", "equipamento": ["halteres", "banco"], "video": "https://youtu.be/yuOPcpMmYJk?si=5oNVCA_ZZ97VrhUr"},
    # BÍCEPS
    {"nome": "Rosca Direta com Barra", "grupo": "biceps", "series_reps": "3x12", "equipamento": ["barra"], "video": "https://youtu.be/cCbiBI-FNDA?si=4BhHgF1jjnNbm_9v"},
    {"nome": "Rosca Alternada com Halteres", "grupo": "biceps", "series_reps": "3x12 cada braço", "equipamento": ["halteres"], "video": "https://youtu.be/wD0XsLI3S7s?si=3PMtq7MuOSsxQPh3"},
    {"nome": "Rosca Scott", "grupo": "biceps", "series_reps": "3x10", "equipamento": ["banco scott", "barra ou halter"], "video": "https://youtu.be/0FPOPvuXDp8?si=U6Nvso2MnQ73L6Mg"},
    {"nome": "Rosca Martelo", "grupo": "biceps", "series_reps": "3x12", "equipamento": ["halteres"], "video": "https://youtu.be/UZCzZJ0_2jg?si=VHQzKXyh7vFOkUJJ"},
    # TRÍCEPS
    {"nome": "Tríceps Pulley (corda)", "grupo": "triceps", "series_reps": "3x15", "equipamento": ["pulley", "corda"], "video": "https://youtu.be/7le1JRUUagM?si=SfsJ_9MYYxgFTYf0"},
    {"nome": "Tríceps Francês com Halter", "grupo": "triceps", "series_reps": "3x12", "equipamento": ["halter", "banco"], "video": "https://youtu.be/GKpHcN1xM3o?si=DcuCwUgzsZkguIXB"},
    {"nome": "Mergulho nas Paralelas", "grupo": "triceps", "series_reps": "3x12", "equipamento": ["paralelas"], "video": "https://youtu.be/9XOT04mvPqs?si=SM3wo9G8dWQTk8Aj"},
    # PERNAS
    {"nome": "Agachamento Livre com Barra", "grupo": "quadriceps/gluteos", "series_reps": "4x10", "equipamento": ["barra", "rack"], "video": "https://youtu.be/XS85nxNn3uQ?si=DRVvjV3x0ZR3woy2"},
    {"nome": "Leg Press 45°", "grupo": "quadriceps/gluteos", "series_reps": "4x12", "equipamento": ["leg press"], "video": "https://youtu.be/3KJKb1aN6HA?si=BtvtBjlse_rCquYu"},
    {"nome": "Cadeira Extensora", "grupo": "quadriceps", "series_reps": "3x15", "equipamento": ["cadeira extensora"], "video": "https://youtu.be/sY-qK1MrBSc?si=3D56JFR1JnifRmbw"},
    {"nome": "Mesa Flexora", "grupo": "posteriores de coxa", "series_reps": "3x15", "equipamento": ["mesa flexora"], "video": "https://youtu.be/9OU0Y6Jz8d0?si=am0pejJXB_usrWHt"},
    {"nome": "Stiff com Barra", "grupo": "posteriores/gluteos", "series_reps": "3x12", "equipamento": ["barra"], "video": "https://youtu.be/F8q6ZIizAcY?si=sZs0Ednohf5aWPLm"},
    {"nome": "Avanço com Halteres", "grupo": "quadriceps/gluteos", "series_reps": "3x12 cada perna", "equipamento": ["halteres"], "video": "https://youtu.be/6Pc3OB4wnBo?si=IeDZy6UrVons_Let"},
    {"nome": "Panturrilha em Pé (máquina)", "grupo": "panturrilha", "series_reps": "4x20", "equipamento": ["máquina de panturrilha"], "video": "https://youtu.be/PNLdWhbgxkU?si=tJ4JCi3Vhswreg4C"},
    # ABDÔMEN
    {"nome": "Abdominal na Polia Alta", "grupo": "abdomen", "series_reps": "3x15", "equipamento": ["polia alta", "corda"], "video": "https://youtu.be/C68dbYflq2w?si=OpPFTz2nUF2BxfJ8"},
    {"nome": "Prancha Frontal", "grupo": "abdomen/core", "series_reps": "3x45 segundos", "equipamento": [], "video": "https://youtu.be/a6JT9hOy5Rs?si=K-Qdxs8PB4TEcSRI"},
    {"nome": "Levantamento Terra", "grupo": "full body/costas/posteriores", "series_reps": "4x8", "equipamento": ["barra"], "video": "https://youtu.be/50AkPBZwACQ?si=L11Gx-ikbZccEI20"},
]

# CASA — 33 exercícios
EXERCICIOS_CASA = [
    # PEITO / TRÍCEPS
    {"nome": "Flexão de Braço (padrão)", "grupo": "peito/triceps", "series_reps": "3x12", "equipamento": [], "video": "https://youtu.be/dHgoYiCraCw?si=BrynIzygiot8PNNl"},
    {"nome": "Flexão de Braço Inclinada (pés na cadeira)", "grupo": "peito superior", "series_reps": "3x10", "equipamento": ["cadeira"], "video": "https://youtu.be/6Yawb7dvGUk?si=FGc2OznE8wcYZYaD"},
    {"nome": "Flexão de Braço Declinada (mãos na cadeira)", "grupo": "peito inferior", "series_reps": "3x12", "equipamento": ["cadeira"], "video": "https://www.youtube.com/watch?v=H23VZ7IZwG4"},
    {"nome": "Flexão de Braço Diamante", "grupo": "triceps/peito", "series_reps": "3x10", "equipamento": [], "video": "https://youtu.be/PAauHMIhWKg?si=Jx-J97G1jUrqC4Rc"},
    {"nome": "Tríceps no Banco (mergulho)", "grupo": "triceps", "series_reps": "3x12", "equipamento": ["cadeira ou banco firme"], "video": "https://youtu.be/TCVj8cliLNo?si=SOfFv3DbDpSgUkfr"},
    # COSTAS / BÍCEPS
    {"nome": "Remada com Elástico", "grupo": "costas", "series_reps": "3x15", "equipamento": ["elástico"], "video": "https://youtu.be/izyppcUlGfI?si=wIoNnI3Rc3_4cIQV"},
    {"nome": "Remada com Halter (apoio na cadeira)", "grupo": "costas", "series_reps": "3x12 cada lado", "equipamento": ["halter", "cadeira"], "video": "https://youtu.be/ylyZu9TaHQs?si=x3nGX9KSm5YR7IaL"},
    {"nome": "Superman (extensão lombar no chão)", "grupo": "lombar/gluteos", "series_reps": "3x15", "equipamento": [], "video": "https://youtu.be/z0rx9swRDR0?si=6fUDirUMrfeWTtM1"},
    {"nome": "Barra Fixa em Casa (barra de porta)", "grupo": "costas/biceps", "series_reps": "3x ao máximo", "equipamento": ["barra de porta"], "video": "https://youtu.be/HpxwBDaQvZc?si=4Xz3TSmHLspuqEW0"},
    {"nome": "Rosca com Halter (em pé)", "grupo": "biceps", "series_reps": "3x12 cada braço", "equipamento": ["halteres"], "video": "https://youtu.be/6O_hVOEArG4?si=icKAgAxiASlFVM5T"},
    {"nome": "Rosca com Elástico", "grupo": "biceps", "series_reps": "3x15", "equipamento": ["elástico"], "video": "https://youtu.be/Fa9UTrrxwH8?si=aQRKYu9tOx4mX75S"},
    # OMBROS
    {"nome": "Desenvolvimento com Halteres (sentado)", "grupo": "ombros", "series_reps": "3x12", "equipamento": ["halteres", "cadeira"], "video": "https://youtu.be/ja3qMvBtaXQ?si=4KljtS-AW62Tgh9V"},
    {"nome": "Elevação Lateral com Garrafa de Água", "grupo": "ombros", "series_reps": "3x15", "equipamento": ["garrafas de água"], "video": "https://youtu.be/I8B6yuHV2NE?si=hv2Xn2U678JFwrXx"},
    {"nome": "Elevação Lateral com Elástico", "grupo": "ombros", "series_reps": "3x15", "equipamento": ["elástico"], "video": "https://youtu.be/R7Wzu0ErpCQ?si=R_Ds4lqNgREzuu8A"},
    {"nome": "Pike Push-up (flexão em V)", "grupo": "ombros/triceps", "series_reps": "3x10", "equipamento": [], "video": "https://youtu.be/XckEEwa1BPI?si=0RF3f5K5gxLb8L0z"},
    # PERNAS — SEM EQUIPAMENTO
    {"nome": "Agachamento com Peso Corporal", "grupo": "quadriceps/gluteos", "series_reps": "4x15", "equipamento": [], "video": "https://youtu.be/h5ZOoULsAJo?si=_Jf_CJjhL6lDG7T8"},
    {"nome": "Agachamento Sumô (peso corporal)", "grupo": "adutores/gluteos", "series_reps": "3x15", "equipamento": [], "video": "https://youtu.be/n8NCoU0ZiMo?si=Syc0bfXdrnUBkCm0"},
    {"nome": "Avanço (afundo) no lugar", "grupo": "quadriceps/gluteos", "series_reps": "3x12 cada perna", "equipamento": [], "video": "https://youtu.be/vIIVlJZWMLs?si=xCutScOhbnjJve9E"},
    {"nome": "Agachamento Búlgaro (pé na cadeira)", "grupo": "quadriceps/gluteos", "series_reps": "3x10 cada perna", "equipamento": ["cadeira"], "video": "https://youtu.be/HTedLXOg89Y?si=jvs_ZsNWBytWZ09Y"},
    {"nome": "Agachamento com Cadeira (para iniciantes)", "grupo": "quadriceps/gluteos", "series_reps": "3x12", "equipamento": ["cadeira"], "video": "https://youtu.be/qZw8UNyHEuA?si=AtmpMDgPIyKESWjv"},
    {"nome": "Ponte de Glúteos (no chão)", "grupo": "gluteos/posteriores", "series_reps": "3x15", "equipamento": [], "video": "https://youtu.be/4bqiyjxyJsM?si=bSHcT1bCQsoG1Bfm"},
    {"nome": "Elevação de Quadril Unilateral", "grupo": "gluteos", "series_reps": "3x12 cada lado", "equipamento": [], "video": "https://youtu.be/Iaztg8k1BbM?si=xf6MTC7LYqpkJ7ML"},
    {"nome": "Stiff com Halteres", "grupo": "posteriores/gluteos", "series_reps": "3x12", "equipamento": ["halteres"], "video": "https://youtu.be/IWvqmrT2lTA?si=Jw5ZzM4Hs--g4YqC"},
    {"nome": "Panturrilha em Pé (usando degrau ou chão)", "grupo": "panturrilha", "series_reps": "4x20", "equipamento": ["degrau opcional"], "video": "https://youtu.be/Qun1n_RQbvA?si=dMJ_ssoAhaz-NQSk"},
    # ABDÔMEN / CORE
    {"nome": "Prancha Frontal", "grupo": "core/abdomen", "series_reps": "3x45 segundos", "equipamento": [], "video": "https://youtu.be/a6JT9hOy5Rs?si=TH1f1PgcMZ2Jnl0v"},
    {"nome": "Abdominal Crunch (no chão)", "grupo": "abdomen", "series_reps": "3x20", "equipamento": [], "video": "https://youtu.be/fR_KzGyKW3w?si=r7oZ9CfhOR6I-43d"},
    {"nome": "Abdominal Bicicleta", "grupo": "abdomen obliquo", "series_reps": "3x20", "equipamento": [], "video": "https://youtu.be/apmprS8H1MY?si=GJigCIuFp-3WUxov"},
    {"nome": "Mountain Climber", "grupo": "core/cardio", "series_reps": "3x30 segundos", "equipamento": [], "video": "https://youtu.be/ZhiCSdOVJp0?si=ESlQjmBVnE3g_0-Z"},
    # IMPROVISO EM CASA
    {"nome": "Agachamento com Mochila (improviso de peso)", "grupo": "quadriceps/gluteos", "series_reps": "3x12", "equipamento": ["mochila com carga"], "video": "https://youtu.be/FS1Omr3jSeE?si=4fVXmQa3J-Ia0nqz"},
    {"nome": "Remada com Mochila (apoio na cadeira)", "grupo": "costas", "series_reps": "3x12 cada lado", "equipamento": ["mochila com carga", "cadeira"], "video": "https://youtu.be/mrYBMjhm2hw?si=IZmD7kTwgWTWIAS-"},
    {"nome": "Elevação de Panturrilha na Escada", "grupo": "panturrilha", "series_reps": "4x20", "equipamento": ["escada ou degrau"], "video": "https://youtu.be/Qun1n_RQbvA?si=reBcKiE8qMR2VmRT"},
]


# FUNÇÕES AUXILIARES
def get_exercicios_por_local(local: str) -> list:
    """Retorna a lista de exercícios conforme o local de treino."""
    local = local.lower().strip()
    if "academia" in local:
        return EXERCICIOS_ACADEMIA
    return EXERCICIOS_CASA


def get_exercicios_por_grupo(local: str, grupo: str) -> list:
    """Retorna exercícios de um grupo muscular específico para o local informado."""
    todos = get_exercicios_por_local(local)
    grupo = grupo.lower().strip()
    return [e for e in todos if grupo in e["grupo"].lower()]


def formatar_exercicios_para_prompt(exercicios: list) -> str:
    """Formata a lista de exercícios em texto compacto para o prompt."""
    linhas = []
    for e in exercicios:
        linhas.append(
            f"  - {e['nome']} ({e['grupo']}): {e['series_reps']} | Vídeo: {e['video']}"
        )
    return "\n".join(linhas)


def get_contexto_exercicios(local: str) -> str:
    """Retorna um bloco pronto para ser injetado no prompt do bot."""
    exercicios = get_exercicios_por_local(local)
    texto = f"EXERCÍCIOS DISPONÍVEIS PARA {local.upper()} (use SOMENTE estes ao montar o treino):\n"
    texto += formatar_exercicios_para_prompt(exercicios)
    return texto
