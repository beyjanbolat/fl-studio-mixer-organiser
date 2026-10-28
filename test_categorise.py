from categorise import categorise
import pytest
# def test_kick():
#     assert categorise("ThaiKick_01_SP") == ("Kick", "Drums")

@pytest.mark.parametrize("raw, expected", [
    ("Serum", ("Serum", "Synth")),
    ("Serum #2", ("Serum", "Synth")),
    ("Kontakt 7", ("Kontakt", "Synth")),
    ("PL_TS_Snare_One", ("Snare", "Drums"))
])
def test_names(raw, expected):
    assert categorise(raw) == expected