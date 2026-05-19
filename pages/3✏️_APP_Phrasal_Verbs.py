import streamlit as st
import pandas as pd
import random
from pathlib import Path

# =============================
# High School Grade 1 Phrasal Verbs App
# File required: phrasal_verbs_from_book.csv
# Columns: order, category, phrasal_verb, korean_meaning, cf_note
# =============================

st.set_page_config(
    page_title="Phrasal Verbs Practice",
    page_icon="📘",
    layout="wide"
)

# ---------- Basic Styling ----------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #ff6b35;
    }
    .sub-text {
        font-size: 17px;
        color: #555;
    }
    .word-card {
        background-color: #fff7f0;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #ffd2b8;
        margin-bottom: 14px;
    }
    .phrasal-word {
        font-size: 28px;
        font-weight: 800;
        color: #e85d04;
    }
    .meaning-text {
        font-size: 20px;
        color: #222;
    }
    .cf-text {
        font-size: 15px;
        color: #666;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Data Loading ----------
@st.cache_data
def load_data():
    possible_files = [
        "phrasal_verbs_from_book.csv",
        "data/phrasal_verbs_from_book.csv"
    ]

    file_path = None
    for f in possible_files:
        if Path(f).exists():
            file_path = f
            break

    if file_path is None:
        st.error("phrasal_verbs_from_book.csv 파일을 app.py와 같은 폴더 또는 data 폴더에 넣어 주세요.")
        st.stop()

    df = pd.read_csv(file_path)

    required_cols = ["order", "category", "phrasal_verb", "korean_meaning", "cf_note"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"CSV 컬럼명이 맞지 않습니다. 빠진 컬럼: {missing}")
        st.stop()

    df["cf_note"] = df["cf_note"].fillna("")
    df = df.sort_values("order").reset_index(drop=True)
    return df


df = load_data()

# ---------- Header ----------
st.markdown('<div class="main-title">📘 Phrasal Verbs Practice</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">고등학교 1학년 수준의 구동사 학습 앱입니다. 먼저 뜻을 익히고, 바로 퀴즈로 확인해 보세요.</div>', unsafe_allow_html=True)
st.divider()

# ---------- Sidebar ----------
st.sidebar.header("학습 설정")
mode = st.sidebar.radio(
    "메뉴 선택",
    ["1. Learn", "2. Quick Test", "3. Review Wrong Answers"],
    index=0
)

items_per_page = st.sidebar.slider("한 번에 볼 표현 수", 5, 20, 10)

# ---------- Session State ----------
if "wrong_items" not in st.session_state:
    st.session_state.wrong_items = []

if "quiz_items" not in st.session_state:
    st.session_state.quiz_items = []

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ---------- Learn Mode ----------
if mode == "1. Learn":
    st.subheader("📖 Learn Phrasal Verbs")

    total_pages = (len(df) - 1) // items_per_page + 1
    page = st.selectbox("학습 범위 선택", list(range(1, total_pages + 1)))

    start = (page - 1) * items_per_page
    end = start + items_per_page
    page_df = df.iloc[start:end]

    for _, row in page_df.iterrows():
        st.markdown(
            f"""
            <div class="word-card">
                <div class="phrasal-word">{int(row['order'])}. {row['phrasal_verb']}</div>
                <div class="meaning-text">뜻: {row['korean_meaning']}</div>
                <div class="cf-text">cf. {row['cf_note']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.info("추천 학습 방법: 표현을 소리 내어 읽고, cf. 표현까지 함께 확인하세요.")

# ---------- Quick Test Mode ----------
elif mode == "2. Quick Test":
    st.subheader("📝 Quick Test")

    quiz_size = st.selectbox("문항 수", [5, 10, 15], index=1)

    if st.button("새 테스트 시작"):
        st.session_state.quiz_items = df.sample(min(quiz_size, len(df)), random_state=random.randint(1, 100000)).to_dict("records")
        st.session_state.submitted = False

    if not st.session_state.quiz_items:
        st.warning("먼저 '새 테스트 시작' 버튼을 눌러 주세요.")
        st.stop()

    answers = []
    for i, item in enumerate(st.session_state.quiz_items, start=1):
        st.markdown(f"### Q{i}. {item['phrasal_verb']}")

        correct = item["korean_meaning"]
        other_options = df[df["korean_meaning"] != correct]["korean_meaning"].sample(3).tolist()
        options = other_options + [correct]
        random.shuffle(options)

        answer = st.radio(
            "뜻을 고르세요.",
            options,
            key=f"q_{item['order']}"
        )
        answers.append((item, answer, correct))

    if st.button("제출하기"):
        st.session_state.submitted = True
        score = 0
        wrong_now = []

        st.divider()
        st.subheader("결과")

        for item, answer, correct in answers:
            if answer == correct:
                score += 1
                st.success(f"✅ {item['phrasal_verb']} = {correct}")
            else:
                st.error(f"❌ {item['phrasal_verb']} | 선택: {answer} / 정답: {correct}")
                wrong_now.append(item)

        st.session_state.wrong_items.extend(wrong_now)
        st.session_state.wrong_items = list({x['phrasal_verb']: x for x in st.session_state.wrong_items}.values())

        st.markdown(f"## 점수: {score} / {len(answers)}")

        if score == len(answers):
            st.balloons()
            st.success("완벽합니다! 다음 표현으로 넘어가도 좋아요.")
        elif score >= len(answers) * 0.7:
            st.info("좋아요! 틀린 표현만 한 번 더 복습하세요.")
        else:
            st.warning("아직 익숙하지 않은 표현이 있어요. Learn 메뉴에서 다시 확인해 보세요.")

# ---------- Review Wrong Answers ----------
else:
    st.subheader("🔁 Review Wrong Answers")

    if not st.session_state.wrong_items:
        st.success("아직 오답이 없습니다. Quick Test를 먼저 풀어 보세요.")
    else:
        st.write(f"현재 오답 표현 수: {len(st.session_state.wrong_items)}")

        for item in st.session_state.wrong_items:
            st.markdown(
                f"""
                <div class="word-card">
                    <div class="phrasal-word">{item['phrasal_verb']}</div>
                    <div class="meaning-text">뜻: {item['korean_meaning']}</div>
                    <div class="cf-text">cf. {item['cf_note']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.button("오답 목록 초기화"):
            st.session_state.wrong_items = []
            st.rerun()

# ---------- Footer ----------
st.divider()
st.caption("Designed for Grade 1 high school English vocabulary learning.")

