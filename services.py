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
            status_detail = status_type.get("detail") or status_type.get("description", "")
            
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
    """Retorna os jogos da Série A + Override da Chapecoense vs Flamengo com escudos personalizados."""
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
            }
        ]
        
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
