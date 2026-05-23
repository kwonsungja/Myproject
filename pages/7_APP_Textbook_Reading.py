import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="APP Textbook Reading",
    page_icon="📘",
    layout="wide"
)

st.title("📘 APP Textbook Reading")
st.caption("Vocabulary → Textbook Reading → Reading Expansion")

# -----------------------------
# Data loading
# -----------------------------

@st.cache_data
def load_data(book):

    base_path = Path(__file__).resolve().parents[1] / "data"

    file_map = {
        "공통영어1": "common_english1_reading_full.csv",
        "공통영어2": "common_english2_reading_full.csv"
    }

    file_path = base_path / file_map[book]

    if not file_path.exists():
        st.error("CSV 파일을 찾을 수 없습니다.")
        st.write("현재 찾는 위치:", file_path)
        st.write("data 폴더 파일 목록:", list(base_path.iterdir()))
        st.stop()

    return pd.read_csv(file_path, encoding="utf-8-sig")

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("Reading Options")

book = st.sidebar.selectbox(
    "교과서 선택",
    ["공통영어1", "공통영어2"]
)

df = load_data(book)

lesson = st.sidebar.selectbox(
    "Lesson 선택",
    df["lesson"].unique()
)

row = df[df["lesson"] == lesson].iloc[0]


# -----------------------------
# Header
# -----------------------------

st.markdown(f"## {book} · {row['lesson']}")
st.markdown(f"### {row['title']}")

st.divider()


# -----------------------------
# Summary
# -----------------------------

st.subheader("📝 Summary")
st.info(row["summary"])


# -----------------------------
# Key Expressions
# -----------------------------

st.subheader("🔑 Key Expressions")

key_expressions = str(row["key_expressions"]).split(";")

for exp in key_expressions:
    exp = exp.strip()
    if exp:
        st.markdown(f"- **{exp}**")


# -----------------------------
# Full Text
# -----------------------------

st.subheader("📖 Textbook Reading Text")

with st.expander("본문 텍스트 보기", expanded=True):
    st.write(row["full_text"])

# -----------------------------
# Further Reading
# -----------------------------

st.divider()

st.subheader("📚 Further Reading")

st.markdown(f"### {row['further_reading_title']}")

with st.expander("Read Further"):
    st.write(row["further_reading_text"])


# -----------------------------
# Reading Task
# -----------------------------

st.subheader("🎯 Reading Task")
st.success(row["reading_task"])


# -----------------------------
# Quiz
# -----------------------------

st.subheader("❓ Comprehension Quiz")

st.markdown(f"**Q. {row['quiz']}**")

user_answer = st.text_input("Your answer")

if st.button("Check Answer"):
    answer = str(row["answer"]).strip()

    if user_answer.strip() == "":
        st.warning("답을 입력해 주세요.")
    elif user_answer.lower().strip() in answer.lower():
        st.success("Good job! Your answer is acceptable.")
        st.markdown(f"**Suggested answer:** {answer}")
    else:
        st.error("다시 한 번 생각해 보세요.")
        st.markdown(f"**Suggested answer:** {answer}")


# -----------------------------
# Learning Reflection
# -----------------------------

st.divider()

st.subheader("💬 Reflection")

reflection = st.text_area(
    "오늘 본문에서 새롭게 배운 표현이나 내용을 적어보세요.",
    height=120
)

if reflection:
    st.success("좋아요. 본문 읽기와 어휘 학습이 잘 연결되고 있어요.")
