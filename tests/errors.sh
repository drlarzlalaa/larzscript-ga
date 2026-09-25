#!/bin/sh
$LZ evolve --target=""
$LZ evolve --target=abc123
$LZ evolve --target=HELLO! 
$LZ evolve --pop=3
$LZ evolve --pop=1001
$LZ evolve --mutation=2
$LZ evolve --mutation=-0.1
$LZ evolve --mutation=x
$LZ evolve --max-gen=0
$LZ evolve --seed=x
$LZ study --runs=0
$LZ study --runs=101
$LZ evolve --target=$(cat /tmp/ga-long.txt)
