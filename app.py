import os
import urllib.parse

import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# ── 페이지 설정 ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="나의 유럽 교환학생 기록기",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 테마 팔레트 (라이트 / 다크) ─────────────────────────────────────────────
LIGHT = {
    "BG": "#F7F6F3", "TEXT": "#37352F",
    "SIDEBAR_BG": "#FBFAF8", "SIDEBAR_BORDER": "#E8E5DE",
    "CARD_BG": "#FFFFFF", "CARD_BORDER": "#E8E5DE",
    "HERO_G1": "#ffffff", "HERO_G2": "#f0ede6",
    "MUTED": "#959CA6",
    "SUB": "#787672",
    "TAG_BG": "#EAE7DF", "TAG_TEXT": "#5F5B53",
    "BADGE_BG": "#F0EDE6", "BADGE_TEXT": "#5F5B53", "BADGE_BORDER": "#E0DDD6",
    "HL_BG": "#FFF3CD", "HL_TEXT": "#37352F",
    "PH_G1": "#EAE7DF", "PH_G2": "#D9D5CC", "PH_TEXT": "#9B9792", "PH_BORDER": "#C7C3BA",
    "BTN_BG": "#37352F", "BTN_TEXT": "#FFFFFF", "BTN_HOVER": "#5F5B53",
    "INPUT_BG": "#FFFFFF", "INPUT_BORDER": "#E0DDD6",
    "HR": "#E8E5DE",
    "SHADOW": "rgba(55,53,47,0.06)",
    "TABLE_HEAD_BG": "#F0EDE6", "TABLE_ALT": "#FAF9F6",
}
DARK = {
    "BG": "#191919", "TEXT": "#E6E6E3",
    "SIDEBAR_BG": "#202020", "SIDEBAR_BORDER": "#2F2F2F",
    "CARD_BG": "#242424", "CARD_BORDER": "#393939",
    "HERO_G1": "#2C2C2C", "HERO_G2": "#1E1E1E",
    "MUTED": "#959CA6",
    "SUB": "#9B9792",
    "TAG_BG": "#333333", "TAG_TEXT": "#C9C7C2",
    "BADGE_BG": "#2E2E2E", "BADGE_TEXT": "#C9C7C2", "BADGE_BORDER": "#3A3A3A",
    "HL_BG": "#4A4327", "HL_TEXT": "#FFE9A8",
    "PH_G1": "#2E2E2E", "PH_G2": "#242424", "PH_TEXT": "#8A8A86", "PH_BORDER": "#444444",
    "BTN_BG": "#E6E6E3", "BTN_TEXT": "#191919", "BTN_HOVER": "#C9C7C2",
    "INPUT_BG": "#2A2A2A", "INPUT_BORDER": "#3A3A3A",
    "HR": "#2F2F2F",
    "SHADOW": "rgba(0,0,0,0.45)",
    "TABLE_HEAD_BG": "#2E2E2E", "TABLE_ALT": "#1F1F1F",
}

# ── 커스텀 CSS 템플릿 (노션 스타일) ─────────────────────────────────────────
CSS_TEMPLATE = """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css');
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&family=Playfair+Display:wght@700&display=swap');

html, body, .stApp, [class*="css"] {
    font-family: 'Pretendard', 'Noto Sans KR', 'DM Sans', sans-serif;
    color: __TEXT__;
}
.stApp, [data-testid="stAppViewContainer"] { background-color: __BG__; }
[data-testid="stHeader"] { background: transparent; }
.main .block-container { padding-top: 2rem; padding-left: 3rem; padding-right: 3rem; max-width: 1100px; }

/* 사이드바 */
[data-testid="stSidebar"] {
    background-color: __SIDEBAR_BG__;
    border-right: 1px solid __SIDEBAR_BORDER__;
}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: __TEXT__ !important;
}

/* 히어로 카드 */
.hero-card {
    background: linear-gradient(135deg, __HERO_G1__ 0%, __HERO_G2__ 100%);
    border: 1px solid __CARD_BORDER__; border-radius: 16px;
    padding: 2rem 2.5rem 1.6rem; margin-bottom: 1.4rem;
    box-shadow: 0 2px 12px __SHADOW__;
}
.hero-title-wrap { display:flex; align-items: baseline; flex-wrap: wrap; gap: 2px; margin: 0 0 0.3rem; }
.hero-ko { font-family: 'Pretendard', sans-serif; font-weight: 700; font-size: 2.5rem; color: __TEXT__; line-height: 1.1; }
.hero-en { font-family: 'Degular', 'DM Sans', sans-serif; font-weight: 500; font-size: 2.26rem; color: __TEXT__; line-height: 1.1; }
.hero-subtitle { font-family: 'DM Sans', sans-serif; font-size: 1rem; color: __SUB__; margin: 0 0 0.2rem; }
.hero-date {
    display: inline-block; background: __BTN_BG__; color: __BTN_TEXT__;
    font-size: 0.82rem; font-weight: 500; border-radius: 20px;
    padding: 4px 14px; margin-top: 8px; margin-bottom: 6px; letter-spacing: 0.03em;
}
.hero-tag {
    display: inline-block; background: __TAG_BG__; color: __TAG_TEXT__;
    font-size: 0.78rem; font-weight: 500; border-radius: 20px;
    padding: 3px 12px; margin-right: 6px; margin-top: 6px;
}

/* 섹션 헤더 (요청 3: Pretendard / #959CA6 / 크게) */
.section-header {
    font-family: 'Pretendard', sans-serif; font-size: 1.32rem; font-weight: 600;
    letter-spacing: 0; text-transform: none; color: __MUTED__;
    margin: 2rem 0 0.9rem; border-bottom: 1px solid __CARD_BORDER__; padding-bottom: 0.55rem;
}

.city-badge {
    display: inline-block; background: __BADGE_BG__; color: __BADGE_TEXT__;
    font-size: 0.8rem; font-weight: 500; border-radius: 8px;
    padding: 4px 10px; margin: 3px 3px 3px 0; border: 1px solid __BADGE_BORDER__;
}
.desc-block {
    background: __CARD_BG__; border: 1px solid __CARD_BORDER__; border-radius: 12px;
    padding: 1.4rem 1.6rem; min-height: 240px;
    line-height: 1.85; font-size: 0.93rem; color: __TEXT__;
}
.desc-block p { margin: 0 0 0.6rem; }
.desc-block .highlight { display: inline-block; background: __HL_BG__; color: __HL_TEXT__; border-radius: 4px; padding: 1px 6px; font-weight: 500; }

/* 앨범 컨테이너 (사진 기능/경로 — 변경 없음) */
.album-wrap {
    background: __CARD_BG__; border: 1px solid __CARD_BORDER__; border-radius: 12px;
    overflow: hidden; min-height: 240px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.img-placeholder {
    background: linear-gradient(135deg, __PH_G1__ 0%, __PH_G2__ 100%);
    border-radius: 8px; height: 200px; width: 100%;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    color: __PH_TEXT__; font-size: 0.85rem; border: 1.5px dashed __PH_BORDER__; gap: 8px;
}
.img-placeholder .icon { font-size: 2.2rem; }
.album-counter { font-size: 0.78rem; color: __MUTED__; margin-top: 6px; }

/* 메트릭 카드 (요청 3: 라벨 Pretendard / #959CA6 / 크게) */
[data-testid="stMetric"] {
    background: __CARD_BG__; border: 1px solid __CARD_BORDER__; border-radius: 12px;
    padding: 1.1rem 1.4rem; box-shadow: 0 1px 4px __SHADOW__;
}
[data-testid="stMetricLabel"] {
    color: __MUTED__ !important; font-size: 1.22rem !important;
    font-family: 'Pretendard', sans-serif !important; font-weight: 600 !important;
}
[data-testid="stMetricLabel"] p { font-size: 1.22rem !important; color: __MUTED__ !important; font-weight: 600 !important; }
[data-testid="stMetricValue"] { color: __TEXT__ !important; font-size: 2rem !important; font-weight: 700 !important; }

/* 일정 / TOP5 HTML 테이블 */
.notion-table {
    width: 100%; border-collapse: collapse; background: __CARD_BG__;
    border: 1px solid __CARD_BORDER__; border-radius: 12px; overflow: hidden;
    font-family: 'Pretendard', sans-serif; margin-top: 0.2rem;
}
.notion-table th {
    background: __TABLE_HEAD_BG__; color: __MUTED__; font-size: 0.95rem; font-weight: 600;
    text-align: left; padding: 12px 16px; border-bottom: 1px solid __CARD_BORDER__;
}
.notion-table td {
    padding: 12px 16px; font-size: 0.94rem; color: __TEXT__;
    border-bottom: 1px solid __CARD_BORDER__; vertical-align: top; line-height: 1.55;
}
.notion-table tr:nth-child(even) td { background: __TABLE_ALT__; }
.notion-table tr:last-child td { border-bottom: none; }
.itin-date { font-weight: 600; white-space: nowrap; }
.itin-city {
    display: inline-block; background: __BADGE_BG__; color: __BADGE_TEXT__;
    border: 1px solid __BADGE_BORDER__; border-radius: 8px;
    padding: 2px 10px; font-size: 0.85rem; white-space: nowrap;
}

/* 입력 / 버튼 */
.stTextInput input {
    border: 1px solid __INPUT_BORDER__ !important; border-radius: 8px !important;
    background: __INPUT_BG__ !important; color: __TEXT__ !important;
    font-family: 'Pretendard', sans-serif; font-size: 0.9rem; padding: 0.5rem 0.8rem;
}
.stTextInput input:focus { border-color: __MUTED__ !important; box-shadow: none !important; }
.stButton > button {
    background: __BTN_BG__ !important; color: __BTN_TEXT__ !important;
    border: 1px solid __CARD_BORDER__ !important; border-radius: 8px !important;
    font-family: 'Pretendard', sans-serif; font-size: 0.86rem;
    font-weight: 500; padding: 0.45rem 1rem; transition: all 0.15s ease;
}
.stButton > button:hover { background: __BTN_HOVER__ !important; }
hr { border: none; border-top: 1px solid __HR__; margin: 1.5rem 0; }
.stSelectbox > div > div, .stRadio > div {
    border-radius: 8px !important; background: transparent !important;
}
.stSelectbox div[data-baseweb="select"] > div {
    border: 1px solid __INPUT_BORDER__ !important; background: __INPUT_BG__ !important;
}
.map-caption { color: __MUTED__; font-size: 0.9rem; font-weight: 600; margin: 0.2rem 0 0.6rem; font-family:'Pretendard',sans-serif; }
.overview-note { color: __MUTED__; font-size: 0.95rem; font-family:'Pretendard',sans-serif; }
</style>
"""


def build_css(palette: dict) -> str:
    css = CSS_TEMPLATE
    for key, val in palette.items():
        css = css.replace(f"__{key}__", val)
    return css


# ── 데이터 정의 ──────────────────────────────────────────────────────────────
COUNTRY_DATA = {

    # ──────────────────── 영국 ────────────────────
    "🇬🇧 영국": {
        "emoji": "🇬🇧", "name": "영국", "en_name": "United Kingdom",
        "city_display": "Oxford · Bath · London · Bournemouth · Winchester",
        "city_list": ["Oxford", "Bath", "London", "Bournemouth", "Winchester"],
        "travel_date": "2025.09.16 – 2025.12.24",
        "color": "#C41E3A",
        "visited_cities": 5,
        "fav_restaurants": 8,
        "total_spent": "₩3,450,000", "spent_krw": 3450000,
        "banner_emoji": "🏰",
        "tags": ["#런던", "#옥스퍼드", "#해리포터", "#피시앤칩스"],
        "description": [
            "🏙️ <span class='highlight'>런던</span>에서 시작된 교환학생 생활은 상상 그 이상이었다.",
            "☕ 코번트 가든의 카페에서 노트북 펼쳐두고 과제하던 오후들.",
            "🎭 크리스마스이브날 엄마와 함께 본 뮤지컬 <span class='highlight'>오페라의 유령</span>은 정말 환상적이었다.",
            "🥹 친구들이 해준 서프라이즈 페어웰 파티 때, 영국이 그리울 것 같아 펑펑 울었다.",
            "🌧️ 비가 자주 왔지만, 그게 또 런던의 감성이었다.",
        ],
        "image_list": [
            "images/uk1.jpg",
            "images/uk2.jpg",
            "images/uk3.jpg",
        ],
        "top_places": pd.DataFrame({
            "방문 날짜": ["2025.09.20", "2025.10.05", "2025.10.28", "2025.11.15", "2025.12.10"],
            "장소": ["🏰 Tower of London", "📚 Oxford Bodleian Library", "🌿 Bath Roman Baths", "🎭 West End – Phantom of the Opera", "🎡 Winter Wonderland, Hyde Park"],
            "좋았던 이유": ["천년 역사의 웅장함이 압도적이었다", "해리포터 촬영지! 책 냄새가 좋았다", "로마 시대 온천, 타임슬립한 기분", "엄마와 함께여서 더 특별한 공연이었다", "크리스마스 분위기가 절정이었다"],
        }),
        "restaurants": [
            {"name": "Dishoom", "lat": 51.5117, "lon": -0.1240, "city": "London"},
            {"name": "The Ledbury", "lat": 51.5137, "lon": -0.2049, "city": "London"},
            {"name": "Padella", "lat": 51.5050, "lon": -0.0898, "city": "London"},
            {"name": "St. John Restaurant", "lat": 51.5207, "lon": -0.1009, "city": "London"},
            {"name": "Bao Soho", "lat": 51.5133, "lon": -0.1318, "city": "London"},
            {"name": "The Walnut Tree", "lat": 51.7609, "lon": -3.0089, "city": "Oxford"},
            {"name": "Cherwell Boathouse", "lat": 51.7667, "lon": -1.2559, "city": "Oxford"},
            {"name": "The Pump Room", "lat": 51.3813, "lon": -2.3592, "city": "Bath"},
        ],
        "itinerary": [
            ("2025.09.16", "London", "🛬 히드로 공항 도착 · 기숙사 입소 · 동네 마트 첫 장보기"),
            ("2025.09.20", "London", "🏰 Tower of London 탐방 · 타워브리지 산책 · Dishoom 첫 저녁"),
            ("2025.10.05", "Oxford", "📚 Bodleian Library · 크라이스트처치 칼리지(해리포터 촬영지)"),
            ("2025.10.18", "Winchester", "⛪ Winchester Cathedral · 제인 오스틴 하우스 · 골목 카페"),
            ("2025.10.28", "Bath", "🌿 Roman Baths · Royal Crescent 산책 · The Pump Room 티타임"),
            ("2025.11.08", "Bournemouth", "🏖️ Bournemouth Beach 산책 · 부두 노을 감상"),
            ("2025.11.15", "London", "🎭 West End 'Phantom of the Opera' 관람 · 소호 야경"),
            ("2025.12.10", "London", "🎡 Hyde Park Winter Wonderland · 크리스마스 마켓 투어"),
            ("2025.12.24", "London", "🎄 코번트 가든 크리스마스이브 · 친구들과 페어웰 디너"),
        ],
    },

    # ──────────────────── 프랑스 ────────────────────
    "🇫🇷 프랑스": {
        "emoji": "🇫🇷", "name": "프랑스", "en_name": "France",
        "city_display": "Paris",
        "city_list": ["Paris"],
        "travel_date": "2025.12.25 – 2025.12.31",
        "color": "#003087",
        "visited_cities": 1,
        "fav_restaurants": 6,
        "total_spent": "₩2,120,000", "spent_krw": 2120000,
        "banner_emoji": "🗼",
        "tags": ["#에펠탑", "#루브르", "#크루아상", "#파리"],
        "description": [
            "🥐 아침마다 동네 <span class='highlight'>불랑제리</span>에서 사 먹던 크루아상의 맛.",
            "🎨 미술관에서 보던 작품들이 눈앞에 있으니 정말 신기했다.",
            "🌉 저녁에 본 에펠탑과 낮에 본 에펠탑 모두 아름다웠다.",
            "🍷 나폴레옹의 모자가 보관되어 있는 미슐랭 레스토랑 <span class='highlight'>Le Procope</span>에서 교환시절 사귄 영국인 친구를 만났다.",
            "🖼️ 퐁피두 현대 미술관에서 크리스마스날 본 전시는 정말 웅장했다.",
        ],
        "image_list": [
            "images/paris1.jpg",
            "images/paris2.jpg",
            "images/paris3.jpg",
        ],
        "top_places": pd.DataFrame({
            "방문 날짜": ["2025.12.25", "2025.12.26", "2025.12.27", "2025.12.28", "2025.12.30"],
            "장소": ["🖼️ Centre Pompidou", "🗼 Tour Eiffel", "🏛️ Musée du Louvre", "☕ Le Procope", "🌿 Jardin du Luxembourg"],
            "좋았던 이유": ["크리스마스날 현대미술 전시, 웅장했다", "낮과 밤 모두 아름다운 파리의 심볼", "명화들이 눈앞에 실재함에 감동받았다", "나폴레옹의 흔적이 있는 역사적인 레스토랑", "겨울 정원의 고요한 아름다움"],
        }),
        "image_list": [
            "images/paris1.jpg",
            "images/paris2.jpg",
            "images/paris3.jpg",
        ],
        "restaurants": [
            {"name": "Le Procope", "lat": 48.8528, "lon": 2.3397, "city": "Paris"},
            {"name": "L'Ambroisie", "lat": 48.8533, "lon": 2.3555, "city": "Paris"},
            {"name": "Septime", "lat": 48.8527, "lon": 2.3790, "city": "Paris"},
            {"name": "Du Pain et des Idées", "lat": 48.8706, "lon": 2.3614, "city": "Paris"},
            {"name": "Frenchie", "lat": 48.8638, "lon": 2.3469, "city": "Paris"},
            {"name": "Chez L'Ami Jean", "lat": 48.8607, "lon": 2.3059, "city": "Paris"},
        ],
        "itinerary": [
            ("2025.12.25", "Paris", "🖼️ Centre Pompidou 현대미술 전시 · 마레 지구 산책"),
            ("2025.12.26", "Paris", "🗼 Tour Eiffel 전망 · 트로카데로 야경"),
            ("2025.12.27", "Paris", "🏛️ Musée du Louvre 관람 · 튈르리 정원 산책"),
            ("2025.12.28", "Paris", "☕ Le Procope 점심 · 생제르맹 카페 투어"),
            ("2025.12.29", "Paris", "⛪ Notre-Dame · Sainte-Chapelle · 센강 유람선"),
            ("2025.12.30", "Paris", "🌿 Jardin du Luxembourg · 라탱 지구 골목"),
            ("2025.12.31", "Paris", "🥐 몽마르트 · 사크레쾨르 · 마지막 불랑제리 크루아상"),
        ],
    },

    # ──────────────────── 이탈리아 ────────────────────
    "🇮🇹 이탈리아": {
        "emoji": "🇮🇹", "name": "이탈리아", "en_name": "Italy",
        "city_display": "Salerno · Napoli · Positano · Capri",
        "city_list": ["Salerno", "Napoli", "Positano", "Capri"],
        "travel_date": "2025.09.06 – 2025.09.15",
        "color": "#009246",
        "visited_cities": 4,
        "fav_restaurants": 12,
        "total_spent": "₩2,450,000", "spent_krw": 2450000,
        "banner_emoji": "🍋",
        "tags": ["#살레르노", "#나폴리", "#포지타노", "#카프리"],
        "description": [
            "🌊 <span class='highlight'>포지타노</span>의 에메랄드빛 바다는 너무 아름다웠다.",
            "🍕 나폴리에서 먹은 진짜 피자 마르게리따 — 이탈리아 피자는 다르다.",
            "🍋 카프리 섬에서 마신 레몬 그라니따, 지금도 생각난다.",
            "⛵ 살레르노에서 포지타노로 가는 페리 위에서 본 아말피 해안은 절경이었다.",
            "🫙 골목 구석구석 레몬으로 만든 리몬첼로 가게가 가득했다.",
        ],
        "image_list": [
            "images/italy1.jpg",
            "images/italy2.jpg",
            "images/italy3.jpg",
        ],
        "top_places": pd.DataFrame({
            "방문 날짜": ["2025.09.07", "2025.09.08", "2025.09.09", "2025.09.11", "2025.09.13"],
            "장소": ["🏛️ Pompeii Ruins, Napoli", "🍕 Pizzeria Starita, Napoli", "🌊 Spiaggia Grande, Positano", "⛵ Capri Blue Grotto", "🌅 Amalfi Coast Ferry"],
            "좋았던 이유": ["화산재에 덮인 도시, 역사가 생생했다", "나폴리 현지인이 추천한 피자, 인생 최고", "에메랄드빛 바다에 수영, 천국이 여기", "동굴 속 파란 빛이 신비로웠다", "아말피 해안 전경, 말이 필요없었다"],
        }),
        "restaurants": [
            {"name": "Pizzeria Starita", "lat": 40.8597, "lon": 14.2468, "city": "Napoli"},
            {"name": "Da Michele", "lat": 40.8510, "lon": 14.2681, "city": "Napoli"},
            {"name": "Trattoria da Emilia", "lat": 40.6822, "lon": 14.8490, "city": "Positano"},
            {"name": "Lo Guarracino", "lat": 40.6271, "lon": 14.6025, "city": "Positano"},
            {"name": "Ristorante Aurora, Capri", "lat": 40.5501, "lon": 14.2438, "city": "Capri"},
            {"name": "La Fontelina, Capri", "lat": 40.5448, "lon": 14.2227, "city": "Capri"},
            {"name": "Pasticceria Pantaleone", "lat": 40.6504, "lon": 14.7735, "city": "Salerno"},
            {"name": "Il Vicolo, Salerno", "lat": 40.6810, "lon": 14.7581, "city": "Salerno"},
            {"name": "Osteria del Buongustaio", "lat": 40.8543, "lon": 14.2540, "city": "Napoli"},
            {"name": "Trattoria San Ferdinando", "lat": 40.8371, "lon": 14.2512, "city": "Napoli"},
            {"name": "Il Geranio, Capri", "lat": 40.5503, "lon": 14.2426, "city": "Capri"},
            {"name": "Chez Black, Positano", "lat": 40.6282, "lon": 14.4855, "city": "Positano"},
        ],
        "itinerary": [
            ("2025.09.06", "Napoli", "🛬 나폴리 도착 · 스파카나폴리 골목 탐방"),
            ("2025.09.07", "Napoli", "🏛️ Pompeii 유적지 데이트립 · 화산재 도시 투어"),
            ("2025.09.08", "Napoli", "🍕 Pizzeria Starita 마르게리따 · 나폴리 항구 노을"),
            ("2025.09.09", "Positano", "⛵ 살레르노→포지타노 페리 · Spiaggia Grande 해변"),
            ("2025.09.10", "Positano", "🌊 포지타노 절벽 마을 산책 · 리몬첼로 가게 투어"),
            ("2025.09.11", "Capri", "🚤 Blue Grotto 동굴 보트 투어 · 파란 빛 감상"),
            ("2025.09.12", "Capri", "🍋 Anacapri · 몬테 솔라로 리프트 · 레몬 그라니따"),
            ("2025.09.13", "Amalfi", "🌅 아말피 해안 페리 절경 투어"),
            ("2025.09.14", "Salerno", "🫙 살레르노 구시가지 · Pasticceria Pantaleone"),
            ("2025.09.15", "Salerno", "✈️ 영국행 출국 준비 · 마지막 에스프레소"),
        ],
    },

    # ──────────────────── 스페인 ────────────────────
    "🇪🇸 스페인": {
        "emoji": "🇪🇸", "name": "스페인", "en_name": "Spain",
        "city_display": "Barcelona · Madrid",
        "city_list": ["Barcelona", "Madrid"],
        "travel_date": "2025.12.31 – 2026.01.11",
        "color": "#AA151B",
        "visited_cities": 2,
        "fav_restaurants": 9,
        "total_spent": "₩2,110,000", "spent_krw": 2110000,
        "banner_emoji": "🏖️",
        "tags": ["#가우디", "#사그라다파밀리아", "#타파스", "#마드리드"],
        "description": [
            "⛪ <span class='highlight'>사그라다 파밀리아</span>는 사진으로는 절대 느낄 수 없는 압도감이 있다.",
            "🌅 바르셀로네타 해변에서 저녁 노을을 보며 상그리아 한 잔.",
            "🥘 마드리드 산 미겔 시장에서 먹은 하몬과 타파스 조합은 최고였다.",
            "🌀 구엘 공원에서 가우디의 상상력에 감탄하며 한 시간을 머물렀다.",
            "💃 플라멩코 공연 — 무용수의 눈빛이 아직도 잊히지 않는다.",
        ],
        "image_list": [
            "images/spain1.jpg",
            "images/spain2.jpg",
            "images/spain3.jpg",
        ],
        "top_places": pd.DataFrame({
            "방문 날짜": ["2025.12.31", "2026.01.02", "2026.01.04", "2026.01.07", "2026.01.09"],
            "장소": ["⛪ Sagrada Família", "🌀 Park Güell", "🎨 Museo del Prado, Madrid", "🥘 Mercado de San Miguel", "💃 Flamenco Show, Tablao"],
            "좋았던 이유": ["완공 전에 직접 본 가우디의 걸작", "모자이크 도마뱀과 도시 전망이 환상적", "벨라스케스·고야의 원작에 압도됐다", "마드리드 최고의 식재료 시장이었다", "정열적인 플라멩코, 평생 잊지 못할 공연"],
        }),
        "restaurants": [
            {"name": "Bar del Pla", "lat": 41.3844, "lon": 2.1761, "city": "Barcelona"},
            {"name": "Bodega Sepúlveda", "lat": 41.3804, "lon": 2.1622, "city": "Barcelona"},
            {"name": "La Cova Fumada", "lat": 41.3902, "lon": 2.1984, "city": "Barcelona"},
            {"name": "Cervecería Catalana", "lat": 41.3919, "lon": 2.1600, "city": "Barcelona"},
            {"name": "El Xampanyet", "lat": 41.3841, "lon": 2.1810, "city": "Barcelona"},
            {"name": "Sobrino de Botín", "lat": 40.4141, "lon": -3.7093, "city": "Madrid"},
            {"name": "Casa Dani", "lat": 40.4354, "lon": -3.6776, "city": "Madrid"},
            {"name": "Mercado de San Miguel", "lat": 40.4155, "lon": -3.7089, "city": "Madrid"},
            {"name": "DiverXO", "lat": 40.4597, "lon": -3.6906, "city": "Madrid"},
        ],
        "itinerary": [
            ("2025.12.31", "Barcelona", "🛬 바르셀로나 도착 · 고딕 지구 · 새해 카운트다운"),
            ("2026.01.01", "Barcelona", "🏖️ Barceloneta 해변 · 새해 첫 상그리아"),
            ("2026.01.02", "Barcelona", "🌀 Park Güell · 가우디 모자이크 · 도시 전망"),
            ("2026.01.03", "Barcelona", "⛪ Sagrada Família · 카사 바트요 · 람블라스 거리"),
            ("2026.01.04", "Madrid", "🚄 마드리드 이동 · Museo del Prado 명화 관람"),
            ("2026.01.05", "Madrid", "🥘 Mercado de San Miguel 타파스 · 솔 광장"),
            ("2026.01.06", "Madrid", "🏰 Palacio Real · 레티로 공원 산책"),
            ("2026.01.07", "Madrid", "🍖 Sobrino de Botín 점심 · 그란비아 쇼핑"),
            ("2026.01.09", "Madrid", "💃 Tablao 플라멩코 공연 · 마지막 밤"),
            ("2026.01.11", "Madrid", "✈️ 귀국 · 4개월의 유럽 여정 마무리"),
        ],
    },
}

# 전체 여정 순서 (날짜 기준)
JOURNEY_ORDER = ["🇮🇹 이탈리아", "🇬🇧 영국", "🇫🇷 프랑스", "🇪🇸 스페인"]


# ── 공통 렌더 함수 ───────────────────────────────────────────────────────────
def render_hero(data: dict):
    tags_html = "".join(f"<span class='hero-tag'>{t}</span>" for t in data["tags"])
    cities_html = "".join(f"<span class='city-badge'>📍 {c}</span>" for c in data["city_list"])
    st.markdown(f"""
    <div class='hero-card'>
        <div class='hero-title-wrap'>
            <span class='hero-ko'>{data['banner_emoji']} {data['name']}</span>
            <span class='hero-en'>-{data['en_name']}</span>
        </div>
        <div class='hero-subtitle'>교환학생 2025</div>
        <div><span class='hero-date'>🗓️ {data['travel_date']}</span></div>
        <div style='margin-top:8px;'>{cities_html}</div>
        <div style='margin-top:4px;'>{tags_html}</div>
    </div>
    """, unsafe_allow_html=True)


def render_places_table(df: pd.DataFrame):
    rows = ""
    for _, r in df.iterrows():
        rows += (
            f"<tr><td class='itin-date'>{r['방문 날짜']}</td>"
            f"<td>{r['장소']}</td><td>{r['좋았던 이유']}</td></tr>"
        )
    st.markdown(
        f"<table class='notion-table'><tr><th>📅 방문 날짜</th><th>📍 장소</th>"
        f"<th>💗 좋았던 이유</th></tr>{rows}</table>",
        unsafe_allow_html=True,
    )


def render_itinerary_table(itinerary: list):
    rows = ""
    for i, (date, city, plan) in enumerate(itinerary, start=1):
        rows += (
            f"<tr><td class='itin-date'>Day {i}<br>{date}</td>"
            f"<td><span class='itin-city'>{city}</span></td><td>{plan}</td></tr>"
        )
    st.markdown(
        f"<table class='notion-table'><tr><th>📆 일자</th><th>📍 도시</th>"
        f"<th>🧭 세부 일정</th></tr>{rows}</table>",
        unsafe_allow_html=True,
    )


def render_spend_chart(dark: bool):
    chart_df = pd.DataFrame({
        "국가": [v["name"] for v in COUNTRY_DATA.values()],
        "총 지출(만원)": [v["spent_krw"] // 10000 for v in COUNTRY_DATA.values()],
        "총 지출": [v["spent_krw"] for v in COUNTRY_DATA.values()],
    })
    # 같은 톤 안에서: 지출 낮음 → 흐리게, 지출 높음 → 진하게
    bar_range = ["#5A5751", "#E6E6E3"] if dark else ["#CFCAC0", "#37352F"]
    axis_color = "#C9C7C2" if dark else "#5F5B53"

    chart = (
        alt.Chart(chart_df)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=46)
        .encode(
            x=alt.X("국가:N", sort="-y", title=None,
                    axis=alt.Axis(labelColor=axis_color, labelFontSize=13,
                                  labelFont="Pretendard", labelAngle=0,
                                  domainColor=axis_color, ticks=False)),
            y=alt.Y("총 지출:Q", title=None,
                    axis=alt.Axis(labelColor=axis_color, labelFontSize=11,
                                  format="~s", grid=False, domain=False, ticks=False)),
            color=alt.Color("총 지출:Q", scale=alt.Scale(range=bar_range), legend=None),
            tooltip=[alt.Tooltip("국가:N", title="국가"),
                     alt.Tooltip("총 지출:Q", title="총 지출(₩)", format=",")],
        )
        .properties(height=300)
        .configure_view(strokeWidth=0)
        .configure(background="transparent")
    )
    st.altair_chart(chart, use_container_width=True)


def render_restaurant_map(selected_key: str, data: dict, dark: bool):
    rests = data["restaurants"]
    sel_key = f"sel_rest_{selected_key}"
    if sel_key not in st.session_state or st.session_state[sel_key] >= len(rests):
        st.session_state[sel_key] = 0
    sel = st.session_state[sel_key]
    chosen = rests[sel]

    st.markdown(
        f"<p class='map-caption'>📍 현재 지도 위치 : <b>{chosen['name']}</b> · {chosen['city']}</p>",
        unsafe_allow_html=True,
    )

    # 정확한 위치(위도/경도)로 구글맵 임베드 — 딱 그 장소에 핀 표시
    q = urllib.parse.quote(f"{chosen['name']}, {chosen['city']}")
    embed = (
        f"https://maps.google.com/maps?q={q}"
        f"&ll={chosen['lat']},{chosen['lon']}&z=16&hl=ko&output=embed"
    )
    components.html(
        f'<iframe width="100%" height="430" frameborder="0" '
        f'style="border:0;border-radius:12px;" loading="lazy" '
        f'src="{embed}" allowfullscreen></iframe>',
        height=445,
    )

    st.markdown(
        f"<p class='overview-note'>👇 아래 맛집을 클릭하면 지도가 그 위치로 이동해요 "
        f"({len(rests)}곳)</p>",
        unsafe_allow_html=True,
    )
    cols = st.columns(3)
    for i, r in enumerate(rests):
        label = ("✅ " if i == sel else "🍽️ ") + r["name"]
        with cols[i % 3]:
            if st.button(label, key=f"rbtn_{selected_key}_{i}", use_container_width=True,
                         help=f"{r['name']} · {r['city']}"):
                st.session_state[sel_key] = i
                st.rerun()


# ── 사이드바 ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✈️ 나의 유럽여행 기록")
    st.markdown("<p style='font-size:0.82rem;color:#9B9792;margin-top:-10px;'>교환학생 2025.09~2026.01</p>", unsafe_allow_html=True)

    # 요청 2: 다크모드 토글
    dark_mode = st.toggle("🌙 다크 모드", value=False, key="dark_mode")
    st.markdown("---")

    # 요청 7: 페이지(보기) 선택 — 여행 기록 / 여행 일정 / 전체 요약
    view = st.radio(
        "📂 보기 선택",
        ["📖 여행 기록", "🗓️ 여행 일정 확인하기", "🌍 전체 여정 요약"],
        index=0,
    )

    st.markdown("---")
    # 요청 6: '국가 선택' → '기억저장소'
    selected = st.selectbox("🗂️ 기억저장소", list(COUNTRY_DATA.keys()), index=0)

    st.markdown("---")
    total_all = sum(v["spent_krw"] for v in COUNTRY_DATA.values())
    st.markdown("**📊 전체 여행 통계**")
    st.markdown("- 🗺️ 방문 국가: **4개국**")
    st.markdown(f"- 🏙️ 총 방문 도시: **{sum(v['visited_cities'] for v in COUNTRY_DATA.values())}개**")
    st.markdown(f"- 💸 총 지출: **₩{total_all:,}**")
    # 요청 1: 'made with 💛 by 교환학생 나' 문구 삭제 (제거됨)

# ── CSS 주입 (다크모드 반영) ────────────────────────────────────────────────
palette = DARK if dark_mode else LIGHT
st.markdown(build_css(palette), unsafe_allow_html=True)

data = COUNTRY_DATA[selected]


# ════════════════════════════════════════════════════════════════════════════
# 페이지 1 : 여행 기록
# ════════════════════════════════════════════════════════════════════════════
if view == "📖 여행 기록":
    render_hero(data)

    # ─── 섹션 1: 핵심 통계 ──────────────────────────────────────────────
    st.markdown("<div class='section-header'>📌 핵심 기록</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏙️ 방문 도시 수", f"{data['visited_cities']}개")
    with col2:
        st.metric("🍽️ 최애 맛집 수", f"{data['fav_restaurants']}곳")
    with col3:
        st.metric("💸 총 지출", data["total_spent"])

    # ─── 섹션 2: 사진 앨범 & 설명 (사진 기능/경로 — 변경 없음) ───────────
    st.markdown("<div class='section-header'>📸 현장 기록</div>", unsafe_allow_html=True)
    col_img, col_desc = st.columns([1, 1.2], gap="medium")

    with col_img:
        imgs = data["image_list"]
        key_idx = f"album_idx_{selected}"
        if key_idx not in st.session_state:
            st.session_state[key_idx] = 0
        idx = st.session_state[key_idx]

        img_path = imgs[idx]
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.markdown(f"""
            <div class='img-placeholder'>
                <div class='icon'>{data['banner_emoji']}</div>
                <div>📷 {img_path}</div>
                <div style='font-size:0.75rem;color:#B5B2AB'>이 경로에 사진을 넣어주세요</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"<p class='album-counter' style='text-align:center;'>📷 {idx+1} / {len(imgs)}</p>", unsafe_allow_html=True)

        btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
        with btn_col1:
            if st.button("◀", key=f"prev_{selected}", help="이전 사진"):
                st.session_state[key_idx] = (idx - 1) % len(imgs)
                st.rerun()
        with btn_col3:
            if st.button("▶", key=f"next_{selected}", help="다음 사진"):
                st.session_state[key_idx] = (idx + 1) % len(imgs)
                st.rerun()

    with col_desc:
        desc_items = "".join(f"<p>{item}</p>" for item in data["description"])
        st.markdown(f"<div class='desc-block'>{desc_items}</div>", unsafe_allow_html=True)

    # ─── 섹션 3: 지출 비교 차트 (요청 5: 톤 그라데이션) ────────────────
    st.markdown("<div class='section-header'>💰 4개국 지출 비교</div>", unsafe_allow_html=True)
    render_spend_chart(dark_mode)
    st.caption("💡 영국에서 가장 여행을 많이 다녀서 가장 지출이 컸다.")

    # ─── 섹션 4: TOP 5 장소 ────────────────────────────────────────────
    st.markdown("<div class='section-header'>🏆 가장 마음에 들었던 장소 TOP 5</div>", unsafe_allow_html=True)
    render_places_table(data["top_places"])

    # ─── 섹션 5: 맛집 지도 (요청 4: 구글맵 정확 위치 + 클릭 이동) ───────
    st.markdown("<div class='section-header'>🗺️ 최애 맛집 지도</div>", unsafe_allow_html=True)
    render_restaurant_map(selected, data, dark_mode)

    # ─── 섹션 6: 나의 기록 남기기 ───────────────────────────────────────
    st.markdown("<div class='section-header'>💬 나의 기록 남기기</div>", unsafe_allow_html=True)
    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.markdown(f"**⭐ {data['name']}에 대한 만족도**")
        satisfaction = st.slider(
            "만족도", min_value=1, max_value=10, value=8,
            key=f"slider_{selected}", label_visibility="collapsed",
        )
        emoji_map = {
            (1, 3): ("😞", "다음엔 더 잘 될 거야..."),
            (4, 5): ("😐", "나쁘진 않았어!"),
            (6, 7): ("😊", "꽤 좋았어!"),
            (8, 9): ("😄", "정말 좋았다!"),
            (10, 10): ("🤩", "인생 여행지야!!"),
        }
        for (low, high), (em, msg) in emoji_map.items():
            if low <= satisfaction <= high:
                st.markdown(f"### {em}")
                st.markdown(f"**{satisfaction}/10점** — {msg}")
                break

    with col_right:
        st.markdown("**📝 다시 간다면 꼭 하고 싶은 것**")
        wish = st.text_input(
            "입력", placeholder=f"{data['name']}에서 꼭 하고 싶은 것을 적어보세요 ✍️",
            key=f"wish_{selected}", label_visibility="collapsed",
        )
        if st.button("💾 저장하기", key=f"save_{selected}"):
            if wish.strip():
                st.success(f"✅ 저장 완료! 🗺️ **'{data['name']}'에서 꼭 할 것:** {wish.strip()}")
                st.balloons()
            else:
                st.warning("✏️ 내용을 먼저 입력해 주세요!")

    st.markdown("<br><br>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# 페이지 2 : 여행 일정 확인하기 (요청 7)
# ════════════════════════════════════════════════════════════════════════════
elif view == "🗓️ 여행 일정 확인하기":
    render_hero(data)

    st.markdown("<div class='section-header'>🗓️ 일자별 여행 일정</div>", unsafe_allow_html=True)

    n_days = len(data["itinerary"])
    n_cities = len(data["city_list"])
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("📆 총 일정", f"{n_days}일")
    with c2:
        st.metric("🏙️ 방문 도시", f"{n_cities}곳")
    with c3:
        st.metric("🗓️ 여행 기간", data["travel_date"].split("–")[0].strip())

    st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)
    render_itinerary_table(data["itinerary"])
    st.caption("💡 표는 대표 일정 기준으로 정리했어요. 날짜·동선은 자유롭게 수정해서 쓰세요.")
    st.markdown("<br><br>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# 페이지 3 : 전체 여정 요약 (요청 9 — 추가 기능)
# ════════════════════════════════════════════════════════════════════════════
elif view == "🌍 전체 여정 요약":
    st.markdown(f"""
    <div class='hero-card'>
        <div class='hero-title-wrap'>
            <span class='hero-ko'>🌍 전체 여정</span>
            <span class='hero-en'>-Grand Tour 2025–26</span>
        </div>
        <div class='hero-subtitle'>이탈리아 → 영국 → 프랑스 → 스페인</div>
        <div><span class='hero-date'>🗓️ 2025.09.06 – 2026.01.11</span></div>
    </div>
    """, unsafe_allow_html=True)

    # 종합 통계
    st.markdown("<div class='section-header'>📊 한눈에 보는 여정</div>", unsafe_allow_html=True)
    total_cities = sum(v["visited_cities"] for v in COUNTRY_DATA.values())
    total_rest = sum(v["fav_restaurants"] for v in COUNTRY_DATA.values())
    total_spent = sum(v["spent_krw"] for v in COUNTRY_DATA.values())

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("🗺️ 방문 국가", "4개국")
    with m2:
        st.metric("🏙️ 방문 도시", f"{total_cities}곳")
    with m3:
        st.metric("🍽️ 최애 맛집", f"{total_rest}곳")
    with m4:
        st.metric("💸 총 지출", f"₩{total_spent:,}")

    # 여정 타임라인 (날짜순)
    st.markdown("<div class='section-header'>🧭 나라별 여정 타임라인</div>", unsafe_allow_html=True)
    timeline_rows = ""
    for k in JOURNEY_ORDER:
        v = COUNTRY_DATA[k]
        timeline_rows += (
            f"<tr><td class='itin-date'>{v['travel_date']}</td>"
            f"<td>{v['banner_emoji']} <b>{v['name']}</b> · {v['en_name']}</td>"
            f"<td>{v['city_display']}</td>"
            f"<td>{v['total_spent']}</td></tr>"
        )
    st.markdown(
        f"<table class='notion-table'><tr><th>🗓️ 기간</th><th>🏳️ 국가</th>"
        f"<th>📍 도시</th><th>💸 지출</th></tr>{timeline_rows}</table>",
        unsafe_allow_html=True,
    )

    # 지출 비교
    st.markdown("<div class='section-header'>💰 4개국 지출 비교</div>", unsafe_allow_html=True)
    render_spend_chart(dark_mode)
    st.caption("💡 같은 색 톤 안에서, 지출이 클수록 진하게 표시돼요.")

    # 전체 맛집 지도 (모든 핀 표시)
    st.markdown("<div class='section-header'>🗺️ 전체 맛집 지도</div>", unsafe_allow_html=True)
    all_rest = []
    for v in COUNTRY_DATA.values():
        for r in v["restaurants"]:
            all_rest.append({"latitude": r["lat"], "longitude": r["lon"]})
    st.map(pd.DataFrame(all_rest), zoom=3, use_container_width=True)
    st.caption("💡 유럽 곳곳에 흩어진 나의 최애 맛집들 (정확한 핀은 '여행 기록' 페이지 지도에서 확인하세요)")

    st.markdown("<br><br>", unsafe_allow_html=True)