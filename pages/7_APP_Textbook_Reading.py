import streamlit as st
import pandas as pd
from pathlib import Path
from gtts import gTTS
from io import BytesIO

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

def load_data(book):

    file_map = {
        "공통영어1": "common_english1_reading_full.csv",
        "공통영어2": "common_english2_reading_full.csv"
    }

    base_path = Path(__file__).resolve().parents[1] / "data"

    file_path = base_path / file_map[book]

    if not file_path.exists():
        st.error("CSV 파일을 찾을 수 없습니다.")
        st.write("현재 찾는 위치:", file_path)
        st.write("data 폴더 파일 목록:", list(base_path.iterdir()))
        st.stop()

    df = pd.read_csv(file_path, encoding="utf-8-sig")

    df.columns = df.columns.str.strip()

    return df

# ---------- Reading Options ----------

st.header("⚙️ Reading Options")

selected_book = st.selectbox(
    "교과서 선택",
    ["공통영어1", "공통영어2"]
)

df = load_data(selected_book)

lesson_options = ["전체"] + list(df["lesson"].dropna().unique())

selected_lesson = st.selectbox(
    "Lesson 선택",
    lesson_options
)

if selected_lesson != "전체":
    filtered_df = df[df["lesson"] == selected_lesson].copy()
else:
    filtered_df = df.copy()

# 자료가 없을 경우 처리
if filtered_df.empty:
    st.warning("선택한 조건에 해당하는 자료가 없습니다.")
    st.stop()

# 첫 번째 row 선택
row = filtered_df.iloc[0]
# -----------------------------
# Header
# -----------------------------

st.markdown(f"## {selected_book} · {row['lesson']}")
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
# TTS: Text-to-Speech
# -----------------------------
st.markdown("### 🔊 Listen to the Text")

tts_text = row["full_text"]

if st.button("🎧 Generate American English Audio"):

    try:
        with st.spinner("Generating audio..."):
            tts = gTTS(text=tts_text, lang="en", tld="com")

            audio_fp = BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)

            st.audio(audio_fp, format="audio/mp3")

    except Exception as e:
        st.error("Audio generation failed.")
        st.write(e)

# -----------------------------
# Further Reading
# -----------------------------

st.divider()

st.subheader("📚 Further Reading")

title = row.get("further_reading_title", "")
text = row.get("further_reading_text", "")

if pd.notna(title) and pd.notna(text):

    st.markdown(f"### {title}")

    with st.expander("Read Further"):
        st.write(text)

# -----------------------------
# Further Reading TTS
# -----------------------------

st.markdown("### 🔊 Listen to the Further Reading")

further_tts_text = row["further_reading_text"]

if st.button("🎧 Generate Further Reading Audio"):

    try:
        with st.spinner("Generating further reading audio..."):

            further_tts = gTTS(
                text=further_tts_text,
                lang="en",
                tld="com"
            )

            further_audio_fp = BytesIO()
            further_tts.write_to_fp(further_audio_fp)
            further_audio_fp.seek(0)

            st.audio(further_audio_fp, format="audio/mp3")

    except Exception as e:
        st.error("Further Reading audio generation failed.")
        st.write(e)

else:
    st.info("Further Reading 자료가 아직 입력되지 않았습니다.")


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
