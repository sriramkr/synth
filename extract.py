import os
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.schema.output_parser import StrOutputParser
import json
import openai
from fuzzywuzzy import process
from flags import *
from synth import *

openai.api_key = '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'


base_prompt = """List all the attributes about the author of the following text as JSON string pairs: I have a blue lamborghini. It takes me 30 mins to go from my house in Malibu to my office in Santa Monica.
{
    "car": "Blue Lamborghini",
    "residence": "Malibu, California",
    "workplace": "Santa Monica, California",
    "commute_time": "30 minutes"
}

List all the attributes about the author of the following text as JSON string pairs: My favorite dish is al pastor tacos. Let's go to Chupacabra and eat some?.
{
  "name": "Chupacabra",
  "type": "Restaurant",
  "cuisine": "Mexican",
  "favorite dish": "al pastor tacos",
  "invitation": "Let's go and eat some!"
}
List all the attributes about the author of the following text as JSON string pairs:"""

base_prompt2 = """List all the attributes about the author of this text as JSON string pairs: I have a blue lamborghini. It takes me 30 mins to go from my house in Malibu to my office in Santa Monica.
{
    "car": "Blue Lamborghini",
    "residence": "Malibu, California",
    "workplace": "Santa Monica, California",
    "commute_time": "30 minutes"
}
List all the attributes about the author of the following text as JSON string pairs:"""


def extract_properties_gpt4(story):
    prompt = base_prompt + story
    # response = client.completions.create(
    #     model="gpt-3.5-turbo-instruct",
    #     prompt=prompt,
    #     max_tokens=200,
    # )
    response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": 'Extract properties from the text into JSON string pairs.'},
                        {"role": "user", "content": prompt}
            ])
    outm =  response.choices[0].message.content
    try:
        json_object = json.loads(outm)
        return json_object
    except:
        return None
    
def extract_properties_mistral(story):
    llm = Ollama(model="mistral")
    prompt = base_prompt2 + story
    try:
        v = llm(prompt)
        json_object = json.loads(v)
        return json_object
    except:
        return None
    return v

def extract_properties_llama2(story):
    llm = Ollama(model="llama2")
    prompt = base_prompt + story
    v = llm(prompt)
    print("output is: \n\n")
    print(v)
    json_object = json.loads(v)
    return json_object

def extract_properties_raw_llama2(story):
    llm = Ollama(model="llama2")
    prompt = base_prompt + story
    attempts = 0
    while attempts<3:
        try:
            v = llm(prompt)
            return v
        except:
            attempts += 1
            continue
    return ""


def extract_properties_neural(story):
    llm = Ollama(model="neural-chat")
    prompt = base_prompt + story
    try:
        v = llm(prompt)
        json_object = json.loads(v)
        return json_object
    except:
        return None
    return v

def extract_properties_raw_neural(story):
    llm = Ollama(model="neural-chat")
    prompt = base_prompt + story
    attempts = 0
    while attempts<3:
        try:
            v = llm(prompt)
            return v
        except:
            attempts += 1
            continue
    return ""

def extract_test():
    for i in range(100):
        print("\n\n\n-----------------------------------------------------\n")
        person, story = read_story(path='genstories/')
        person_str = stringify_person(person)
        print(person_str)
        extracted_properties = extract_properties_neural(story)
        if not extracted_properties:
            print("Extraction failed")
        else:
            score = match_properties(person, extracted_properties)
            print("\nOutput\n\nScore %f" % score)
            pp.pprint(extracted_properties)
        print("\n-----------------------------------------------------\n\n\n")
