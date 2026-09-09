"""
Advisory rules engine.

Takes a farmer's profile (crop + growth stage) and today's conditions
(rain probability, temperature, wind, mandi price change) and returns
the specific, bilingual advisory message(s) that apply — plus a plain
english/hindi "why" explanation for each, so the reasoning is never a
black box.

This is a deliberately simple, transparent rules engine rather than a
model — for a farmer-facing safety message ("hold off spraying"), a
rule you can point to and justify beats a prediction you can't.
"""

import os

import requests

CROPS = {
    "soybean": {"en": "Soybean", "hi": "सोयाबीन", "te": "సోయాబీన్", "mandi": "Berasia Mandi"},
    "wheat":   {"en": "Wheat",   "hi": "गेहूं",   "te": "గోధుమ", "mandi": "Bhopal Mandi"},
    "cotton":  {"en": "Cotton",  "hi": "कपास",    "te": "పత్తి", "mandi": "Ichhawar Mandi"},
    "onion":   {"en": "Onion",   "hi": "प्याज",    "te": "ఉల్లిపాయ", "mandi": "Berasia Mandi"},
    "rice":    {"en": "Rice",    "hi": "धान",      "te": "వరి", "mandi": "Bhopal Mandi"},
    "maize":   {"en": "Maize",   "hi": "मक्का",    "te": "మొక్కజొన్న", "mandi": "Sehore Mandi"},
    "tomato":  {"en": "Tomato",  "hi": "टमाटर",    "te": "టమాటా", "mandi": "Berasia Mandi"},
}

SPRAY_SENSITIVE_STAGES = {"Vegetative", "Flowering"}


def evaluate_rules(farmer: dict, conditions: dict) -> list[dict]:
    """
    farmer: {"crop": "wheat", "stage": "Pre-harvest", ...}
    conditions: {"rain": 0-100, "temp": celsius, "wind": km/h, "price": pct change}
    Returns a list of {"en":..., "hi":..., "why":...} dicts, highest-priority first.
    Never returns an empty list — falls back to a baseline "all normal" message.
    """
    crop = CROPS.get(farmer["crop"], CROPS["wheat"])
    rain, temp, wind, price = conditions["rain"], conditions["temp"], conditions["wind"], conditions["price"]
    stage = farmer["stage"]
    fired = []

    if rain >= 60 and stage in SPRAY_SENSITIVE_STAGES:
        fired.append({
            "en": f"Hold spraying on your {crop['en']} - rain likely in 24-48h, could wash it off before it works. -KrishiSetu",
            "hi": f"अपनी {crop['hi']} पर छिड़काव रोकें - 24-48 घंटों में बारिश संभव है। -कृषि सेतु",
            "te": f"మీ {crop['te']}పై పిచికారీ చేయకండి - రాబోయే 24-48 గంటల్లో వర్షం పడే అవకాశం ఉంది. -కృషి సేతు",
            "why": f"Rain >= 60% AND stage = {stage} (spray-sensitive window)",
        })
    if rain >= 60 and stage == "Pre-harvest":
        fired.append({
            "en": f"Rain expected before harvest. Consider early harvest or covered storage for {crop['en']}. -KrishiSetu",
            "hi": f"कटाई से पहले बारिश संभव है। {crop['hi']} की जल्दी कटाई करें या ढका भंडारण करें। -कृषि सेतु",
            "te": f"కోతకు ముందు వర్షం పడే అవకాశం ఉంది. {crop['te']}ను ముందుగా కోయండి లేదా కప్పి నిల్వ చేయండి. -కృషి సేతు",
            "why": "Rain >= 60% AND stage = Pre-harvest",
        })
    if temp >= 40:
        fired.append({
            "en": f"High heat ({temp}C) ahead. Irrigate {crop['en']} early morning or evening. -KrishiSetu",
            "hi": f"अधिक गर्मी ({temp}°C) की संभावना है। सुबह या शाम सिंचाई करें। -कृषि सेतु",
            "te": f"అధిక వేడి ({temp}°C) ఉండవచ్చు. {crop['te']}కు ఉదయం లేదా సాయంత్రం నీరు పెట్టండి. -కృషి సేతు",
            "why": "Max temperature >= 40C",
        })
    if wind >= 40:
        fired.append({
            "en": f"Strong winds ({wind}km/h) ahead. Stake plants, avoid spraying today. -KrishiSetu",
            "hi": f"तेज़ हवा ({wind} किमी/घं) संभव है। छिड़काव न करें, पौधों को सहारा दें। -कृषि सेतु",
            "te": f"బలమైన గాలులు ({wind} కి.మీ/గం) వీచవచ్చు. మొక్కలకు ఆసరా ఇవ్వండి, ఈరోజు పిచికారీ చేయకండి. -కృషి సేతు",
            "why": "Wind speed >= 40 km/h",
        })
    if price >= 8:
        fired.append({
            "en": f"{crop['en']} price at {crop['mandi']} up {price}% this week. Good time to sell if ready. -KrishiSetu",
            "hi": f"{crop['mandi']} में {crop['hi']} का भाव इस सप्ताह {price}% ऊपर है। -कृषि सेतु",
            "te": f"{crop['mandi']}లో {crop['te']} ధర ఈ వారం {price}% పెరిగింది. పంట సిద్ధంగా ఉంటే అమ్మడానికి మంచి సమయం. -కృషి సేతు",
            "why": "Mandi price change >= +8%",
        })
    if price <= -8:
        fired.append({
            "en": f"{crop['en']} price at {crop['mandi']} down {abs(price)}% this week. Hold if you can store. -KrishiSetu",
            "hi": f"{crop['mandi']} में {crop['hi']} का भाव इस सप्ताह {abs(price)}% नीचे है। -कृषि सेतु",
            "te": f"{crop['mandi']}లో {crop['te']} ధర ఈ వారం {abs(price)}% తగ్గింది. నిల్వ చేయగలిగితే వేచి ఉండండి. -కృషి సేతు",
            "why": "Mandi price change <= -8%",
        })
    if not fired:
        fired.append({
            "en": f"No unusual conditions for your {crop['en']} today. -KrishiSetu",
            "hi": f"आज {crop['hi']} के लिए कोई असामान्य स्थिति नहीं। -कृषि सेतु",
            "te": f"ఈరోజు మీ {crop['te']}కు అసాధారణ పరిస్థితులు లేవు. -కృషి సేతు",
            "why": "No threshold crossed - baseline message",
        })
    return fired


def build_personalized_message(farmer: dict, weather: dict, price: dict, advisory: dict) -> str:
    """Compose one actionable message from today's farmer-specific signals."""
    crop = CROPS.get(farmer["crop"], CROPS["wheat"])
    name = farmer["name"].split()[0]
    location = farmer.get("village") or "your farm"
    language = farmer.get("language", "en")
    crop_name = crop.get(language, crop["en"])
    lines = [
        f"Namaste {name}, Krishi Setu update for {location}:",
        f"{crop_name}: {advisory[language].replace(' -KrishiSetu', '').replace(' -कृषि सेतु', '').replace(' -కృషి సేతు', '')}",
        f"Weather: {weather['temp']}C, rain chance {weather['rain']}%, wind {weather['wind']} km/h.",
        f"Mandi: {price['market']} {price['price']} per quintal ({price['change']:+d}% vs yesterday).",
    ]
    if language == "hi":
        lines[0] = f"नमस्ते {name}, {location} के लिए कृषि सेतु संदेश:"
        lines[2] = f"मौसम: {weather['temp']}°C, बारिश की संभावना {weather['rain']}%, हवा {weather['wind']} किमी/घं।"
        lines[3] = f"मंडी: {price['market']} में भाव {price['price']} रुपये/क्विंटल ({price['change']:+d}%)।"
    elif language == "te":
        lines[0] = f"నమస్కారం {name}, {location} కోసం కృషి సేతు సందేశం:"
        lines[1] = f"{crop['te']}: {advisory['te'].replace(' -కృషి సేతు', '')}"
        lines[2] = f"వాతావరణం: {weather['temp']}°C, వర్షం అవకాశం {weather['rain']}%, గాలి {weather['wind']} కి.మీ/గం."
        lines[3] = f"మార్కెట్: {price['market']}లో ధర క్వింటాల్‌కు {price['price']} ({price['change']:+d}%)."
    return "\n".join(lines)


def generate_fresh_message(farmer: dict, weather: dict, price: dict, advisory: dict) -> str | None:
    """Ask an optional AI provider to freshly phrase a grounded advisory."""
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    local_provider = "localhost" in base_url or "127.0.0.1" in base_url
    if not api_key and not local_provider:
        return None
    language = farmer.get("language", "en")
    language_name = {"en": "English", "hi": "Hindi", "te": "Telugu"}.get(language, "English")
    prompt = (
        f"Write a fresh, concise farmer advisory in {language_name} for {farmer['name']} in {farmer['village']}. "
        f"Crop: {farmer['crop']}; growth stage: {farmer['stage']}. "
        f"Weather: {weather['temp']}C, rain chance {weather['rain']}%, wind {weather['wind']} km/h. "
        f"Market: {price['market']}, {price['price']} per quintal, change {price['change']}%. "
        f"Grounded rule advisory: {advisory[language]}. "
        "Use only these facts, give one clear action, and do not invent schemes, dates, prices, or contacts."
    )
    try:
        response = requests.post(
            base_url + "/chat/completions",
            headers={"Content-Type": "application/json", **({"Authorization": f"Bearer {api_key}"} if api_key else {})},
            json={
                "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                "temperature": 0.8,
                "messages": [
                    {"role": "system", "content": "You write safe agricultural advisories grounded only in supplied facts."},
                    {"role": "user", "content": prompt},
                ],
            },
            timeout=20,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()
        return content or None
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError):
        return None
