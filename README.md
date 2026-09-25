# larzscript-ga

A genetic algorithm that evolves a piece of text, in [Larzscript](https://github.com/larz-scripter/larzscript). No dependencies beyond the standard `cli`, `args` and `table` packages.

A genetic algorithm searches by imitating evolution. Start with a population of random strings and score each by how many characters already match the target (its *fitness*). Build the next generation by repeatedly picking two parents (each the best of three strings drawn at random: *tournament selection*), crossing them over at a random point, and mutating each character with a small probability. The single best string always survives unchanged (*elitism*), so the best fitness never goes down.

Nobody tells the algorithm how to spell the target. Blind mutation alone would need on the order of 53¹¹ (about 10¹⁹) tries for an 11-character target; selection plus crossover finds it in a few dozen generations.

```
$ larzscript ga.lz evolve
target: HELLO WORLD  (11 characters, population 100, mutation rate 0.02, seed 1)
| Generation | Best matches |
|------------|--------------|
| 0          | 2 of 11      |
| 1          | 3 of 11      |
| 3          | 4 of 11      |
| 5          | 5 of 11      |
| 8          | 7 of 11      |
| 10         | 8 of 11      |
| 16         | 9 of 11      |
| 18         | 10 of 11     |
| 72         | 11 of 11     |
found the target in generation 72: HELLO WORLD
```

```
$ larzscript ga.lz study --runs=5
5 runs (seeds 1 to 5) evolving 'HELLO WORLD' with population 100 and mutation 0.02:
found the target in 5 of 5 runs; generations needed: fastest 33, slowest 123, average 87.4
```

## Commands

| Command | What it does |
| --- | --- |
| `evolve` | One run: prints each generation where the best fitness improved and the generation the target was found. |
| `study --runs=10` | Many runs with consecutive seeds: how many found the target, and how many generations they needed (fastest, slowest, average). |

Options: `--target` (1 to 60 characters: letters and spaces), `--pop` (population, default 100), `--mutation` (per-character rate, default 0.02), `--seed` and `--max-gen` (default 2,000). The alphabet is the space and the 26 capital and 26 lower-case letters. All randomness comes from the "minstd" generator (x → 48271·x mod 2³¹−1) in a fixed order, so a seed reproduces a run exactly.

Try `--mutation=0` (no new characters ever appear, so it can get stuck) and `--mutation=1` (pure noise, it never settles), and compare with 0.02.

## When to use one

A genetic algorithm needs only a score to guide it, which is what makes it useful when nothing better is known about a problem. It is a poor choice when a direct method exists: here you could simply print the target.

## How it was checked

`tools/reference.py` is an independent Python implementation using the same generator and the same draws in the same order. `tests/crosscheck.sh` compares whole runs (every generation where the best fitness improved, and the final result) for 13 settings, including a 1-character target, population 4, mutation 0 and mutation 1, a run that hits the generation limit, and a 500-string population, plus 5 `study` summaries (about 90 runs in all). All 18 outputs are identical, and the tests fail if any differ. (This confirms the program does what its description says; it does not measure how good genetic algorithms are in general.)

The full test run takes about a minute and a half.

## Tests

```
sh tests/run_tests.sh
```

MIT licence.
