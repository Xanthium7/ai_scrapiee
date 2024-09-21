from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.9,
    api_key=OPENAI_API_KEY,
)


template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)


def parse_with_ai(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description})
        print(f"Parsed the {i} of {len(dom_chunks)}")
        print(response.content)
        parsed_results.append(response.content)

    now_to_check = "\n".join(parsed_results)
    print("NOW TO CHECKKKKKK", now_to_check)
    new_response = chain.invoke(
        {"dom_content": now_to_check, "parse_description": parse_description})
    return new_response.content
