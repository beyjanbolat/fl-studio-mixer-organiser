# name=FL Mixer Organiser
# url= https://github.com/beyjanbolat/fl-mixer-organiser

import channels
import mixer
import plugins
import utils

from categorise import CATEGORY_COLOURS, make_plan

GET_FIRST_INSERT = 1  # getTrackInfo(1) gives the first insert
SLOTS_PER_TRACK = 10  # effect slots on each mixer track
AUTOMATION_CLIP = 5   # automation clips don't produce sound, so skip

# type preview(), apply() or undo() in View > Script output > Interpreter
_plan = None      # what preview() worked out
_seen = None      # the channels as preview() saw them
_snapshot = None  # old state saved by apply(), so undo() can put it back


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


def preview():
    """Show what apply() would do. Changes nothing in the project."""
    global _plan, _seen
    first = mixer.getTrackInfo(GET_FIRST_INSERT)
    last = mixer.trackCount() - 2  # minus master and the current track
    _seen = _read_channels()
    _, names, targets = _seen
    _plan = make_plan(names, targets, first, last, _busy_tracks(first, last))
    moved = 0
    for item in _plan:
        channel = item["channel"]
        if targets[channel] < first:
            moved += 1
        print(names[channel], "-->", item["name"], "(" + item["category"] + ")", "[Insert " + str(item["track"]) + "]")
    if moved:
        print(moved, "channels are not routed yet and will be sent to the insert shown.")
    if len(_plan) < len(names):
        print(len(names) - len(_plan), "channels left out: no free insert or they share a track")
    print("FL Mixer Organiser: preview of", len(_plan), "tracks, nothing changed yet.")
    print("Type apply() to do it.")


def apply():
    """Do what preview() showed. Saves the old state first."""
    global _plan, _snapshot
    if _snapshot is not None:
        print("FL Mixer Organiser: already applied. Type undo() first.")
        return
    if _plan is None:
        print("FL Mixer Organiser: type preview() first.")
        return
    if _read_channels() != _seen:
        print("FL Mixer Organiser: the project changed since the preview. Type preview() again.")
        return
    ids, names, targets = _seen

    # save the old state first so undo() can put it back
    _snapshot = {"channels": {}, "tracks": {}}
    for item in _plan:
        _snapshot["channels"][ids[item["channel"]]] = targets[item["channel"]]
        track = item["track"]
        _snapshot["tracks"][track] = (mixer.getTrackName(track), mixer.getTrackColor(track))

    for item in _plan:
        channels.setTargetFxTrack(ids[item["channel"]], item["track"], True)
        mixer.setTrackName(item["track"], item["name"])
        red, green, blue = CATEGORY_COLOURS[item["category"]]
        mixer.setTrackColor(item["track"], utils.RGBToColor(red, green, blue))
    print("FL Mixer Organiser: done,", len(_plan), "tracks. Type undo() to put it back.")
    _plan = None


def undo():
    """Put back what apply() changed."""
    global _plan, _snapshot
    if _snapshot is None:
        print("FL Mixer Organiser: nothing to undo")
        return
    for channel, track in _snapshot["channels"].items():
        channels.setTargetFxTrack(channel, track, True)
    for track, (name, colour) in _snapshot["tracks"].items():
        mixer.setTrackName(track, name)
        mixer.setTrackColor(track, colour & 0xFFFFFF)
    _snapshot = None
    _plan = None
    print("FL Mixer Organiser: undone")


def OnInit():
    print("FL Mixer Organiser ready. Type preview(), apply() or undo() in the Interpreter tab.")
