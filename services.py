from datetime import datetime, timezone, timedelta
import urllib.request
import json

# Definição do fuso horário de Brasília (UTC-3)
BRT = timezone(timedelta(hours=-3))

# URLs oficiais da API pública da ESPN
ESPN_BRASILEIRA_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/bra.1/scoreboard"
ESPN_SERIE_B_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/bra.2/scoreboard"


def fetch_espn_data(url):
    """Busca dados atualizados da API da ESPN sem cache."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            },
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Erro na requisição para {url}: {e}")
    return {}


def formatar_status_tempo(date_str, state, status_detail):
    """Formata datas de jogos agendados (PRE) em BRT."""
    if state != "pre" or not date_str:
        return status_detail

    try:
        dt_jogo_utc = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        dt_jogo_brt = dt_jogo_utc.astimezone(BRT)
        agora_brt = datetime.now(BRT)

        delta_dias = (dt_jogo_brt.date() - agora_brt.date()).days
        hora_minuto = dt_jogo_brt.strftime("%H:%M")

        if delta_dias == 0:
            return f"Hoje às {hora_minuto}"
        elif delta_dias == 1:
            return f"Amanhã às {hora_minuto}"
        else:
            return dt_jogo_brt.strftime("%d/%m às %H:%M")
    except Exception:
        return status_detail


def _jogo_dentro_janela_partida(date_str, agora_brt):
    """Retorna True se a partida começou há menos de 2h15 (evita falso encerramento da ESPN)."""
    if not date_str:
        return False
    try:
        dt_jogo_utc = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        dt_jogo_brt = dt_jogo_utc.astimezone(BRT)
        decorrido = agora_brt - dt_jogo_brt
        return timedelta(minutes=-5) <= decorrido <= timedelta(hours=2, minutes=15)
    except Exception:
        return False


def _verificar_intervalo_espn(status_info):
    """
    Consulta estritamente os campos da ESPN para confirmar se o jogo está no intervalo.
    Evita falso positivo com 'First Half' ou 'Second Half' (bola rolando).
    """
    status_type = status_info.get("type", {})
    state = (status_type.get("state") or "").lower()
    if state != "in":
        return False

    type_name = (status_type.get("name") or "").upper()
    description = (status_type.get("description") or "").strip().lower()
    detail = (status_type.get("detail") or "").strip().lower()
    short_detail = (status_type.get("shortDetail") or "").strip().lower()

    if type_name == "STATUS_HALFTIME":
        return True

    termos_exatos = {"halftime", "half time", "intervalo", "ht"}
    if description in termos_exatos or detail in termos_exatos or short_detail in termos_exatos:
        return True

    return False


def _eh_jogo_coritiba_santos(match):
    """Identifica o confronto Coritiba x Santos para evitar duplicação com manual_matches."""
    home = ((match.get("home_team") or {}).get("name") or "").lower()
    away = ((match.get("away_team") or {}).get("name") or "").lower()
    times = {home, away}
    return any("coritiba" in t for t in times) and any("santos" in t for t in times)


def parse_espn_matches(data):
    """Processa o JSON da ESPN refletindo em tempo real Intervalo, Ao Vivo, Agendado e Encerrado."""
    matches = []
    if not data or not isinstance(data, dict) or "events" not in data:
        return matches

    agora_brt = datetime.now(BRT)

    for event in data.get("events", []):
        try:
            match_id = str(event.get("id", ""))
            name = event.get("name", "")
            date_str = event.get("date", "")

            status_info = event.get("status", {})
            status_type = status_info.get("type", {})
            state = (status_type.get("state") or "pre").lower()
            completed = bool(status_type.get("completed", False))

            dentro_janela = _jogo_dentro_janela_partida(date_str, agora_brt)
            no_intervalo = _verificar_intervalo_espn(status_info)

            if no_intervalo:
                status_code = "INTERVALO"
                status_detail = "Em Descanso"
            elif state == "in":
                status_code = "LIVE"
                raw_detail = (
                    status_type.get("shortDetail")
                    or status_type.get("detail")
                    or status_type.get("description")
                    or "Em andamento"
                )
                status_detail = raw_detail
            elif (state == "post" or completed) and not dentro_janela:
                status_code = "ENCERRADO"
                status_detail = "Encerrado"
            elif (state == "post" or completed) and dentro_janela:
                # Proteção contra falso encerramento da ESPN enquanto a partida ainda está na janela normal
                status_code = "LIVE"
                raw_detail = status_type.get("shortDetail") or status_type.get("detail") or "Em andamento"
                status_detail = "Em andamento" if "final" in raw_detail.lower() or "ft" in raw_detail.lower() else raw_detail
            else:
                status_code = "PRE"
                raw_detail = status_type.get("detail") or status_type.get("description", "")
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
                    "score": str(comp.get("score", "0")),
                }
                if comp.get("homeAway") == "home":
                    home_team = team_info
                else:
                    away_team = team_info

            matches.append(
                {
                    "id": match_id,
                    "name": name,
                    "date": date_str,
                    "status": status_code,
                    "status_text": status_detail,
                    "home_team": home_team,
                    "away_team": away_team,
                }
            )
        except Exception:
            continue

    return matches


def obter_jogos_serie_a():
    """Retorna os jogos da Série A (ESPN + Overrides manuais sem duplicação)."""
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
                    "score": "0",
                },
                "away_team": {
                    "name": "Flamengo",
                    "logo": "https://i.postimg.cc/c4mpD6zM/bola-removebg-preview.png",
                    "score": "0",
                },
                "status": "PRE",
                "status_text": "21:30",
                "date": "2026-12-02T21:30:00-03:00",
                "timestamp": int(datetime(2026, 12, 2, 21, 30, tzinfo=BRT).timestamp()),
            },
            {
                "id": "cor_san_2026",
                "name": "Coritiba vs Santos",
                "home_team": {
                    "name": "Coritiba",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/2034.png",
                    "score": "0",
                },
                "away_team": {
                    "name": "Santos",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/212.png",
                    "score": "0",
                },
                "status": "PRE",
                "status_text": "19:30",
                "date": "2026-11-18T19:30:00-03:00",
                "timestamp": int(datetime(2026, 11, 18, 19, 30, tzinfo=BRT).timestamp()),
            },
            {
                "id": "vas_int_2026",
                "name": "Vasco da Gama vs Internacional",
                "home_team": {
                    "name": "Vasco da Gama",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/3310.png",
                    "score": "0",
                },
                "away_team": {
                    "name": "Internacional",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/159.png",
                    "score": "0",
                },
                "status": "PRE",
                "status_text": "19:30",
                "date": "2026-11-19T19:30:00-03:00",
                "timestamp": int(datetime(2026, 11, 19, 19, 30, tzinfo=BRT).timestamp()),
            },
            {
                "id": "flu_mir_2026",
                "name": "Fluminense vs Mirassol",
                "home_team": {
                    "name": "Fluminense",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/3445.png",
                    "score": "0",
                },
                "away_team": {
                    "name": "Mirassol",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/2027.png",
                    "score": "0",
                },
                "status": "PRE",
                "status_text": "18:30",
                "date": "2026-11-22T18:30:00-03:00",
                "timestamp": int(datetime(2026, 11, 22, 18, 30, tzinfo=BRT).timestamp()),
            },
            {
                "id": "san_gre_2026",
                "name": "Santos vs Grêmio",
                "home_team": {
                    "name": "Santos",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/212.png",
                    "score": "0",
                },
                "away_team": {
                    "name": "Grêmio",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/131.png",
                    "score": "0",
                },
                "status": "PRE",
                "status_text": "21:00",
                "date": "2026-11-23T21:00:00-03:00",
                "timestamp": int(datetime(2026, 11, 23, 21, 0, tzinfo=BRT).timestamp()),
            },
            {
                "id": "vit_san_2026",
                "name": "EC Vitória vs Santos",
                "home_team": {
                    "name": "EC Vitória",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/3457.png",
                    "score": "0",
                },
                "away_team": {
                    "name": "Santos",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/212.png",
                    "score": "0",
                },
                "status": "PRE",
                "status_text": "16:00",
                "date": "2026-11-29T16:00:00-03:00",
                "timestamp": int(datetime(2026, 11, 29, 16, 0, tzinfo=BRT).timestamp()),
            },
            {
                "id": "san_bot_2026",
                "name": "Santos vs Botafogo",
                "home_team": {
                    "name": "Santos",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/212.png",
                    "score": "0",
                },
                "away_team": {
                    "name": "Botafogo",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/3440.png",
                    "score": "0",
                },
                "status": "PRE",
                "status_text": "21:30",
                "date": "2026-12-02T21:30:00-03:00",
                "timestamp": int(datetime(2026, 12, 2, 21, 30, tzinfo=BRT).timestamp()),
            },
        ]

        for mm in manual_matches:
            mm["status_text"] = formatar_status_tempo(
                mm.get("date"), mm.get("status", "").lower(), mm.get("status_text")
            )

        existing_ids = {m["id"] for m in matches}
        tem_coritiba_santos_espn = any(_eh_jogo_coritiba_santos(m) for m in matches)

        for mm in manual_matches:
            if mm["id"] == "cor_san_2026" and tem_coritiba_santos_espn:
                continue
            if mm["id"] not in existing_ids:
                matches.append(mm)
                existing_ids.add(mm["id"])

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
