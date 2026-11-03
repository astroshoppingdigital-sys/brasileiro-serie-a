from datetime import datetime
import requests

# Links oficiais dos escudos e da logo fornecidos por você
ESCUDOS_CLUBES = {
    "santos": "https://i.postimg.cc/j2tjm9P0/santos-fc.png",
    "coritiba": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Coritiba_Foot_Ball_Club_logo.svg/1200px-Coritiba_Foot_Ball_Club_logo.svg.png",
    "gremio": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Gr%C3%AAmio_Foot-Ball_Porto-Alegrense_logo.svg/1200px-Gr%C3%AAmio_Foot-Ball_Porto-Alegrense_logo.svg.png",
    "vitoria": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Esporte_Clube_Vit%C3%B3ria_logo.svg/1200px-Esporte_Clube_Vit%C3%B3ria_logo.svg.png",
    "botafogo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Botafogo_de_Futebol_e_Regatas_logo.svg/1200px-Botafogo_de_Futebol_e_Regatas_logo.svg.png"
}

LOGO_SITE = "https://i.postimg.cc/K8PR1kCv/Gemini-Generated-Image-hozi2rhozi2rhozi-removebg-preview.png"

def obter_jogos_serie_a(api_endpoint: str = None):
    """
    Retorna a lista dos próximos jogos do Santos com os mandos de campo corretos
    (Coritiba mandante, Grêmio mandante, Vitória mandante e Santos mandante contra o Botafogo),
    com ativação automática da escalação 10 minutos antes na aba Ao Vivo.
    """
    jogos_santos = [
        {
            "id": "coritiba-santos-2026",
            "homeTeam": {"name": "Coritiba", "logo": ESCUDOS_CLUBES["coritiba"]}, # Mandante (Esquerda)
            "awayTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},     # Visitante (Direita)
            "date": "18/11",
            "time": "19:30",
            "timestamp_jogo": "2026-11-18T19:30:00",
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado - 18/11, 19:30",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status_transmissao": "OFFLINE",
            "escalacao": []
        },
        {
            "id": "santos-gremio-2026",
            "homeTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},     # Mandante (Esquerda)
            "awayTeam": {"name": "Grêmio", "logo": ESCUDOS_CLUBES["gremio"]},     # Visitante (Direita)
            "date": "23/11",
            "time": "21:00",
            "timestamp_jogo": "2026-11-23T21:00:00",
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado - 23/11, 21:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status_transmissao": "OFFLINE",
            "escalacao": []
        },
        {
            "id": "vitoria-santos-2026",
            "homeTeam": {"name": "EC Vitória", "logo": ESCUDOS_CLUBES["vitoria"]}, # Mandante (Esquerda)
            "awayTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},     # Visitante (Direita)
            "date": "29/11",
            "time": "A confirmar",
            "timestamp_jogo": "2026-11-29T16:00:00",
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado - 29/11",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status_transmissao": "OFFLINE",
            "escalacao": []
        },
        {
            "id": "santos-botafogo-2026",
            "homeTeam": {"name": "Santos", "logo": ESCUDOS_CLUBES["santos"]},     # Mandante (Esquerda)
            "awayTeam": {"name": "Botafogo", "logo": ESCUDOS_CLUBES["botafogo"]}, # Visitante (Direita)
            "date": "02/12",
            "time": "15:00",
            "timestamp_jogo": "2026-12-02T15:00:00",
            "status": "SCHEDULED",
            "statusCustomizado": "Agendado - 02/12, 15:00",
            "score": {"fullTime": {"home": 0, "away": 0}},
            "logo_transmissao_offline": LOGO_SITE,
            "status_transmissao": "OFFLINE",
            "escalacao": []
        }
    ]

    agora = datetime.now()

    # Lógica de tempo para verificar os 10 minutos pré-jogo
    for jogo in jogos_santos:
        try:
            data_jogo = datetime.strptime(jogo["timestamp_jogo"], "%Y-%m-%dT%H:%M:%S")
            diferenca_minutos = (data_jogo - agora).total_seconds() / 60

            # Se estiver entre 10 minutos antes e o início da partida:
            if -90 <= diferenca_minutos <= 10:
                if diferenca_minutos > 2:
                    jogo["status"] = "LIVE"
                    jogo["statusCustomizado"] = "AO VIVO • Pré-jogo (Escalação Confirmada)"
                    jogo["status_transmissao"] = "PRE_JOGO"
                    
                    # Injeta a escalação do Santos na API para exibir no campinho
                    jogo["escalacao"] = [
                        {"posicao": "GOL", "nome": "João Paulo"},
                        {"posicao": "LD", "nome": "Aderlan"},
                        {"posicao": "ZAG", "nome": "Gil"},
                        {"posicao": "ZAG", "nome": "Joaquim"},
                        {"posicao": "LE", "nome": "Felipe Jonatan"},
                        {"posicao": "VOL", "nome": "João Schmidt"},
                        {"posicao": "MEI", "nome": "Diego Pituca"},
                        {"posicao": "MEI", "nome": "Otero"},
                        {"posicao": "ATA", "nome": "Guilherme"},
                        {"posicao": "ATA", "nome": "Furch"},
                        {"posicao": "ATA", "nome": "Pedrinho"}
                    ]
                else:
                    jogo["status"] = "LIVE"
                    jogo["statusCustomizado"] = "AO VIVO • 1° Tempo"
                    jogo["status_transmissao"] = "AO_VIVO"
                    jogo["escalacao"] = []
        except Exception as e:
            print(f"Erro ao processar data do jogo: {e}")

    return jogos_santos
