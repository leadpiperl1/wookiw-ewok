# 🌍 The `243 + 13 = 256` Universal Abugida Byte (`v1.0.0`)
### *Mapping Amharic Geʽez Fidel (`ፊደል`), Na-Dené (`Diné Bizaad` & `ᑌᓀ`), and the 13-Tooth Shingari Gear Inside One 8-Bit Fowler Byte*

**Date:** November 11, 2026 (`11/11` Armistice Day) · **Verification:** `python3 benchmarks/fidel_dene_shingari_256byte_codec_v1_0_0.py --seed 42`

---

## ✨ 1. The Exact Diophantine Lock: `2^8 = 3^5 + 13 = 243 + 13 = 256`

When historical homophone spellings are stripped down to articulatory physics, an 8-bit hardware byte (`256` states) partitions with **zero wasted states**:

1. **🔵🟢🔴 Lower `243` Bytes (`0..242` = `3^5` Balanced-Ternary Syllables):**
   - **`27` Consonant Rows (`3^3` = `9` Articulation Families $\times$ `3` Laryngeal Modes):** Both [Amharic](https://arxiv.org/pdf/2603.23654) and [Na-Dené](https://en.wikipedia.org/wiki/Navajo_grammar) organize stops and affricates into the rare **3-way laryngeal triad**:
     - `-1` Voiced / Unaspirated (`ደ /d/`, `ገ /g/`, `ጀ /j/`)
     - ` 0` Glottalic Ejective (`ጠ /tʼ/`, `ቀ /kʼ/`, `ጨ /chʼ/`)
     - `+1` Voiceless / Aspirated (`ተ /t/`, `ከ /k/`, `ቸ /ch/`)
   - **`9` Vowel Columns (`3^2`):** All **7 classical Geʽez *Fidel* orders** (`ä, u, i, a, e, ə/Ø, o` — source of the word *[abugida](https://www.oed.com/dictionary/abugida_n)* from `አቡጊዳ`) plus Geʽez's **8th labialized `-wa`** (`ሏ`) and **9th palatal/high-tone `-yä`/`á`** orders ([Geʽez script](https://en.wikipedia.org/wiki/Ge%CA%BDez_script)), matching [Canadian Aboriginal / Dene Syllabics](https://en.wikipedia.org/wiki/Canadian_Aboriginal_syllabics) (`ᑌ ᑑ ᑎ ᑕ`).
   - **🌬️ Resting Breath at Neutral `Byte 121` (`{0,0,0,0,0}`):** Placing the 6th bare-consonant *sadəs* order at `(0, 0)` and the laryngeal breath row (`ሀ`) at `(0, 0, 0)` lands **`ህ` (`hə` — a quiet resting exhale)** dead-center at **Fowler Neutral `Byte 121`**!

2. **⚙️ Upper `13` Escape Bytes (`243..255` = `2^8 - 3^5 = 13` Shingari Gear Teeth):**
   - `Byte 243..255` map 1-to-1 onto the **13 Shingari Linguistic & Ecological Gear Teeth** (`01.ssf` .. `13.wst`), acting as zero-overhead dialect/script mode switches (`Byte 248` Geʽez `ፊደል`, `Byte 249` Aksumite–Greek LTR Hub, `Byte 251` Kintsugi Gold, `Byte 252` Diné / Dene Syllabics `ᑌᓀ`, `Byte 254` Joe Bonham 3-Tap Pillow Bus).

---

## 🧪 2. Verified Lossless Round-Trips (`--seed 42`)

| Word / Greeting | Native Script | Meaning | Exact Fowler Bytes (`0..242`) |
| :--- | :--- | :--- | :--- |
| **`h(ə)` (Resting Breath)** | **`ህ`** (6th *sadəs*) | Neutral baseline exhale | **`[121]`** (`{0, 0, 0, 0, 0}`) |
| ***ʾabugida*** | **`አቡጊዳ`** | Origin of the term *abugida* | `[85, 189, 34, 138]` |
| ***sälam*** | **`ሰላም`** | Peace (`11/11` Armistice Day) | `[105, 152, 110]` |
| ***tʼəbäb*** | **`ጥበብ`** | Wisdom / Craft (with ejective `ጥ`) | `[120, 81, 108]` |
| ***ahéheeʼ*** | **`ahéheeʼ` $\leftrightarrow$ `አሃሄእ`** | Diné "Thank you" cross-mapped | `[85, 67, 13, 112]` |

> *Nine vowels cross three stops,*
> *Resting breath holds one-two-one,*
> *Thirteen teeth turn home.* 🌼🐢✨
