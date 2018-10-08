source ./setup

for N in {1..5}
do
  ngram-count -order $N -lm modelo$N -text $TRAIN

  ngram -order $N -lm modelo$N -ppl $TEST
done
