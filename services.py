from datetime import datetime, timezone, timedelta
import urllib.request
import json

# Definição do fuso horário de Brasília (UTC-3)
BRT = timezone(timedelta(hours=-3))

# URLs oficiais da API pública da ESPN
ESPN_BRASILEIRA_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/bra.1/scoreboard"
ESPN_SERIE_B_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/bra.2/scoreboard"

def fetch_espn_data(url):
    """Busca dados da API usando urllib (nativo do Python)."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Erro na requisição para {url}: {e}")
    return {}

def formatar_status_tempo(date_str, state, status_detail):
    """
    Calcula dinamicamente o rótulo de tempo para jogos agendados (PRE):
    - Se for no mesmo dia: 'Hoje às HH:MM'
    - Se for no dia seguinte (Amanhã): 'Amanhã às HH:MM'
    - Se for em outra data: exibe 'DD/MM às HH:MM'
    Se o jogo estiver ao vivo ou encerrado, respeita o estado da ESPN.
    """
    if state != "pre" or not date_str:
        return status_detail

    try:
        # Converte a data do jogo para o fuso de Brasília
        dt_jogo_utc = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        dt_jogo_brt = dt_jogo_utc.astimezone(BRT)
        
        agora_brt = datetime.now(BRT)
        
        data_jogo = dt_jogo_brt.date()
        data_hoje = agora_brt.date()
        
        hora_minuto = dt_jogo_brt.strftime("%H:%M")
        
        # Diferença exata de dias
        delta_dias = (data_jogo - data_hoje).days
        
        if delta_dias == 0:
            return f"Hoje às {hora_minuto}"
        elif delta_dias == 1:
            return f"Amanhã às {hora_minuto}"
        else:
            # Para jogos mais distantes, mostra a data e o horário certinho
            return dt_jogo_brt.strftime("%d/0%m às %H:%M" if dt_jogo_brt.month < 10 else "%d/%m às %H:%M")
    except Exception:
        return status_detail

def parse_espn_matches(data):
    """Processa o JSON da ESPN no formato padrão do backend."""
    matches = []
    if not data or not isinstance(data, dict) or "events" not in data:
        return matches

    for event in data.get("events", []):
        try:
            match_id = str(event.get("id", ""))
            name = event.get("name", "")
            date_str = event.get("date", "")
            
            status_info = event.get("status", {})
            status_type = status_info.get("type", {})
            state = status_type.get("state", "pre")  # 'pre', 'in', 'post'
            
            # Padroniza para 'LIVE' quando estiver em andamento
            status_code = "LIVE" if state == "in" else state.upper()
            
            raw_detail = status_type.get("detail") or status_type.get("description", "")
            
            # Aplica a inteligência de cálculo de tempo para todos os jogos agendados
            status_detail = formatar_status_tempo(date_str, state, raw_detail)
            
            competitions = event.get("competitions", [])
            if not competitions:
                continue
                
            competition = competitions[0]
            competitors = competition.get("competitors", [])
            
            home_team = None
            away_team = None
            
            for comp in competitors:
                team_data = comp.get("team", {})
                team_info = {
                    "name": team_data.get("displayName") or team_data.get("name", "Time"),
                    "logo": team_data.get("logo", ""),
                    "score": str(comp.get("score", "0"))
                }
                if comp.get("homeAway") == "home":
                    home_team = team_info
                else:
                    away_team = team_info

            matches.append({
                "id": match_id,
                "name": name,
                "date": date_str,
                "status": status_code,
                "status_text": status_detail,
                "home_team": home_team,
                "away_team": away_team
            })
        except Exception:
            continue

    return matches

def obter_jogos_serie_a():
    """Retorna os jogos da Série A + Overrides manuais atualizados."""
    try:
        raw_data = fetch_espn_data(ESPN_BRASILEIRA_URL)
        matches = parse_espn_matches(raw_data)
        
        manual_matches = [
            {
                "id": "chap_fla_2026",
                "name": "Chapecoense vs Flamengo",
                "home_team": {
                    "name": "Chapecoense",
                    "logo": "https://i.postimg.cc/y8KNRJZh/13635096-m-removebg-preview.png",
                    "score": "0"
                },
                "away_team": {
                    "name": "Flamengo",
                    "logo": "https://i.postimg.cc/c4mpD6zM/bola-removebg-preview.png",
                    "score": "0"
                },
                "status": "PRE",
                "status_text": "21:30",
                "date": "2026-12-02T21:30:00-03:00",
                "timestamp": int(datetime(2026, 12, 2, 21, 30, tzinfo=BRT).timestamp())
            },
            {
                "id": "cor_san_2026",
                "name": "Coritiba vs Santos",
                "home_team": {
                    "name": "Coritiba",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/2034.png",
                    "score": "0"
                },
                "away_team": {
                    "name": "Santos",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/212.png",
                    "score": "0"
                },
                "status": "PRE",
                "status_text": "19:30",
                "date": "2026-11-18T19:30:00-03:00",
                "timestamp": int(datetime(2026, 11, 18, 19, 30, tzinfo=BRT).timestamp())
            },
            {
                "id": "vas_int_2026",
                "name": "Vasco da Gama vs Internacional",
                "home_team": {
                    "name": "Vasco da Gama",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/3310.png",
                    "score": "0"
                },
                "away_team": {
                    "name": "Internacional",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/159.png",
                    "score": "0"
                },
                "status": "PRE",
                "status_text": "19:30",
                "date": "2026-11-19T19:30:00-03:00",
                "timestamp": int(datetime(2026, 11, 19, 19, 30, tzinfo=BRT).timestamp())
            },
            {
                "id": "flu_mir_2026",
                "name": "Fluminense vs Mirassol",
                "home_team": {
                    "name": "Fluminense",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/3445.png",
                    "score": "0"
                },
                "away_team": {
                    "name": "Mirassol",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/2027.png",
                    "score": "0"
                },
                "status": "PRE",
                "status_text": "18:30",
                "date": "2026-11-22T18:30:00-03:00",
                "timestamp": int(datetime(2026, 11, 22, 18, 30, tzinfo=BRT).timestamp())
            },
            {
                "id": "san_gre_2026",
                "name": "Santos vs Grêmio",
                "home_team": {
                    "name": "Santos",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/212.png",
                    "score": "0"
                },
                "away_team": {
                    "name": "Grêmio",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/131.png",
                    "score": "0"
                },
                "status": "PRE",
                "status_text": "21:00",
                "date": "2026-11-23T21:00:00-03:00",
                "timestamp": int(datetime(2026, 11, 23, 21, 0, tzinfo=BRT).timestamp())
            },
            {
                "id": "vit_san_2026",
                "name": "EC Vitória vs Santos",
                "home_team": {
                    "name": "EC Vitória",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/3457.png",
                    "score": "0"
                },
                "away_team": {
                    "name": "Santos",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/212.png",
                    "score": "0"
                },
                "status": "PRE",
                "status_text": "16:00",
                "date": "2026-11-29T16:00:00-03:00",
                "timestamp": int(datetime(2026, 11, 29, 16, 0, tzinfo=BRT).timestamp())
            },
            {
                "id": "san_bot_2026",
                "name": "Santos vs Botafogo",
                "home_team": {
                    "name": "Santos",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/212.png",
                    "score": "0"
                },
                "away_team": {
                    "name": "Botafogo",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/3440.png",
                    "score": "0"
                },
                "status": "PRE",
                "status_text": "21:30",
                "date": "2026-12-02T21:30:00-03:00",
                "timestamp": int(datetime(2026, 12, 2, 21, 30, tzinfo=BRT).timestamp())
            }
        ]
        
        # Aplica a formatação inteligente de tempo também nos jogos manuais/overrides
        for mm in manual_matches:
            mm["status_text"] = formatar_status_tempo(mm.get("date"), mm.get("status", "").lower(), mm.get("status_text"))

        existing_ids = {m["id"] for m in matches}
        for mm in manual_matches:
            if mm["id"] not in existing_ids:
                matches.append(mm)
                
        return matches
    except Exception as e:
        print(f"Erro em obter_jogos_serie_a: {e}")
        return []

def obter_jogos_serie_b():
    """Retorna os jogos da Série B."""
    try:
        raw_data = fetch_espn_data(ESPN_SERIE_B_URL)
        return parse_espn_matches(raw_data)
    except Exception as e:
        print(f"Erro em obter_jogos_serie_b: {e}")
        return []
