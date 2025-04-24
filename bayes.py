import streamlit as st
import fitz
from groq import Groq
import os

# Caminho dinâmico da imagem
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(CURRENT_DIR, "logo.png")

# Caminho do PDF a ser carregado automaticamente
PDF_PATH = os.path.join(CURRENT_DIR, "Planejamento de Estudos - IA.pdf")  # <- Substitua pelo nome do seu PDF

# Configurar chave da Groq
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Função para extrair texto de um PDF
def extract_text_from_pdf(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text("text")
    return text

# Motor de inferência para o sistema inteligente
def chat_with_groq(prompt, context):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Você é um assistente que responde com base em documentos fornecidos."},
            {"role": "user", "content": f"{context}\n\nPergunta: {prompt}"}
        ]
    )
    return response.choices[0].message.content    

# Interface
def main():
    st.title("Sistema de Organização de Estudos")
    st.image(LOGO_PATH, width=300, caption="Sistema Inteligente")

    # Carregar automaticamente o texto do PDF
    if "document_text" not in st.session_state:
        try:
            st.session_state["document_text"] = extract_text_from_pdf(PDF_PATH)
            st.success("PDF carregado automaticamente.")
        except Exception as e:
            st.error(f"Erro ao carregar o PDF: {e}")
            return

    # Campo para digitar a pergunta
    user_input = st.text_input("Digite a sua pergunta")

    if user_input and "document_text" in st.session_state:
        response = chat_with_groq(user_input, st.session_state["document_text"])
        st.write("Resposta:", response)

if __name__ == "__main__":
    main()
