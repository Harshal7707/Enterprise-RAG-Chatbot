import streamlit as st
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# For Key Import
def get_key(name):
    return st.secrets.get(name, "")

# Gemini llm importing
def get_llm():
    gemini_key = get_key("GEMINI_API_KEY")
    if gemini_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",  
                google_api_key=gemini_key,
                convert_system_message_to_human=True
            )
            st.session_state["llm_backend"] = "Gemini (Google Generative AI)"
            return llm
        except Exception as e:
            st.warning(f"Could not load Gemini: {e}")

    hf_token = get_key("HUGGINGFACEHUB_API_TOKEN")
    if hf_token:
        from langchain_community.llms import HuggingFaceHub
        llm = HuggingFaceHub(
            repo_id="HuggingFaceH4/zephyr-7b-beta",
            huggingfacehub_api_token=hf_token,
            model_kwargs={"temperature": 0.7, "max_new_tokens": 1024}
        )
        st.session_state["llm_backend"] = "HuggingFace (Zephyr-7B)"
        return llm

    st.error("No LLM API key found. Please add a Gemini or HuggingFace API key to your .streamlit/secrets.toml.")
    st.stop()

# Also for OpenAI
def get_embeddings():
    openai_key = get_key("OPENAI_API_KEY")
    if openai_key:
        try:
            from langchain_openai import OpenAIEmbeddings
            return OpenAIEmbeddings(api_key=openai_key)
        except Exception as e:
            st.warning(f"Could not load OpenAI embeddings, falling back to HF: {e}")

    # for Hugging Face
    from langchain_community.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings()

def split_knowledge(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_text(text)

def build_vectorstore(chunks, embeddings):
    return Chroma.from_texts(chunks, embedding=embeddings, persist_directory="chroma_db")

def build_chain(vectorstore, llm):
    from langchain.chains import RetrievalQA
    retriever = vectorstore.as_retriever()
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )

st.set_page_config(page_title="Enterprise RAG Chatbot", layout="wide")
st.title(":rocket: Enterprise RAG Chatbot (Gemini/HuggingFace Edition)")
st.caption("API keys are loaded securely from .streamlit/secrets.toml - never hardcode keys!")

st.write("**Paste your knowledge base or notes below. Nothing is uploaded or saved.**")

knowledge_base = st.text_area("Knowledge Base (paste notes, documents, or any reference text here)", height=230, key="kb_input")

if knowledge_base.strip():
    with st.spinner("Indexing your knowledge base..."):
        chunks = split_knowledge(knowledge_base)
        embeddings = get_embeddings()
        vectorstore = build_vectorstore(chunks, embeddings)
        llm = get_llm()
        qa_chain = build_chain(vectorstore, llm)

    if "history" not in st.session_state:
        st.session_state.history = []

    prompt = st.chat_input("Ask something about your knowledge base...")
    if prompt:
        st.session_state.history.append(("user", prompt))
        with st.spinner("AI is thinking..."):
            response = qa_chain({"query": prompt})["result"]
        st.session_state.history.append(("assistant", response))

    for speaker, message in st.session_state.history:
        st.chat_message(speaker).markdown(message)

    # Feedback UI
    if st.session_state.get("history", []):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍"):
                st.success("Thanks for your positive feedback!")
        with col2:
            if st.button("👎"):
                st.warning("We appreciate your feedback for improvement.")

else:
    st.info("Paste your knowledge base and start chatting!")


if "llm_backend" in st.session_state:
    st.caption(f"Model in use: `{st.session_state['llm_backend']}`")

# Gradio interface
import gradio as gr

def gradio_chat(question):
    if not knowledge_base.strip():
        return "No knowledge base provided."
    chunks = split_knowledge(knowledge_base)
    embeddings = get_embeddings()
    vectorstore = build_vectorstore(chunks, embeddings)
    llm = get_llm()
    qa_chain = build_chain(vectorstore, llm)
    resp = qa_chain({"query": question})["result"]
    return resp

if st.button("Launch Gradio Demo"):
    demo = gr.Interface(gradio_chat, "text", "text", title="RAG Chatbot Demo (Gemini/HF)")
    demo.launch(share=False)
