from datetime import date
import requests

def obter_jogos_serie_a(api_endpoint: str = None):
    """
    Retorna os jogos da Série A organizados para alimentar as abas:
    Agendados, Ao Vivo e Encerrados, além de injetar a logo oficial do site.
    """
    if not api_endpoint:
        api_endpoint = "https://sua-api-de-futebol.com/api/jogos"

    try:
        response = requests.get(api_endpoint, timeout=10)
        if response.status_code != 200:
            return []
        
        data = response.json()
        partidas = data.get("matches", data.get("response", data if isinstance(data, list) else []))
        
        if not partidas:
            return []

        # Garante que a logo do site e os parâmetros de exibição offline estejam em todas as partidas
        logo_site = "https://i.postimg.cc/K8PR1kCv/Gemini-Generated-Image-hozi2rhozi2rhozi-removebg-preview.png"
        
        for p in partidas:
            p["logo_transmissao_offline"] = logo_site
            status_atual = str(p.get("status", "")).upper()
            is_live = status_atual in ["LIVE", "IN_PLAY", "AO_VIVO"]
            p["status_transmissao"] = "AO_VIVO" if is_live else "OFFLINE"

        return partidas

    except Exception as e:
        print(f"Erro ao buscar dados da API: {e}")
        return []
