from datetime import datetime, timezone, timedelta
import requests

# Definição do fuso horário de Brasília (UTC-3)
BRT = timezone(timedelta(hours=-3))

def get_espn_scoreboard(league="bra.1"):
    """
    Busca os dados de placares ao vivo da API da ESPN para a liga especificada.
    Padrão: bra.1 (Série A)
    """
    url = f"https://site.web.api.espn.com/apis/site/v2/sports/soccer/{league}/scoreboard"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Erro ao buscar dados da ESPN para {league}: {e}")
    return None

def parse_espn_matches(data):
    """
    Processa o JSON bruto da ESPN e converte no formato padronizado do backend.
    """
    matches = []
    if not data or "events" not in data:
        return matches

    for event in data["events"]:
        match_id = event.get("id")
        name = event.get("name")
        date_str = event.get("date")
        
        # Dados da competição / status
        status_info = event.get("status", {})
        status_type = status_info.get("type", {})
        state = status_type.get("state")  # 'pre', 'in', 'post'
        status_detail = status_type.get("detail") or status_type.get("description")
        
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
                "name": team_data.get("displayName") or team_data.get("name"),
                "logo": team_data.get("logo"),
                "score": comp.get("score", "0")
            }
            if comp.get("homeAway") == "home":
                home_team = team_info
            else:
                away_team = team_info

        matches.append({
            "id": match_id,
            "name": name,
            "date": date_str,
            "status": state,
            "status_text": status_detail,
            "home_team": home_team,
            "away_team": away_team
        })

    return matches

def get_serie_a_matches():
    """
    Retorna as partidas da Série A, integrando a automação da ESPN 
    e adicionando manualmente entradas programadas específicas (como Chapecoense x Flamengo).
    """
    # 1. Puxa os dados automatizados da API da ESPN (Série A: bra.1)
    raw_data = get_espn_scoreboard("bra.1")
    matches = parse_espn_matches(raw_data)
    
    # Lista de jogos manuais/programados que precisam constar obrigatoriamente
    manual_matches = [
        {
            "id": "chap_fla_2026",
            "name": "Chapecoense vs Flamengo",
            "home_team": {
                "name": "Chapecoense",
                "logo": "https://i.postimg.cc/xxx/chapecoense.png",
                "score": "0"
            },
            "away_team": {
                "name": "Flamengo",
                "logo": "https://i.postimg.cc/xxx/flamengo.png",
                "score": "0"
            },
            "status": "pre",
            "status_text": "21:30",
            "date": "2026-12-02T21:30:00-03:00",
            "timestamp": int(datetime(2026, 12, 2, 21, 30, tzinfo=BRT).timestamp())
        }
    ]
    
    # Evita duplicidade caso a ESPN já retorne o jogo na listagem oficial
    existing_ids = {m["id"] for m in matches}
    for mm in manual_matches:
        if mm["id"] not in existing_ids:
            matches.append(mm)
            
    return matches

def get_serie_b_matches():
    """
    Retorna as partidas da Série B usando o endpoint correspondente (bra.2).
    """
    raw_data = get_espn_scoreboard("bra.2")
    return parse_espn_matches(raw_data)
