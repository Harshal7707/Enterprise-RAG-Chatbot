import os

def get_llm():
    # Try Gemini API first
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if api_key:
            llm = ChatGoogleGenerativeAI(model="gemini-pro")  # or "gemini-2.0-flash" or latest
            return llm
    except ImportError:
        pass

    # Fallback to HuggingFace if Gemini isn't available or free
    from langchain_community.llms import HuggingFaceHub
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    llm = HuggingFaceHub(
        repo_id="HuggingFaceH4/zephyr-7b-beta", # Use a lightweight, open model (e.g., zephyr-7b),
        model_kwargs={"temperature": 0.7, "max_new_tokens": 1024},
    )
    return llm
