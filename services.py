
from datetime import date
import requests

def obter_jogos_serie_a(api_endpoint: str = None):
    """
    Busca a partida em destaque no topo da live:
    1. Procura jogo rolando AO VIVO.
    2. Se não houver, procura o jogo agendado para HOJE.
    3. Se não houver jogo hoje, pega o PRÓXIMO jogo agendado (ex: o jogo de amanhã).
    4. Fallback final: se não houver futuro, pega a última partida encerrada.
    """
    if not api_endpoint:
        # Coloque a URL padrão da sua API aqui caso o endpoint não seja passado
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

        # 1. Procura jogo ao vivo agora
        partida_destaque = next((p for p in partidas if p.get("status") in ["LIVE", "IN_PLAY"]), None)

        # 2. Se não houver ao vivo, procura jogo para HOJE
        if not partida_destaque:
            partida_destaque = next((p for p in partidas if str(p.get("date", "")).startswith(hoje)), None)

        # 3. Se não houver jogo hoje, pega o PRÓXIMO jogo agendado (como o de amanhã)
        if not partida_destaque:
            partidas_futuras = [p for p in partidas if p.get("status") in ["SCHEDULED", "TIMED", "AGENDADO"] or str(p.get("date", "")) > hoje]
            if partidas_futuras:
                partida_destaque = partidas_futuras[0]

        # 4. Fallback: Se não houver futuro, pega a última partida encerrada
        if not partida_destaque:
            partidas_finalizadas = [p for p in partidas if p.get("status") in ["FINISHED", "FT", "Partida Finalizada"]]
            if partidas_finalizadas:
                partida_destaque = partidas_finalizadas[-1]
                partida_destaque["statusCustomizado"] = "Partida Finalizada"
            else:
                partida_destaque = partidas[0]

        # Retorna a lista contendo a partida destaque ou a lista completa conforme esperado pelo main.py
        return [partida_destaque] if partida_destaque else partidas

    except Exception as e:
        print(f"Erro ao buscar dados da API: {e}")
        return []
