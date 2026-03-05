from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate


def load_prompt(path: Path) -> ChatPromptTemplate:
    template = path.read_text()
    return ChatPromptTemplate.from_template(template)
