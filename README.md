# 🎲 Blind Fortune's Rigged Raffle

This app is a neutral, automated **Session Organiser & Leader Rotator** for your club's gaming nights. It bins the manual guesswork and ensures choosing a session leader is always fair, transparent, and completely automated.

---

### 📋 The Needs It Covers
* **`[👤]` Central Master Roster:** Keeps a clean, duplicate-free list of all verified club members.
* **`[💾]` Session Memory:** Tracks who played with whom in past sessions so the club never forgets its history.
* **`[⚖️]` No-Drama Referee:** Drops the need for debates or repetitive arguments over who has to organise the table each night.

---

### ⚙️ How the Leader Rotation Works
The app operates on a clever set of rules based on who turns up to play:

* **`[🎲]` New Player Combos ➔ Pure Random Draw:** If the mix of players turning up today has *never* played together before, the app acts as a virtual tombola. It shuffles the list, sets a locked turn order, and picks the first leader.
* **`[🔄]` Known Player Combos ➔ Mandatory Rotation:** If this exact group has played together before, the app remembers them. Instead of a re-roll, it bumps the last leader down the queue and automatically gives the crown to the next person in line. Everyone gets a fair turn!
* **`[📐]` Dynamic Group Sizes:** The club is flexible, and so is the app. It handles tables of 3, 4, or more players independently without breaking the history of other groups.

---

### `[🛠️]` Under the Hood: Data Structure (`Groups.txt`)
* **`[🔑]` The Main Core Data Type:** The system stores the session log using a serialized **Key-Value Pair (Dictionary Style Mapping)** on each line, matching a unique player identity block to their session state.
* **`[🧩]` The Sub-Type Breakdown:**
  * **The Key `(Tuple)`:** Composed of `(String: Group Code, Integer: Group Size, String: Player Name)`. This acts as a rigid, unique identifier.
  * **The Value `[List]`:** Composed of `[Boolean: Is Current Leader?, Integer: Queue Turn Order, String: Last Active Game Date]`. This holds the live, mutable status of the player.

---

### `[📢]` Why BF RIGGED Raffle?
* **The "Booooohhh!!!" Factor:** Any leadership this app produces will be welcomed with a collective "Booooohhh!!!". 
* **The Dilemma:** Everyone wanted to be the leader... but this works for them anyway! 😆😆😆😆
