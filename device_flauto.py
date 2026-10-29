# name=FL Mixer Organiser
# url= https://github.com/beyjanbolat/fl-mixer-organiser

import channels
import mixer
import plugins
import utils

from categorise import CATEGORY_COLOURS, make_plan

GET_FIRST_INSERT = 1  # getTrackInfo(1) gives the first insert
GET_LAST_INSERT = 2   # getTrackInfo(2) gives the last insert
SLOTS_PER_TRACK = 10  # effect slots on each mixer track
AUTOMATION_CLIP = 5   # automation clips dont produce soound, so skip

# play note 36 on a MIDI keyboard to organise, 38 to undo
# FL only sends notes to a script that is set on a MIDI input
ORGANISE_NOTE = 36
UNDO_NOTE = 38

_snapshot = None


def _read_channels():
    """Read every channel that makes sound: its index, name and mixer track."""
    ids, names, targets = [], [], []
    for i in range(channels.channelCount(True)):
        if channels.getChannelType(i, True) == AUTOMATION_CLIP:
            continue
        ids.append(i)
        names.append(channels.getChannelName(i, True))
        targets.append(channels.getTargetFxTrack(i, True))
    return ids, names, targets


def _busy_tracks(first, last):
    """Find the inserts that already have a plugin on them."""
    busy = set()
    for track in range(first, last + 1):
        for slot in range(SLOTS_PER_TRACK):
            if plugins.isValid(track, slot):
                busy.add(track)
                break
    return busy


def organise():
    """Name, colour and route the mixer track of every channel."""
    global _snapshot
    first = mixer.getTrackInfo(GET_FIRST_INSERT)
    last = mixer.getTrackInfo(GET_LAST_INSERT)
    ids, names, targets = _read_channels()
    plan = make_plan(names, targets, first, last, _busy_tracks(first, last))

    # save the old state first so undo() can put it back
    _snapshot = {"channels": {}, "tracks": {}}
    for item in plan:
        _snapshot["channels"][ids[item["channel"]]] = targets[item["channel"]]
        track = item["track"]
        _snapshot["tracks"][track] = (mixer.getTrackName(track), mixer.getTrackColor(track))

    for item in plan:
        channels.setTargetFxTrack(ids[item["channel"]], item["track"], True)
        mixer.setTrackName(item["track"], item["name"])
        red, green, blue = CATEGORY_COLOURS[item["category"]]
        mixer.setTrackColor(item["track"], utils.RGBToColor(red, green, blue))
        print("track", item["track"], "->", item["name"], "(" + item["category"] + ")")
    print("FL Mixer Organiser: done,", len(plan), "tracks")


def undo():
    """Put back what organise() changed."""
    if _snapshot is None:
        print("FL Mixer Organiser: nothing to undo")
        return
    for channel, track in _snapshot["channels"].items():
        channels.setTargetFxTrack(channel, track, True)
    for track, (name, colour) in _snapshot["tracks"].items():
        mixer.setTrackName(track, name)
        mixer.setTrackColor(track, colour & 0xFFFFFF)
    print("FL Mixer Organiser: undone")


def OnInit():
    print("FL Mixer Organiser ready. Note", ORGANISE_NOTE, "= organise, note", UNDO_NOTE, "= undo")


def OnMidiMsg(event):
    if (event.status & 0xF0) == 0x90 and event.data2 > 0:
        if event.data1 == ORGANISE_NOTE:
            organise()
            event.handled = True
        elif event.data1 == UNDO_NOTE:
            undo()
            event.handled = True
