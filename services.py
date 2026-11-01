from datetime import date
import requests

def obter_jogos_serie_a(api_endpoint: str = None):
    """
    Busca a partida em destaque no topo da live (mesmo offline):
    1. Procura jogo rolando AO VIVO.
    2. Se não houver, busca o próximo jogo agendado / futuro (ex: Santos x Bragantino).
    3. Se não houver nenhum jogo futuro na API, usa o último jogo finalizado como histórico.
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

        # 1. Prioridade máxima: Jogo AO VIVO agora
        partida_destaque = next((p for p in partidas if p.get("status") in ["LIVE", "IN_PLAY"]), None)

        # 2. Segunda prioridade: O próximo jogo agendado ou jogo de hoje (funciona mesmo offline!)
        if not partida_destaque:
            # Filtra partidas que vão acontecer hoje ou em datas futuras
            partidas_futuras = [
                p for p in partidas 
                if p.get("status") in ["SCHEDULED", "TIMED", "AGENDADO", "NOT_STARTED"] or str(p.get("date", "")) >= hoje
            ]
            if partidas_futuras:
                # Pega o primeiro jogo agendado da fila (o mais próximo cronologicamente)
                partida_destaque = partidas_futuras[0]

        # 3. Fallback: Se a temporada acabou e não tem jogo futuro, mostra o último encerrado
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
