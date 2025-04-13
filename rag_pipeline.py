# rag_pipeline.py

import os
import re
from typing import List, Dict

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI
from langchain import LLMChain

# ─── 1) Initialize your LLM ────────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model="gpt-3.5-turbo",
    temperature=0.3,
    max_tokens=500
)

# ─── 2) High‑level summary prompt ──────────────────────────────────────────────
high_level_prompt = PromptTemplate(
    template="""
Summarize the following text into three simple and clear main ideas.
Use easy vocabulary and short sentences. Each point should help someone who struggles with focus or reading.

{text}

MAIN IDEAS:
1.
2.
3.
""",
    input_variables=["text"],
)

# ─── 3) Expansion prompt ───────────────────────────────────────────────────────
expand_prompt = PromptTemplate(
    template="""
For each main idea below, write three short and clear supporting points.
Use simple words. Each point should explain or give an example.
Write in a way that helps people with ADHD or reading difficulties.

MAIN IDEAS:
{text}

DETAILED EXPLANATIONS:
Point 1:
1.1
1.2
1.3

Point 2:
2.1
2.2
2.3

Point 3:
3.1
3.2
3.3
""",
    input_variables=["text"],
)

# ─── 4) (Optional) Topic & keywords extraction ─────────────────────────────────
topic_prompt = PromptTemplate(
    template="""
In one or two words, give a concise topic label for this summary sentence:

{text}

Topic:
""",
    input_variables=["text"],
)

keyword_prompt = PromptTemplate(
    template="""
Extract up to five comma‑separated keywords from the following summary sentence.
Only output the keywords, nothing else.

Summary:
{text}

Keywords:
""",
    input_variables=["text"],
)

topic_chain = LLMChain(llm=llm, prompt=topic_prompt)
keyword_chain = LLMChain(llm=llm, prompt=keyword_prompt)

# ─── 5) Build your summarize chains ────────────────────────────────────────────
summary_chain = load_summarize_chain(
    llm=llm, chain_type="stuff", prompt=high_level_prompt
)
expand_chain = load_summarize_chain(
    llm=llm, chain_type="stuff", prompt=expand_prompt
)

# ─── 6) Helper to split text ───────────────────────────────────────────────────
def prepare_text_for_langchain(text: str) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )
    chunks = splitter.split_text(text)
    return [Document(page_content=chunk) for chunk in chunks]

# ─── 7) The real pipeline ─────────────────────────────────────────────────────
def generate_langchain_summary(text: str) -> Dict:
    # a) split & high‑level summary
    docs = prepare_text_for_langchain(text)
    high_raw = summary_chain.run(docs).strip()
    # extract lines beginning “1.”, “2.”, “3.”
    high_lines = [ln.strip() for ln in high_raw.split("\n") if re.match(r'^\d+\.', ln.strip())]
    # pad/truncate to exactly 3
    while len(high_lines) < 3:
        high_lines.append(f"{len(high_lines)+1}. Additional point.")
    high_lines = high_lines[:3]

    # b) expand each high‑level point
    expand_raw = expand_chain.run([Document(page_content="\n".join(high_lines))]).strip()
    expanded: List[List[str]] = []
    current: List[str] = []
    for ln in expand_raw.split("\n"):
        ln = ln.strip()
        if re.match(r'^\d+\.\d+', ln):
            current.append(ln)
        elif ln.lower().startswith("point") and current:
            expanded.append(current)
            current = []
    if current:
        expanded.append(current)
    # pad to 3×3
    while len(expanded) < 3:
        expanded.append([f"{len(expanded)+1}.1 Extra", f"{len(expanded)+1}.2 Extra", f"{len(expanded)+1}.3 Extra"])
    for i, section in enumerate(expanded):
        while len(section) < 3:
            section.append(f"{i+1}.{len(section)+1} Extra")

    # c) extract topic & keywords from first high‑level sentence
    seed = re.sub(r'^\d+\.\s*', '', high_lines[0])
    topic = topic_chain.run({"text": seed}).strip()
    raw_kw = keyword_chain.run({"text": seed})
    keywords = [kw.strip() for kw in raw_kw.split(",") if kw.strip()]

    return {
        "high_level": high_lines,
        "expanded": expanded,
        "topic": topic,
        "keywords": keywords
    }



# import re
# from typing import List, Dict
# # These imports are here if you later re-enable the real pipeline
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.schema import Document
# from langchain.prompts import PromptTemplate
# from langchain.chains.summarize import load_summarize_chain
# from langchain_openai import ChatOpenAI
# import os

# # ——— STUB: replace with real LLM code when ready ———
# # def generate_langchain_summary(text: str) -> Dict:
# #     """
# #     Demo stub that returns fixed JSON so your frontend
# #     can develop without hitting OpenAI.
# #     """
# #     return {
# #       "high_level": [
# #         "Demo point 1: key takeaway",
# #         "Demo point 2: another takeaway",
# #         "Demo point 3: final takeaway"
# #       ],
# #       "expanded": [
# #         ["1.1 detail", "1.2 detail", "1.3 detail"],
# #         ["2.1 detail", "2.2 detail", "2.3 detail"],
# #         ["3.1 detail", "3.2 detail", "3.3 detail"]
# #       ]
# #     }



# # rag_pipeline.py

# # rag_pipeline.py

# from typing import Dict

# def generate_langchain_summary(text: str) -> Dict:
#     """
#     Demo stub returning the exact JSON shape you checked into GitHub.
#     """
#     return {
#       "title": "AI-Powered Multisensory Summarization Tool",
#       "topic": "Cognitive-friendly learning",
#       "keywords": [
#         "AI summarization",
#         " visual representation",
#         " cognitive load",
#         " multisensory integration",
#         " gamified feedback"
#       ],
#       "high_level": [
#         "1. The tool provides a 3-line summary and visual representation of complex content, making it easier to understand for users with limited attention or working memory.",
#         "2. The AI adapts the summary and visuals based on the user's preferences and cognitive profile, enhancing comprehension and reducing cognitive load.",
#         "3. The tool incorporates gamified and sensory-rich feedback loops to reinforce understanding and motivation, making it accessible to a wide range of users, including those with cognitive disabilities."
#       ],
#       "expanded": [
#         [
#           "1.1 The tool provides a short and simple summary of complex information in just three lines.",
#           "1.2 The tool also uses visual representations, like pictures or diagrams, to help users understand the content better.",
#           "1.3 This is especially helpful for people who have difficulty paying attention or remembering information for long periods of time."
#         ],
#         [
#           "2.1 The AI in the tool can adapt the summary and visuals based on what the user prefers.",
#           "2.2 It can also adjust the content to match the user's cognitive profile, which means it can cater to their specific needs and abilities.",
#           "2.3 This customization helps users comprehend the information more easily and reduces the mental effort required to understand it."
#         ],
#         [
#           "3.1 The tool incorporates elements of games and interactive activities to make the learning experience more engaging and enjoyable.",
#           "3.2 It also includes sensory-rich feedback, like sounds or visuals, to provide immediate reinforcement and motivation.",
#           "3.3 These features make the tool accessible to a wide range of users, including those with cognitive disabilities, as it can accommodate different learning styles and preferences."
#         ]
#       ]
#     }


# # ——— Example real pipeline (commented out) ———
# #
# # llm = ChatOpenAI(
# #     openai_api_key=os.getenv("OPENAI_API_KEY"),
# #     model="gpt-3.5-turbo",
# #     temperature=0.3
# # )
# #
# # high_level_prompt = PromptTemplate(
# #     template="""Summarize the following text into three simple and clear main ideas.
# # Use easy vocabulary and short sentences. Each point should help someone who struggles with focus or reading.
# #
# # {text}
# #
# # MAIN IDEAS:
# # 1.
# # 2.
# # 3.
# # """,
# #     input_variables=["text"],
# # )
# #
# # expand_prompt = PromptTemplate(
# #     template="""For each main idea below, write three short and clear supporting points.
# # Use simple words. Each point should explain or give an example.
# # Write in a way that helps people with ADHD or reading difficulties.
# #
# # MAIN IDEAS:
# # {text}
# #
# # DETAILED EXPLANATIONS:
# # Point 1:
# # 1.1
# # 1.2
# # 1.3
# #
# # Point 2:
# # 2.1
# # 2.2
# # 2.3
# #
# # Point 3:
# # 3.1
# # 3.2
# # 3.3
# # """,
# #     input_variables=["text"],
# # )
# #
# # summary_chain = load_summarize_chain(
# #     llm=llm, chain_type="stuff", prompt=high_level_prompt
# # )
# # expand_chain = load_summarize_chain(
# #     llm=llm, chain_type="stuff", prompt=expand_prompt
# # )
# #
# # def generate_langchain_summary(text: str) -> Dict:
# #     docs = RecursiveCharacterTextSplitter(
# #         chunk_size=1000, chunk_overlap=100,
# #         separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
# #     ).split_text(text)
# #     high_raw = summary_chain.run([Document(page_content=c) for c in docs]).strip()
# #     # …etc…
# #     return {"high_level": high_lines, "expanded": expanded}