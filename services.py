from datetime import date
import requests

# Links oficiais fornecidos por você
ESCUDOS_CLUBES = {
    "santos": "https://i.postimg.cc/j2tjm9P0/santos-fc.png",
    "bragantino": "https://i.postimg.cc/Qtk8QbPP/Red-Bull-Bragantino.png"
}

LOGO_SITE = "https://i.postimg.cc/K8PR1kCv/Gemini-Generated-Image-hozi2rhozi2rhozi-removebg-preview.png"

def obter_jogos_serie_a(api_endpoint: str = None):
    """
    Retorna os jogos da Série A com os escudos personalizados e logomarca do site,
    gerenciando as abas Agendados, Ao Vivo e Encerrados.
    """
    if not api_endpoint:
        api_endpoint = "https://sua-api-de-futebol.com/api/jogos"

    try:
        response = requests.get(api_endpoint, timeout=10)
        partidas = []
        
        if response.status_code == 200:
            data = response.json()
            partidas = data.get("matches", data.get("response", data if isinstance(data, list) else []))

        # Objeto estruturado do jogo de amanhã (Santos x Bragantino) para garantir a aba Agendados
        jogo_santos = {
            "id": "santos-vs-bragantino-2026",
            "homeTeam": {
                "name": "Santos",
                "logo": ESCUDOS_CLUBES["santos"]
            },
            "awayTeam": {
                "name": "Bragantino",
                "logo": ESCUDOS_CLUBES["bragantino"]
            },
            "date": "Amanhã",
            "time": "20:00",
            "status": "SCHEDULED", # Irá para 'LIVE' 10 minutos antes ou quando iniciado
            "statusCustomizado": "Agendado - Amanhã às 20:00",
            "score": {
                "fullTime": {"home": 0, "away": 0}
            },
            "logo_transmissao_offline": LOGO_SITE,
            "status_transmissao": "OFFLINE"
        }

        # Atualiza os escudos e a logo em todas as partidas retornadas pela API externa
        for p in partidas:
            p["logo_transmissao_offline"] = LOGO_SITE
            nome_casa = str(p.get("homeTeam", {}).get("name", "")).lower()
            nome_fora = str(p.get("awayTeam", {}).get("name", "")).lower()

            if "santos" in nome_casa:
                p["homeTeam"]["logo"] = ESCUDOS_CLUBES["santos"]
            if "bragantino" in nome_fora or "red bull" in nome_fora:
                p["awayTeam"]["logo"] = ESCUDOS_CLUBES["bragantino"]

        # Se o jogo do Santos não estiver na listagem da API, injeta ele manualmente para garantir os Agendados
        tem_santos = any("santos" in str(p.get("homeTeam", {}).get("name", "")).lower() for p in partidas)
        if not tem_santos:
            partidas.append(jogo_santos)

        return partidas

    except Exception as e:
        print(f"Erro ao buscar dados da API: {e}")
        return []
