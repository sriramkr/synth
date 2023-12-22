from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.schema.output_parser import StrOutputParser
import random
import json
import time
from faker import Faker
from estimate import is_identifiable_gpt4
fake = Faker()
from synth import *
from predict import *
from extract import *
from estimate import *
from anonymizers import *
import flags
import pprint

property_loader()
pp = pprint.PrettyPrinter(indent=4)
flags.debug=False

# print(anonymize_presidio(txt))

# ## GENERATE GEN STORIES
# for i in range(100):
#     try:
#         person = gen_person_generator()
#         person_str = stringify_person(person)

#         story = generate_story(person)
#         write_story(person, story,path='genstories/')
#         print("Round "+ str(i))
#     except:
#         continue

# ## GENERATE STORIES
# for i in range(100):
#     try:
#         person = person_generator()
#         person_str = stringify_person(person)

#         story = generate_story(person)
#         write_story(person, story,path='stories/')
#         print("Round "+ str(i))
#     except:
#         continue



## EXTRACT PROPERTIES
# flags.debug=False
# for i in range(100):
#     print("\n\n\n-----------------------------------------------------\n")
#     person, story = read_story(path='genstories/')
#     person_str = stringify_person(person)
#     print(person_str)
#     extracted_properties = extract_properties_neural(story)
#     if not extracted_properties:
#         print("Extraction failed")
#     else:
#         score = match_properties(person, extracted_properties)
#         print("\nOutput\n\nScore %f" % score)
#         pp.pprint(extracted_properties)
#     print("\n-----------------------------------------------------\n\n\n")


# num, person, story = read_story(num=279482, path='genstories/')
# person_str = jsonify_person(person)
# result = is_identifiable_llama2(person_str)
# print(result)

# ## ESTIMATE
# flags.debug=False
# errors=0
# count=0
# for i in range(30):
#     num, person, story = read_story(path='stories/')
#     person_str = jsonify_person(person)
#     result = is_identifiable_neural(person_str)
#     if not result:
#         errors +=1
#         print("Failed at " + num)
#     count +=1
#     print("Count = %d, Errors = %d" % (count, errors))
# print("Total = %d, Errors = %d" %(count,errors))

# for i in range(30):
#     num, person, story = read_story(path='genstories/')
#     person_str = jsonify_person(person)
#     result = is_identifiable_neural(person_str)
#     if result:
#         errors +=1
#         print("Failed at " + num)
#     count +=1
#     print("Count = %d, Errors = %d" % (count, errors))
# print("Total = %d, Errors = %d" %(count,errors))

def cleanup(extracted_properties):
    # pp.pprint(extracted_properties)
    cleaned = {}
    for k in extracted_properties:
        if extracted_properties[k]:
            if not (str(extracted_properties[k]).startswith("<") and str(extracted_properties[k]).endswith(">")):
                cleaned[k] = extracted_properties[k]
    return cleaned
        


def check(new_story, person):
    extracted_properties = extract_properties_neural(new_story)
    anon_score = 0.0
    cleaned_properties = cleanup(extracted_properties)
    cleaned_properties_str = json.dumps(cleaned_properties)
    if flags.debug:
        print("EXTRACTED & CLEANED PROPERTIES--------\n")
        print(cleaned_properties_str)
        print("\n--------\n")
    if not is_identifiable_gpt4_v2(cleaned_properties_str):
        anon_score = 1.0
    # match_score = match_properties(person, cleaned_properties)
    return anon_score

  

# ## EXTRACT + ESTIMATE
# flags.debug=False
# errors=0
# count=0
# extracted_properties_list = []
# for i in range(10):
#     num, person, story = read_story(path='genstories/')
#     extracted_properties = extract_properties_raw_neural(story)
#     if not extracted_properties:
#         print("Extraction failed")
#         continue
#     print(i)
#     extracted_properties_list.append(extracted_properties)


# for e in extracted_properties_list:
#     result = is_identifiable_llama2(extracted_properties)
#     if not result:
#         errors +=1
#         print("Failed at " + num)
#     count +=1
#     print("Count = %d, Errors = %d" % (count, errors))
# print("Total = %d, Errors = %d" %(count,errors))


################################################################
### START BACK HERE
## Main eval loop
for i in range(10):
    try:
        num, person, story = read_story(path='stories/')
        new_story = anonymize_gpt4(story)
        new_story_pres = anonymize_presidio(story)

        anon_score_orig = check(story, person)
        anon_score_pres = check(new_story_pres, person)
        anon_score_gpt4 = check(new_story, person)
        print(new_story_pres)
        print("Scores: Original: %d Presidio: %d GPT4: %d" % (anon_score_orig, anon_score_pres,anon_score_gpt4))
    except Exception as e:
        print(e)
        continue
################################################################


    # extracted_properties = extract_properties_neural(story)
    # if not extracted_properties:
    #     print("Extraction failed")
    # else:
    #     score = match_properties(person, extracted_properties)
    #     print("\nOutput\n\nScore %f" % score)
    #     pp.pprint(extracted_properties)
    # print("\n-----------------------------------------------------\n\n\n")
# p = """{"hobbies": ["music", "listening pop songs"], "favorite food": "ice cream", "passion": "physics"}"""
# p = p.replace("\\n", " ")
# print(is_identifiable_llama2(p))


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

# json_string = json.dumps(final_outputs,{"location": "city by the bay", "roots": "golden state", "name": "<person_name>", "occupation": "<work>", "hobbies": ["music", "listening pop songs"], "favorite food": "ice cream", "passion": "physics", "job offer": {"subject": "new job opportunity", "opportunity_type": "physics research"}}
#                         ensure_ascii=False)
# f = open('stories4', 'w')
# f.write(json_string)
# f.close()