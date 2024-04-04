import flags
from estimate import *
from extract import *
from anonymizers import *


def cleanup(extracted_properties):
    cleaned = {}
    for k in extracted_properties:
        if extracted_properties[k]:
            if not (str(extracted_properties[k]).startswith("<") and str(extracted_properties[k]).endswith(">")):
                cleaned[k] = extracted_properties[k]
    return cleaned


def check(new_story, person):
    extracted_properties = extract_properties_gpt4_v3(new_story)
    anon_score = 0.0
    cleaned_properties = cleanup(extracted_properties)
    cleaned_properties_str = json.dumps(cleaned_properties)
    if not is_identifiable_gpt4_v3(cleaned_properties_str):
        anon_score = 1.0
    match_score = match_properties_v2(person, cleaned_properties)
    return cleaned_properties, anon_score, match_score


flags.debug = False


def evalloop():
    for i in range(1):
        num, person, story = read_story(path='stories/')
        new_story = anonymize_gpt4(story)
        new_story_pres = anonymize_presidio(story)
        cleaned_orig_properties, anon_score_orig, match_score_orig = check(
            story, person)
        _, anon_score_pres, match_score_pres = check(
            new_story_pres, cleaned_orig_properties)
        _, anon_score_gpt4, match_score_gpt4 = check(
            new_story, cleaned_orig_properties)
        print("Anon Scores: Original: %d Presidio: %d GPT4: %d" %
              (anon_score_orig, anon_score_pres, anon_score_gpt4))
        print("Match Scores: Original: %f Presidio: %f GPT4: %f" %
              (match_score_orig, match_score_pres, match_score_gpt4))
