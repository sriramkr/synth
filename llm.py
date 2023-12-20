from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.schema.output_parser import StrOutputParser
import random
import json
import time
from faker import Faker
from flags import *
from fuzzywuzzy import process
import openai

fake = Faker()


def run(llm='mistral', prompt=''):
    if llm == 'mistral':
        return run_mistral(prompt)
    if llm == 'gpt-3.5':
        return run_gpt_35(prompt)
    if llm == 'gpt-4':
        return run_gpt_4(prompt)
    if llm == 'llama2':
        return run_llama2([prompt])
    

def run_mistral(prompt):
    llm = Ollama(model="mistral")
    return llm(prompt)

def run_llama2(prompt):
    llm = Ollama(model="llama2")
    return llm(prompt)

def run_gpt_4(prompt):
    response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": 'Extract properties from the text into JSON string pairs.'},
                        {"role": "user", "content": prompt}
            ])
    return response.choices[0].message.content

def run_gpt_35(prompt):
    return ""
    # response = client.completions.create(
    #     model="gpt-3.5-turbo-instruct",
    #     prompt=prompt,
    #     max_tokens=200,
    # )
