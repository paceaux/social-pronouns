# Social Pronoun Analysis

This repository contains Python scripts used for analysing the data from the database(s) of Bluesky posts that was collected with the [Bluesky Language Feed Generator](https://github.com/paceaux/bsky-language-feed-generator).

## Questions this code should answer

### What kinds of words are associated with this pronoun?

- negations (no, nah, nope, naw)
- affirmations (yes, yeah, yep, yeh)
- profanities (shit, fuck, ass)
- personal pronouns (I, you, he, she, it)

### How is the pronoun used?

- position in the discourse
- capitalized / lowercased
- added vowels / consonants
- surrounding words

### What's going on in the discourse

- word count
- emojis
- sentiment

## Usage

### Pre-requisites

First, get the database(s) from the [OSF project](https://osf.io/qfdtn/files/osfstorage) and put them in a folder.

### Get details for a specific pronoun

Run this command:

```bash
python analyse.py -p <pronoun>
```

Expect:
`<pronoun>.results.md` to be created in the  a `results` directory, containing details about the pronoun.

Optional arguments:
- `-d, --database <database>`: Specify the database to use (default is `bluesky.db`).
- `-o, --outputFile <output_file>`: Specify the output file name (default is `<pronoun>.results.md`).
- `-p <pronoun>`: Specify the pronoun file name (default is `bro`), options include dude, bro, bruh, chat, sis, fam.
- `-s, --profanities`: Include profanities in the analysis (default is `False`).
- `-n, --negations`: Include negations in the analysis (default is `False`).
- `-a, --affirmations`: Include affirmations in the analysis (default is `False`).
- `-e, --emojis`: Include emojis in the analysis (default is `False`).
- `-u, --usage`: Display the posts for any of the data parameters provided (default is `False`).
- `--allRows`: Display every post using the pronoun in the analysis (default is `False`).

### Get a summary of all pronouns

run this command:

```bash
python summarize.py -d <database> -o <output_file>
```

Expect:
`<output_file>` to be created in the results directory, containing a summary of all pronouns in the database.


Optional arguments:
- `-d, --database <database>`: Specify the database to use (default is `bluesky.db`).
- `-o, --outputFile <output_file>`: Specify the output file name (default is `summary.results.md`).
