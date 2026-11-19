from datetime import datetime, timezone, timedelta
import urllib.request
import unicodedata
import json

# Definição do fuso horário de Brasília (UTC-3)
BRT = timezone(timedelta(hours=-3))

# URL oficial da API pública da ESPN para a Série A
ESPN_BRASILEIRA_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/bra.1/scoreboard"

MAX_RODADAS = 38
RODADA_INICIAL_FOCO = 35


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


def _normalizar_texto(txt):
    """Remove acentos e padroniza nomes de times para evitar duplicados."""
    if not txt:
        return ""
    nfkd = unicodedata.normalize("NFKD", str(txt).lower().strip())
    limpo = "".join(c for c in nfkd if not unicodedata.combining(c))
    aliases = {
        "athletico paranaense": "athletico-pr",
        "ec vitoria": "vitoria",
        "vasco": "vasco da gama",
        "bragantino": "red bull bragantino",
    }
    return aliases.get(limpo, limpo)


def _chave_confronto(match):
    """Gera chave única (times ordenados + data BRT) para eliminar jogos duplicados."""
    home = _normalizar_texto((match.get("home_team") or {}).get("name"))
    away = _normalizar_texto((match.get("away_team") or {}).get("name"))
    times_ord = tuple(sorted([home, away]))

    date_str = match.get("date") or ""
    dia_brt = ""
    if date_str:
        try:
            dt_brt = datetime.fromisoformat(date_str.replace("Z", "+00:00")).astimezone(BRT)
            dia_brt = dt_brt.strftime("%Y-%m-%d")
        except Exception:
            dia_brt = date_str[:10]

    return (times_ord, dia_brt)


def _inferir_rodada_por_data(date_str, rodada_espn=None):
    """Define a rodada real (35 a 38) com base na data do jogo em BRT."""
    if date_str:
        try:
            dt_brt = datetime.fromisoformat(date_str.replace("Z", "+00:00")).astimezone(BRT)
            data_jogo = dt_brt.date()

            if data_jogo <= datetime(2026, 11, 20).date():
                return 35
            elif data_jogo <= datetime(2026, 11, 24).date():
                return 36
            elif data_jogo <= datetime(2026, 11, 30).date():
                return 37
            else:
                return 38
        except Exception:
            pass

    if rodada_espn:
        return max(RODADA_INICIAL_FOCO, min(MAX_RODADAS, int(rodada_espn)))
    return RODADA_INICIAL_FOCO


def _timestamp_jogo(date_str):
    """Retorna timestamp inteiro para ordenação cronológica estável."""
    if not date_str:
        return 0
    try:
        return int(datetime.fromisoformat(date_str.replace("Z", "+00:00")).timestamp())
    except Exception:
        return 0


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


def _verificar_intervalo_espn(status_info):
    """Consulta estritamente os campos da ESPN para confirmar intervalo."""
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
    return (
        description in termos_exatos
        or detail in termos_exatos
        or short_detail in termos_exatos
    )


def _eh_jogo_coritiba_santos(match):
    """Identifica o confronto Coritiba x Santos."""
    home = _normalizar_texto((match.get("home_team") or {}).get("name"))
    away = _normalizar_texto((match.get("away_team") or {}).get("name"))
    times = {home, away}
    return "coritiba" in times and "santos" in times


def _corrigir_placar_coritiba_santos(matches):
    """Garante o resultado oficial: Santos 1 x 0 Coritiba."""
    for m in matches:
        if not _eh_jogo_coritiba_santos(m):
            continue

        home = dict(m.get("home_team") or {})
        away = dict(m.get("away_team") or {})

        home_nome = _normalizar_texto(home.get("name"))
        away_nome = _normalizar_texto(away.get("name"))

        if "santos" in home_nome:
            home["score"] = "1"
            away["score"] = "0"
        elif "coritiba" in home_nome:
            home["score"] = "0"
            away["score"] = "1"
        elif "santos" in away_nome:
            away["score"] = "1"
            home["score"] = "0"

        m["home_team"] = home
        m["away_team"] = away
        m["status"] = "ENCERRADO"
        m["status_text"] = "Encerrado"


def _extrair_rodada_espn(data, event=None):
    """Extrai o número da rodada da Série A na ESPN garantindo o intervalo 1..38."""
    rodada = None
    if isinstance(event, dict):
        week = event.get("week") or {}
        if isinstance(week, dict) and week.get("number"):
            rodada = week.get("number")

    if not rodada and isinstance(data, dict):
        week = data.get("week") or {}
        if isinstance(week, dict) and week.get("number"):
            rodada = week.get("number")
        elif data.get("leagues"):
            league_week = (data["leagues"][0].get("season") or {}).get("type", {})
            if isinstance(league_week, dict) and league_week.get("week"):
                rodada = league_week.get("week")

    try:
        rodada_int = int(rodada)
        return max(1, min(MAX_RODADAS, rodada_int))
    except (TypeError, ValueError):
        return None


def calcular_rodada_atual_serie_a(matches, data_espn=None):
    """
    Calcula automaticamente a rodada atual da Série A (35 a 38):
    - Mantém na rodada atual enquanto houver jogo não encerrado nela.
    - Avança automaticamente para 36, 37 e 38 assim que os jogos da rodada encerrarem.
    """
    rodada_fonte = _extrair_rodada_espn(data_espn) or RODADA_INICIAL_FOCO
    jogos_validos = [m for m in matches if m.get("rodada")]

    if not jogos_validos:
        return max(RODADA_INICIAL_FOCO, min(MAX_RODADAS, rodada_fonte))

    rodadas_presentes = sorted({int(m["rodada"]) for m in jogos_validos})

    for r in rodadas_presentes:
        if r < RODADA_INICIAL_FOCO:
            continue
        jogos_da_rodada = [m for m in jogos_validos if int(m["rodada"]) == r]
        tem_jogo_pendente = any(
            m.get("status") in ("LIVE", "INTERVALO", "PRE") for m in jogos_da_rodada
        )
        if tem_jogo_pendente:
            return max(RODADA_INICIAL_FOCO, min(MAX_RODADAS, r))

    proxima_rodada = max(RODADA_INICIAL_FOCO, rodada_fonte, max(rodadas_presentes)) + 1
    return max(RODADA_INICIAL_FOCO, min(MAX_RODADAS, proxima_rodada))


def parse_espn_matches(data, rodada_padrao=None):
    """Processa o JSON da ESPN da Série A refletindo Intervalo, Ao Vivo, Agendado, Encerrado e Rodada."""
    matches = []
    if not data or not isinstance(data, dict) or "events" not in data:
        return matches

    rodada_geral = _extrair_rodada_espn(data) or rodada_padrao

    for event in data.get("events", []):
        try:
            match_id = str(event.get("id", ""))
            name = event.get("name", "")
            date_str = event.get("date", "")
            rodada_espn = _extrair_rodada_espn(data, event) or rodada_geral
            rodada_evento = _inferir_rodada_por_data(date_str, rodada_espn)

            status_info = event.get("status", {})
            status_type = status_info.get("type", {})
            state = (status_type.get("state") or "pre").lower()
            completed = bool(status_type.get("completed", False))
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
            elif state == "post" or completed:
                status_code = "ENCERRADO"
                status_detail = "Encerrado"
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
                    "timestamp": _timestamp_jogo(date_str),
                    "rodada": rodada_evento,
                    "status": status_code,
                    "status_text": status_detail,
                    "home_team": home_team,
                    "away_team": away_team,
                }
            )
        except Exception:
            continue

    return matches


def _buscar_jogos_espn_rodadas_35_a_38():
    """Busca jogos da ESPN cobrindo o recorte atual e as datas das rodadas 35 a 38 sem duplicar."""
    acumulado = []
    ids_vistos = set()
    confrontos_vistos = set()

    raw_principal = fetch_espn_data(ESPN_BRASILEIRA_URL)
    for m in parse_espn_matches(raw_principal):
        chave = _chave_confronto(m)
        if m["id"] and m["id"] not in ids_vistos and chave not in confrontos_vistos:
            acumulado.append(m)
            ids_vistos.add(m["id"])
            confrontos_vistos.add(chave)

    datas_consulta = [
        "20261118",
        "20261119",
        "20261121",
        "20261122",
        "20261123",
        "20261126",
        "20261129",
        "20261202",
        "20261203",
    ]

    for dt_str in datas_consulta:
        raw_dia = fetch_espn_data(f"{ESPN_BRASILEIRA_URL}?dates={dt_str}")
        for m in parse_espn_matches(raw_dia):
            chave = _chave_confronto(m)
            if m["id"] and m["id"] not in ids_vistos and chave not in confrontos_vistos:
                acumulado.append(m)
                ids_vistos.add(m["id"])
                confrontos_vistos.add(chave)

    return acumulado, raw_principal


def obter_jogos_serie_a():
    """Retorna os jogos da Série A da rodada 35 até a 38 sem duplicatas e com rodadas corretas."""
    try:
        matches, raw_principal = _buscar_jogos_espn_rodadas_35_a_38()

        manual_matches = [
            {
                "id": "chap_fla_2026",
                "name": "Chapecoense vs Flamengo",
                "rodada": 38,
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
                "rodada": 35,
                "home_team": {
                    "name": "Coritiba",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/3456.png",
                    "score": "0",
                },
                "away_team": {
                    "name": "Santos",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/2674.png",
                    "score": "1",
                },
                "status": "ENCERRADO",
                "status_text": "Encerrado",
                "date": "2026-11-18T19:30:00-03:00",
                "timestamp": int(datetime(2026, 11, 18, 19, 30, tzinfo=BRT).timestamp()),
            },
            {
                "id": "vas_int_2026",
                "name": "Vasco da Gama vs Internacional",
                "rodada": 35,
                "home_team": {
                    "name": "Vasco da Gama",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/3454.png",
                    "score": "0",
                },
                "away_team": {
                    "name": "Internacional",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/1936.png",
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
                "rodada": 36,
                "home_team": {
                    "name": "Fluminense",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/3445.png",
                    "score": "0",
                },
                "away_team": {
                    "name": "Mirassol",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/9169.png",
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
                "rodada": 36,
                "home_team": {
                    "name": "Santos",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/2674.png",
                    "score": "0",
                },
                "away_team": {
                    "name": "Grêmio",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/6273.png",
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
                "rodada": 37,
                "home_team": {
                    "name": "EC Vitória",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/3457.png",
                    "score": "0",
                },
                "away_team": {
                    "name": "Santos",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/2674.png",
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
                "rodada": 38,
                "home_team": {
                    "name": "Santos",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/2674.png",
                    "score": "0",
                },
                "away_team": {
                    "name": "Botafogo",
                    "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/6086.png",
                    "score": "0",
                },
                "status": "PRE",
                "status_text": "21:30",
                "date": "2026-12-02T21:30:00-03:00",
                "timestamp": int(datetime(2026, 12, 2, 21, 30, tzinfo=BRT).timestamp()),
            },
        ]

        existing_ids = {m["id"] for m in matches}
        existing_confrontos = {_chave_confronto(m) for m in matches}

        for mm in manual_matches:
            if mm.get("status", "").lower() == "pre":
                mm["status_text"] = formatar_status_tempo(
                    mm.get("date"), "pre", mm.get("status_text")
                )

            chave_mm = _chave_confronto(mm)
            if mm["id"] not in existing_ids and chave_mm not in existing_confrontos:
                matches.append(mm)
                existing_ids.add(mm["id"])
                existing_confrontos.add(chave_mm)

        matches_filtrados = [
            m for m in matches
            if not m.get("rodada") or (RODADA_INICIAL_FOCO <= int(m["rodada"]) <= MAX_RODADAS)
        ]

        _corrigir_placar_coritiba_santos(matches_filtrados)

        rodada_atual = calcular_rodada_atual_serie_a(matches_filtrados, raw_principal)
        for m in matches_filtrados:
            m["rodada"] = _inferir_rodada_por_data(m.get("date"), m.get("rodada") or rodada_atual)
            m["rodada_atual"] = rodada_atual
            if not m.get("timestamp"):
                m["timestamp"] = _timestamp_jogo(m.get("date"))

        matches_filtrados.sort(key=lambda item: (int(item.get("rodada") or 35), int(item.get("timestamp") or 0)))
        return matches_filtrados
    except Exception as e:
        print(f"Erro em obter_jogos_serie_a: {e}")
        return []


def obter_rodada_atual_serie_a():
    """Retorna o número inteiro da rodada atual da Série A (de 35 até 38)."""
    matches = obter_jogos_serie_a()
    if matches and matches[0].get("rodada_atual"):
        return matches[0]["rodada_atual"]
    return RODADA_INICIAL_FOCO


def obter_jogos_serie_b():
    """Mantida apenas para compatibilidade de importação no main.py."""
    return []
