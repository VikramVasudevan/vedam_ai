import json
import gradio as gr
from openai import OpenAI
from db import VedamDatabase
from ocr_loader import OcrLoader
from vedam_pdf_reader import VedamPdfReader
import logging
from dotenv import load_dotenv
from config import VedamConfig

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv(override=True)

db = VedamDatabase()
llm = OpenAI()

def init():
    logger.info("Hello from vedam-ai!")
    for scripture in VedamConfig.scriptures:
        OcrLoader(scripture_name=scripture["name"]).load()
    # vedamPdfReader = VedamPdfReader()
    # vedamPdfReader.read()
    # response = db.search(query="front-line fighters", n_results=2)
    # logger.info("response = \n\n %s", response)
    logger.info("****initialized")


def generate_prompt(scripture_title, question, context):
    prompt = f"""You are a knowledgeable assistant on the {scripture_title}. You are an expert in English and Sanskrit.
Answer strictly using the context provided below. If the answer is not directly stated in the verses, but can be inferred from the explanatory notes, you may use that — clearly mentioning it’s an interpretation.
Use clear Markdown formatting with the following structure:
- Use `###` headings for different sections
- Use bullet points for lists
- Put Sanskrit and English texts in **separate lines**
- Keep all formatting readable in a chat interface
- Give verbatim details from the context as much as possible
- Always give supporting verses in Sanskrit from the context

Here is the question:
**{question}**

Context:
{context}
------------------------------------------------------------------
Provide the answer in Markdown."""

    return [{"role": "system", "content": prompt}]


def chat(message, history, scripture):
    response = db.search(query=message, n_results=2, collection_name=scripture["collection_name"])
    logger.info("response = \n\n %s", response)
    response_str = json.dumps(response, indent=1, ensure_ascii=False)

    is_first_turn = not history or all(m["role"] != "user" for m in history)

    system_prompt = generate_prompt(
        scripture_title=scripture["title"],
        question=message,
        context=response_str
    )

    all_messages = system_prompt + history + [{"role" : "user", "content" : message}]

    ai_response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=all_messages,
        max_tokens=1200,
        temperature=0.3,
    )

    return [{"role": "assistant", "content": ai_response.choices[0].message.content.strip()}]



def make_chat_interface(scripture):
    def wrapped_chat(message, history):
        return chat(message, history, scripture)

    with gr.Blocks() as tab_ui:
        gr.ChatInterface(
            type="messages",
            fn=wrapped_chat,
            title=scripture["title"]
        )
    return tab_ui


def render():
    interfaces = [make_chat_interface(scripture) for scripture in VedamConfig.scriptures]
    tab_titles = [scripture["title"] for scripture in VedamConfig.scriptures]

    demo = gr.TabbedInterface(interface_list=interfaces, tab_names=tab_titles)
    demo.launch()


if __name__ == "__main__":
    init()
    render()
