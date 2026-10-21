# Oblique Strategies

**Play it in the browser: <https://allthemalware.github.io/Oblique/>**

A nudge for when you're stuck. Draw a card; if the studio wisdom of Brian
Eno and Peter Schmidt won't shake it loose, maybe one of the stranger cards
will.

**215 cards:** 113 after Eno & Schmidt's 1975 deck, plus 102 of my own —
sigils in the ultrasonic, the Old Ones, a fundamental tuned to a dying star.

## Two ways to draw

- **`Oblique_Strategies.py`** — a self-contained terminal deck. Just run it:
  any key deals another card, `q` quits. Piped or with `--once` it prints one
  and exits. Point `--file` at your own JSON array of strings for a different
  deck.

  ```sh
  ./Oblique_Strategies.py          # interactive
  ./Oblique_Strategies.py --once   # one card, then exit
  ```

- **`index.html`** — the same deck as a single self-contained file for the
  browser, over a faint drifting field of Conway's Game of Life. Any key (or a
  tap) deals another. This is what's served at the link above; open the file
  directly to run it offline.

An html port of a python port of [an emacs
port](https://github.com/wandersoncferreira/oblique-strategies) of the deck.
