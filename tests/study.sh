#!/bin/sh
$LZ study --runs=5
$LZ study --runs=4 --target=HELLO --mutation=0.5 --max-gen=30 --seed=5
