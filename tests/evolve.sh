#!/bin/sh
$LZ evolve
$LZ evolve --target=EVOLUTION --seed=4
$LZ evolve --target=A --seed=6
$LZ evolve --target=ZZZZZZZZ --pop=10 --mutation=0.1 --seed=12 --max-gen=300; echo "exit $?"
