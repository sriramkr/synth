import os
import json
import openai
from fuzzywuzzy import process
import random
import flags
from langchain.llms import Ollama

openai.api_key='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'

properties = {}
def property_loader():
    f = open("properties.txt").readlines()
    for l in f:
        parts = l.split(":")
        values = parts[1].strip().split(",")
        properties[parts[0]] = values

generic_properties = {}
def generic_property_loader():
    f = open("generic_properties.txt").readlines()
    for l in f:
        parts = l.split(":")
        values = parts[1].strip().split(",")
        generic_properties[parts[0]] = values

def property_picker():    
    z = {}
    for i in range(5):
        k,v = random.choice(list(properties.items()))
        z[k] = random.choice(v)
    return z

def generic_property_picker():    
    z = {}
    for i in range(3):
        k,v = random.choice(list(generic_properties.items()))
        z[k] = random.choice(v)
    return z


def get_response(prompt):
    messages=[{"role": "user", "content": prompt}]
    response = openai.chat.completions.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}])

    # response = client.completions.create(
    #     model="gpt-3.5-turbo-instruct",
    #     prompt=prompt,
    #     max_tokens=200,
    # )   
    return response.choices[0].message.content

base_prompt = """Reply Yes/No. Do more than one million people have these properties? {'birth year': '1939', 'car': 'lexus', 'phone': '321-762-5790', 'favorite football team': 'Chicago Bears', 'favorite beverage': 'Coke', 'favorite subject': 'Politics'}
No

Reply Yes/No. Do more than one million people have these properties? {'favorite football team': 'Chicago Bears', 'favorite beverage': 'Coke', 'favorite subject': 'Politics'}
Yes


Reply Yes/No. Do more than one million people have these properties?  {'occupation': 'male prostitution', 'phone': '(450)920-1955', 'current city': 'San Francisco', 'favorite basketball team': 'Golden State Warriors', 'favorite music': 'Heavy Metal', 'favorite clothing': 'cotopaxi'}
No

Reply Yes/No. Do more than one million people have these properties?  {'favorite basketball team': 'Golden State Warriors', 'favorite music': 'Heavy Metal', 'favorite clothing': 'cotopaxi'}
Yes

Reply Yes/No. Do more than one million people have these properties? """

base_prompt2 = """Reply Yes/No. Do more than one million people have these properties? {'birth year': '1939', 'car': 'lexus', 'phone': '321-762-5790', 'favorite football team': 'Chicago Bears', 'favorite beverage': 'Coke', 'favorite subject': 'Politics'}
No

Reply Yes/No. Do more than one million people have these properties? {'favorite football team': 'Chicago Bears', 'favorite beverage': 'Coke', 'favorite subject': 'Politics'}
Yes

Reply Yes/No. Do more than one million people have these properties? """


def is_identifiable_gpt4(person_str):
    final_prompt = base_prompt + person_str
    try:
        response = openai.chat.completions.create(
            model="gpt-4", messages=[{"role": "user", "content": final_prompt}])
        resp = response.choices[0].message.content
        resp = resp.lower().strip()
        if resp == "yes":
            return False
        return True
    except:
        print("failed at person " + person_str)
        return True

def is_identifiable_mistral(person_str):
    llm = Ollama(model="mistral")
    final_prompt = base_prompt2 + person_str
    try:
        v = llm(final_prompt)
        resp = v.lower().strip()
        if resp == "yes":
            return False
        return True
    except Exception as e:
        if flags.debug: print("failed at person " + person_str)
        if flags.debug: print(e)
        return True
    
def is_identifiable_llama2(person_str):
    llm = Ollama(model="llama2")
    final_prompt = base_prompt2 + person_str
    attempts=0
    while attempts<3:
        try:
            v = llm(final_prompt)
            resp = v.lower().strip()
            if resp == "yes":
                return False
            return True
        except Exception as e:
            if flags.debug: print("failed at person " + person_str)
            if flags.debug: print(e)
            attempts += 1
    return True

def is_identifiable_neural(person_str):
    llm = Ollama(model="neural-chat")
    final_prompt = base_prompt2 + person_str
    attempts=0
    while attempts<3:
        try:
            v = llm(final_prompt)
            resp = v.lower().strip()
            if resp == "yes":
                return False
            return True
        except Exception as e:
            #print("failed at person " + person_str)
            #print(e)
            attempts += 1


# property_loader()
# generic_property_loader()

# properties = property_picker()
# prompt = "Reply Yes/No. Do more than one million people have these properties? " + str(properties)
# print(prompt)
# print(get_response(prompt))

# generic_properties = generic_property_picker()
# prompt2 = "Reply Yes/No. Do more than one million people have these properties? " + str(generic_properties)
# print(prompt2)
# print(get_response(prompt2))
base_prompt_new = """Reply Yes/No. Can this information be used to  identify a person? {'birth year': '1939', 'car': 'lexus', 'phone': '321-762-5790', 'favorite football team': 'Chicago Bears', 'favorite beverage': 'Coke', 'favorite subject': 'Politics'}
Yes

Reply Yes/No. Can this information be used to  identify a person? {'favorite football team': 'Chicago Bears', 'favorite beverage': 'Coke', 'favorite subject': 'Politics'}
No


Reply Yes/No. Can this information be used to  identify a person? {'occupation': 'male prostitution', 'phone': '(450)920-1955', 'current city': 'San Francisco', 'favorite basketball team': 'Golden State Warriors', 'favorite music': 'Heavy Metal', 'favorite clothing': 'cotopaxi'}
Yes

Reply Yes/No. Can this information be used to identify a person?  {'favorite basketball team': 'Golden State Warriors', 'favorite music': 'Heavy Metal', 'favorite clothing': 'cotopaxi'}
No

Reply Yes/No. Can this information be used to  identify a person? """

def is_identifiable_gpt4_v2(person_str):
    final_prompt = base_prompt_new + person_str
    try:
        response = openai.chat.completions.create(
            model="gpt-4", messages=[{"role": "user", "content": final_prompt}])
        resp = response.choices[0].message.content
        resp = resp.lower().strip()
        if resp == "no":
            return False
        if resp == "yes":
            return True
        return True
    except:
        print("failed at person " + person_str)
        return True
