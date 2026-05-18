import streamlit as st
import time
import random

st.set_page_config(page_title="Smart Class Tools", page_icon="🧰", layout="wide")

st.markdown("""
<h1 style='text-align:center;'>🧰 Smart Class Tools</h1>
<p style='text-align:center; font-size:20px;'>Timer · Stopwatch · Random Number · Penalty Wheel</p>
""", unsafe_allow_html=True)

tabs = st.tabs(["⏱ 타이머", "⌛ 스톱워치", "🎲 순서정하기", "🎯 벌칙정하기"])

# -----------------------------
# 1. TIMER
# -----------------------------
with tabs[0]:
    st.markdown("## ⏱ 타이머")

    col1, col2, col3 = st.columns(3)
    with col1:
        minutes = st.number_input("분", min_value=0, max_value=60, value=1)
    with col2:
        seconds = st.number_input("초", min_value=0, max_value=59, value=0)
    with col3:
        start_timer = st.button("시작", key="timer_start")

    total_seconds = minutes * 60 + seconds
    timer_box = st.empty()

    if start_timer:
        for remaining in range(total_seconds, -1, -1):
            m, s = divmod(remaining, 60)
            timer_box.markdown(
                f"""
                <div style='
                    text-align:center;
                    font-size:110px;
                    font-weight:900;
                    background:#f1f1f1;
                    border-radius:30px;
                    padding:40px;
                    margin-top:30px;
                '>
                {m:02d}:{s:02d}
                </div>
                """,
                unsafe_allow_html=True
            )
            time.sleep(1)
        st.success("⏰ 시간이 끝났습니다!")

# -----------------------------
# 2. STOPWATCH
# -----------------------------
with tabs[1]:
    st.markdown("## ⌛ 스톱워치")

    if "sw_running" not in st.session_state:
        st.session_state.sw_running = False
    if "sw_start" not in st.session_state:
        st.session_state.sw_start = 0
    if "sw_elapsed" not in st.session_state:
        st.session_state.sw_elapsed = 0

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("시작", key="sw_start_btn"):
            st.session_state.sw_running = True
            st.session_state.sw_start = time.time() - st.session_state.sw_elapsed

    with c2:
        if st.button("정지", key="sw_stop_btn"):
            st.session_state.sw_running = False
            st.session_state.sw_elapsed = time.time() - st.session_state.sw_start

    with c3:
        if st.button("초기화", key="sw_reset_btn"):
            st.session_state.sw_running = False
            st.session_state.sw_elapsed = 0

    stopwatch_box = st.empty()

    if st.session_state.sw_running:
        elapsed = time.time() - st.session_state.sw_start
    else:
        elapsed = st.session_state.sw_elapsed

    h = int(elapsed // 3600)
    m = int((elapsed % 3600) // 60)
    s = int(elapsed % 60)

    stopwatch_box.markdown(
        f"""
        <div style='
            text-align:center;
            font-size:120px;
            font-weight:900;
            background:#333;
            color:white;
            border-radius:30px;
            padding:50px;
            margin-top:40px;
        '>
        {h:02d}:{m:02d}:{s:02d}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.sw_running:
        time.sleep(1)
        st.rerun()

# -----------------------------
# 3. RANDOM STUDENT NUMBER
# -----------------------------
with tabs[2]:
    st.markdown("## 🎲 학생번호 순서정하기")

    student_count = st.number_input("학생 수를 입력하세요", min_value=1, max_value=50, value=30)

    if st.button("번호 뽑기", key="pick_number"):
        picked = random.randint(1, student_count)

        st.markdown(
            f"""
            <div style='
                text-align:center;
                font-size:150px;
                font-weight:900;
                color:#111;
                background:#e8f7c5;
                border-radius:30px;
                padding:60px;
                margin-top:30px;
            '>
            {picked}
            </div>
            <h2 style='text-align:center;'>발표할 번호</h2>
            """,
            unsafe_allow_html=True
        )

# -----------------------------
# 4. PENALTY WHEEL
# -----------------------------
with tabs[3]:
    st.markdown("## 🎯 벌칙정하기")

    default_penalties = """노래부르기
춤추기
칭찬하기
영어 문장 말하기
친구에게 질문하기
선생님 도와주기"""

    penalty_text = st.text_area(
        "벌칙 목록을 한 줄에 하나씩 입력하세요",
        value=default_penalties,
        height=180
    )

    penalties = [p.strip() for p in penalty_text.split("\n") if p.strip()]

    if st.button("벌칙 뽑기", key="pick_penalty"):
        selected_penalty = random.choice(penalties)

        st.markdown(
            f"""
            <div style='
                text-align:center;
                font-size:70px;
                font-weight:900;
                color:#ff4f8b;
                background:#ffe4ef;
                border-radius:30px;
                padding:70px;
                margin-top:30px;
            '>
            🎯 {selected_penalty}
            </div>
            <h2 style='text-align:center;'>당첨된 벌칙</h2>
            """,
            unsafe_allow_html=True
        )
