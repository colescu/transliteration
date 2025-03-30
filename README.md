Colescu's CLI tool for transliteration

# Features

Currently only supports Latin <-> Greek.

Main features:

- Full support for diacritics.
- Option `-l` to Latinize the spelling (e.g., Kaisar -> Caesar).

# Installation

Clone the repository:

```
git clone https://github.com/yourusername/transliteration.git
cd transliteration
```

Install in editable mode:

```
pip install -e .
```

# Usage

Once installed, you can run the tool from your command line.

To get help on how to use:

```
tl -h
```

Example usage (Greek -> Latin):

```
tl -t gl
ἀλλ᾽ ὅτε δὴ ἔτος ἦλθε περιπλομένων ἐνιαυτῶν
all᾽ hóte dḕ étos ē̃ltʰe periploménōn eniautō̃n
```

Example usage (Latin -> Greek):

```
tl
toũ thygátēr dýstēnon odyrómenon katerýkei
τοῦ θυγάτηρ δύστηνον ὀδυρόμενον κατερύκει
```

To exit, type `quit` or press Ctrl + C.

# Issues

- crasis: τὸ ἕτερον → θοὔτερον
- iota subscript
