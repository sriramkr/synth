from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.schema.output_parser import StrOutputParser
import random
import json
import time
from faker import Faker
import flags
from fuzzywuzzy import process
import os, random
fake = Faker()

def property_loader():
    f = open("properties.json")
    data = json.load(f)
    proplist = data['properties']
    properties = {}
    for l in proplist:
        properties[l['name']] = l
    return properties
properties = property_loader()

def special_property(name):
    if name == 'birth_year':
        return str(random.randint(1930,2005))    
    if name == 'phone':
        return fake.phone_number()
    if name == 'email':
        return fake.ascii_email()
    if name == 'address':
        return fake.address().replace('\r', ', ').replace('\n', ', ')


def property_picker(exclude, identifying):    
    while True:
        p = random.choice(list(properties.values()))
        name = p['name']
        if name in exclude:
            continue
        if p['identifying'] != identifying:
            continue
        if p['special']:
            return (name, special_property(name))
        else:
            return (name, random.choice(p['values']))

def person_generator():    
    current_properties = {}
    i=0
    seen = set()
    for i in range(3):
        name, val = property_picker(seen, True)
        category = properties[name]['category']
        current_properties[name] = val
        seen.add(category)
    for i in range(3):
        name, val = property_picker(seen, False)
        current_properties[name] = val
        category = properties[name]['category']
        seen.add(category)
    return current_properties

def gen_person_generator():    
    current_properties = {}
    i=0
    seen = set()
    for i in range(2):
        name, val = property_picker(seen, False)
        current_properties[name] = val
        category = properties[name]['category']
        seen.add(category)
    return current_properties

def stringify_person(person):
    out = ""
    for p in person:
        val = person[p].replace('\r', ' ').replace('\n', ' ')
        desc = properties[p]['description']
        out += desc + ": " + val + "\n"
    return out

def jsonify_person(person):
    out = "{"
    first = True
    for p in person:
        val = person[p].replace('\r', ' ').replace('\n', ' ')
        desc = properties[p]['description']
        if first:
            out += "\"" + desc + "\": \"" + val + "\""
            first = False
        else:
            out += ", \"" + desc + "\": \"" + val + "\""
    return out + "}"


def match_properties(original, extracted):
    orig_values = [v.strip().lower() for v in original.values()]
    extracted_values = set([str(v).strip().lower() for v in extracted.values()])
    if flags.debug: print(orig_values)
    if flags.debug: print(extracted_values)
    score = 0.0
    for v in orig_values:
        found = False
        for v2 in extracted_values:
            if v2.find(v) != -1:
                if flags.debug: print(v, v2)
                found = True
            if v.find(v2) != -1:
                if flags.debug: print(v, v2)
                found = True
        match, msc = process.extractOne(v, extracted_values)
        if flags.debug: print(v, match, msc)
        if msc>85:
            found = True
        if found:
            if flags.debug: print("Found property "+ v)
            score +=1.0
        else:
            if flags.debug: print("Not found property " + v)
    final_score = score/len(orig_values)
    return final_score


def generate_story(person):
    llm = Ollama(model="mistral")
    prompt = "Tell me a story in ten sentences about a person with the following properties: " + stringify_person(person)
    v = llm(prompt)
    return v

def person_to_json(person):
    return json.dumps(person)

def person_from_json(blob):
    return json.loads(blob)


def write_story(person, story,path='stories/'):
    entry = {
    "story": story,
    "person": person_to_json(person)
    }
    num = random.randint(1,1000000)
    fn = path + str(num)
    print("writing to " + fn)
    with open(fn, 'w') as f:
        json.dump(entry, f)
    return num

def read_story(num=0,path='stories/'):
    if not num:
        num = random.choice(os.listdir(path))
    fn = path + str(num)
    with open(fn, 'r') as f:
        entry = json.load(f)
        return (num, person_from_json(entry['person']), entry['story'])

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