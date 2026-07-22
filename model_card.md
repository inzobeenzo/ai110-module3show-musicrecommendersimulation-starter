# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Music Mood Match (Triple M)

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

Music Mood Match generates a ranked top-k list of songs from a fixed 20-song catalog, based on how closely each song's genre, mood, and energy line up with a user's stated preferences. It assumes the user can articulate their taste as three explicit values: a favorite genre, a favorite mood, and a target energy level (0–1). Listeners often won't state "I want energy=0.72," and the system has no way to infer preferences from behavior (skips, replays, session context) the way real-world recommenders like Spotify do. It also assumes those three inputs are well-formed. For example, a real genre string, a real mood string, and a numeric energy in range. This is a classroom exploration project. It's meant to demonstrate how a simple weighted-scoring rule turns stated preferences into ranked output, and to surface where that approach breaks down. 

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Think of it like a checklist a friend runs through for every song in the catalog, giving out points based on how well the song matches what you asked for. Every song has three things the checklist cares about: a genre, mood, and an energy level. You tell the system three things (other variables not accounted for yet) you're looking for: your favorite genre, mood, and how much energy you want. For genre and mood, it's either the song's genre/mood is exactly the one you said, or it isn't. There's no partial credit for "close enough" genres like indie pop counting as pop. Energy works differently as instead of a strict yes/no, the song gets credit for how *close* its energy is to what you asked for. So a song at 0.8 energy still earns decent points from someone who wanted 0.7, just not as many as a song that's exactly 0.7. Each of those three checks is worth a different number of points. As of right now, matching mood is worth more than matching genre, and being close on energy is worth the most of all. Once every song has been given a total score this way, the system just sorts all of them from highest score to lowest and hands you back the top few. It's not learning anything about you over time or comparing you to other listeners, it's re-running this same checklist from scratch every time, purely based on the three preferences you give it in that moment.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog is `data/songs.csv`. It spans 14 different genres and 11 different moods. Energy values range from 0.28 up to 0.97 on the 0–1 scale. The coverage is uneven in a way that matters for recommendations. Lofi has 3 songs and pop, metal, r&b, and classical have 2 each, but 8 of the 14 genres have only 1 song apiece. Moods are similar. "Intense" appears 4 times and "chill" 3 times, but most other moods show up only once. Energy also isn't spread evenly across its range since it directly affects how well the system can serve moderate-energy listeners. Each song also carries a few traits the CSV tracks but the scoring logic doesn't use yet: tempo/bpm, valence, danceability, and acousticness. So parts of musical taste that a real listener might care about exist in the data but currently have no way to influence a recommendation. The catalog also has no lyrics, artist popularity, release date, or any signal about how other listeners responded to a song, since this is a purely content-based system with no behavioral data to draw on.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works best for users whose taste sits in a well-represented part of the catalog. When a user's genre, mood, and energy all point to the same song, that song surfaces at #1 with a clearly higher score than anything else, which is exactly the behavior you'd want. The scoring also captures a pattern I didn't originally expect to work as well as it does as mood pulls together songs from completely different genres. Testing a "Deep Intense Rock" profile, the top results included not just rock but pop (Gym Hero), metal (Riot Frequency), and edm (Pulse Grid) songs, all tagged "intense", which matches the real-world intuition that someone who wants an intense rock song might also enjoy an intense pop or edm song, even though genre-wise they're unrelated. The energy-closeness scoring also behaves sensibly at the edges I tested. When a user asks for an energy level that doesn't exist anywhere in the catalog or contradicts their other preferences, the system doesn't break or default to genre no matter what. It lets mood and energy actually outvote a contradicted genre, which is a more reasonable outcome than blindly trusting the first preference stated.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Features it doesn't consider:** tempo, valence, danceability, and acousticness are all in the csv but none affect the score. Genre and mood are also strict yes/no matches with no partial credit for related values.

**Underrepresented genres/moods:** 8 of 14 genres have only 1 song each, and 5 of 11 moods also appear only once. A fan of any of these has no fallback if their one matching song is a poor fit on the other two traits.

**Where the system overfits to one preference:** energy is bimodal in the data as 9 of 20 songs sit at ≥0.7 and 6 sit below 0.4, leaving only 5 songs in the 0.4–0.7 "moderate" band. A user who wants energy = 0.9 can land within 0.03 of a real song, while a user who wants energy = 0.55 is capped at a worse closeness score no matter what. This isn't a bug in the formula, but a bias in the data itself.

**Who this unintentionally favors:** listeners whose taste sits in a dense part of the catalog get confident, well-supported top-5 lists. Listeners with moderate-energy or niche-genre taste get a top-5 list that looks equally confident but is built from much thinner data, with no signal in the output that it's a weaker match.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

**Profiles tested** (weights: genre=1.0, mood=1.5, energy=2.0), run for real through `run_evaluation.py` against `recommend_songs()`:

| Profile | Preferences | Top result |
|---|---|---|
| High-Energy Pop | pop/happy/0.85 | Sunrise City (4.44) |
| Chill Lofi | lofi/chill/0.35 | Library Rain (4.50) |
| Deep Intense Rock | rock/intense/0.9 | Storm Runner (4.48) |
| conflicting_signals | metal/chill/0.1 | Spacewalk Thoughts (3.14) |
| no_match_genre | opera (absent)/happy/0.5 | Rooftop Lights (2.98) |
| missing_fields | only mood="sad" (absent) | all songs tied at 0.00 |
| boundary_energy | pop/happy/1.5 (out of range) | Sunrise City (3.14) |
| empty_prefs | no preferences | all songs tied at 0.00 |
| type_mismatch_energy | energy="high" (string) | crashes: TypeError |
| exact_tie | classical/romantic/0.355 | Last Light Waltz (4.39) |

**What I looked for:** whether the top pick always matched the "obvious" best song by hand, whether undefined input merely got worse instead of breaking, and whether same-category profiles produced different rankings rather than collapsing to the same songs.

**What surprised me:** I expected genre to dominate by default, but under the current weights the `conflicting_signals` test had mood + energy actually outvote genre as both metal songs dropped to 4th/5th place instead of winning on genre alone. That confirms genre dominance was a property of the old weight values, not something inherent to the scoring approach. And honestly, what really surprised me is that I expected genre to be the most important factor, but after changing the weights, I would say most of the results were very similar, which may be an effect from the dataset itself.

**Comparisons:** High-Energy Pop and Chill Lofi sit at opposite energy extremes and never share a top result, as expected. Deep Intense Rock's top 4 are all "intense" mood songs spanning rock/pop/metal/edm. `no_match_genre` vs. High-Energy Pop shows the system drops an unrecognized genre and ranks on mood + energy alone, with no warning to the user. `missing_fields` and `empty_prefs` produce identical, meaningless 0.00. `exact_tie` wasn't actually close (4.39 vs 2.89) because a mood mismatch (romantic vs. melancholy) separated the two classical songs by more than expected.

**Why "Gym Hero" surfaces for "Happy Pop" fans:** it's pop/intense/0.93, not pop/happy. Basically, it earns genre and energy points but zero mood points. It ranks well as a partial match, not because the system thinks it's happy.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

The most immediate improvement is wiring up acousticness followed by adding danceability or tempo as optional preferences for users who care about those. I'd also add basic input validation by rejecting or clamping an out-of-range energy value, flagging an unrecognized genre instead of ignoring it, and raising clear errors instead of a raw TypeError when energy isn't a number. For explaining recommendations, the `reasons` list already breaks a score into its parts, but it could go further by explicitly telling the user when a preference didn't contribute at all, so a 0.00-score result doesn't look identical to a partial match that happens to score the same. To improve diversity, I'd cap how many results from the same artist or exact genre can appear in one top-5 list, since right now two songs by the same artist can both surface if they happen to score well, crowding out other reasonable options. Handling more complex tastes would mean supporting multiple acceptable genres or moods per user instead of one exact string each, since real listeners rarely have just one favorite genre.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Building this made it clear how much a recommender's behavior comes down to a handful of weight numbers rather than anything resembling real understanding of music. Changing three constants (genre/mood/energy weights) from 2.0/1.5/1.0 to 1.0/1.5/2.0 was enough to flip which kinds of contradictions the system tolerates, without touching a single line of matching logic. The most interesting discovery was that the "genre always wins" bias I expected going in wasn't actually a property of the algorithm's design, it was a property of one specific set of weights I happened to start with, and testing adversarial profiles is what exposed that. It also changed how I think about real apps like Spotify. This project only has to reason about three traits and twenty songs, and it's already easy to find edge cases where the output is technically correct but not actually useful. A production recommender is making the same kind of weighted tradeoffs at a much larger scale, which means the same kinds of blind spots are probably still there, just harder to notice with millions of songs instead of twenty.
