from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.schema.output_parser import StrOutputParser
import random
import json
import time
from faker import Faker
fake = Faker()
from synth import *
from predict import *
from extract import *
import flags
import pprint

property_loader()

# for i in range(100):
#     try:
#         person = person_generator()
#         person_str = stringify_person(person)

#         story = generate_story(person)
#         write_story(person, story)
#         print("Round "+ str(i))
#     except:
#         continue
pp = pprint.PrettyPrinter(indent=4)

flags.debug=False
for i in range(100):
    print("\n\n\n-----------------------------------------------------\n")
    person, story = read_story()
    person_str = stringify_person(person)
    print(person_str)
    extracted_properties = extract_properties_mistral(story)
    if not extracted_properties:
        print("Extraction failed")
    else:
        score = match_properties(person, extracted_properties)
        print("\nOutput\n\nScore %f" % score)
        pp.pprint(extracted_properties)
    print("\n-----------------------------------------------------\n\n\n")
            




# llm = Ollama(model="mistral")
# prompt = "Tell me a story in ten sentences about a person with the following properties: " + stringify_person(person)
# v = llm(prompt)
# print(v)

#print(detect_iid(stringify_person(person)))

# output, failure = anonymizer(v)

# if failure:
#     print("Failed")
# else:
    
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