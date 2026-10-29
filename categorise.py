
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


# colour for each category as (red, green, blue)
# device_flauto.py turns these into FL colours with utils.RGBToColor
CATEGORY_COLOURS = {
    "Drums": (220, 50, 50),
    "Bass": (230, 140, 30),
    "Synth": (60, 130, 240),
    "Vocals": (170, 110, 230),
    "FX": (240, 220, 50),
    "unknown": (110, 110, 110),
}


def _first_free(taken, first_insert, last_insert):
    """Return the lowest insert that is not taken, or None if they all are."""
    for track in range(first_insert, last_insert + 1):
        if track not in taken:
            return track
    return None


def make_plan(names, targets, first_insert, last_insert, busy_tracks):
    """What each mixer track should be called. Does not touch FL.

    Args:
        names: channel names, one per channel.
        targets: the mixer track each channel gives. Anything below
            first_insert (Master is 0) counts as not routed yet.
        first_insert: number of the first insert track.
        last_insert: number of the last insert track.
        busy_tracks: inserts that already have plugins on them.

    Returns:
        A list with one dict per channel that gets a track:
        {"channel": i, "track": t, "name": clean name, "category": category}
        A channel is left out if it shares a track that is already named,
        or if there is no free insert left.
    """
    taken = set(busy_tracks)
    for track in targets:
        if track >= first_insert:
            taken.add(track)

    named_tracks = set()
    counts = {}
    plan = []
    for i, raw in enumerate(names):
        track = targets[i]
        if track < first_insert:
            track = _first_free(taken, first_insert, last_insert)
            if track is None:
                continue
            taken.add(track)
        elif track in named_tracks:
            continue
        named_tracks.add(track)

        clean, category = categorise(raw)
        counts[clean] = counts.get(clean, 0) + 1
        if counts[clean] > 1:
            clean = clean + " " + str(counts[clean])
        plan.append({"channel": i, "track": track, "name": clean, "category": category})
    return plan