import json
import gradio as gr
from db import VedamDatabase
from vedam_pdf_reader import VedamPdfReader
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

db = VedamDatabase()


def init():
    logger.info("Hello from vedam-ai!")
    vedamPdfReader = VedamPdfReader()
    vedamPdfReader.read()
    # response = db.search(query="front-line fighters", n_results=2)
    # logger.info("response = \n\n %s", response)
    logger.info("****initialized")


def chat(message, history):
    response = db.search(query=message, n_results=2)
    logger.info("response = \n\n %s", response)
    response_str = json.dumps(response, indent=1, ensure_ascii=False)
    return [{"role": "assistant", "content": response_str}]


def render():
    demo = gr.ChatInterface(
        fn=chat,
        type="messages",
        title="Vedam Chatbot",
    )
    demo.launch()


if __name__ == "__main__":
    init()
    render()
