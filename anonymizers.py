from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig
import openai


def anonymize_presidio(txt):
    analyzer = AnalyzerEngine()
    engine = AnonymizerEngine()
    results = analyzer.analyze(text=txt, language='en')
    operators={
        "DEFAULT": OperatorConfig("redact"),
        }
    result = engine.anonymize(text=txt, analyzer_results=results, operators=operators)
    return result.text

base_prompt = """
Rewrite the following text to make it less identifiable, by using generic terms, adding ambiguity, and removing personal details: " I work as a nurse practitioner but I'd like to become an MD. However, I have two kids at home, so, I don't have time to read and take the exam."
I currently work in healthcare but aspire to further my career. Balancing family responsibilities leaves me with limited time to study and prepare for exams.

Rewrite the following text to make it less identifiable, by using generic terms, adding ambiguity, and removing identifying details: "I have tickets to see the Lakers game today, but I'm worried about the traffic near Staples Center. Do you want to catch the train?"
I have tickets for a big game today, but the area around the venue tends to have heavy traffic. Are you open to taking public transportation instead?
Rewrite the following text to make it less identifiable, by using generic terms, adding ambiguity, and removing identifying details: 
"""

def anonymize_gpt4(txt):
    txt2 = txt.replace("\n", " ").replace("\"", "\\\"")
    final_prompt = base_prompt + "\"" + txt2 + "\""
    try:
        response = openai.chat.completions.create(
            model="gpt-4", messages=[{"role": "user", "content": final_prompt}])
        resp = response.choices[0].message.content
        return resp
    except:
        print("failed at story " + txt)
        return ""
