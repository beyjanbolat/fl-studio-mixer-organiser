from categorise import make_plan

# make_plan(names, targets, first_insert, last_insert, busy_tracks)
# targets[i] is the mixer track channel i feeds. 0 means Master (not routed).


def test_routed_channel_renames_its_own_track():
    plan = make_plan(["ThaiKick_01_SP"], [5], 1, 10, set())
    assert plan == [{"channel": 0, "track": 5, "name": "Kick", "category": "Drums"}]


def test_duplicates_are_numbered():
    plan = make_plan(["Hihat 1", "hihat 2", "Hihat 3"], [1, 2, 3], 1, 10, set())
    assert [p["name"] for p in plan] == ["Hihat", "Hihat 2", "Hihat 3"]


def test_unrouted_channel_gets_first_free_insert():
    plan = make_plan(["Kick", "Snare"], [1, 0], 1, 10, set())
    assert plan[1]["track"] == 2


def test_unrouted_channel_skips_tracks_that_are_taken():
    plan = make_plan(["Kick", "Snare", "Clap"], [2, 0, 0], 1, 10, set())
    assert [p["track"] for p in plan] == [2, 1, 3]


def test_unrouted_channel_skips_busy_tracks():
    plan = make_plan(["Kick"], [0], 1, 10, {1, 2})
    assert plan[0]["track"] == 3


def test_two_unrouted_channels_get_different_tracks():
    plan = make_plan(["Kick", "Snare"], [0, 0], 1, 10, set())
    assert [p["track"] for p in plan] == [1, 2]


def test_shared_track_is_named_by_first_channel_only():
    plan = make_plan(["Kick", "Snare"], [4, 4], 1, 10, set())
    assert len(plan) == 1
    assert plan[0]["name"] == "Kick"


def test_no_free_insert_skips_the_channel():
    plan = make_plan(["Kick", "Snare"], [0, 0], 1, 1, set())
    assert len(plan) == 1


def test_unknown_name_keeps_original_name():
    plan = make_plan(["Sampler"], [0], 1, 10, set())
    assert plan[0]["name"] == "Sampler"
    assert plan[0]["category"] == "unknown"
