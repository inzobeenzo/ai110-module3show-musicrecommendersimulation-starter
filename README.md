# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Real-world recommenders largely lean on collaborative filtering, which is inferring what a user will like based on patterns across millions of other users with similar behavior layered with implicit signals like skips, replays, watch time, and session context rather than explicit ratings. Content-based filtering, which is matching a user's stated or inferred preferences directly against a song's own attributes plays a supporting role, and is mainly useful for cases where a new user or new song has no behavioral history yet. This simulation isolates the content-based half of that picture. With only 10 songs and no user population to analyze for behavioral patterns, collaborative filtering isn't feasible here. Instead, this version prioritizes a transparent scoring rule: it takes a small number of user preferences and directly measures how closely each song's own attributes match them, weighting a categorical identity signal above a more situational/subjective one, and using distance-based scoring for numeric traits like energy so "closer to what you asked for", not simply "higher" or "lower", wins.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
  Each song has the identifying variables of id, title and artist with taste-related features including genre, mood, energy, valence, danceability, acousticness, and tempo/bpm. As of right now, the system takes into account genre, mood, energy, and acousticness as there isn't usually an explicit preference written for these and are typically dependent on the previous features.
- What information does your `UserProfile` store
  It just store the 4 major fields that a song recommender would typically ask. These include favorite genre, mood, preferred energy, and if they like acoustic. It's much more narrower as the user is telling the system what they want in general, not every attribute a song should have.
- How does your `Recommender` compute a score for each song
  Based on the csv and what was researched, the top features include genre, mood, energy, and acoustics with the top 2 being genre and mood. These are weighted by 2, 1.5, 1, 1 respectively and both genre and mood are just an exact match or not, energy uses a closeness formula (1 - abs(difference)) as 1 - energy or energy by itself wouldn't make sense, and acousticness is 1 or 0 based on the preference being above 0.5 or not.
- How do you choose which songs to recommend
  After the recommender produces a computed score for each song, another function will sort that list and return the top k numbers that match the users preference. To preface, scoring and ranking will be kept separate as scoring answers how good a specific song is for a user, while ranking answers with all the scores, which and how many do I show?

You can include a simple diagram or bullet list if helpful.

Song features used in scoring:
- genre (categorical — e.g., pop, lofi, rock, ambient, jazz, synthwave, indie pop)
- mood (categorical — e.g., happy, chill, intense, relaxed, moody, focused)
- energy (continuous, 0–1)
- acousticness (continuous, 0–1, thresholded at 0.5 for matching)

Song fields present but not used in scoring: id, title, artist (identifiers), tempo_bpm, valence, danceability (captured in the data but no corresponding preference in UserProfile yet).

UserProfile fields:
- favorite_genre (str) — matched exactly against Song.genre
- favorite_mood (str) — matched exactly against Song.mood
- target_energy (float, 0–1) — compared to Song.energy via distance, not exact match
- likes_acoustic (bool) — compared to Song.acousticness via a threshold

---

## Algorithm Recipe

**Score** each song as the sum of:

| Component | Rule | Weight |
|---|---|---|
| Genre match | `song.genre == user.favorite_genre` → full points, else 0 | 2.0 |
| Mood match | `song.mood == user.favorite_mood` → full points, else 0 | 1.5 |
| Energy closeness | `1 - abs(song.energy - user.target_energy)` | 1.0 |
| Acousticness match | `(song.acousticness > 0.5) == user.likes_acoustic` → full points, else 0 | 1.0 |

```python
def score_song(user: UserProfile, song: Song) -> float:
    score = 0.0
    if song.genre == user.favorite_genre:
        score += 2.0
    if song.mood == user.favorite_mood:
        score += 1.5
    score += (1 - abs(song.energy - user.target_energy)) * 1.0
    if (song.acousticness > 0.5) == user.likes_acoustic:
        score += 1.0
    return score
```

**Rank**: sort all songs by score descending, return the top `k`. Scoring and ranking are separate steps — scoring judges one song at a time; ranking decides which and how many to surface.

**Example** — user wants `genre="lofi", mood="chill", target_energy=0.35, likes_acoustic=True`: *Library Rain* (lofi/chill/0.35 energy/0.86 acoustic) scores 2.0+1.5+1.0+1.0 = **5.5**, edging out *Midnight Coding* (lofi/chill/0.42/0.71) at **5.43**, while *Spacewalk Thoughts* (ambient/chill/0.28/0.92) only reaches **3.43** — the genre mismatch there costs more than its better acousticness fit gains.

### Expected biases

- **Over-prioritizes genre.** A perfect mood/energy match in an adjacent genre (e.g., "ambient" vs "lofi") can still lose to a same-genre song with weaker mood/energy fit, since genre is both the heaviest weight and strictly boolean (no partial credit for related genres).
- **Boolean mood/acousticness hide near-misses.** "Chill" vs "relaxed" scores the same as "chill" vs "aggressive"; acousticness at 0.49 scores the same as 0.05 — both collapse a spectrum into a hard yes/no.
- **Catalog imbalance.** With only 20 songs and uneven genre representation (three lofi tracks vs. one classical), some taste profiles get richer, more differentiated results than others independent of the algorithm itself.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loading songs from data/songs.csv...
Loaded songs: 20

User profile: genre=pop, mood=happy, energy=0.8

Top recommendations:
========================================
1. Sunrise City by Neon Echo - Score: 4.48
     - genre match (+2.0)
     - mood match (+1.5)
     - energy closeness 0.98 (+0.98)
----------------------------------------
2. Gym Hero by Max Pulse - Score: 2.87
     - genre match (+2.0)
     - energy closeness 0.87 (+0.87)
----------------------------------------
3. Rooftop Lights by Indigo Parade - Score: 2.46
     - mood match (+1.5)
     - energy closeness 0.96 (+0.96)
----------------------------------------
4. Concrete Bloom by Verse Fifty - Score: 1.00
     - energy closeness 1.00 (+1.00)
----------------------------------------
5. Night Drive Loop by Neon Echo - Score: 0.95
     - energy closeness 0.95 (+0.95)
----------------------------------------
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

conflicting_signals
  profile: {'genre': 'metal', 'mood': 'chill', 'energy': 0.1}
------------------------------------------------------------
  1. Spacewalk Thoughts by Orbit Bloom - Score: 2.32
       - mood match (+1.5), energy closeness 0.82 (+0.82)
  2. Library Rain by Paper Lanterns - Score: 2.25
       - mood match (+1.5), energy closeness 0.75 (+0.75)
  3. Midnight Coding by LoRoom - Score: 2.18
       - mood match (+1.5), energy closeness 0.68 (+0.68)
  4. Riot Frequency by Grey Anvil - Score: 2.16
       - genre match (+2.0), energy closeness 0.16 (+0.16)
  5. Iron Choir by Grey Anvil - Score: 2.13
       - genre match (+2.0), energy closeness 0.13 (+0.13)
============================================================

no_match_genre
  profile: {'genre': 'opera', 'mood': 'happy', 'energy': 0.5}
------------------------------------------------------------
  1. Rooftop Lights by Indigo Parade - Score: 2.24
       - mood match (+1.5), energy closeness 0.74 (+0.74)
  2. Sunrise City by Neon Echo - Score: 2.18
       - mood match (+1.5), energy closeness 0.68 (+0.68)
  3. Dust Road Home by Marion Hale - Score: 0.98
       - energy closeness 0.98 (+0.98)
  4. Velvet Static by Nadia Cross - Score: 0.95
       - energy closeness 0.95 (+0.95)
  5. Midnight Coding by LoRoom - Score: 0.92
       - energy closeness 0.92 (+0.92)
============================================================

missing_fields
  profile: {'mood': 'sad'}
------------------------------------------------------------
  1. Sunrise City by Neon Echo - Score: 0.00
       - no scoring factors matched
  2. Midnight Coding by LoRoom - Score: 0.00
       - no scoring factors matched
  3. Storm Runner by Voltline - Score: 0.00
       - no scoring factors matched
  4. Library Rain by Paper Lanterns - Score: 0.00
       - no scoring factors matched
  5. Gym Hero by Max Pulse - Score: 0.00
       - no scoring factors matched
============================================================

boundary_energy
  profile: {'genre': 'pop', 'mood': 'happy', 'energy': 1.5}
------------------------------------------------------------
  1. Sunrise City by Neon Echo - Score: 3.82
       - genre match (+2.0), mood match (+1.5), energy closeness 0.32 (+0.32)
  2. Gym Hero by Max Pulse - Score: 2.43
       - genre match (+2.0), energy closeness 0.43 (+0.43)
  3. Rooftop Lights by Indigo Parade - Score: 1.76
       - mood match (+1.5), energy closeness 0.26 (+0.26)
  4. Iron Choir by Grey Anvil - Score: 0.47
       - energy closeness 0.47 (+0.47)
  5. Pulse Grid by Kilo Watt - Score: 0.45
       - energy closeness 0.45 (+0.45)
============================================================

empty_prefs
  profile: {}
------------------------------------------------------------
  1. Sunrise City by Neon Echo - Score: 0.00
       - no scoring factors matched
  2. Midnight Coding by LoRoom - Score: 0.00
       - no scoring factors matched
  3. Storm Runner by Voltline - Score: 0.00
       - no scoring factors matched
  4. Library Rain by Paper Lanterns - Score: 0.00
       - no scoring factors matched
  5. Gym Hero by Max Pulse - Score: 0.00
       - no scoring factors matched
============================================================

type_mismatch_energy
  profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 'high'}
------------------------------------------------------------
  CRASHED: TypeError: unsupported operand type(s) for -: 'float' and 'str'
============================================================

exact_tie
  profile: {'genre': 'classical', 'mood': 'romantic', 'energy': 0.355}
------------------------------------------------------------
  1. Last Light Waltz by Elin Marsh - Score: 4.45
       - genre match (+2.0), mood match (+1.5), energy closeness 0.95 (+0.95)
  2. Glass Cathedral by Elin Marsh - Score: 2.95
       - genre match (+2.0), energy closeness 0.95 (+0.95)
  3. Velvet Static by Nadia Cross - Score: 2.30
       - mood match (+1.5), energy closeness 0.80 (+0.80)
  4. Library Rain by Paper Lanterns - Score: 0.99
       - energy closeness 0.99 (+0.99)
  5. Faded Photograph by Nadia Cross - Score: 0.99
       - energy closeness 0.99 (+0.99)
============================================================

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

My biggest learning moment was recognizing how trivial it is to make a system, but how hard it is to make it right. You can truly take any input as a numerical value, and output something relevant with those numbers as long as you have the right context. I used AI tools frequently in implementation, drafting/designing, and attacking questions I was confused about. I double-checked them when the spec explicitly said to make an output a tuple or to add reason on top of the answer. What surprised me the most about simple algorithms, is that it is truly simple. You can take 3 broad categories and still narrow it down to more-or-less accurate recommendations with some math. I would definitely try incorporating many more songs and attributes to see how much more accurate the recommender can get, and if it would actually recommend me good songs based on my personal music taste. Bias in a system like this doesn't come from the math being wrong, but from the math being applied to lopsided data. When I tested adversarial profiles, I expected genre to dominate every result no matter what, since that was the original weighting, but after I rebalanced the weights to favor energy, that bias mostly disappeared, which taught me the "genre always wins" behavior wasn't a property of the algorithm itself, it was a property of one specific set of numbers I happened to start with. The more persistent bias turned out to be in the catalog: energy values cluster at the high and low ends with a gap in the middle, and several genres only have one song each. That means listeners with moderate-energy or niche-genre tastes get recommendation lists that look just as confident as everyone else's, but are actually built from much thinner data, with nothing in the output to signal that difference. A real-world recommender with millions of songs probably still has versions of this same gap, just harder to notice at that scale.

