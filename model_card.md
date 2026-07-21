# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

It matches songs to your vibe: your favorite genre, mood, energy level, and
whether you like acoustic music.

---

## 2. Intended Use  

VibeMatch takes one listener's taste and picks the top 5 songs for them from a
small song list. It gives a short reason for each pick, like "genre match" or
"energy close." It assumes the user can describe their taste with four things:
genre, mood, energy, and acoustic preference.

**What it is for:** This is a classroom project. It is made for learning how
recommender systems turn data into suggestions, and for exploring how the scoring
rules change the results.

**What it should NOT be used for:** It is not a real music app. It should not be
used to make real recommendations for real users, because the song list is tiny
and the scoring is very simple. It does not listen to audio or read lyrics, so it
should not be trusted to judge how a song actually sounds.

---

## 3. How the Model Works  

The model gives every song a score, then shows the 5 highest-scoring songs.

Each song earns points like this:

- **Same genre as the user?** +1 point.
- **Same mood as the user?** +1 point.
- **Close to the energy the user wants?** Up to +2 points. The closer the match,
  the more points. A perfect match gets the full 2 points; a far-off one gets
  little or none.
- **User likes acoustic AND the song is acoustic?** +0.5 points.

Then the model adds up the points and sorts the songs from highest to lowest.
The top 5 are the recommendations.

**What I changed from the starter:** In the starter, genre was the most important
thing (worth 2 points) and energy was worth only 1. I flipped this: I made genre
worth 1 point and energy worth up to 2. This makes energy the most powerful part
of the score.

---

## 4. Data  

The song list has **18 songs**. I did not add or remove any songs.

Each song has these features: title, artist, genre, mood, energy, tempo,
valence (how positive it sounds), danceability, and acousticness. My scoring only
uses genre, mood, energy, and acousticness. Tempo, valence, and danceability are
in the data but not used.

There are many genres (pop, lofi, rock, jazz, metal, reggae, and more) and many
moods (happy, chill, intense, sad-sounding ones, and more).

**Limits of the data:**

- The list is very small (only 18 songs).
- Most genres have only one song. Only lofi (3 songs) and pop (2 songs) have more
  than one. So fans of niche genres have almost nothing to pick from.
- The energy levels are lopsided. Songs are either fairly calm or very energetic,
  with almost nothing in the middle. This means a listener who wants "medium
  energy" can never get a great match.
- There are no lyrics and no actual audio, so the model cannot understand how a
  song really feels.

---

## 5. Strengths  

The system works well for listeners with clear, strong tastes.

- A "study music" fan (calm, acoustic, low energy) gets calm, acoustic songs.
  This matched my own gut feeling about what they should hear.
- A "gym" fan (loud, high energy) gets loud, high-energy songs.
- Listeners who are very different from each other get very different lists. That
  is a good sign — the system is really responding to their choices.
- Every recommendation comes with a short reason, so it is easy to see *why* a
  song was picked. This makes the system easy to trust and easy to debug.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

The clearest weakness I found is that the "acoustic bonus" is not really an acoustic bonus at all — it is a hidden bias toward calm music. When I checked the dataset, all 8 songs that qualify for the +0.5 acoustic reward (`acousticness >= 0.6`) happen to be low-energy tracks (energy 0.42 or below), because in this catalog acoustic songs are also the quiet ones. As a result, a high-energy listener who says they love acoustic music gets no benefit from that preference, since no energetic acoustic songs exist to reward — the bonus only ever helps the chill, studying-type user. This matters because the acoustic feature stops being an independent signal and instead quietly stacks on top of the energy score, pushing the whole system further toward low-energy recommendations. In short, the scoring unintentionally favors the "calm acoustic studier" and under-serves anyone whose taste combines high energy with acoustic sound.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

### Profiles I tested

I tested three listeners with clear tastes:

- **Chill Lofi Studier** — likes lofi, low energy, acoustic (study music).
- **High-Energy Pop** — likes pop, happy, high energy.
- **Deep Intense Rock** — likes rock, intense, very high energy.

For each one, I checked whether the top songs actually matched what the listener
asked for, then compared the three profiles against each other.

### What surprised me

I was surprised that the two high-energy listeners (Pop and Rock) got very
similar song lists. Even though they like different genres, they both want loud,
fast music, and my system pays the most attention to energy. So two different
tastes ended up sharing most of the same songs. This showed me that energy is
doing most of the work in my scoring.

### Comparing the profiles

- **Chill Lofi Studier vs. High-Energy Pop:** These are opposites, and the results
  show it. The studier gets calm, quiet, acoustic songs. The pop fan gets bright,
  loud, upbeat songs. They share no songs at all. This makes sense because one
  wants low energy and the other wants high energy.

- **High-Energy Pop vs. Deep Intense Rock:** These two are similar. Both want high
  energy, so several of the same loud songs appear on both lists. The main
  difference is the #1 pick: the pop fan's top song is a happy pop song, and the
  rock fan's top song is an intense rock song. So the genre and mood only really
  decide the top of the list, and the rest is shared high-energy songs.

- **Chill Lofi Studier vs. Deep Intense Rock:** This is the biggest contrast: quiet
  study music vs. loud, aggressive music. They share no songs, which is exactly
  what I would expect from two tastes that are so far apart.

In short, listeners who are far apart in energy get very different lists, and
listeners who are close in energy get similar lists. That told me the energy
setting is the most powerful part of my system.

---

## 8. Future Work  

If I kept building this, I would change these things:

1. **Add more songs, especially medium-energy ones.** This would fix the gap in
   the data and help listeners who want something in between calm and loud.
2. **Treat similar moods as related.** Right now "chill," "relaxed," and
   "laid-back" are seen as totally different. I would group similar moods so the
   mood score helps more often.
3. **Separate "acoustic" from "calm."** Today the acoustic bonus only ever helps
   quiet songs. I would fix the scoring (or the data) so liking acoustic music
   works for energetic songs too.

---

## 9. Personal Reflection  

I learned that a recommender is really just a set of simple rules adding up
points. Small choices in those rules have a big effect on what people see.

The most interesting thing I found was that changing the weights (making energy
matter more than genre) barely changed the top pick for each listener. This
happened because of the data itself: calm genres tend to have calm songs, so
energy and genre often point to the same songs.

This changed how I think about music apps. Now I know that what an app shows you
depends a lot on the hidden weights and on which songs are even in the list. If a
type of music is missing from the data, the app can never suggest it — no matter
what you ask for.
