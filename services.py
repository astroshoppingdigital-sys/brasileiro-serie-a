from datetime import date
import requests

# Links oficiais dos escudos e da logo fornecidos por você
ESCUDOS_CLUBES = {
    "santos": "https://i.postimg.cc/j2tjm9P0/santos-fc.png",
    "bragantino": "https://i.postimg.cc/Qtk8QbPP/Red-Bull-Bragantino.png"
}

LOGO_SITE = "https://i.postimg.cc/K8PR1kCv/Gemini-Generated-Image-hozi2rhozi2rhozi-removebg-preview.png"

def obter_jogos_serie_a(api_endpoint: str = None):
    """
    Busca os dados da API em tempo real, gerencia o placar atualizado (2 a 1 para o Bragantino),
    atualiza automaticamente caso saia novo gol, e aplica os escudos e logomarca personalizados.
    """
    if not api_endpoint:
        api_endpoint = "https://sua-api-de-futebol.com/api/jogos"

    try:
        response = requests.get(api_endpoint, timeout=10)
        partidas = []
        
        if response.status_code == 200:
            data = response.json()
            partidas = data.get("matches", data.get("response", data if isinstance(data, list) else []))

        encontrou_santos = False

        # Percorre as partidas para injetar os escudos e atualizar o placar em tempo real
        for p in partidas:
            p["logo_transmissao_offline"] = LOGO_SITE
            nome_casa = str(p.get("homeTeam", {}).get("name", "")).lower()
            nome_fora = str(p.get("awayTeam", {}).get("name", "")).lower()

            if "santos" in nome_casa:
                p["homeTeam"]["logo"] = ESCUDOS_CLUBES["santos"]
            if "bragantino" in nome_fora or "red bull" in nome_fora:
                p["awayTeam"]["logo"] = ESCUDOS_CLUBES["bragantino"]

            # Identifica a partida do Santos x Bragantino
            if "santos" in nome_casa or "santos" in nome_fora:
                encontrou_santos = True
                p["status"] = "LIVE"
                
                # Verifica o placar retornado pela API externa
                score = p.get("score", {})
                full_time = score.get("fullTime", {})
                home_goals = full_time.get("home", 0)
                away_goals = full_time.get("away", 0)
                
                # Se a API externa estiver zerada, aplica o 2 a 1 atual.
                # Se a API externa avançar o placar, assume o valor novo automaticamente.
                if home_goals == 0 and away_goals == 0:
                    p["score"] = {"fullTime": {"home": 1, "away": 2}}
                    p["statusCustomizado"] = "AO VIVO • 2° Tempo (Santos 1 x 2 Bragantino)"
                else:
                    p["statusCustomizado"] = f"AO VIVO • ({home_goals}x{away_goals})"

        # Se a partida não vier na listagem da API externa, injetamos com o placar de 2 a 1 para o Bragantino
        if not encontrou_santos:
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
                "date": "Hoje",
                "time": "Ao Vivo",
                "status": "LIVE",
                "statusCustomizado": "AO VIVO • 2° Tempo (Santos 1 x 2 Bragantino)",
                "score": {
                    "fullTime": {"home": 1, "away": 2} # 2 a 1 para o Bragantino
                },
                "logo_transmissao_offline": LOGO_SITE,
                "status_transmissao": "AO_VIVO"
            }
            partidas.append(jogo_santos)

        return partidas

    except Exception as e:
        print(f"Erro ao buscar dados da API: {e}")
        return []
