from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.schema.output_parser import StrOutputParser
import random
import json
import time

properties = {}
def property_loader():
    f = open("properties.txt").readlines()
    for l in f:
        parts = l.split(":")
        values = parts[1].strip().split(",")
        properties[parts[0]] = values

def property_picker():    
    z = {}
    for i in range(5):
        k,v = random.choice(list(properties.items()))
        z[k] = random.choice(v)
    return z

property_loader()

final_outputs=[]
llm = Ollama(model="mistral")

for i in range(100):
    print(i)

    selected_properties = property_picker()

    prompt = "Tell me a story in five sentences about a person with the following properties: " + str(selected_properties)

    v = llm(prompt)

    output = {}
    output["properties"] = selected_properties
    output["story"] = v
    final_outputs.append(output)
    time.sleep(0.01)

json_string = json.dumps(final_outputs,
                        ensure_ascii=False)
f = open('stories4', 'w')
f.write(json_string)
f.close()