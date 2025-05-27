import streamlit as st
from PIL import Image
import os
import google.generativeai as genai
from dotenv import load_dotenv

st.set_page_config(page_title="Dra. Luma - Análise de Alimentos", layout="centered")

st.title("🍽️ Análise de Alimentos na Gravidez")

# Carregar API
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash")

# Inicializa histórico próprio da página de alimentos
if "historico_alimentos" not in st.session_state:
    st.session_state.historico_alimentos = []


# 🔥 Funções para cards visuais
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


# 🔍 Função para extrair nome do alimento
def extrair_nome_do_resultado(resposta):
    linhas = resposta.splitlines()
    for linha in linhas:
        if linha.lower().startswith("nome:"):
            titulo = linha.split(":", 1)[1].strip()
            if titulo and titulo.lower() != "não identificado":
                return titulo
    return "Alimento via imagem"


st.markdown("Envie uma foto de um alimento ou digite o nome dele para saber se é indicado durante a gravidez.")

# Opção de análise
opcao = st.radio("Selecione o modo de análise:", ["📸 Foto do alimento", "✍️ Digitar nome do alimento"])

# 📸 Análise por imagem
if opcao == "📸 Foto do alimento":
    imagem = st.file_uploader("📸 Envie a foto do alimento", type=["jpg", "jpeg", "png"])

    if imagem:
        with st.spinner("Analisando com muito carinho..."):
            try:
                image = Image.open(imagem)

                prompt = """
                Você é uma nutricionista especializada na saúde de gestantes.

                Observe a imagem atentamente e siga exatamente este formato de resposta:

                Identifique cada alimento ou item visível no prato ou embalagem, listando um por um.

                Para cada alimento, responda:
                - Se é seguro ou não para gestantes (Sim, Não ou Depende).
                - Calorias estimadas por 100g ou 100ml (e, se aplicável, informe também por unidade média).
                - Benefícios para a gestação, se houver.

                Em seguida, forneça uma estimativa das calorias totais do prato ou da embalagem como um todo, considerando os alimentos presentes e uma quantidade média razoável para uma refeição.

                Finalize sempre com um alerta acolhedor, reforçando que esta é uma estimativa baseada na imagem e que a gestante deve sempre consultar seu nutricionista ou médico antes de consumir.

                Caso algum alimento não possa ser identificado com segurança na imagem, informe isso de forma acolhedora, dizendo: "Não foi possível identificar com precisão este item na imagem."

                A resposta deve ser organizada, clara, direta e acolhedora, em tom simpático e profissional.
                """

                response = model.generate_content([prompt, image])
                resultado = response.text.strip()

                titulo = extrair_nome_do_resultado(resultado)

                if resultado:
                    card_sucesso("Análise realizada com sucesso!")
                    st.subheader("✅ Resultado da Análise")
                    st.markdown(resultado)

                    # Salvar no histórico
                    st.session_state.historico_alimentos.insert(0, {
                        "titulo": titulo,
                        "conteudo": resultado
                    })
                    st.session_state.historico_alimentos = st.session_state.historico_alimentos[:5]
                else:
                    card_falha("Falha ao realizar a análise. Tente novamente.")

            except Exception as e:
                card_falha("Falha ao realizar a análise. Verifique a imagem e tente novamente.")
                st.error(f"Ocorreu um erro: {e}")


# Análise por texto
elif opcao == "✍️ Digitar nome do alimento":
    nome_alimento = st.text_input("✍️ Digite o nome do alimento")

    if nome_alimento:
        if st.button("🔍 Analisar"):
            with st.spinner("Analisando com muito carinho..."):
                try:
                    prompt = f"""
Você é uma nutricionista especializada em saúde da gestante. Responda diretamente sobre o alimento **{nome_alimento}**, sem introduções, sem saudações e sem repetições.

Informe:

1. Se o alimento é seguro para gestantes (Sim, Não ou Depende).
2. Informe as calorias por 100g ou 100ml.
3. Diga se possui algum benefício na gestação.
4. Finalize sempre lembrando que a gestante deve consultar seu nutricionista ou médico antes de consumir.

Caso não consiga identificar o alimento, diga isso de forma acolhedora.
"""

                    response = model.generate_content(prompt)
                    resultado = response.text.strip()

                    if resultado:
                        card_sucesso("Análise realizada com sucesso!")
                        st.subheader("Resultado da Análise")
                        st.markdown(resultado)

                        st.session_state.historico_alimentos.insert(0, {
                            "titulo": nome_alimento,
                            "conteudo": resultado
                        })
                        st.session_state.historico_alimentos = st.session_state.historico_alimentos[:5]
                    else:
                        card_falha("Falha ao realizar a análise. Tente novamente.")

                except Exception as e:
                    card_falha("Falha ao realizar a análise. Verifique o nome e tente novamente.")
                    st.error(f"Ocorreu um erro: {e}")


# 🔍 Histórico de análises
st.subheader("🔍 Histórico de Análises Anteriores")

if st.session_state.historico_alimentos:
    for item in st.session_state.historico_alimentos:
        with st.expander(f"🗂️ {item['titulo']}"):
            st.markdown(item['conteudo'])
else:
    st.info("Nenhuma análise realizada ainda.")
