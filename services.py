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
    Controla o clássico São Paulo x Corinthians para HOJE (04/11/2026) às 21:30.
    Entra no ar 10 minutos antes (21:20) e transmite até o fim.
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
        placar_away = dados_api_externa.get("score_home", 0)

    agora = datetime.now()

    # --- CONFIGURAÇÃO DO CLÁSSICO PARA HOJE ÀS 21:30 ---
    data_jogo_sp_cor = datetime(2026, 11, 4, 21, 30, 0)
    dif_minutos_sp = (data_jogo_sp_cor - agora).total_seconds() / 60

    status_fim_jogo = ["FINISHED", "FIN", "COMPLETED", "MATCH_FINISHED", "ENCERRADO"]

    jogo_majestoso = {
        "id": "sao-paulo-x-corinthians",
        "homeTeam": {"name": "São Paulo", "logo": ESCUDOS_CLUBES["sao_paulo"]},
        "awayTeam": {"name": "Corinthians", "logo": ESCUDOS_CLUBES["corinthians"]},
        "date": "04/11/2026",
        "time": "21:30",
        "timestamp_jogo": data_jogo_sp_cor.isoformat(),
        "score": {"fullTime": {"home": placar_home, "away": placar_away}},
        "logo_transmissao_offline": LOGO_SITE,
        "escalacao": []
    }

    # Lógica de estados do clássico
    if status_externo in status_fim_jogo:
        jogo_majestoso["status"] = "FINISHED"
        jogo_majestoso["statusCustomizado"] = "FIM DE JOGO"
        jogo_majestoso["status_transmissao"] = "OFFLINE"
    elif dif_minutos_sp <= 10:
        # Faltam 10 minutos ou menos (a partir das 21:20): vai para o ar (AO VIVO)
        jogo_majestoso["status"] = "LIVE"
        jogo_majestoso["statusCustomizado"] = "AO VIVO • Em Andamento"
        jogo_majestoso["status_transmissao"] = "AO_VIVO"
    else:
        # Antes das 21:20: fica garantido na aba AGENDADOS
        jogo_majestoso["status"] = "SCHEDULED"
        jogo_majestoso["statusCustomizado"] = "Agendado"
        jogo_majestoso["status_transmissao"] = "OFFLINE"


    # --- OUTROS JOGOS DA AGENDA ---
    jogos_cadastrados = [
        jogo_majestoso,
        {
            "id": "santos-coritiba",
            "homeTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},
            "awayTeam": {"name": "Coritiba", "logo": ESCUDOS_CLUBES["coritiba"]},
            "date": "15/11/2026",
            "time": "16:00",
            "timestamp_jogo": "2026-11-15T16:00:00",
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status_transmissao": "OFFLINE",
            "escalacao": []
        }
    ]

    return jogos_cadastrados
