# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeKriket 1.0**  

---

## 2. Intended Use  

The recommender is to recommend song to users based on their preferences compare to a list of songs.

---

## 3. How the Model Works  

The code is pretty simple, I compare each songs attributes to the user's attributes and give each of them a score of importance. The ones that scores higher get recommended to the user.

---

## 4. Data

The catalog contains 18 songs. 8 songs were added or removed from the original dataset.

The genres represented are: pop, lofi, rock, ambient, jazz, synthwave, indie pop, country, metal, soul, folk, hip-hop, bossa nova, electronic, and blues. Every genre has exactly one song except lofi, which has three (*Midnight Coding*, *Library Rain*, *Focus Flow*), and pop, which has two (*Sunrise City*, *Gym Hero*).

The moods represented are: happy, chill, intense, relaxed, moody, focused, nostalgic, angry, uplifting, melancholic, energetic, romantic, eerie, and sad.

Several areas of musical taste are missing from the dataset. Most genres only have one representative song, so a listener who likes jazz will only ever be compared against *Coffee Shop Stories* — there is no variety within that genre. Mainstream styles like R&B, classical, reggae, and Latin pop are absent entirely. On the mood side, common emotional states like "motivated," "anxious," or "nostalgic and upbeat at the same time" have no representation. The catalog is also too small to surface meaningful diversity in the top 5 results — for some profiles, the recommender runs out of strong matches and fills the remaining spots with whatever scores least badly.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

Prompts:

- Features it does not consider
- Genres or moods that are underrepresented
- Cases where the system overfits to one preference
- Ways the scoring might unintentionally favor some users

One key weakness revealed by the adversarial experiments is that the scorer treats mood and energy as completely independent signals, even when they contradict each other. When the "High Energy + Sad Mood" profile was tested, songs like *Gym Hero* (loud, upbeat pop) ranked in the top 5 alongside the one genuinely sad blues track — because high energy closeness earned nearly as many points as a mood match. In practice, a user who wants sad music almost certainly does not want an intense workout anthem, but the model has no way to detect or penalize that contradiction. This means users with emotionally conflicting preferences receive a confusing mix of results that satisfy each preference in isolation without ever capturing the actual feeling they are after. A future version could address this by grouping mood and energy into a single "emotional coherence" check before scoring, rather than weighting them as separate, unrelated axes.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

Six user profiles were tested in total — three standard listeners and three adversarial edge cases designed to stress-test the scoring logic.

**Standard profiles tested:**

- *High-Energy Pop* — a fan of upbeat, danceable pop music
- *Chill Lofi* — someone studying or relaxing, preferring soft acoustic background music
- *Deep Intense Rock* — a listener who wants loud, aggressive, high-tempo rock

**Adversarial profiles tested:**

- *High Energy + Sad Mood* — a contradiction: maximum energy but sad mood
- *Nonexistent Genre (k-pop)* — a genre with zero matching songs in the catalog
- *Zero Energy + Max Acoustic* — the quietest, most acoustic preference possible

For each profile, the goal was to check whether the top 5 recommendations actually felt right for that listener type — not just mathematically close, but emotionally sensible.

**What was surprising — the Gym Hero problem:**

*Gym Hero* is a high-energy pop workout track. Its mood in the dataset is tagged as "intense," not "happy." So when the High-Energy Pop profile ran — asking for happy pop — *Gym Hero* still ranked third.

Here is why: the recommender gives points for genre, mood, energy, and acoustic feel separately, then adds them up. *Gym Hero* is pop (full genre points) and has an energy level almost identical to what the user asked for (nearly full energy points). It missed on mood — but those two wins were enough to push it into the top 3 anyway.

Think of it like a restaurant recommendation app that scores by cuisine, price, distance, and rating. If you ask for a *cheap, cheerful Italian place*, a loud, expensive Italian steakhouse could still rank highly because it nails cuisine and distance while missing on price and vibe. The system does not understand that some factors are deal-breakers — it just adds up the points regardless.

This was the single most instructive result: mood is supposed to be the highest-weighted preference (35% of the score), yet *Gym Hero* overcame a zero mood score by doing well everywhere else. It suggests the gap between "most important" and "must match" is still wide enough to produce recommendations that feel off.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems : It was pretty intersting to make
- Something unexpected or interesting you discovered: Conflicting attributes are not liked by algorithms. 
- How this changed the way you think about music recommendation apps : Makes me appreciate the works put into their model to find me new sonds.
