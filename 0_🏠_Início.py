import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Dra. Luma - Cuidados na Gravidez",
    layout="centered",
    page_icon="💖"
)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.empty()

with col2:
    st.image("assets/LogoLuma.png", width=200)

with col3:
    st.empty()


# Título principal
st.title("**Dra. Luma - Cuidados na Gravidez**")

st.markdown(
    """

    Aqui você pode:
    - 🍽️ **Analisar alimentos** para saber se são indicados na gravidez.
    - 💊 **Analisar medicamentos** e entender se são seguros para gestantes.
    - ℹ️ **Sobre** este app, sua missão e os desenvolvedores.

    ---
    🚨 **Atenção:** Este aplicativo não substitui orientação médica ou nutricional. Consulte sempre um profissional de saúde de sua confiança.

    ---
    """,
    unsafe_allow_html=True
)

# 🌟 Chamada de ação
st.subheader("📍 Selecione uma opção no menu lateral para começar!")
