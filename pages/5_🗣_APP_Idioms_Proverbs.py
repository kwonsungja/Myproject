import streamlit as st
import pandas as pd
import random
from pathlib import Path

# ==========================================
# Idioms & Proverbs App
# ==========================================

st.set_page_config(
    page_title="Idioms & Proverbs",
    page_icon="📘",
    layout="wide"
)

# ---------- Style ----------
st.markdown("""
<style>

/* 전체 기본 글자 */
html, body, [class*="css"] {
    font-size: 17px;
}

/* Sidebar menu text */
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a span,
section[data-testid="stSidebar"] a p {
    font-size: 18px !important;
    font-weight: 500 !important;
}

/* 메뉴 선택 라벨 */
div[data-testid="stRadio"] > label {
    font-size: 24px !important;
    font-weight: 700 !important;
}

/* 라디오 선택지 글자 */
div[role="radiogroup"] label p {
    font-size: 22px !important;
    font-weight: 500 !important;
}

/* selectbox 라벨 */
label p {
    font-size: 19px !important;
    font-weight: 600 !important;
}

.word-card {
    background-color: #fff7f0;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #ffd2b8;
    margin-bottom: 14px;
}

.guided-card {
    background-color: #f3f8ff;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #cfe3ff;
    margin-bottom: 14px;
}

.review-card {
    background-color: #f7fff4;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #cdebc3;
    margin-bottom: 14px;
}

.expression-text {
    font-size: 26px;
    font-weight: 800;
    color: #e85d04;
}

.meaning-text {
    font-size: 19px;
    color: #222;
    margin-top: 6px;
}

.example-text {
    font-size: 17px;
    color: #444;
    margin-top: 8px;
}

.tip-text {
    font-size: 16px;
    color: #666;
    margin-top: 6px;
}

.question-text {
    font-size: 26px !important;
    font-weight: 700 !important;
    margin-top: 24px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<h1 style='text-align:center; font-size:36px; margin-bottom:10px;'>
📘 APP Idioms & Proverbs (Grade 1)
</h1>

<div style='text-align:center; font-size:18px; color:#555; line-height:1.8;'>

Learn idioms and proverbs through meaning, context, guided practice, and review.
<br>
공통영어1 · 관용표현과 속담을 문맥 속에서 학습하는 고등학교 1학년용 숙어 앱입니다.

</div>
""", unsafe_allow_html=True)


# ---------- Load Data ----------
CSV_FILE = "idioms_proverbs_for_grade1.csv"

@st.cache_data
def load_data():

    path1 = Path(CSV_FILE)
    path2 = Path("data") / CSV_FILE

    if path1.exists():
        df = pd.read_csv(path1)
    elif path2.exists():
        df = pd.read_csv(path2)
    else:
        st.error(f"{CSV_FILE} 파일을 찾을 수 없습니다.")
        st.stop()

    required = [
        "order",
        "category",
        "expression",
        "korean_meaning",
        "cf_note"
    ]

    missing = [c for c in required if c not in df.columns]

    if missing:
        st.error(f"빠진 컬럼: {missing}")
        st.stop()

    df = df.fillna("")
    df = df.sort_values("order").reset_index(drop=True)

    return df


df = load_data()

# ---------- Session State ----------
if "idiom_wrong_items" not in st.session_state:
    st.session_state.idiom_wrong_items = []

if "idiom_guided_items" not in st.session_state:
    st.session_state.idiom_guided_items = []

if "idiom_check_items" not in st.session_state:
    st.session_state.idiom_check_items = []

# ---------- Learning Settings ----------
st.header("⚙️ 학습 설정")

mode = st.radio(
    "메뉴 선택",
    [
        "📘 Learn",
        "🧩 Guided Practice",
        "✅ Practice Check",
        "🔁 Review"
    ],
    index=0
)

category = st.selectbox(
    "학습 범위",
    ["전체"] + list(df["category"].unique())
)

if category == "전체":
    filtered_df = df.copy()
else:
    filtered_df = df[df["category"] == category].copy()

items_per_page = st.slider(
    "한 번에 볼 표현 수",
    5,
    20,
    10
)

# ==========================================
# 1. Learn
# ==========================================
if mode == "📘 Learn":

    st.subheader("📘 Learn")
    st.info("목표: 숙어와 속담의 의미, 관련 표현, 분류를 먼저 이해합니다.")

    st.write(f"현재 학습 항목 수: **{len(filtered_df)}개**")

    if filtered_df.empty:
        st.warning("선택한 범위에 해당하는 항목이 없습니다.")
        st.stop()

    total_pages = (len(filtered_df) - 1) // items_per_page + 1
    page = st.selectbox("📖숙어 페이지(10개씩 선택)", list(range(1, total_pages + 1)))

    start = (page - 1) * items_per_page
    end = start + items_per_page
    page_df = filtered_df.iloc[start:end]

    for _, row in page_df.iterrows():

        st.markdown(
            f"""
            <div class="word-card">

            <div class="expression-text">
            {int(row['order'])}. {row['expression']}
            </div>

            <div class="meaning-text">
            뜻: {row['korean_meaning']}
            </div>

            <div class="tip-text">
            cf. {row['cf_note']}
            </div>

            <div class="tip-text">
            분류: {row['category']}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

# ==========================================
# 2. Guided Practice
# ==========================================
elif mode == "🧩 Guided Practice":

    st.subheader("🧩 Guided Practice")
    st.info("목표: 힌트를 보면서 숙어와 속담의 의미를 확인합니다.")

    if filtered_df.empty:
        st.warning("선택한 범위에 해당하는 항목이 없습니다.")
        st.stop()

    practice_size = st.selectbox(
        "연습 문항 수",
        [5, 10, 15],
        index=0
    )

    if st.button("새 Guided Practice 시작"):

        guided_items = filtered_df.sample(
            min(practice_size, len(filtered_df)),
            random_state=random.randint(1, 100000)
        ).to_dict("records")

        for item in guided_items:

            correct = item["korean_meaning"]

            wrong_pool = df[
                df["korean_meaning"] != correct
            ]["korean_meaning"].dropna().unique().tolist()

            wrongs = random.sample(
                wrong_pool,
                min(2, len(wrong_pool))
            )

            options = wrongs + [correct]
            random.shuffle(options)

            item["options"] = options

        st.session_state.idiom_guided_items = guided_items

    if st.session_state.idiom_guided_items:

        answers = []

        for i, item in enumerate(st.session_state.idiom_guided_items, start=1):

            st.markdown(
                f"""
                <div class="guided-card">

                <div class="expression-text">
                Q{i}. {item['expression']}
                </div>

                <div class="tip-text">
                💡 Hint: {item['cf_note']}
                </div>

                <div class="tip-text">
                분류: {item['category']}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            answer = st.radio(
                "💡 뜻을 고르세요.",
                item["options"],
                index=None,
                key=f"idiom_guided_{i}"
            )

            answers.append((item, answer))

        if st.button("Guided Practice 확인"):

            score = 0

            for item, answer in answers:

                if answer == item["korean_meaning"]:

                    score += 1

                    st.success(
                        f"정답입니다: {item['expression']} = {item['korean_meaning']}"
                    )

                else:

                    st.warning(
                        f"다시 확인해 보세요. 정답은 '{item['korean_meaning']}'입니다."
                    )

            st.markdown(f"## 점수: {score} / {len(answers)}")

            if score == len(answers):
                st.success("🎉 Perfect Score!")
                st.balloons()
        
# ==========================================
# 3. Practice Check
# ==========================================
elif mode == "✅ Practice Check":

    st.subheader("✅ Practice Check")
    st.info("목표: 힌트 없이 숙어와 속담의 의미를 스스로 확인합니다.")

    if filtered_df.empty:
        st.warning("선택한 범위에 해당하는 항목이 없습니다.")
        st.stop()

    quiz_size = st.selectbox(
        "문항 수",
        [5, 10, 15, 20],
        index=1
    )

    if st.button("새 Practice Check 시작"):

        quiz_items = filtered_df.sample(
            min(quiz_size, len(filtered_df)),
            random_state=random.randint(1, 100000)
        ).to_dict("records")

        for item in quiz_items:

            correct = item["korean_meaning"]

            wrong_pool = df[
                df["korean_meaning"] != correct
            ]["korean_meaning"].dropna().unique().tolist()

            wrongs = random.sample(
                wrong_pool,
                min(3, len(wrong_pool))
            )

            options = wrongs + [correct]
            random.shuffle(options)

            item["options"] = options

        st.session_state.idiom_check_items = quiz_items

    if st.session_state.idiom_check_items:

        answers = []

        for i, item in enumerate(st.session_state.idiom_check_items, start=1):

            st.markdown(
                f"<div class='question-text'>Q{i}. {item['expression']}</div>",
                unsafe_allow_html=True
            )

            answer = st.radio(
                "💡 뜻을 고르세요.",
                item["options"],
                index=None,
                key=f"idiom_check_{i}"
            )

            answers.append((item, answer))

        if st.button("Practice Check 제출"):

            score = 0

            for item, answer in answers:

                correct = item["korean_meaning"]

                if answer == correct:

                    score += 1

                    st.success(
                        f"✅ {item['expression']} = {correct}"
                    )

                else:

                    st.error(
                        f"❌ {item['expression']} → 정답: {correct}"
                    )

                    st.write(f"cf.: {item['cf_note']}")

                    if item not in st.session_state.idiom_wrong_items:
                        st.session_state.idiom_wrong_items.append(item)

            st.markdown(f"## 점수: {score} / {len(answers)}")
            if score == len(answers):
               st.success("🎉 Perfect Score!")
               st.balloons()

# ==========================================
# 4. Review
# ==========================================
else:

    st.subheader("🔁 Review")
    st.info("목표: 틀린 숙어와 속담을 다시 복습하며 장기 기억으로 연결합니다.")

    if not st.session_state.idiom_wrong_items:

        st.success("아직 오답이 없습니다. Practice Check를 먼저 풀어 보세요.")

    else:

        st.write(f"현재 오답 수: **{len(st.session_state.idiom_wrong_items)}개**")

        for item in st.session_state.idiom_wrong_items:

            st.markdown(
                f"""
                <div class="review-card">

                <div class="expression-text">
                {item['expression']}
                </div>

                <div class="meaning-text">
                뜻: {item['korean_meaning']}
                </div>

                <div class="tip-text">
                cf. {item['cf_note']}
                </div>

                <div class="tip-text">
                분류: {item['category']}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        if st.button("오답 초기화"):

            st.session_state.idiom_wrong_items = []

            st.rerun()

# ---------- Footer ----------
st.divider()
st.caption("Designed for Grade 1 idioms and proverbs learning.")
