from transformers import pipeline

# Load a named entity recognition pipeline
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

def run_transformer_ner(text):
    results = ner_pipeline(text)
    structured_entities = []

    for ent in results:
        structured_entities.append({
            "entity": ent["entity_group"],
            "word": ent["word"],
            "score": round(ent["score"], 3),
            "start": ent["start"],
            "end": ent["end"]
        })

    return structured_entities
