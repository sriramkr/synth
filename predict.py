import os
import json
import openai
from fuzzywuzzy import process

openai.api_key = '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'

def detect_iid(current_properties):
    prompt = "Reply Yes or No. Do more than one million people in the world have the following properties? " + str(current_properties)
    response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": 'You are a helpful statistician'},
                    {"role": "user", "content": prompt}
            ])
    return response.choices[0].message.content

