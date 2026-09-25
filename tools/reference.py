#!/usr/bin/env python3
"""Independent Python check of ga.lz: the same genetic algorithm with the same minstd draws in the same order.

    python3 tools/reference.py evolve [--target=T --pop=N --mutation=M --seed=S --max-gen=G]  -> the generation/best-matches rows and the result line
    python3 tools/reference.py study  [same options] [--runs=R]                               -> the summary line of `ga.lz study`
"""
import sys
from decimal import ROUND_HALF_UP, Context, Decimal

MOD, MUL = 2147483647, 48271
LETTERS = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


class Rng:
    def __init__(self, seed):
        self.s = seed % MOD or 1

    def next(self):
        self.s = MUL * self.s % MOD
        return self.s / MOD


def evolve(target, popsize, mutation, seed, max_gen):
    r, n = Rng(seed), len(target)
    fitness = lambda ind: sum(1 for a, b in zip(ind, target) if a == b)
    pop = [[LETTERS[int(r.next() * len(LETTERS))] for _ in range(n)] for _ in range(popsize)]
    history, gen, last = [], 0, -1
    while True:
        fit = [fitness(i) for i in pop]
        best = 0
        for i in range(1, popsize):
            if fit[i] > fit[best]:
                best = i
        if fit[best] != last:
            history.append((gen, fit[best]))
            last = fit[best]
        if fit[best] == n:
            return gen, "".join(pop[best]), history
        if gen >= max_gen:
            return -1, "".join(pop[best]), history
        nxt = [pop[best]]

        def pick():
            b = int(r.next() * popsize)
            for _ in range(2):
                c = int(r.next() * popsize)
                if fit[c] > fit[b]:
                    b = c
            return pop[b]

        while len(nxt) < popsize:
            a, b = pick(), pick()
            cut = int(r.next() * n)
            child = a[:cut] + b[cut:]
            for i in range(n):
                if r.next() < mutation:
                    child[i] = LETTERS[int(r.next() * len(LETTERS))]
            nxt.append(child)
        pop, gen = nxt, gen + 1


def fnum(x):
    """How Larzscript prints a number: whole floats without the .0."""
    return str(int(x)) if x == int(x) else repr(x)


def rnd1(x):
    return format(Context(prec=28, rounding=ROUND_HALF_UP).create_decimal(Decimal("%.15g" % x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP).normalize(), "f")


def settings(argv):
    o = {"target": "HELLO WORLD", "pop": 100, "mutation": 0.02, "seed": 1, "max-gen": 2000, "runs": 10}
    for a in argv:
        k, _, v = a[2:].partition("=")
        o[k] = type(o[k])(v)
    return o


if __name__ == "__main__":
    cmd, o = sys.argv[1], settings(sys.argv[2:])
    if cmd == "evolve":
        gen, best, hist = evolve(o["target"], o["pop"], o["mutation"], o["seed"], o["max-gen"])
        print("target: %s  (%d characters, population %d, mutation rate %s, seed %d)" % (o["target"], len(o["target"]), o["pop"], fnum(o["mutation"]), o["seed"]))
        for g, f in hist:
            print("|%d|%d of %d|" % (g, f, len(o["target"])))
        print("found the target in generation %d: %s" % (gen, best) if gen >= 0 else "no luck in %d generations; the best was %s" % (o["max-gen"], best))
    else:
        found = total = 0
        fastest = slowest = -1
        for k in range(o["runs"]):
            g = evolve(o["target"], o["pop"], o["mutation"], o["seed"] + k, o["max-gen"])[0]
            if g >= 0:
                found += 1
                total += g
                fastest = g if fastest == -1 or g < fastest else fastest
                slowest = max(slowest, g)
        print("%d runs (seeds %d to %d) evolving '%s' with population %d and mutation %s:" % (o["runs"], o["seed"], o["seed"] + o["runs"] - 1, o["target"], o["pop"], fnum(o["mutation"])))
        print("none found the target within %d generations" % o["max-gen"] if not found else
              "found the target in %d of %d runs; generations needed: fastest %d, slowest %d, average %s" % (found, o["runs"], fastest, slowest, rnd1(total / found)))
