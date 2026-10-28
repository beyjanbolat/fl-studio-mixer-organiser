

categories = {
    "Drums": ["Kick", "Hat", "Snare", "Rim", "Ride", "Cymbal"],
    "Synth": ["Kontakt", "Serum", "Analog Lab"],


}
def categorise(name):
    small = name.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in small:
                return (keyword, category)
    return (name, "unknown")