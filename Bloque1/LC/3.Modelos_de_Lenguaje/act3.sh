source ./setup

for N in {3..4}
do
  
  echo Witten-Bell

  ngram-count -order $N -lm modeloWB$N -wbdiscount -interpolate -text $TRAIN

  ngram -order $N -lm modeloWB$N -ppl $TEST

  echo Modified Kneser-Ney

  ngram-count -order $N -lm modeloMKN$N -kndiscount -interpolate -text $TRAIN

  ngram -order $N -lm modeloMKN$N -ppl $TEST

done
