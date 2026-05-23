import streamlit as st

# ---------- Page Config ----------
st.set_page_config(
    page_title="English Opens Your World",
    page_icon="📚",
    layout="wide"
)

# ---------- Sidebar Style ----------
st.markdown("""
<style>

/* Sidebar menu text */
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a span,
section[data-testid="stSidebar"] a p {
    font-size: 16px !important;
    font-weight: 500 !important;
}

/* Sidebar spacing */
section[data-testid="stSidebar"] li {
    margin-bottom: 2px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div style="background: linear-gradient(135deg, #F8FBFF, #EEF4FA); padding: 10px 25px; border-radius: 20px; border: 1px solid #D8E6F2; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">

<h1 style="color:#1F2A44; font-size:34px; margin-top:5px; margin-bottom:0px;">
🌍 English Opens Your World
</h1>

<h3 style="color:#4A5568; font-weight:400; font-size:18px; line-height:1.15; margin-top:8px; margin-bottom:4px;">
Explore vocabulary, reading, communication, and real English learning experiences
</h3>

<p style="color:#6B7280; font-size:13px; margin-top:0px; margin-bottom:4px; letter-spacing:2px;">
LEARN • EXPRESS • DISCOVER • GROW
</p>

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# ---------- Intro Section ----------
col1, col2 = st.columns([1.15, 1])

with col1:

    st.markdown("## 🌱 App Learning Plan")

    st.markdown("""
This app is designed for high school English learners who want to improve vocabulary and reading skills in meaningful contexts.

Instead of memorizing isolated words, students learn English through:

- 📖 Reading passages
- 🌿 Word roots and word formation
- 🔗 Collocations and natural expressions
- 🔍 Multiple meanings in context
- 🗣 Communication activities
- 📝 Quiz and feedback systems

The goal is to help learners build confidence and connect English to real-life communication.
""")

with col2:

    st.image(
    "https://raw.githubusercontent.com/kwonsungja/Myproject/main/final_home_image.png",
    use_container_width=True
)

# ---------- Main Features ----------
st.markdown("---")
st.markdown("## ✨ Main Features")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("""
    <div style="
        background-color:#FFF7E8;
        padding:28px;
        border-radius:20px;
        height:250px;
        border:1px solid #F2D7A7;
        box-shadow:0 2px 10px rgba(0,0,0,0.04);
    ">

    <h3>🌿 Word Roots</h3>

    <p>
    Students learn prefixes, roots, and suffixes to understand how vocabulary is formed.
    </p>

    <p>
    <b>Example:</b><br>
    bio = life → biology, biography
    </p>

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div style="
        background-color:#EEFFF4;
        padding:28px;
        border-radius:20px;
        height:250px;
        border:1px solid #B9E4C9;
        box-shadow:0 2px 10px rgba(0,0,0,0.04);
    ">

    <h3>🔗 Collocations</h3>

    <p>
    Students learn common word combinations used in authentic English.
    </p>

    <p>
    <b>Example:</b><br>
    make a decision / take responsibility
    </p>

    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div style="
        background-color:#F4F0FF;
        padding:28px;
        border-radius:20px;
        height:250px;
        border:1px solid #D7C8F3;
        box-shadow:0 2px 10px rgba(0,0,0,0.04);
    ">

    <h3>🔍 Multiple Meanings</h3>

    <p>
    Students compare different meanings of the same word across contexts.
    </p>

    <p>
    <b>Example:</b><br>
    light = brightness / not heavy
    </p>

    </div>
    """, unsafe_allow_html=True)

# ---------- Second Feature Row ----------
st.write("")

col4, col5 = st.columns(2)

with col4:

    st.markdown("""
    <div style="
        background-color:#EAF4FF;
        padding:28px;
        border-radius:20px;
        height:220px;
        border:1px solid #BFD7F0;
        box-shadow:0 2px 10px rgba(0,0,0,0.04);
    ">

    <h3>📖 Reading Context</h3>

    <p>
    Students read passages and discover how vocabulary works naturally in context.
    </p>

    <p>
    Reading activities encourage comprehension, inference, and critical thinking.
    </p>

    </div>
    """, unsafe_allow_html=True)

with col5:

    st.markdown("""
    <div style="
        background-color:#FFF1F6;
        padding:28px;
        border-radius:20px;
        height:220px;
        border:1px solid #F4BCC9;
        box-shadow:0 2px 10px rgba(0,0,0,0.04);
    ">

    <h3>📝 Quiz & Feedback</h3>

    <p>
    Students check understanding through quizzes and receive immediate feedback.
    </p>

    <p>
    Personalized review supports long-term vocabulary retention.
    </p>

    </div>
    """, unsafe_allow_html=True)

# ---------- Learning Flow ----------
st.markdown("---")

st.markdown("## 🧭 Learning Flow")

st.markdown("""
### Step-by-Step Learning Process

1️⃣ Select a reading passage  

2️⃣ Learn key vocabulary and expressions  

3️⃣ Explore roots, collocations, and meanings  

4️⃣ Read the passage again with deeper understanding  

5️⃣ Complete vocabulary and comprehension quizzes  

6️⃣ Receive feedback and review difficult words  
""")

# ---------- Motivation Section ----------
st.markdown("---")

st.markdown("""
<div style="
    background-color:#F8FBFF;
    padding:35px;
    border-radius:20px;
    text-align:center;
    border:1px solid #D9E6F2;
">

<h2 style="color:#1F2A44;">
✨ Build Your English. Shape Your Future.
</h2>

<p style="
    color:#4B5563;
    font-size:18px;
    line-height:1.9;
">
English is not just a school subject.  
It is a bridge to communication, knowledge, and opportunities around the world.
</p>

</div>
""", unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("---")

st.markdown("""
<div style="
    text-align:center;
    color:#6B7280;
    padding-bottom:20px;
">

<p>
Designed for app-based English learning in a high school classroom
</p>

<p>
📚 Vocabulary • Reading • Communication • Growth
</p>

</div>
""", unsafe_allow_html=True)
