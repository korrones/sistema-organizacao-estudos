import streamlit as st
import fitz
from groq import Groq
import os  # NOVO

# Caminho dinâmico da imagem (NOVO)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(CURRENT_DIR, "logo.png")

# Configurar chave da Groq
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# função para extrair os arquivos     
def extract_files(uploader):
    text = ""
    for pdf in uploader:
        pdf_bytes = pdf.read()
        doc = fitz.Document(stream=pdf_bytes, filetype="pdf")  # forma alternativa
        for page in doc:
            text += page.get_text("text")
        doc.close()
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
    
# CRIAR A INTERFACE
def main():
    st.title("O nome do meu sistema inteligente")
    st.image(LOGO_PATH, width=200, caption="Sistema Inteligente")  # NOVO

    with st.sidebar:
        st.header("UPLoader Files")
        uploader = st.file_uploader("Adicione arquivos", type="pdf", accept_multiple_files=True)

    if uploader:
        text = extract_files(uploader)
        st.session_state["document_text"] = text  # ALTERADO

    user_input = st.text_input("Digite a sua pergunta")

    if user_input and "document_text" in st.session_state:  # NOVO
        response = chat_with_groq(user_input, st.session_state["document_text"])
        st.write("Resposta:", response)

if __name__ == "__main__":
    main()
