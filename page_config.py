import streamlit as st 

def setup():
    st.set_page_config(
    page_title="AI Resume Enhancer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ______ Custom CSS for better UI
    st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        color: #155724;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #e7f3ff;
        border-left: 4px solid #2196f3;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 100%;
        padding: 0.5rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)
