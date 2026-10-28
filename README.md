# fl-studio-mixer-automation

Python tool that renames and categorises FL Studio channels by keyword.

**Status: v0 (the name-categorising core).** It is a pure Python function with tests. It does **not** run inside FL Studio yet.

## Problem and plan

Channel names in a real FL Studio project are messy: `ThaiKick_01_SP`, `Serum`, `vox lead 2`, `Sample_12`.

The goal is one script that cleans the names, assigns each channel a category and (later) a colour, and builds buses, without touching anything by hand.

Today only the first part exists: given a channel name, work out a clean name and a category.

## What it does today

`categorise(name)` returns `(clean_name, category)`. These rows are real cases from the test suite:

| Raw name | Clean name | Category |
|---|---|---|
| `ThaiKick_01_SP` | `Kick` | Drums |
| `CleanHat_01_SP` | `Hat` | Drums |
| `PL_TS_Snare_One` | `Snare` | Drums |
| `Serum #2` | `Serum` | Synth |
| `Kontakt 7` | `Kontakt` | Synth |
| `vox lead 2` | `Vox` | Vocals |
| `Riser` | `Riser` | FX |
| `Track 1(consolidated)` | `Track 1(consolidated)` | unknown |
| `Chat` | `Chat` | unknown |

Categories: Drums, Vocals, FX, Bass, Synth. A name that matches nothing keeps its original name and gets `unknown`.

## How it works

- **Keywords per category.** A dict maps each category to a list of keywords. Matching ignores case.
- **Priority.** Categories are checked in dict order and the first match wins. Drums is checked before Bass, so `808 Kick` is Drums. Vocals is checked before Synth, so `vox lead 2` is Vocals.
- **Word-start rule.** A keyword only counts where a word starts in the original name: at the beginning, after a non-letter (`_`, space, a digit), or at a capital letter after a lowercase one (`CleanHat`). That is why `CleanHat` is a Hat and `Chat` is not.
- **Keyword source.** The drum, vocal and FX keywords were informed by a random sample of 800 file names from my own sample library. The synth plugin names are general knowledge.

## Architecture

The logic is kept free of any FL Studio code, so it can be tested outside FL.

- **Core (exists):** `categorise()`, pure Python.
- **FL adapter (planned, v1):** a thin layer that reads channel names through the FL Studio scripting API and writes the results back. Not started. API reference: https://il-group.github.io/FL-Studio-API-Stubs

## Project structure

```
categorise.py        # keyword dict, categorise(), is_word_start()
test_categorise.py   # pytest tests
README.md
LICENSE
.gitignore
```

## Run the tests

```
pip install pytest
pytest
```

Developed on Python 3.13. Currently 17 test cases.

## Roadmap

| Version | What | Status |
|---|---|---|
| v0 | `categorise()` core with tests | done |
| v1 | One-shot organise inside FL: names, categories, colours | not started |
| v2 | Buses, respecting existing routing | not started |
| v3 | Live mode | not started |

## Design decisions

- **Plain substring matching: rejected.** It matched `hat` inside `Chat`. Replaced by the word-start rule.
- **Fuzzy matching for typos: rejected for v0.** It is a bigger feature. Common misspellings are added as keywords instead (for example `Kik`).
- **Keywords as data, not code.** Adding a keyword is one entry in a dict, with no new logic.

## Known limitations

- A keyword written in ALL CAPS or glued into the middle of a word is not matched (`KICKDRUM`).
- Misspellings are matched only if listed as keywords.
- Only the first occurrence of a keyword is checked, so `Chat Hat` can be missed.
- Only the channel name is used. The plugin or sample behind a channel is not looked at.
- Not yet tried on whole FL projects. The tests use individual names.

## Prior art

AutoRoute Sync is an existing FL Studio tool for routing and naming channels. This project is a separate effort aimed at organising existing projects.

## License

MIT

---

Built while working on BeatShip, a release-automation app I'm developing.
