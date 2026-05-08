import streamlit as st

st.set_page_config(
    page_title="Voca & Reading App",
    page_icon="📚",
    layout="wide"
)

# ---------- Header ----------
st.markdown("""
<div style="
    background: linear-gradient(135deg, #EAF4FF, #F8FBFF);
    padding: 45px;
    border-radius: 22px;
    border: 1px solid #D6E6F5;
    text-align: center;
">
    <h1 style="color:#1F2A44; font-size:42px;">
        📚 Voca & Reading Learning App
    </h1>
    <h3 style="color:#4A5568;">
        Learn vocabulary through roots, collocations, multiple meanings, and reading contexts
    </h3>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# ---------- Intro ----------
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("## 🌱 App Learning Plan")
    st.markdown("""
This app is designed for high school English learners.  
Students learn vocabulary not as isolated words, but through **meaningful reading contexts**.

The app connects:

- **Word roots**
- **Collocations**
- **Multiple meanings**
- **Reading passages**
- **Comprehension questions**
- **Vocabulary review**
""")

with col2:
    st.image("https://github.com/kwonsungja/Myproject/blob/main/final%20home%20image.png", use_container_width=True)

# ---------- Main Features ----------
st.markdown("---")
st.markdown("## ✨ Main Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="
        background-color:#FFF7E6;
        padding:25px;
        border-radius:18px;
        height:220px;
        border:1px solid #F3D8A8;
    ">
    <h3>🌿 Word Roots</h3>
    <p>Students learn how word meanings are formed through prefixes, roots, and suffixes.</p>
    <p><b>Example:</b> bio = life → biology, biography</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background-color:#EFFFF4;
        padding:25px;
        border-radius:18px;
        height:220px;
        border:1px solid #B7E4C7;
    ">
    <h3>🔗 Collocations</h3>
    <p>Students learn common word combinations used in real English.</p>
    <p><b>Example:</b> make a decision, take responsibility</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="
        background-color:#F3EFFF;
        padding:25px;
        border-radius:18px;
        height:220px;
        border:1px solid #D5C7F2;
    ">
    <h3>🔍 Multiple Meanings</h3>
    <p>Students compare different meanings of the same word in different contexts.</p>
    <p><b>Example:</b> light = not heavy / brightness</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

col4, col5 = st.columns(2)

with col4:
    st.markdown("""
    <div style="
        background-color:#EAF4FF;
        padding:25px;
        border-radius:18px;
        height:200px;
        border:1px solid #BBD7F0;
    ">
    <h3>📖 Reading Context</h3>
    <p>Students read short passages and understand how vocabulary works in context.</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div style="
        background-color:#FFF0F6;
        padding:25px;
        border-radius:18px;
        height:200px;
        border:1px solid #F4B6C2;
    ">
    <h3>📝 Quiz & Feedback</h3>
    <p>Students check their understanding through vocabulary and reading questions.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- Learning Flow ----------
st.markdown("---")
st.markdown("## 🧭 Learning Flow")

st.markdown("""
1. Select a reading passage  
2. Learn key vocabulary from the passage  
3. Study word roots, collocations, and multiple meanings  
4. Read the passage again  
5. Answer vocabulary and reading comprehension questions  
6. Receive feedback and review difficult words  
""")

# ---------- Footer ----------
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#6B7280;">
    <p>Designed for app-based English learning in a high school classroom</p>
</div>
""", unsafe_allow_html=True)
