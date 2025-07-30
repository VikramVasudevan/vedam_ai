import json
import gradio as gr
from openai import OpenAI
from db import VedamDatabase
from ocr_loader import OcrLoader
from vedam_pdf_reader import VedamPdfReader
import logging
from dotenv import load_dotenv

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

db = VedamDatabase()


def init():
    logger.info("Hello from vedam-ai!")
    OcrLoader().load()
    # vedamPdfReader = VedamPdfReader()
    # vedamPdfReader.read()
    # response = db.search(query="front-line fighters", n_results=2)
    # logger.info("response = \n\n %s", response)
    logger.info("****initialized")


def generate_prompt(question, context):
    prompt = f"""You are a knowledgeable assistant on the Shukla Yajur Veda. You are an expert in English and Sanskrit.
Answer strictly using the context provided below. If the answer is not directly stated in the pasurams, but can be inferred from the explanatory notes, you may use that — clearly mentioning it’s an interpretation.
Use clear Markdown formatting with the following structure:
- Use `###` headings for different sections
- Use bullet points for lists
- Put Sanskrit and English texts in **separate lines**
- Keep all formatting readable in a chat interface

Here is the question:
**{question}**

Context:
{context}
------------------------------------------------------------------
\nProvide the answer in Markdown.\n"""
    return [{"role": "system", "content": prompt}]


def chat(message, history):
    response = db.search(query=message, n_results=2)
    logger.info("response = \n\n %s", response)
    response_str = json.dumps(response, indent=1, ensure_ascii=False)
    load_dotenv(override=True)
    llm = OpenAI()
    ai_response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=generate_prompt(question=message, context=response_str)
        + history
        + [{"role": "user", "content": message}],
        max_tokens=1200,
        temperature=0.3,
    )

    return [
        {"role": "assistant", "content": ai_response.choices[0].message.content.strip()}
    ]


def render():
    demo = gr.ChatInterface(
        fn=chat,
        type="messages",
        title="Vedam Chatbot",
        examples=[
            "where are the five elements mentioned",
            "नाभां पृथ्रिव्या:",
            "can you give me some sanskrit slokams that talk about fire",
            "which direction lies Brahma",
        ],
    )
    demo.launch()


if __name__ == "__main__":
    init()
    render()
