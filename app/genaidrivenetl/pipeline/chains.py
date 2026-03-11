from pathlib import Path

from langchain_core.output_parsers import StrOutputParser

from genaidrivenetl.prompts.loader import load_prompt


def build_chain(llm, prompt_file: Path):
    prompt = load_prompt(prompt_file)
    return prompt | llm | StrOutputParser()
