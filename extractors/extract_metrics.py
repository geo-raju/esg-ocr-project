import re
import pandas as pd

def clean_text(text):
    text = text.replace("−", "-")  # Fix minus sign
    text = re.sub(r"\s+", " ", text)

    # OCR artifact corrections
    text = text.replace("Okg", "0kg") 
    text = text.replace("COze", "CO2e")
    text = text.replace("CO2ze", "CO2e")
    text = text.replace("COve", "CO2e")
    text = text.replace("CO₂e", "CO2e")
    text = text.replace("kg COze", "kg CO2e")
    text = text.replace("“", "\"").replace("”", "\"")

    return text

def extract_scope_emissions(text):
    scope_pattern = r"(Scope\s*[123])[^0-9a-zA-Z]{0,20}(zero|[\d,\.]+)\s*(kg|tons|t)?\s*(CO2[eE]?)?"
    results = []
    for match in re.finditer(scope_pattern, text, re.IGNORECASE):
        metric, value, unit1, unit2 = match.groups()
        unit = f"{unit1 or ''} {unit2 or ''}".strip()
        results.append({
            "metric": metric.strip(),
            "value": value.replace(",", ""),
            "unit": unit
        })
    return results

def extract_energy_usage(text):
    energy_pattern = r"(energy (?:usage|consumption)[^0-9]{0,20})([\d,\.]+)\s*(kWh|MWh|GWh)"
    results = []
    for match in re.finditer(energy_pattern, text, re.IGNORECASE):
        label, value, unit = match.groups()
        results.append({
            "metric": label.strip(),
            "value": value.replace(",", ""),
            "unit": unit
        })
    return results

def extract_water_usage(text):
    water_pattern = r"(water (?:usage|consumption)[^0-9]{0,20})([\d,\.]+)\s*(liters|gallons|m3|m³)"
    results = []
    for match in re.finditer(water_pattern, text, re.IGNORECASE):
        label, value, unit = match.groups()
        results.append({
            "metric": label.strip(),
            "value": value.replace(",", ""),
            "unit": unit
        })
    return results

def extract_general_emissions(text):
    general_pattern = r"(carbon footprint|total emissions|GHG reductions|GHG emissions)[^0-9]{0,20}([\d,\.]+)\s*(kg|tons|t)?\s*(CO2[eE]?)?"
    results = []
    for match in re.finditer(general_pattern, text, re.IGNORECASE):
        label, value, unit1, unit2 = match.groups()
        unit = f"{unit1 or ''} {unit2 or ''}".strip()
        results.append({
            "metric": label.strip(),
            "value": value.replace(",", ""),
            "unit": unit
        })
    return results

def extract_esg_metrics(text):
    text = clean_text(text)

    emissions = extract_scope_emissions(text)
    energy = extract_energy_usage(text)
    water = extract_water_usage(text)
    general = extract_general_emissions(text)

    all_metrics = emissions + energy + water + general

    df = pd.DataFrame(all_metrics)
    return df

def enrich_metrics_with_context(df, ner_matches):
    if df.empty or "metric" not in df.columns:
        return df

    context_tags = []
    for metric in df["metric"]:
        matched = False
        for ner in ner_matches:
            if ner["match"].lower() in metric.lower():
                context_tags.append(ner["match"])
                matched = True
                break
        if not matched:
            context_tags.append("UNKNOWN")
    df["ner_context"] = context_tags
    return df