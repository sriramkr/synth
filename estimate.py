import os
import json
import openai
from fuzzywuzzy import process
import random

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

property_loader()
generic_property_loader()

properties = property_picker()
prompt = "Reply Yes/No. Do more than one million people have these properties? " + str(properties)
print(prompt)
print(get_response(prompt))

generic_properties = generic_property_picker()
prompt2 = "Reply Yes/No. Do more than one million people have these properties? " + str(generic_properties)
print(prompt2)
print(get_response(prompt2))
