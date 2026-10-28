# fl-studio-mixer-automation

A tested Python function that turns messy FL Studio channel names into a clean name and a category: `ThaiKick_01_SP` becomes `('Kick', 'Drums')`.

## Why

Channel names in a real FL Studio project are a mess: sample-pack names, plugin names, numbers, handles. Before you can colour, group or route channels automatically, you need to know what each one is. This function is that first step.

## Try it

Needs Python 3 (developed on 3.13).

```
pip install pytest
pytest
python -c "from categorise import categorise; print(categorise('ThaiKick_01_SP'))"
```

Output of the last line:

```
('Kick', 'Drums')
```

## Examples

Real cases from the test suite (17 in total):

| Raw name | Clean name | Category |
|---|---|---|
| `ThaiKick_01_SP` | `Kick` | Drums |
| `CleanHat_01_SP` | `Hat` | Drums |
| `HAT LOOP 91 BPM` | `Hat` | Drums |
| `Hihat 1` | `Hihat` | Drums |
| `PL_TS_Snare_One` | `Snare` | Drums |
| `Serum #2` | `Serum` | Synth |
| `vox lead 2` | `Vox` | Vocals |
| `Riser` | `Riser` | FX |
| `Chat` | `Chat` | unknown |
| `Track 1(consolidated)` | `Track 1(consolidated)` | unknown |

Categories: Drums, Vocals, FX, Bass, Synth. A name that matches nothing keeps its original name and gets `unknown`.

## How it works

- **Keywords as data.** A dict maps each category to a list of keywords. Adding a keyword is one entry, no new logic. Matching ignores case; the clean name is the keyword as spelled in the dict.
- **First match wins.** Categories are checked in order: Drums, Vocals, FX, Bass, Synth. So `808 Kick` is Drums, not Bass, and `vox lead 2` is Vocals, not Synth (`Lead` is a synth keyword).
- **Word-start rule.** A keyword only counts where a word starts: at the beginning, after a non-letter (`_`, space, digit), or at a capital after a lowercase letter (`CleanHat`).
- **No FL Studio imports.** The logic is plain Python, so pytest runs it outside FL.

## How it got here

1. I took a random sample of 800 file names from my own sample library and counted the most common words. That gave the drum, vocal and FX keywords. Synth plugin names (Serum, Kontakt, ...) are general knowledge.
2. The first version used plain substring matching. It matched `hat` inside `Chat`. I replaced it with the word-start rule.
3. Re-running on the sample showed the new rule broke compound names: `Hihat 1` and `Openhat` came back `unknown`, because `hat` sits mid-word. I added `Hihat` and `OpenHat` as their own keywords.
4. Order mattered: with `Hat` listed before `OpenHat`, `OpenHat` returned `Hat` (the capital H counts as a word start). Longer keywords now come first.

What I learned: test against real data, not only hand-picked examples. The word-start fix passed my own cases; only the real names showed what it broke.

## Known limitations

- Only the first occurrence of a keyword is checked: `Chat Hat` returns `unknown`.
- A keyword glued mid-word in lowercase is not found: `bigkick` returns `unknown`.
- Misspellings match only if listed as keywords (for example `Kik`). Fuzzy matching was left out on purpose.
- Numbers are dropped, so two kicks both become `Kick`.
- Only the name is used, not the plugin or sample behind the channel.
- Tested on individual names, not yet on whole FL projects.

## Project structure

```
categorise.py        # keyword dict, categorise(), is_word_start()
test_categorise.py   # pytest tests
```

## Status

Working and tested as a standalone function. It does not run inside FL Studio yet. Next: a thin adapter that reads channel names through the FL Studio Python scripting API (https://il-group.github.io/FL-Studio-API-Stubs) and writes the results back.

## License

MIT

---

Built while working on BeatShip, a release-automation app I'm developing.
