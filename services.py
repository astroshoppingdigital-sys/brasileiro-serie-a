from datetime import date
import httpx

async def buscar_partida_destaque(api_endpoint: str):
    """
    Busca a partida em destaque no topo da live:
    1. Procura jogo rolando AO VIVO.
    2. Se não houver, procura o jogo agendado para HOJE.
    3. Se não houver jogo hoje, pega o próximo jogo agendado (ex: o jogo de amanhã que já está na API).
    4. Fallback final: se não houver futuro, pega a última partida encerrada.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_endpoint)
            if response.status_code != 200:
                return None
            
            data = response.json()
            partidas = data.get("matches", data.get("response", []))
            
            if not partidas:
                return None

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
                    partida_destaque = partidas_futuras[0] # Pega o próximo da fila
            
            # 4. Fallback: Se não houver futuro, pega a última partida encerrada
            if not partida_destaque:
                partidas_finalizadas = [p for p in partidas if p.get("status") in ["FINISHED", "FT", "Partida Finalizada"]]
                if partidas_finalizadas:
                    partida_destaque = partidas_finalizadas[-1]
                    partida_destaque["statusCustomizado"] = "Partida Finalizada"
                else:
                    partida_destaque = partidas[0]

            return partida_destaque

    except Exception as e:
        print(f"Erro ao buscar dados da API: {e}")
        return None
