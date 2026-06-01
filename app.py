import streamlit as st
import pandas as pd

# ── 페이지 설정 ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="나의 유럽 교환학생 기록기",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 커스텀 CSS (노션 스타일) ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', 'DM Sans', sans-serif;
    background-color: #F7F6F3;
    color: #37352F;
}
[data-testid="stSidebar"] {
    background-color: #FBFAF8;
    border-right: 1px solid #E8E5DE;
}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span { color: #37352F !important; font-size: 0.92rem; }
.main .block-container { padding-top: 2rem; padding-left: 3rem; padding-right: 3rem; max-width: 1100px; }

.hero-card {
    background: linear-gradient(135deg, #ffffff 0%, #f0ede6 100%);
    border: 1px solid #E8E5DE; border-radius: 16px;
    padding: 2rem 2.5rem 1.6rem; margin-bottom: 1.4rem;
    box-shadow: 0 2px 12px rgba(55,53,47,0.06);
}
.hero-title { font-family: 'Playfair Display', serif; font-size: 2.4rem; font-weight: 700; color: #37352F; margin: 0 0 0.3rem; }
.hero-subtitle { font-family: 'DM Sans', sans-serif; font-size: 1rem; color: #787672; margin: 0 0 0.2rem; }
.hero-date {
    display: inline-block;
    background: #37352F; color: #fff;
    font-size: 0.82rem; font-weight: 500;
    border-radius: 20px; padding: 4px 14px; margin-top: 8px; margin-bottom: 6px;
    letter-spacing: 0.03em;
}
.hero-tag {
    display: inline-block; background: #EAE7DF; color: #5F5B53;
    font-size: 0.78rem; font-weight: 500; border-radius: 20px;
    padding: 3px 12px; margin-right: 6px; margin-top: 6px;
}
.section-header {
    font-family: 'DM Sans', sans-serif; font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.12em; text-transform: uppercase; color: #9B9792;
    margin: 2rem 0 0.8rem; border-bottom: 1px solid #E8E5DE; padding-bottom: 0.5rem;
}
.city-badge {
    display: inline-block; background: #F0EDE6; color: #5F5B53;
    font-size: 0.8rem; font-weight: 500; border-radius: 8px;
    padding: 4px 10px; margin: 3px 3px 3px 0; border: 1px solid #E0DDD6;
}
.desc-block {
    background: #FFFFFF; border: 1px solid #E8E5DE; border-radius: 12px;
    padding: 1.4rem 1.6rem; min-height: 240px;
    line-height: 1.85; font-size: 0.93rem; color: #37352F;
}
.desc-block p { margin: 0 0 0.6rem; }
.desc-block .highlight { display: inline-block; background: #FFF3CD; border-radius: 4px; padding: 1px 6px; font-weight: 500; }

/* 앨범 컨테이너 */
.album-wrap {
    background: #FFFFFF; border: 1px solid #E8E5DE; border-radius: 12px;
    overflow: hidden; min-height: 240px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.img-placeholder {
    background: linear-gradient(135deg, #EAE7DF 0%, #D9D5CC 100%);
    border-radius: 8px; height: 200px; width: 100%;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    color: #9B9792; font-size: 0.85rem; border: 1.5px dashed #C7C3BA; gap: 8px;
}
.img-placeholder .icon { font-size: 2.2rem; }
.album-counter { font-size: 0.78rem; color: #9B9792; margin-top: 6px; }

[data-testid="stMetric"] {
    background: #FFFFFF; border: 1px solid #E8E5DE; border-radius: 12px;
    padding: 1.1rem 1.4rem; box-shadow: 0 1px 4px rgba(55,53,47,0.04);
}
[data-testid="stMetricLabel"] { color: #9B9792 !important; font-size: 0.8rem !important; }
[data-testid="stMetricValue"] { color: #37352F !important; font-size: 1.9rem !important; font-weight: 700 !important; }

[data-testid="stBarChartContainer"], .stBarChart {
    background: #FFFFFF; border: 1px solid #E8E5DE; border-radius: 12px; padding: 0.5rem;
}
[data-testid="stDataFrameContainer"] {
    background: #FFFFFF; border: 1px solid #E8E5DE; border-radius: 12px; overflow: hidden;
}
.stSlider > div > div { color: #37352F; }
.stTextInput input {
    border: 1px solid #E0DDD6 !important; border-radius: 8px !important;
    background: #FFFFFF !important; font-family: 'Noto Sans KR', sans-serif;
    font-size: 0.9rem; padding: 0.5rem 0.8rem;
}
.stTextInput input:focus { border-color: #B5B2AB !important; box-shadow: none !important; }
.stButton > button {
    background: #37352F !important; color: #FFFFFF !important;
    border: none !important; border-radius: 8px !important;
    font-family: 'Noto Sans KR', sans-serif; font-size: 0.88rem;
    font-weight: 500; padding: 0.5rem 1.4rem; transition: background 0.15s ease;
}
.stButton > button:hover { background: #5F5B53 !important; }
hr { border: none; border-top: 1px solid #E8E5DE; margin: 1.5rem 0; }
.stSuccess { border-radius: 10px !important; border-left: 4px solid #4A9B6F !important; background: #F0FAF4 !important; }
.stSelectbox > div > div { border-radius: 8px !important; border: 1px solid #E0DDD6 !important; background: #FFFFFF !important; }
</style>
""", unsafe_allow_html=True)

# ── 데이터 정의 ──────────────────────────────────────────────────────────────
COUNTRY_DATA = {

    # ──────────────────── 영국 ────────────────────
    "🇬🇧 영국": {
        "emoji": "🇬🇧", "name": "영국",
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
    },

    # ──────────────────── 프랑스 ────────────────────
    "🇫🇷 프랑스": {
        "emoji": "🇫🇷", "name": "프랑스",
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
        "restaurants": [
            {"name": "Le Procope", "lat": 48.8528, "lon": 2.3397, "city": "Paris"},
            {"name": "L'Ambroisie", "lat": 48.8533, "lon": 2.3555, "city": "Paris"},
            {"name": "Septime", "lat": 48.8527, "lon": 2.3790, "city": "Paris"},
            {"name": "Du Pain et des Idées", "lat": 48.8706, "lon": 2.3614, "city": "Paris"},
            {"name": "Frenchie", "lat": 48.8638, "lon": 2.3469, "city": "Paris"},
            {"name": "Chez L'Ami Jean", "lat": 48.8607, "lon": 2.3059, "city": "Paris"},
        ],
    },

    # ──────────────────── 이탈리아 ────────────────────
    "🇮🇹 이탈리아": {
        "emoji": "🇮🇹", "name": "이탈리아",
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
    },

    # ──────────────────── 스페인 ────────────────────
    "🇪🇸 스페인": {
        "emoji": "🇪🇸", "name": "스페인",
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
            "images/barcelona1.jpg",
            "images/barcelona2.jpg",
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
    },
}

# ── 사이드바 ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✈️ 나의 유럽여행 기록")
    st.markdown("<p style='font-size:0.82rem;color:#9B9792;margin-top:-10px;'>교환학생 2025.09~2026.01</p>", unsafe_allow_html=True)
    st.markdown("---")

    selected = st.selectbox("🌍 국가 선택", list(COUNTRY_DATA.keys()), index=0)

    st.markdown("---")
    total_all = sum(v["spent_krw"] for v in COUNTRY_DATA.values())
    st.markdown("**📊 전체 여행 통계**")
    st.markdown(f"- 🗺️ 방문 국가: **4개국**")
    st.markdown(f"- 🏙️ 총 방문 도시: **{sum(v['visited_cities'] for v in COUNTRY_DATA.values())}개**")
    st.markdown(f"- 💸 총 지출: **₩{total_all:,}**")
    st.markdown("---")
    st.markdown("<p style='font-size:0.78rem;color:#B5B2AB;text-align:center;'>made with 💛 by 교환학생 나</p>", unsafe_allow_html=True)

# ── 메인 화면 ────────────────────────────────────────────────────────────────
data = COUNTRY_DATA[selected]

# ─── 히어로 카드 ──────────────────────────────────────────────────────────
tags_html = "".join(f"<span class='hero-tag'>{t}</span>" for t in data["tags"])
cities_html = "".join(f"<span class='city-badge'>📍 {c}</span>" for c in data["city_list"])

st.markdown(f"""
<div class='hero-card'>
    <div class='hero-title'>{data['banner_emoji']} {data['name']} 여행기</div>
    <div class='hero-subtitle'>교환학생 2025</div>
    <div><span class='hero-date'>🗓️ {data['travel_date']}</span></div>
    <div style='margin-top:8px;'>{cities_html}</div>
    <div style='margin-top:4px;'>{tags_html}</div>
</div>
""", unsafe_allow_html=True)

# ─── 섹션 1: 핵심 통계 ──────────────────────────────────────────────────
st.markdown("<div class='section-header'>📌 핵심 기록</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🏙️ 방문 도시 수", f"{data['visited_cities']}개")
with col2:
    st.metric("🍽️ 최애 맛집 수", f"{data['fav_restaurants']}곳")
with col3:
    st.metric("💸 총 지출", data["total_spent"])

# ─── 섹션 2: 사진 앨범 & 설명 ──────────────────────────────────────────
st.markdown("<div class='section-header'>📸 현장 기록</div>", unsafe_allow_html=True)

col_img, col_desc = st.columns([1, 1.2], gap="medium")

with col_img:
    imgs = data["image_list"]
    key_idx = f"album_idx_{selected}"
    if key_idx not in st.session_state:
        st.session_state[key_idx] = 0

    idx = st.session_state[key_idx]

    import os
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

# ─── 섹션 3: 지출 비교 차트 ────────────────────────────────────────────
st.markdown("<div class='section-header'>💰 4개국 지출 비교</div>", unsafe_allow_html=True)

chart_df = pd.DataFrame({
    "국가": [v["name"] for v in COUNTRY_DATA.values()],
    "총 지출 (₩)": [v["spent_krw"] for v in COUNTRY_DATA.values()],
}).set_index("국가")

st.bar_chart(chart_df, height=260, use_container_width=True, color="#37352F")
st.caption("💡 영국에서 가장 여행을 많이 다녀서 가장 지출이 컸다.")

# ─── 섹션 4: TOP 5 장소 ────────────────────────────────────────────────
st.markdown("<div class='section-header'>🏆 가장 마음에 들었던 장소 TOP 5</div>", unsafe_allow_html=True)
st.dataframe(data["top_places"], use_container_width=True, hide_index=True)

# ─── 섹션 5: 맛집 지도 ─────────────────────────────────────────────────
st.markdown("<div class='section-header'>🗺️ 최애 맛집 지도</div>", unsafe_allow_html=True)

map_df = pd.DataFrame(data["restaurants"])
map_df = map_df.rename(columns={"lat": "latitude", "lon": "longitude"})

st.map(map_df, zoom=10, use_container_width=True)

with st.expander(f"📋 맛집 목록 보기 ({data['fav_restaurants']}곳)"):
    for r in data["restaurants"]:
        st.markdown(f"- 🍽️ **{r['name']}** — {r['city']}")

# ─── 섹션 6: 나의 기록 남기기 ───────────────────────────────────────────
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