import spacy
from spacy.matcher import Matcher

# Load English language model
nlp = spacy.load("en_core_web_sm")

# Initialize matcher
matcher = Matcher(nlp.vocab)

# ESG-like patterns
patterns = [
    # carbon footprint
    [{"LOWER": "carbon"}, {"LOWER": "footprint"}],

    # scope emissions
    [{"LOWER": "scope"}, {"IS_DIGIT": True}, {"LOWER": "emissions"}],
    [{"LOWER": "scope"}, {"IS_DIGIT": True}],

    # GHG emissions / reductions
    [{"LOWER": "ghg"}, {"LOWER": {"IN": ["emissions", "reductions"]}}],

    # energy consumption
    [{"LOWER": "energy"}, {"LOWER": {"IN": ["use", "usage", "consumption"]}}],

    # water usage
    [{"LOWER": "water"}, {"LOWER": {"IN": ["use", "usage", "consumption"]}}],

    # global warming potential
    [{"LOWER": "global"}, {"LOWER": "warming"}, {"LOWER": "potential"}],
    [{"LOWER": "gwp"}],

    # climate change
    [{"LOWER": "climate"}, {"LOWER": "change"}]
]

# Add patterns to matcher
matcher.add("ESG_METRIC", patterns)

def run_spacy_ner(text):
    doc = nlp(text)
    matches = matcher(doc)

    results = []
    for _, start, end in matches:
        span = doc[start:end]
        results.append({
            "match": span.text,
            "start": span.start_char,
            "end": span.end_char
        })

    return results
