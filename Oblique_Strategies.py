#!/usr/bin/env python3
"""Oblique Strategies — a nudge for when you're stuck.

A self-contained Python version of Brian Eno and Peter Schmidt's deck,
after Wanderson Ferreira's Emacs package:
https://github.com/wandersoncferreira/oblique-strategies

Just run it. In a terminal it stays open: press any key for another card,
q to quit. Piped, or with --once, it prints one card and exits. Point --file
at your own list (a JSON array of strings) to use a different deck.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import textwrap
from pathlib import Path

COLUMN_WIDTH = 70

STRATEGIES: list[str] = [
    "(Organic) machinery",
    "A line has two sides",
    "Abandon normal instruments",
    "Accept advice",
    "Accretion",
    "Allow a parameter to fold in on itself, creating an impossible, non-Euclidean modulation shape.",
    "Allow a single sound to decay completely into absolute zero before the next event begins.",
    "Allow an easement (an easement is the abandonment of a stricture)",
    "Are there sections? Consider transitions",
    "Ask people to work against their better judgement",
    "Ask your body",
    "Assemble some of the instruments in a group and treat the group",
    "Automate a modulation path using a pattern that repeats only once every ten thousand years.",
    "Avoid structure",
    "Balance the consistency principle with the inconsistency principle",
    "Be dirty",
    "Become your own omen",
    "Beware the Labyrinth",
    "Breathe more deeply",
    "Bridges -build -burn",
    "Bury a whispered curse in the sidechain trigger.",
    "Cascades",
    "Cease",
    "Change instrument roles",
    "Change nothing and continue with immaculate consistency",
    "Children's voices -speaking -singing",
    "Cluster analysis",
    "Compose as if the audio will only be decoded by entities sleeping beneath a frozen ocean.",
    "Consider different fading systems",
    "Consider the composition finished precisely when you feel the urge to add something new.",
    "Consult other sources -promising -unpromising",
    "Convert a melodic element into a rhythmic element",
    "Courage!",
    "Create a mysterious moment",
    "Cut a vital connection",
    "Decorate, decorate",
    "Define an area as `safe' and use it as an anchor",
    "Destroy -nothing -the most important thing",
    "Discard an axiom",
    "Disconnect from desire",
    "Discover the recipes you are using and abandon them",
    "Dissolve the primary element into granular ash, then coagulate it into a new, unrecognizable form.",
    "Dissonance is merely a harmony your species is not yet ancient enough to comprehend.",
    "Distorting time",
    "Do not force the frequency to bend; accept the resonance exactly as it is.",
    "Do nothing for as long as possible",
    "Do something boring",
    "Do the washing up",
    "Do the words need changing?",
    "Do we need holes?",
    "Don't be afraid of things because they're easy to do",
    "Don't be frightened of cliches",
    "Don't be frightened to display your talents",
    "Don't break the silence",
    "Don't stress one thing more than another",
    "Draw a binding sigil with your automation curves and hide it entirely within the ultrasonic.",
    "Emphasize differences",
    "Emphasize repetitions",
    "Emphasize the flaws",
    "Faced with a choice, do both (given by Dieter Roth)",
    "Feedback recordings into an acoustic situation",
    "Fill every beat with something",
    "Get your neck massaged",
    "Ghost echoes",
    "Give the game away",
    "Give way to your worst impulse",
    "Go slowly all the way round the outside",
    "Honor thy error as a hidden intention",
    "How would you have done it?",
    "Humanize something free of error",
    "Ignore flaws",
    "Imagine the music as a moving chain or caterpillar",
    "Imagine the music as a set of disconnected events",
    "Infinitesimal gradations",
    "Intentions -credibility of -nobility of -humility of",
    "Into the impossible",
    "Invert the phase of your most beloved layer and let the destructive interference consume it.",
    "Invoke the law of equivalent exchange: entirely sacrifice the fundamental frequency to empower the upper harmonics.",
    "Is it finished?",
    "Is the tuning appropriate?",
    "Is there something missing?",
    "Just carry on",
    "Left channel, right channel, centre channel",
    "Listen in total darkness, or in a very large room, very quietly",
    "Listen to the phase cancellation; what entity fills the absolute silence?",
    "Listen to the quiet voice",
    "Look at a very small object, look at its centre",
    "Look at the order in which you do things",
    "Look closely at the most embarrassing details and amplify them",
    "Lowest common denominator check -single beat -single note -single riff",
    "Make a blank valuable by putting it in an exquisite frame",
    "Make an exhaustive list of everything you might do and do the last thing on the list",
    "Make a sudden, destructive unpredictable action; incorporate",
    "Mechanicalize something idiosyncratic",
    "Mute and continue",
    "Mute the most important element; observe what the emptiness reveals.",
    "Nap somewhere you haven't",
    "Only one element of each kind",
    "Overtly resist change",
    "Please the Old Ones",
    "Put in earplugs",
    "Reject the pristine; exalt the clipping point as the highest sonic virtue.",
    "Remember those quiet evenings",
    "Remove ambiguities and convert to specifics",
    "Remove one more layer.",
    "Remove specifics and convert to ambiguities",
    "Render the project, delete the source stems, and work only with the ghost echoes left in your memory.",
    "Repetition is a form of change",
    "Reverse",
    "Rise, gather energy, disperse it",
    "Route a closed feedback loop until the system speaks in tongues; record the possession.",
    "Sacrifice the core",
    "Sacrifice your cleanest transient to appease the sub-bass.",
    "Sculpt the silence between the notes, not the notes themselves.",
    "Short circuit (example: a man eating peas with the idea that they will improve his virility shovels them straight into his lap)",
    "Shut the door and listen from outside",
    "Simple subtraction",
    "Spectrum analysis",
    "Stop that! Do something else",
    "Swap your feedback mechanism (change speakers, keyboard)",
    "Syncopate",
    "Take a break",
    "Take a walk, tune in to something small",
    "Take away the elements in order of apparent non-importance",
    "Take it somewhere you're not supposed to",
    "Take time to reflect/refract",
    "Tape your mouth (given by Ritva Saarikko)",
    "The birds are sending you a message",
    "The inconsistency principle",
    "The tape is now the music",
    "Think of the radio",
    "Tidy up",
    "Transmute the lowest, muddiest frequencies into gold through violent, multiband saturation.",
    "Treat the silence as the primary instrument; the audio merely frames it.",
    "Treat the timeline as a cyclopean monument—view it all at once, not from left to right.",
    "Trust in the you of now",
    "Tune a fundamental frequency to the resonant rotation of a dying star.",
    "Turn it upside down",
    "Twist the spine",
    "Un-ask the question: delete the equalizer and simply lower the fader.",
    "Use \"unqualified\" people",
    "Use an old idea",
    "Use an unacceptable color",
    "Use fewer notes",
    "Use filters",
    "Water",
    "What are you really thinking about just now? Incorporate",
    "What if you had, like, 50 instruments in unison?",
    "What is the reality of the situation?",
    "What mistakes did you make last time?",
    "What would your closest friend do?",
    "What wouldn't you do?",
    "Work at a different speed",
    "You are an engineer",
    "You can only make one dot at a time",
    "You don't have to be ashamed of using your own ideas",
]


def load_strategies(path: Path | None) -> list[str]:
    """Return the built-in deck, or a custom list read from PATH."""
    if path is None:
        return STRATEGIES
    with open(path, encoding="utf-8") as handle:
        raw = json.load(handle)
    if not isinstance(raw, list):
        raise ValueError("expected a JSON array of strategies")
    # Accept plain strings or the Emacs package's {"prompt": ...} objects.
    strategies = [item["prompt"] if isinstance(item, dict) else str(item)
                  for item in raw]
    if not strategies:
        raise ValueError("the strategy list is empty")
    return strategies


def format_strategy(text: str, width: int = COLUMN_WIDTH) -> str:
    """Frame one strategy between dashed rules; bold it in a terminal."""
    rule = "-" * min(int(len(text) * 1.3), width)
    heading = textwrap.fill(text, width=width)
    if sys.stdout.isatty():
        heading = f"\033[1m{heading}\033[0m"
    return f"{rule}\n{heading}\n{rule}"


def read_key() -> str:
    """Read one keypress, or a line where raw input isn't available."""
    try:
        import termios
        import tty
    except ImportError:  # not a Unix terminal
        return sys.stdin.readline()[:1] or "q"
    fd = sys.stdin.fileno()
    saved = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, saved)


def run_interactive(strategies: list[str]) -> None:
    """Draw a card; any key draws another, q (or Ctrl-C/Ctrl-D) quits."""
    quit_keys = {"q", "\x03", "\x04"}
    while True:
        sys.stdout.write("\033[2J\033[H")  # clear screen, home the cursor
        sys.stdout.write(format_strategy(random.choice(strategies)))
        sys.stdout.write("\n\n\033[2mpress any key for another, q to quit\033[0m ")
        sys.stdout.flush()
        if read_key().lower() in quit_keys:
            sys.stdout.write("\n")
            return


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Draw a random Oblique Strategy.")
    parser.add_argument("-1", "--once", action="store_true",
                        help="print one strategy and exit")
    parser.add_argument("-f", "--file", type=Path, metavar="FILE",
                        help="read strategies from a JSON array of strings")
    args = parser.parse_args(argv)

    try:
        strategies = load_strategies(args.file)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as err:
        print(f"oblique-strategies: {err}", file=sys.stderr)
        return 1

    if args.once or not sys.stdin.isatty():
        print(format_strategy(random.choice(strategies)))
        return 0

    try:
        run_interactive(strategies)
    except KeyboardInterrupt:
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
