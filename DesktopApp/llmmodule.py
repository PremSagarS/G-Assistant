from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from langchain_community.llms import HuggingFacePipeline
from langchain_experimental.llms import JsonFormer
from dotenv import load_dotenv
import json
import os

load_dotenv()
debugging = os.environ["DEBUGGING"]

if not debugging == "TRUE":
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    hf_model = pipeline("text-generation", model="microsoft/phi-1_5", max_new_tokens = 70)
    hfpipeline = HuggingFacePipeline(pipeline=hf_model)


# Lines below are probably outdated now
# model = AutoModelForCausalLM.from_pretrained("CobraMamba/mamba-gpt-3b-v4")
# tokenizer = AutoTokenizer.from_pretrained("CobraMamba/mamba-gpt-3b-v4")

def summarizeThis(text):
    if debugging == "TRUE":
        return [
            {
                "summary_text": "The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world."
            }
        ]

    return (summarizer(text, max_length=100))

def jsonExtractor(emailText):
    if debugging == "TRUE":
        return {"eventname": "GenAIHackathon", "date": "19-04-2024", "location": "MG Auditorium"}

    PROMPT=f"""You must respond using JSON format.
Extract details of an event from given body of text

{JSON_SCHEMA}

EXAMPLES
--------
{TRAINING_EXAMPLE}

BEGIN! Extract event data
--------
Mail: {emailText}
Data:"""
    text = hfpipeline.invoke(PROMPT, stop=["Mail:","Data:", "Email:", "--------", "}"])
    text = str(text)
    
    # MODEL SPECIFIC TEXT PROCESSING
    text = text[:text.find('Email:')]
    
    # TEXT PROCESSING
    text = (text[text.rfind('{'): text.rfind('}') + 1])
    text = text.replace("\n","").replace("\r\n","")
    return (json.loads(text))


"""
========================================
                   TESTING
========================================
"""

ARTICLE = """ New York (CNN)When Liana Barrientos was 23 years old, she got married in Westchester County, New York.
A year later, she got married again in Westchester County, but to a different man and without divorcing her first husband.
Only 18 days after that marriage, she got hitched yet again. Then, Barrientos declared "I do" five more times, sometimes only within two weeks of each other.
In 2010, she married once more, this time in the Bronx. In an application for a marriage license, she stated it was her "first and only" marriage.
Barrientos, now 39, is facing two criminal counts of "offering a false instrument for filing in the first degree," referring to her false statements on the
2010 marriage license application, according to court documents.
Prosecutors said the marriages were part of an immigration scam.
On Friday, she pleaded not guilty at State Supreme Court in the Bronx, according to her attorney, Christopher Wright, who declined to comment further.
After leaving court, Barrientos was arrested and charged with theft of service and criminal trespass for allegedly sneaking into the New York subway through an emergency exit, said Detective
Annette Markowski, a police spokeswoman. In total, Barrientos has been married 10 times, with nine of her marriages occurring between 1999 and 2002.
All occurred either in Westchester County, Long Island, New Jersey or the Bronx. She is believed to still be married to four men, and at one time, she was married to eight men at once, prosecutors say.
Prosecutors said the immigration scam involved some of her husbands, who filed for permanent residence status shortly after the marriages.
Any divorces happened only after such filings were approved. It was unclear whether any of the men will be prosecuted.
The case was referred to the Bronx District Attorney\'s Office by Immigration and Customs Enforcement and the Department of Homeland Security\'s
Investigation Division. Seven of the men are from so-called "red-flagged" countries, including Egypt, Turkey, Georgia, Pakistan and Mali.
Her eighth husband, Rashid Rajput, was deported in 2006 to his native Pakistan after an investigation by the Joint Terrorism Task Force.
If convicted, Barrientos faces up to four years in prison.  Her next court appearance is scheduled for May 18.
"""

JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "eventname": {"type": "string"},
        "location": {"type": "string"},
        "date": {"type": "string"},
    }
}

TRAINING_EXAMPLE = """
Text: I would like to invite you to Workshop on iOS Development at MG Auditorium on 21st May 2024
Data: {
    "eventname": "Workshop on iOS Development",
    "date": "21-05-2024",
    "location":"MG Auditorium"
}
Text: Students please attend SAP Hackathon on 22nd MAY 2025 at Kasturba Gandhi auditorium
Data: {
    "eventname": "SAP Hackathon",
    "date": "22-05-2024",
    "location":"Kasturba Gandhi auditorium"
}
"""

EMAIL_EXAMPLE = """
event name: GenAIHackathon at MG Auditorium on 19th April 2024
"""

EXAMPLE_PROMPT = f"""You must respond using JSON format.
Extract details of an event from given body of text

{JSON_SCHEMA}

EXAMPLES
--------
{TRAINING_EXAMPLE}

BEGIN! Extract event data
--------
Mail: {EMAIL_EXAMPLE}
Data:"""

if __name__ == "__main__":
    print(jsonExtractor(EMAIL_EXAMPLE))
    print(summarizeThis(ARTICLE))