from datetime import date
import requests

def obter_jogos_serie_a(api_endpoint: str = None):
    """
    Busca os jogos da Série A, garante que o jogo do Santos x Bragantino 
    apareça no topo e retorna a lista completa para a aba Agendados.
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

        hoje = str(date.today())
        partida_destaque = None

        # 1. Prioridade máxima: Jogo AO VIVO rodando agora
        partida_destaque = next((p for p in partidas if p.get("status") in ["LIVE", "IN_PLAY"]), None)

        # 2. Busca especificamente o jogo de Santos x Bragantino para garantir o destaque e exibição nos agendados
        if not partida_destaque:
            partida_destaque = next((
                p for p in partidas 
                if ("santos" in str(p.get("homeTeam", {}).get("name", "")).lower() or "santos" in str(p.get("awayTeam", {}).get("name", "")).lower()) 
                and ("bragantino" in str(p.get("homeTeam", {}).get("name", "")).lower() or "bragantino" in str(p.get("awayTeam", {}).get("name", "")).lower())
            ), None)

        # 3. Se não achar o do Santos especificamente, pega o próximo jogo agendado/futuro da fila
        if not partida_destaque:
            partidas_futuras = [
                p for p in partidas 
                if p.get("status") in ["SCHEDULED", "TIMED", "AGENDADO", "NOT_STARTED"] or str(p.get("date", "")) >= hoje
            ]
            if partidas_futuras:
                partida_destaque = partidas_futuras[0]

        # 4. Fallback: Último jogo encerrado caso não haja mais partidas futuras
        if not partida_destaque:
            partidas_finalizadas = [p for p in partidas if p.get("status") in ["FINISHED", "FT", "Partida Finalizada"]]
            if partidas_finalizadas:
                partida_destaque = partidas_finalizadas[-1]
                partida_destaque["statusCustomizado"] = "Partida Finalizada"
            else:
                partida_destaque = partidas[0]

        # Injeta a logo do seu site e o estado da transmissão no destaque
        if partida_destaque:
            partida_destaque["logo_transmissao_offline"] = "https://i.postimg.cc/K8PR1kCv/Gemini-Generated-Image-hozi2rhozi2rhozi-removebg-preview.png"
            is_live = partida_destaque.get("status") in ["LIVE", "IN_PLAY"]
            partida_destaque["status_transmissao"] = "AO_VIVO" if is_live else "OFFLINE"

        # Retorna a lista completa para preencher os Agendados, mantendo o destaque preparado
        return partidas

    except Exception as e:
        print(f"Erro ao buscar dados da API: {e}")
        return []
