import streamlit as st
from PIL import Image
import os
import google.generativeai as genai
from dotenv import load_dotenv

st.set_page_config(page_title="Dra. Luma - Análise de Medicamentos", layout="centered")

st.title("💊 Análise de Medicamentos na Gravidez")

# Carregar API
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash")

# Inicializa histórico
if "historico_medicamentos" not in st.session_state:
    st.session_state.historico_medicamentos = []

# 🔥 Funções para cards de status
def card_sucesso(mensagem):
    st.markdown(f"""
    <div style="padding:15px; border-radius:10px; background-color:#d4edda; color:#155724; border:1px solid #c3e6cb">
        ✅ {mensagem}
    </div>
    """, unsafe_allow_html=True)

def card_falha(mensagem):
    st.markdown(f"""
    <div style="padding:15px; border-radius:10px; background-color:#f8d7da; color:#721c24; border:1px solid #f5c6cb">
        ❌ {mensagem}
    </div>
    """, unsafe_allow_html=True)


# Função para extrair o nome do medicamento da resposta da IA
def extrair_nome_do_resultado(resposta):
    linhas = resposta.splitlines()

    for linha in linhas:
        if linha.lower().startswith("nome:"):
            titulo = linha.split(":", 1)[1].strip()
            if titulo and titulo.lower() != "não identificado":
                return titulo

    # Fallback se não encontrar
    return "Medicamento via imagem"


st.markdown("Envie uma foto da embalagem do medicamento ou digite o nome dele para saber se é indicado durante a gravidez.")

# Opção de análise
opcao = st.radio("Selecione o modo de análise:", ["📸 Foto do medicamento", "✍️ Digitar nome do medicamento"])

# 📸 Análise por imagem
if opcao == "📸 Foto do medicamento":
    imagem = st.file_uploader("📸 Envie a foto da embalagem", type=["jpg", "jpeg", "png"])

    if imagem:
        with st.spinner("Analisando com muito carinho..."):
            try:
                image = Image.open(imagem)

                prompt = """
Você é uma farmacêutica especializada em saúde da gestante. 

Primeiramente, identifique e informe o nome do medicamento presente na imagem no seguinte formato, exatamente na primeira linha da resposta:

Nome: [nome do medicamento]

Em seguida, responda:

- O medicamento é seguro para gestantes? (Sim, Não ou Depende)
- Justifique de forma clara, objetiva e empática.
- Finalize sempre lembrando que a gestante deve consultar seu médico antes de qualquer uso.

Caso não consiga identificar o medicamento, responda:

Nome: Não identificado
"""

                response = model.generate_content([prompt, image])
                resultado = response.text.strip()

                titulo = extrair_nome_do_resultado(resultado)

                if resultado:
                    card_sucesso("Análise realizada com sucesso!")
                    st.subheader("Resultado da Análise")
                    st.markdown(resultado)

                    # Salvar no histórico
                    st.session_state.historico_medicamentos.insert(0, {
                        "titulo": titulo,
                        "conteudo": resultado
                    })
                    st.session_state.historico_medicamentos = st.session_state.historico_medicamentos[:5]
                else:
                    card_falha("Falha ao realizar a análise. Tente novamente.")

            except Exception as e:
                card_falha("Falha ao realizar a análise. Verifique a imagem e tente novamente.")
                st.error(f"Ocorreu um erro: {e}")


# ✍️ Análise por texto
elif opcao == "✍️ Digitar nome do medicamento":
    nome_medicamento = st.text_input("✍️ Digite o nome do medicamento")

    if nome_medicamento:
        if st.button("🔍 Analisar"):
            with st.spinner("Analisando com muito carinho..."):
                try:
                    prompt = f"""
Você é uma farmacêutica especializada em saúde da gestante. Responda diretamente sobre o medicamento **{nome_medicamento}**, sem introduções, sem saudações e sem repetições.

Informe:

1. Se o medicamento é seguro para gestantes (Sim, Não ou Depende).
2. Justifique de forma clara, objetiva e empática.
3. Categoria de risco na gravidez, se aplicável.
4. Finalize sempre lembrando que a gestante deve consultar seu médico antes de qualquer uso.

Se não conseguir identificar o medicamento, diga isso de forma acolhedora.
"""

                    response = model.generate_content(prompt)
                    resultado = response.text.strip()

                    if resultado:
                        card_sucesso("Análise realizada com sucesso!")
                        st.subheader("✅ Resultado da Análise")
                        st.markdown(resultado)

                        st.session_state.historico_medicamentos.insert(0, {
                            "titulo": nome_medicamento,
                            "conteudo": resultado
                        })
                        st.session_state.historico_medicamentos = st.session_state.historico_medicamentos[:5]
                    else:
                        card_falha("Falha ao realizar a análise. Tente novamente.")

                except Exception as e:
                    card_falha("Falha ao realizar a análise. Verifique o nome e tente novamente.")
                    st.error(f"Ocorreu um erro: {e}")


# 🔍 Histórico
st.subheader("🔍 Histórico de Análises Anteriores")

if st.session_state.historico_medicamentos:
    for item in st.session_state.historico_medicamentos:
        with st.expander(f"🗂️ {item['titulo']}"):
            st.markdown(item['conteudo'])
else:
    st.info("Nenhuma análise realizada ainda.")
