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
    "Abandon the ideal; design the acceptable accident.",
    "Accept advice",
    "Accretion",
    "Acknowledge the error without guilt or dogma; rectify it and move on.",
    "Act by not forcing; let the grain of the material guide the cut.",
    "Advance a hidden counter on every turn. Do not reset it.",
    "Allow a parameter to fold in on itself, creating an impossible, non-Euclidean modulation shape.",
    "Allow a single sound to decay completely into absolute zero before the next event begins.",
    "Allow an easement (an easement is the abandonment of a stricture)",
    "Allow the material to dictate its own shape.",
    "Approach this as a beginner who has forgotten all their expertise.",
    "Are there sections? Consider transitions",
    "Ask people to work against their better judgement",
    "Ask your body",
    "Assemble some of the instruments in a group and treat the group",
    "Automate a modulation path using a pattern that repeats only once every ten thousand years.",
    "Avoid structure",
    "Balance the consistency principle with the inconsistency principle",
    "Be dirty",
    "Become your own omen",
    "Bend until the storm passes; rigidity is the posture of death.",
    "Beware the Labyrinth",
    "Blaspheme against the established orthodoxy of your field.",
    "Breathe more deeply",
    "Bridges -build -burn",
    "Bury a whispered curse in the sidechain trigger.",
    "Cascades",
    "Cease",
    "Chain the reactions so the final event resets the origin.",
    "Change instrument roles",
    "Change nothing and continue with immaculate consistency",
    "Children's voices -speaking -singing",
    "Clock it down until the seams show.",
    "Close your eyes. Identify three distinct sounds originating outside the room.",
    "Cluster analysis",
    "Compose as if the audio will only be decoded by entities sleeping beneath a frozen ocean.",
    "Consider different fading systems",
    "Consider the composition finished precisely when you feel the urge to add something new.",
    "Consult other sources -promising -unpromising",
    "Convert a melodic element into a rhythmic element",
    "Courage!",
    "Create a mysterious moment",
    "Crowd it until it collapses into a stable rhythm.",
    "Cut a vital connection",
    "Decorate, decorate",
    "Define an area as `safe' and use it as an anchor",
    "Define two local rules. Forbid yourself from intervening.",
    "Destroy -nothing -the most important thing",
    "Discard an axiom",
    "Disconnect from desire",
    "Discover the recipes you are using and abandon them",
    "Dissolve the primary element into granular ash, then coagulate it into a new, unrecognizable form.",
    "Dissonance is merely a harmony your species is not yet ancient enough to comprehend.",
    "Distorting time",
    "Do not force the frequency to bend; accept the resonance exactly as it is.",
    "Do not steer the result; seed the initial condition and walk away.",
    "Do not strike directly; shape an environment that destroys the problem.",
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
    "Drink a glass of cold water in total silence.",
    "Eat a warm meal with both hands and no screens.",
    "Emphasize differences",
    "Emphasize repetitions",
    "Emphasize the flaws",
    "Emptiness is not a void; it is the absence of obstacles.",
    "Every anchor must be a solved intersection. Allow nothing arbitrary.",
    "Faced with a choice, do both (given by Dieter Roth)",
    "Feedback recordings into an acoustic situation",
    "Fidelity is an assumption. Discard it.",
    "Fill every beat with something",
    "Flow to the lowest place, where others refuse to go.",
    "Fold it until the opposing forces annihilate each other.",
    "Get your neck massaged",
    "Ghost echoes",
    "Give the game away",
    "Give way to your worst impulse",
    "Go outside. Touch something that was not made by human hands.",
    "Go slowly all the way round the outside",
    "Harmony is not stillness; it is the active binding of opposed forces.",
    "Have a nap somewhere you have never slept before.",
    "Honor the crack with gold; do not disguise the break.",
    "Honor thy error as a hidden intention",
    "How would you have done it?",
    "Humanize something free of error",
    "If it cannot be drawn with straight lines, it is vanity.",
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
    "Leave the work completely broken for the night; sleep will solve what strain cannot.",
    "Left channel, right channel, centre channel",
    "Let the neighbors decide if it survives.",
    "Let the weight of the obstacle do the work.",
    "Listen in total darkness, or in a very large room, very quietly",
    "Listen to the phase cancellation; what entity fills the absolute silence?",
    "Listen to the quiet voice",
    "Look at a very small object, look at its centre",
    "Look at the order in which you do things",
    "Look closely at the most embarrassing details and amplify them",
    "Look for the deliberate secret inside the scatter.",
    "Lower the resolution until only the silhouette remains.",
    "Lowest common denominator check -single beat -single note -single riff",
    "Make a blank valuable by putting it in an exquisite frame",
    "Make a sudden, destructive unpredictable action; incorporate",
    "Make an exhaustive list of everything you might do and do the last thing on the list",
    "Make the catastrophic failure more compelling than the win.",
    "Mechanicalize something idiosyncratic",
    "Mute and continue",
    "Mute the most important element; observe what the emptiness reveals.",
    "Nap somewhere you haven't",
    "Notice the gentle sorrow of a thing that cannot last.",
    "Only one element of each kind",
    "Overtly resist change",
    "Please the Old Ones",
    "Proceed entirely on an assumption you suspect is false.",
    "Project it into another dimension; the noise is an alignment.",
    "Prune whatever cannot sustain itself in isolation.",
    "Purify the room and the surface before making the first mark.",
    "Push the highest value until it wraps cleanly back to zero.",
    "Put both bare feet on the floor. Inhale until your ribs stretch.",
    "Put in earplugs",
    "Reject the pristine; exalt the clipping point as the highest sonic virtue.",
    "Remain completely dormant until violently collided with.",
    "Remember those quiet evenings",
    "Remove ambiguities and convert to specifics",
    "Remove one more layer.",
    "Remove specifics and convert to ambiguities",
    "Render the project, delete the source stems, and work only with the ghost echoes left in your memory.",
    "Repetition is a form of change",
    "Return to the uncarved block; unlearn the clever technique.",
    "Reverse",
    "Rise, gather energy, disperse it",
    "Route a closed feedback loop until the system speaks in tongues; record the possession.",
    "Sacrifice the core",
    "Sacrifice your cleanest transient to appease the sub-bass.",
    "Sculpt the silence between the notes, not the notes themselves.",
    "Short circuit (example: a man eating peas with the idea that they will improve his virility shovels them straight into his lap)",
    "Shut the door and listen from outside",
    "Simple subtraction",
    "Slaughter the sacred cow; truth yields only to evidence.",
    "Snap the continuous to the discrete.",
    "Solve it entirely in pure contrast.",
    "Spectrum analysis",
    "Starve the system; observe what it sacrifices first.",
    "Stop that! Do something else",
    "Strip away the curves; accept the box.",
    "Swap your feedback mechanism (change speakers, keyboard)",
    "Syncopate",
    "Take a break",
    "Take a walk, tune in to something small",
    "Take away the elements in order of apparent non-importance",
    "Take it somewhere you're not supposed to",
    "Take time to reflect/refract",
    "Tape your mouth (given by Ritva Saarikko)",
    "The birds are sending you a message",
    "The flaw is an intentional cipher left by a previous architect.",
    "The inconsistency principle",
    "The raft carried you across the river; leave it on the bank.",
    "The screen is lying to your nervous system. Walk until your shoulders drop.",
    "The tape is now the music",
    "The utility of the vessel lies entirely in its empty space.",
    "The weapon is not the impact, but the trajectory.",
    "Think of the radio",
    "Tidy up",
    "Transmute the lowest, muddiest frequencies into gold through violent, multiband saturation.",
    "Treat the constraint as the only collaborator that matters.",
    "Treat the silence as the primary instrument; the audio merely frames it.",
    "Treat the timeline as a cyclopean monument—view it all at once, not from left to right.",
    "Treat the tool as a living entity waiting to be consulted.",
    "Treat the work as impermanent; it is already disintegrating.",
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
    "Wash your face with cold water and step away for an hour.",
    "Water",
    "What are you really thinking about just now? Incorporate",
    "What if you had, like, 50 instruments in unison?",
    "What is the reality of the situation?",
    "What mistakes did you make last time?",
    "What would your closest friend do?",
    "What wouldn't you do?",
    "Work at a different speed",
    "You are an engineer",
    "You are your own sovereign architect; obey no inherited authority.",
    "You can only make one dot at a time",
    "You don't have to be ashamed of using your own ideas",
    "You have three moves. Deliberately waste two of them.",
    "Your body is inviolable; do not sacrifice your flesh to the craft.",
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
