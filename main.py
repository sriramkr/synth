from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.schema.output_parser import StrOutputParser
import random
import json
import time
from faker import Faker
fake = Faker()

def property_loader():
    f = open("properties.json")
    data = json.load(f)
    return data['properties']
properties = property_loader()

def special_property(name):
    if name == 'birth_year':
        return str(random.randint(1930,2005))    
    if name == 'phone':
        return fake.phone_number()
    if name == 'email':
        return fake.ascii_email()
    if name == 'address':
        return fake.address()

def property_picker(exclude, identifying):    
    while True:
        p = random.choice(list(properties))
        name = p['name']
        if name in exclude:
            continue
        if p['identifying'] != identifying:
            continue
        if p['special']:
            return (name, p['category'], p['description'],special_property(name))
        else:
            return (name, p['category'], p['description'],random.choice(p['values']))

def person_generator():    
    properties = {}
    i=0
    seen = set()
    for i in range(3):
        name, category, desc, val = property_picker(seen, True)
        properties[name] = (desc, val)
        seen.add(category)
    for i in range(3):
        name, category, desc, val = property_picker(seen, False)
        properties[name] = (desc, val)
        seen.add(category)
    return properties

def stringify_person(person):
    out = ""
    for p in person:
        desc, val = person[p]
        out += desc + ": " + val + "\n"
    return out

property_loader()
person = person_generator()
print(stringify_person(person))

llm = Ollama(model="mistral")
prompt = "Tell me a story in ten sentences about a person with the following properties: " + stringify_person(person)
v = llm(prompt)
print(v)

# final_outputs=[]
# llm = Ollama(model="mistral")

# for i in range(100):
#     print(i)

#     selected_properties = property_picker()

#     prompt = "Tell me a story in five sentences about a person with the following properties: " + str(selected_properties)

#     v = llm(prompt)

#     output = {}
#     output["properties"] = selected_properties
#     output["story"] = v
#     final_outputs.append(output)
#     time.sleep(0.01)

# json_string = json.dumps(final_outputs,
#                         ensure_ascii=False)
# f = open('stories4', 'w')
# f.write(json_string)
# f.close()