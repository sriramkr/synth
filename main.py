from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.schema.output_parser import StrOutputParser
import random

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

llm = Ollama(
    model="mistral"
)

selected_properties = property_picker()

prompt = "Tell me a short story about a person with the following properties: " + str(selected_properties)

print(prompt)

s= ""
v = llm(prompt)
print(v)
