from datetime import datetime, timedelta
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
    Controla o clássico São Paulo x Corinthians.
    Entra no ar automaticamente 10 minutos antes da partida e transmite até o fim.
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

    # DEFINA AQUI A DATA E HORA EXATA DO JOGO (Ano, Mês, Dia, Hora, Minuto)
    # Exemplo: Jogo dia 10 de novembro de 2026 às 16:00
    timestamp_jogo = datetime(2026, 11, 10, 16, 0, 0)
    agora = datetime.now()

    # Calcula a diferença em minutos entre o horário atual e o horário do jogo
    diferenca_minutos = (timestamp_jogo - agora).total_seconds() / 60

    jogo_majestoso = {
        "id": "sao-paulo-x-corinthians",
        "homeTeam": {"name": "São Paulo", "logo": ESCUDOS_CLUBES["sao_paulo"]},
        "awayTeam": {"name": "Corinthians", "logo": ESCUDOS_CLUBES["corinthians"]},
        "date": timestamp_jogo.strftime("%d/%m/%Y"),
        "time": timestamp_jogo.strftime("%H:%M"),
        "timestamp_jogo": timestamp_jogo.isoformat(),
        "score": {"fullTime": {"home": placar_home, "away": placar_away}},
        "logo_transmissao_offline": LOGO_SITE,
        "escalacao": []
    }

    status_fim_jogo = ["FINISHED", "FIN", "COMPLETED", "MATCH_FINISHED", "ENCERRADO"]

    # Se a fonte externa decretou fim de jogo, encerra imediatamente
    if status_externo in status_fim_jogo:
        jogo_majestoso["status"] = "FINISHED"
        jogo_majestoso["statusCustomizado"] = "FIM DE JOGO"
        jogo_majestoso["status_transmissao"] = "OFFLINE"
        
    elif diferenca_minutos <= 10:
        # Faltam 10 minutos ou o jogo já começou: ativa a aba ao vivo / player
        jogo_majestoso["status"] = "LIVE"
        jogo_majestoso["statusCustomizado"] = "AO VIVO • Em Andamento"
        jogo_majestoso["status_transmissao"] = "AO_VIVO"
    else:
        # Mais de 10 minutos para começar: fica agendado na tela normal com a logo
        jogo_majestoso["status"] = "SCHEDULED"
        jogo_majestoso["statusCustomizado"] = "Agendado"
        jogo_majestoso["status_transmissao"] = "OFFLINE"

    return [jogo_majestoso]
