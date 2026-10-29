from categorise import categorise
import pytest
# def test_kick():
#     assert categorise("ThaiKick_01_SP") == ("Kick", "Drums")

@pytest.mark.parametrize("raw, expected", [
("Track 1(consolidated)", ('Track 1(consolidated)', 'unknown')),
("Serum", ('Serum', 'Synth')),
("PL_TS_Snare_One", ('Snare', 'Drums')),
("CleanHat_01_SP", ('Hat', 'Drums')),
("DreamyBrazilianHat", ('Hat', 'Drums')),
("LightCrispyRide_01_SP", ('Ride', 'Drums')),
("ThaiKick_01_SP", ('Kick', 'Drums')),
("HAT LOOP 91 BPM", ('Hat', 'Drums')),
("Kontakt 7", ('Kontakt', 'Synth')),
("Serum #2", ('Serum', 'Synth')),
("Analog Lab V", ('Analog Lab', 'Synth')),
("vox lead 2", ('Vox', 'Vocals')),
('Riser', ('Riser', 'FX')),
('Chat', ('Chat', 'unknown')),
('Hihat 1', ('Hihat', 'Drums')),
('Hihat 08D', ('Hihat', 'Drums')),
('OpenHat', ('OpenHat', 'Drums'))
])
def test_names(raw, expected):
    assert categorise(raw) == expected