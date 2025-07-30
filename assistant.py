from typing import List, Dict, Any
import json
import re
import logging
from config import VedamConfig
from openai import OpenAI

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class VedamAssistant:
    def __init__(self):
        self.llm_client = OpenAI()
        self.model_name = "gpt-4o-mini"
        self.n_results = 10

    def _generate_prompt(self, context: str, question: str) -> str:
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
\nProvide the answer in Markdown.\n
"""
        return prompt

    def get_response(
        self,
        user_query: str,
        previous_results: list[dict] = None,
        is_followup: bool = False,
    ) -> tuple[str, list[dict]]:
        logger.info("Getting response ...")
        if is_followup:
            if previous_results:
                logging.info("previous_results available")
            else:
                logging.info("**NO** previous_results available")

        if is_followup and previous_results:
            combined_docs = previous_results
        else:
                # no azhwar names found in request
                # search by page number if available
                match = re.search(
                    r"\b(?:page)?\s*(\d{1,4})(?:st|nd|rd|th)?\b",
                    user_query.lower(),
                )
                if match:
                    requested_number = match.group(1)
                    logger.info(
                        "Executing verse search against database : for verse [%s]",
                        requested_number,
                    )
                    results = self.db.collection.get(
                        where={"page": int(requested_number)},
                        limit=self.n_results,
                        include=["documents", "metadatas"],
                    )
                    if results["documents"]:
                        documents = results["documents"]
                        metadatas = results["metadatas"]
                    else:
                        return (
                            f"Sorry, page {requested_number} was not found.",
                            previous_results,
                        )
                else:
                    logger.info("Executing query against database : [%s]", user_query)
                    results = self.db.search(text=user_query, n_results=self.n_results)
                    documents = results.get("documents", [[]])[0]
                    metadatas = results.get("metadatas", [[]])[0]

            if not documents or not metadatas:
                return "மன்னிக்கவும், பொருத்தமான பதில் இல்லை.", previous_results

            combined_docs = []
            for doc, meta in zip(documents, metadatas):
                combined = {"context": doc}
                if meta:
                    combined.update(meta)
                if "azhwar_name" not in combined or not combined["azhwar_name"]:
                    prabandham = combined.get("prabandham", "")
                    combined["azhwar_name"] = self.get_azhwar_name_for_prabandham(
                        prabandham
                    )
                combined_docs.append(combined)

        prompt = self._generate_prompt(combined_docs, user_query)
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_query},
        ]
        # logger.info("messages = %s", repr(messages))
        response = self.llm_client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=1200,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip(), combined_docs
