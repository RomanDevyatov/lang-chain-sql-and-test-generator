from langchain_openai import ChatOpenAI


def build_llm(
    model: str | None = None, api_key: str | None = None, api_base: str | None = None
) -> ChatOpenAI:
    if api_key is None:
        raise ValueError("api_key is required")
    if model is None:
        raise ValueError("model is required")
    if api_base is None:
        raise ValueError("api_base is required")

    return ChatOpenAI(
        model=model, temperature=0, openai_api_key=api_key, openai_api_base=api_base
    )
