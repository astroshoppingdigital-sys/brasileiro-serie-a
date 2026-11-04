from datetime import datetime
import requests

# Dicionário de escudos dos clubes
ESCUDOS_CLUBES = {
    "santos": "https://i.postimg.cc/j2tjm9P0/santos-fc.png",
    "sao_paulo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Brasao_do_Sao_Paulo_Futebol_Clube.svg/1200px-Brasao_do_Sao_Paulo_Futebol_Clube.svg.png",
    "corinthians": "https://upload.wikimedia.org/wikipedia/pt/b/b4/Corinthians_simbolo.png",
    "coritiba": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Coritiba_Foot_Ball_Club_logo.svg/1200px-Coritiba_Foot_Ball_Club_logo.svg.png",
    "gremio": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Gr%C3%AAmio_Foot-Ball_Porto-Alegrense_logo.svg/1200px-Gr%C3%AAmio_Foot-Ball_Porto-Alegrense_logo.svg.png",
    "vitoria": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Esporte_Clube_Vit%C3%B3ria_logo.svg/1200px-Esporte_Clube_Vit%C3%B3ria_logo.svg.png",
    "botafogo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Botafogo_de_Futebol_e_Regatas_logo.svg/1200px-Botafogo_de_Futebol_e_Regatas_logo.svg.png"
}

LOGO_SITE = "https://i.postimg.cc/K8PR1kCv/Gemini-Generated-Image-hozi2rhozi2rhozi-removebg-preview.png"

def obter_jogos_serie_a(api_endpoint: str = None):
    """
    Controla o clássico São Paulo x Corinthians (21:30).
    Fica em agendados (com o aviso 'Hoje') e só entra ao vivo 10 minutos antes (21:20).
    """
    
    dados_api_externa = None
    if api_endpoint:
        try:
            resposta = requests.get(api_endpoint, timeout=5)
            if resposta.status_code == 200:
                dados_api_externa = resposta.json()
        except Exception as err:
            print(f"Aviso: Não foi possível obter dados da API externa ({err}).")

    status_externo = None
    placar_home = 0
    placar_away = 0

    if dados_api_externa:
        status_externo = dados_api_externa.get("status_partida")
        placar_home = dados_api_externa.get("score_home", 0)
        placar_away = dados_api_externa.get("score_away", 0)

    agora = datetime.now()

    # --- CLÁSSICO DE HOJE: São Paulo x Corinthians (21:30) ---
    data_jogo_sp_cor = datetime(2026, 11, 4, 21, 30, 0)
    
    # Diferença em minutos entre o horário atual e o horário do jogo
    # Valor positivo se faltam minutos para o jogo, negativo se já passou
    diferenca_minutos = (data_jogo_sp_cor - agora).total_seconds() / 60

    status_fim_jogo = ["FINISHED", "FIN", "COMPLETED", "MATCH_FINISHED", "ENCERRADO"]

    jogo_majestoso = {
        "id": "sao-paulo-x-corinthians",
        "homeTeam": {"name": "São Paulo", "logo": ESCUDOS_CLUBES["sao_paulo"]},
        "awayTeam": {"name": "Corinthians", "logo": ESCUDOS_CLUBES["corinthians"]},
        "date": "Hoje",  # Retorna "Hoje" embaixo do horário
        "time": "21:30",
        "timestamp_jogo": data_jogo_sp_cor.isoformat(),
        "score": {"fullTime": {"home": placar_home, "away": placar_away}},
        "logo_transmissao_offline": LOGO_SITE,
        "escalacao": []
    }

    # Lógica estrita dos 10 minutos e fim de jogo
    if status_externo in status_fim_jogo:
        # 1. Se a fonte externa decretou fim de jogo
        jogo_majestoso["status"] = "FINISHED"
        jogo_majestoso["statusCustomizado"] = "FIM DE JOGO"
        jogo_majestoso["status_transmissao"] = "OFFLINE"
    elif 0 <= diferenca_minutos <= 10:
        # 2. Faltam 10 minutos ou menos para começar (a partir das 21:20): vai para AO VIVO
        jogo_majestoso["status"] = "LIVE"
        jogo_majestoso["statusCustomizado"] = "AO VIVO • Em Andamento"
        jogo_majestoso["status_transmissao"] = "AO_VIVO"
    elif diferenca_minutos < 0 and status_externo not in status_fim_jogo:
        # 3. O jogo já passou do horário de início mas a API ainda não disse que acabou: continua AO VIVO transmitindo até o fim
        jogo_majestoso["status"] = "LIVE"
        jogo_majestoso["statusCustomizado"] = "AO VIVO • Em Andamento"
        jogo_majestoso["status_transmissao"] = "AO_VIVO"
    else:
        # 4. Mais de 10 minutos para começar: fica travado na aba AGENDADOS
        jogo_majestoso["status"] = "SCHEDULED"
        jogo_majestoso["statusCustomizado"] = "Agendado"
        jogo_majestoso["status_transmissao"] = "OFFLINE"


    # --- DEMAIS JOGOS DA RETA FINAL DO SANTOS ---
    jogos_cadastrados = [
        jogo_majestoso,
        {
            "id": "coritiba-santos",
            "homeTeam": {"name": "Coritiba", "logo": ESCUDOS_CLUBES["coritiba"]},
            "awayTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},
            "date": "18/11/2026",
            "time": "19:30",
            "timestamp_jogo": "2026-11-18T19:30:00",
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status_transmissao": "OFFLINE",
            "escalacao": []
        },
        {
            "id": "santos-gremio",
            "homeTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},
            "awayTeam": {"name": "Grêmio", "logo": ESCUDOS_CLUBES["gremio"]},
            "date": "23/11/2026",
            "time": "21:00",
            "timestamp_jogo": "2026-11-23T21:00:00",
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status_transmissao": "OFFLINE",
            "escalacao": []
        },
        {
            "id": "vitoria-santos",
            "homeTeam": {"name": "Vitória", "logo": ESCUDOS_CLUBES["vitoria"]},
            "awayTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},
            "date": "29/11/2026",
            "time": "15:00",
            "timestamp_jogo": "2026-11-29T15:00:00",
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status_transmissao": "OFFLINE",
            "escalacao": []
        },
        {
            "id": "santos-botafogo",
            "homeTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},
            "awayTeam": {"name": "Botafogo", "logo": ESCUDOS_CLUBES["botafogo"]},
            "date": "02/12/2026",
            "time": "15:00",
            "timestamp_jogo": "2026-12-02T15:00:00",
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status_transmissao": "OFFLINE",
            "escalacao": []
        }
    ]

    return jogos_cadastrados
