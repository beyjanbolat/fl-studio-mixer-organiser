
categories = {
    "Drums": ["Kick", "Kik", "Snare", "Snr", "Clap", "Hihat", "OpenHat", "Hat", "Rim", "Perc",
              "Shaker", "Tamb", "Conga", "Bongo", "Cowbell", "Crash",
              "Cymbal", "Ride", "Snap", "Fill", "Drum"],
    "Vocals": ["Vox", "Vocal", "Chant", "Chop", "Choir", "Adlib", "Ad-lib",
               "Acapella", "Voice"],
    "FX": ["FX", "SFX", "Riser", "Impact", "Sweep", "Uplifter",
           "Downlifter", "Whoosh", "Noise", "Reverse", "Texture",
           "Atmos", "Foley", "Siren", "Laser", "Glitch", "Transition"],
    "Bass": ["Bass", "808", "Reese"],
    "Synth": ["Synth", "Serum", "Kontakt", "Analog Lab", "Massive", "Sylenth",
              "Vital", "Diva", "Omnisphere", "Nexus", "Pigments", "Spire",
              "Pluck", "Pad", "Stab", "Lead", "Arp", "Chord", "Bell", "Mallet"],
}
def categorise(name):
    small = name.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            index = small.find(keyword.lower())
            if index != -1 and is_word_start(name, index):
                return (keyword, category)
    return (name, "unknown")


def is_word_start(name, i):
    if i == 0:
        return True
    previous = name[i - 1]
    if not previous.isalpha():
        return True
    if name[i].isupper() and previous.islower():
        return True
    return False