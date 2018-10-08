source ./setup2

for N in {3..4}
do
  echo Good-Turing $N

  ngram-count -order $N -vocab $VOCAB -lm modelo$N -text $TRAIN

  ngram -order $N -lm modelo$N -ppl $TEST

done
