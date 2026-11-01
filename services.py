
from datetime import date
import requests

def obter_jogos_serie_a(api_endpoint: str = None):
    """
    Busca a partida em destaque no topo da live:
    1. Prioriza o jogo de HOJE ou o PRÓXIMO jogo agendado (mesmo com a live offline).
    2. Se houver jogo rolando ao vivo, ele assume o destaque.
    3. Só usa partida finalizada como último recurso se não houver mais nenhum jogo futuro.
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

        # 1. Procura primeiro se há um jogo rolando AO VIVO
        partida_destaque = next((p for p in partidas if p.get("status") in ["LIVE", "IN_PLAY"]), None)

        # 2. Se não estiver ao vivo, procura imediatamente o jogo agendado para HOJE ou o PRÓXIMO jogo futuro (ex: Santos x Bragantino amanhã)
        if not partida_destaque:
            # Filtra partidas de hoje ou futuras
            partidas_futuras = [
                p for p in partidas 
                if p.get("status") in ["SCHEDULED", "TIMED", "AGENDADO", "NOT_STARTED"] or str(p.get("date", "")) >= hoje
            ]
            if partidas_futuras:
                partida_destaque = partidas_futuras[0] # Pega o próximo jogo da fila (ex: Santos)

        # 3. Fallback absoluto: Se realmente não houver nenhum jogo agendado para frente, mostra o último encerrado
        if not partida_destaque:
            partidas_finalizadas = [p for p in partidas if p.get("status") in ["FINISHED", "FT", "Partida Finalizada"]]
            if partidas_finalizadas:
                partida_destaque = partidas_finalizadas[-1]
                partida_destaque["statusCustomizado"] = "Partida Finalizada"
            else:
                partida_destaque = partidas[0]

        return [partida_destaque] if partida_destaque else partidas

    except Exception as e:
        print(f"Erro ao buscar dados da API: {e}")
        return []
