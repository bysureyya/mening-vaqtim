import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta

# --- GOOGLE TASDIQLASH KODI (BUNGA TEGMANA) ---
st.markdown(
    """
    <head>
        <meta name="google-site-verification" content="pnj9SApkdw_6joK0E3N4YJkIYrRSyVaYfE1esk1zI7U" />
    </head>
    """, 
    unsafe_allow_html=True
)

# --- SAHIFA SOZLAMALARI ---
st.set_page_config(page_title="Muvaffaqiyat Markazi 2026", layout="wide")

# Dizayn: Yashil Fokus uslubi
st.markdown("""
    <style>
    .main { background-color: #f8faf8; }
    .day-card {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        border-top: 8px solid #4a7c44;
        box-shadow: 0 6px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        min-height: 250px;
    }
    .day-title { color: #2d4f2a; font-weight: bold; text-align: center; font-size: 18px; }
    .date-sub { text-align: center; color: #777; font-size: 12px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 1000 TA IQTIBOSLAR ---
iqtiboslar = [
    "Muvaffaqiyat — bu har kuni takrorlanadigan kichik odatlar yig'indisidir.",
    "Ilhom faqat mehnat jarayonida tug'iladi.",
    "Intizom — bu xohish va natija orasidagi ko'prikdir.",
    "Bugungi harakatingiz ertangi natijangiz poydevoridir.",
    "Vaqtingizni boshqara olmasangiz, hayotingizni ham boshqara olmaysiz.",
    "Eng qiyin qadam — bu boshlash qadami.",
    "To'xtab qolmasangiz, qanchalik sekin borayotganingiz muhim emas.",
    "O'z ustingizda ishlash — bu eng foydali investitsiyadir.",
    "Kichik g'alabalarni bayram qiling, ular katta muvaffaqiyatga yetaklaydi.",
    "Sizning eng katta dushmaningiz — bu kechiktirish odatidir."
] * 100 # Bazani 1000 taga yetkazish uchun

# --- SESSION STATE (Ma'lumotlarni saqlash) ---
if 'hafta_indeksi' not in st.session_state:
    st.session_state.hafta_indeksi = 0  # 0 - joriy hafta, -1 oldingi, 1 keyingi

if 'barcha_vazifalar' not in st.session_state:
    st.session_state.barcha_vazifalar = {} # {hafta_id: {kun: [vazifalar]}}

# Joriy haftani aniqlash
h_id = st.session_state.hafta_indeksi
if h_id not in st.session_state.barcha_vazifalar:
    st.session_state.barcha_vazifalar[h_id] = {kun: [] for kun in ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]}

# --- VAQTNI HISOBLASH ---
bugun = datetime.now()
dushanba = bugun - timedelta(days=bugun.weekday()) + timedelta(weeks=h_id)
sanalar = [(dushanba + timedelta(days=i)).strftime("%d.%m") for i in range(7)]
hafta_kunlari = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]

# --- CHAP MENYU (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Boshqaruv")
    
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ Oldingi", use_container_width=True):
            st.session_state.hafta_indeksi -= 1
            st.rerun()
    with col_nav2:
        if st.button("Keyingi ➡️", use_container_width=True):
            st.session_state.hafta_indeksi += 1
            st.rerun()
            
    if st.button("🏠 Bugungi haftaga qaytish", use_container_width=True):
        st.session_state.hafta_indeksi = 0
        st.rerun()

    st.divider()
    st.info(f"Hozirgi ko'rinish: **{h_id if h_id != 0 else 'Joriy'} hafta**")
    if st.button("🗑️ Ushbu haftani tozalash", type="secondary"):
        st.session_state.barcha_vazifalar[h_id] = {kun: [] for kun in hafta_kunlari}
        st.rerun()

# --- IQTIBOS TANLASH ---
random.seed(h_id) # Har bir hafta uchun unikal iqtibos chiqishi uchun
tanlangan_iqtibos = random.choice(iqtiboslar)

# --- ASOSIY PANEL ---
st.title("🍏 Muvaffaqiyat Markazi")

c1, c2, c3 = st.columns([1.2, 2, 1])

with c1:
    st.markdown(f"""
        <div style="background:white; padding:25px; border-radius:15px; border-left: 8px solid #4a7c44; min-height:220px;">
            <h4 style="color:#4a7c44; margin-top:0;">Hafta iqtibosi:</h4>
            <p style="font-size:16px; font-style:italic; color:#444;">"{tanlangan_iqtibos}"</p>
            <hr>
            <p style="font-size:14px;"><b>Hafta:</b> {sanalar[0]} - {sanalar[-1]}</p>
        </div>
    """, unsafe_allow_html=True)

with c2:
    # Haftalik natijalar grafigi
    vazifalar = st.session_state.barcha_vazifalar[h_id]
    stats = [sum(1 for v in vazifalar[k] if v['done']) for k in hafta_kunlari]
    fig_bar = go.Figure(data=[go.Bar(x=hafta_kunlari, y=stats, marker_color='#6ba264')])
    fig_bar.update_layout(title="Bajarilgan vazifalar", height=230, margin=dict(t=40, b=0, l=0, r=0))
    st.plotly_chart(fig_bar, use_container_width=True, key=f"bar_{h_id}") # Unikal KEY

with c3:
    # Umumiy Progress
    total = sum(len(v) for v in vazifalar.values())
    done = sum(sum(1 for t in v if t['done']) for v in vazifalar.values())
    pct = int((done / total * 100)) if total > 0 else 0
    
    fig_pie = go.Figure(go.Pie(hole=.7, values=[pct, 100-pct], marker=dict(colors=['#4a7c44', '#f0f0f0']), showlegend=False))
    fig_pie.add_annotation(text=f"{pct}%", font_size=35, showarrow=False, font_color="#4a7c44")
    fig_pie.update_layout(height=230, margin=dict(t=30, b=0, l=0, r=0), title="Haftalik Progress")
    st.plotly_chart(fig_pie, use_container_width=True, key=f"pie_{h_id}") # Unikal KEY

# --- KUNLIK REJALAR ---
st.divider()
card_cols = st.columns(7)

for i, kun in enumerate(hafta_kunlari):
    with card_cols[i]:
        st.markdown(f'<div class="day-card"><div class="day-title">{kun}</div><div class="date-sub">{sanalar[i]}</div>', unsafe_allow_html=True)
        
        k_tasks = vazifalar[kun]
        k_done = sum(1 for v in k_tasks if v['done'])
        k_pct = int((k_done / len(k_tasks) * 100)) if len(k_tasks) > 0 else 0
        
        # Kunlik doira
        fig_k = go.Figure(go.Pie(hole=.75, values=[k_pct, 100-k_pct], marker=dict(colors=['#4a7c44', '#f0f0f0']), showlegend=False))
        fig_k.add_annotation(text=f"{k_pct}%", font_size=16, showarrow=False)
        fig_k.update_layout(height=120, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_k, use_container_width=True, key=f"day_{h_id}_{kun}")

        # Vazifalar ro'yxati
        for t_idx, task in enumerate(k_tasks):
            t_col1, t_col2 = st.columns([4, 1])
            with t_col1:
                st.markdown(f'<span style="font-size:12px;">{task["name"]}</span>', unsafe_allow_html=True)
            with t_col2:
                task['done'] = st.checkbox("", value=task['done'], key=f"ch_{h_id}_{kun}_{t_idx}")
        
        # Qo'shish
        with st.expander("+"):
            n_t = st.text_input("Nomi:", key=f"in_{h_id}_{kun}")
            if st.button("Qo'shish", key=f"btn_{h_id}_{kun}"):
                if n_t:
                    st.session_state.barcha_vazifalar[h_id][kun].append({"name": n_t, "done": False})
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
