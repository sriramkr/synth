import flags
from estimate import *
from extract import *
from anonymizers import *


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


def evalloop():
    for i in range(1):
        num, person, story = read_story(path='stories/')
        if flags.debug: print(story)
        new_story = anonymize_gpt4(story)
        if flags.debug: print(new_story)
        new_story_pres = anonymize_presidio(story)
        if flags.debug: print(new_story_pres)
        anon_score_orig = check(story, person)
        anon_score_pres = check(new_story_pres, person)
        anon_score_gpt4 = check(new_story, person)
        print("Scores: Original: %d Presidio: %d GPT4: %d" % (anon_score_orig, anon_score_pres,anon_score_gpt4))
