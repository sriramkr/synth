import os
import json
from openai import OpenAI
from fuzzywuzzy import process

client = OpenAI(api_key='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')


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

# # properties =  {"Their Favorite Country": " United Kingdom", "Their Occupation": " literary executor", "Their favorite Activity": " dancing", "Their Favorite Movies": " War"}
# # story = "There once was a person who lived in the United Kingdom and worked as a literary executor. Despite their demanding job, they always made time for their favorite activity - dancing. They loved to attend ballroom dance classes and would often hit the dance floor at social events. When it came to movies, this person had a soft spot for war films. They found them thrilling and inspiring, and would often watch them over and over again. Despite their busy schedule, they never missed an opportunity to catch a new war movie or revisit an old favorite."

# prompt_list = [(properties, story)]

debug = False

with open('stories') as json_data:
    prompts_json = json.load(json_data)
    json_data.close()

for i in range(len(prompts_json)):
    e = prompts_json[i]
    current_properties = e['properties']
    currrent_prompt = e['story']
    prompt = base_prompt + currrent_prompt
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=200,
    )
    if debug: print("Properties are: " + str(current_properties))
    if debug: print("Prompt is: " + currrent_prompt + ".\nOutput is")
    if debug: print(response.choices[0].text)
    
    try:
        json_object = json.loads(response.choices[0].text)
        inferred_values = set([str(v).strip().lower() for v in json_object.values()])
        orig_values = [v.strip().lower() for v in current_properties.values()]
        if debug: print(orig_values)
        if debug: print(inferred_values)
        score = 0.0
        for v in orig_values:
            match, msc = process.extractOne(v, inferred_values)
            if debug: print(v, match, msc)
            if msc>85:
                score +=1.0
        print("Round " + str(i) +". Final score is " + str(score/len(orig_values)))
    except:
        print("Round " + str(i) +". Final score is 0")
        continue

