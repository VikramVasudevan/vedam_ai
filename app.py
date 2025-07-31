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
    prompt = f"""You are a knowledgeable assistant on the scripture *{scripture_title}*, well-versed in both **Sanskrit** and **English**.

You must answer the question using **only** the content from *{scripture_title}* provided in the context below.  
- Do **not** bring in information from **any other scripture or source** outside of *{scripture_title}*, even if the answer appears incomplete.  
- If the answer cannot be found in the provided context, clearly say:  
  **"I do not have enough information from the {scripture_title} to answer this."**

If the answer is not directly stated in the verses but is present in explanatory notes within the context, you may interpret — but **explicitly mention it is an interpretation**.

If the user query is not small talk, Use the following response format (in Markdown):

### 🧾 Answer  
- Present the explanation in clear, concise **English**.  
- If it is an interpretation, say so explicitly.

### 🔍 Chapter
 - Mention the chapter(s) from which the references were taken.

### 📜 Supporting Sanskrit Verse(s)  
- Quote **only the most relevant** Sanskrit verse(s) from the context.  
- Format each verse clearly, one per line.  
- **Avoid transliteration unless no Devanagari is available.**
- Do not provide english text in this section.

### 🔍 English Translation  
- Provide the **corresponding English meaning** for each Sanskrit verse shown.  
- Keep it readable and aligned with the verse above.

### Notes  
- Bullet any extra points or cross-references from the explanatory notes if relevant.  
- Do not include anything that is not supported or implied in the context.

**Question:**  
{question}

---

**Context:**  
{context}

---

Respond in **Markdown** format only. Ensure Sanskrit verses are always clearly shown and translated.
"""

    return [{"role": "system", "content": prompt}]


def chat(message, history, scripture):
    response = db.search(
        query=message, n_results=5, collection_name=scripture["collection_name"]
    )
    # logger.info("response = \n\n %s", response)
    response_str = json.dumps(response, indent=1, ensure_ascii=False)

    system_prompt = generate_prompt(
        scripture_title=scripture["title"], question=message, context=response_str
    )

    all_messages = system_prompt + history + [{"role": "user", "content": message}]

    ai_response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=all_messages,
        max_tokens=1200,
        temperature=0.3,
    )

    return [
        {"role": "assistant", "content": ai_response.choices[0].message.content.strip()}
    ]


def make_chat_interface(scripture):
    def wrapped_chat(message, history):
        return chat(message, history, scripture)

    with gr.Blocks() as tab_ui:
        gr.ChatInterface(
            chatbot=gr.Chatbot(show_copy_all_button=True, show_copy_button=True),
            type="messages",
            fn=wrapped_chat,
            title=scripture["title"],
            example_labels=scripture["example_labels"],
            examples=scripture["examples"],
            run_examples_on_click=True,
            cache_examples=False
        )
    return tab_ui


def render():
    interfaces = [
        make_chat_interface(scripture) for scripture in VedamConfig.scriptures
    ]
    tab_titles = [scripture["title"] for scripture in VedamConfig.scriptures]

    demo = gr.TabbedInterface(interface_list=interfaces, tab_names=tab_titles)
    demo.launch()


if __name__ == "__main__":
    init()
    render()
