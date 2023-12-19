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

def special_property(p):
    if p['name'] == 'birth_year':
        return random.randint(1930,2005)    
    if p['name'] == 'phone':
        return fake.phone_number()
    if p['name'] == 'email':
        return fake.ascii_email()

def property_picker():    
    picked_properties = {}
    i=0
    seen = set()
    while i<5:
        p = random.choice(list(properties))
        name = p['name']
        if name in seen:
            continue
        val = ""
        if p['special']:
           val = special_property(p)
        else:
            val = random.choice(p['values'])
        picked_properties[name] = p['description'] + ": " + val
        seen.add(name)
        i+=1
    return picked_properties

property_loader()
print(property_picker())

# property_loader()

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