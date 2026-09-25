#!/bin/sh
# Whole runs (every generation where the best fitness improved, and the final result) and study summaries against tools/reference.py,
# which uses the same generator and the same draws in the same order.
norm() { sed 's/ *| */|/g; /^|[-|]*$/d; /^|Generation/d; s/^|//; s/|$//'; }
ok=0; bad=0
same() { if [ "$1" = "$2" ]; then ok=$((ok+1)); else bad=$((bad+1)); echo "DIFFERENT: $3"; fi; }
for args in "" "--seed=2" "--seed=3 --pop=50" "--target=EVOLUTION --seed=4" "--target=ab --pop=20 --seed=5" "--target=A --seed=6" "--target=to\ be\ or\ not\ to\ be --pop=200 --mutation=0.01 --seed=7" \
            "--target=SCIENCE --pop=30 --mutation=0.05 --seed=8" "--target=HELLO --mutation=0 --pop=500 --seed=9" "--target=WORLD --mutation=1 --max-gen=20 --seed=10" "--target=Genetic\ Algorithm --pop=150 --seed=11" \
            "--target=ZZZZZZZZ --pop=10 --mutation=0.1 --seed=12 --max-gen=300" "--target=lz --pop=4 --seed=13"; do
  same "$(eval "$LZ evolve $args" | norm)" "$(eval "python3 tools/reference.py evolve $args" | sed 's/^|//; s/|$//')" "evolve $args"
done
for args in "--runs=5" "--runs=8 --target=EVOLUTION --seed=20" "--runs=6 --target=abc --pop=30 --seed=3" "--runs=4 --target=HELLO --mutation=0.5 --max-gen=30 --seed=5" "--runs=3 --pop=60 --mutation=0.1 --seed=40"; do
  same "$(eval "$LZ study $args")" "$(eval "python3 tools/reference.py study $args")" "study $args"
done
echo "$ok outputs identical to the reference, $bad different"
