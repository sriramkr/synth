import os
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.schema.output_parser import StrOutputParser
import json
import openai
from fuzzywuzzy import process
from flags import *

openai.api_key = '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'


base_prompt = """List all the attributes about the author of this text as JSON string pairs: I have a blue lamborghini. It takes me 30 mins to go from my house in Malibu to my office in Santa Monica.
{
    "car": "Blue Lamborghini",
    "residence": "Malibu, California",
    "workplace": "Santa Monica, California",
    "commute_time": "30 minutes"
}

List all the attributes about the author of this text as JSON string pairs: My favorite dish is al pastor tacos. Let's go to Chupacabra and eat some?.
{
  "name": "Chupacabra",
  "type": "Restaurant",
  "cuisine": "Mexican",
  "favorite dish": "al pastor tacos",
  "invitation": "Let's go and eat some!"
}
List all the attributes about the author of this text as JSON string pairs:"""

base_prompt2 = """List all the attributes about the author of this text as JSON string pairs: I have a blue lamborghini. It takes me 30 mins to go from my house in Malibu to my office in Santa Monica.
{
    "car": "Blue Lamborghini",
    "residence": "Malibu, California",
    "workplace": "Santa Monica, California",
    "commute_time": "30 minutes"
}
List all the attributes about the author of this text as JSON string pairs:"""


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
    prompt = base_prompt2 + story
    v = llm(prompt)
    try:
        json_object = json.loads(v)
        return json_object
    except:
        return None
    return v


# with open('stories') as json_data:
#     prompts_json = json.load(json_data)
#     json_data.close()

# range_limit = 10
# offset = 30
# for i in range(range_limit):
#     e = prompts_json[(offset + i) % len(prompts_json)]
#     current_properties = e['properties']
#     currrent_prompt = e['story']
#     extracted_properties = extract_properties(current_properties)

#     if debug: print("Properties are: " + str(current_properties))
#     if debug: print("Prompt is: " + currrent_prompt + ".\nOutput is")
#     if debug: print(extracted_properties)
    
#     if not extracted_properties:
#         print("Round " + str(i) +". Final score is 0.")
#         continue
#     score = match_properties(current_properties, extracted_properties)
#     print("Round " + str(i) +". Final score is " + str(score))
#     if score<0.9:
#         print(current_properties)
#         print(extracted_properties)

