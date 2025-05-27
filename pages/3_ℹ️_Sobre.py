import streamlit as st

st.set_page_config(page_title="ℹ️ Sobre - Dra. Luma", layout="wide")

st.title("ℹ️ Sobre o App Dra. Luma")

st.markdown(
    """
    ## 🍼 Alimentação e Cuidados na Gravidez — com Dra. Luma

    **Uma IA gentil, feita para ajudar gestantes a saberem o que podem (ou não) consumir durante a gravidez.**  
    Inspirado na minha esposa, que está grávida e vive a dúvida diária:  
    *“Será que posso comer isso?”* ou *“Posso tomar esse remédio?”*

    Este app foi criado durante a **Imersão de IA com o Google Gemini**, promovida pela Alura em parceria com o Google em 2025.  
    E segue em constante evolução, pensado com muito carinho para acolher futuras mamães.

    ---

    <div style="text-align: center; padding-top: 20px;">
        <p style="font-size: 16px;">
            Desenvolvido por <strong>Luiz Felipe Lima</strong> 💻<br>
            <a href="https://github.com/flimaz" target="_blank">🔗 Acesse meu GitHub</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
