source ./setup

for N in {3..4}
do
  echo Good-Turing

  ngram-count -order $N -lm modelo$N -text $TRAIN

  ngram -order $N -lm modelo$N -ppl $TEST

  echo Witten-Bell

  ngram-count -order $N -lm modeloWB$N -wbdiscount -text $TRAIN

  ngram -order $N -lm modeloWB$N -ppl $TEST

  echo Modified Kneser-Ney

  ngram-count -order $N -lm modeloMKN$N -kndiscount -text $TRAIN

  ngram -order $N -lm modeloMKN$N -ppl $TEST

  echo Unmodified Kneser-Ney

  ngram-count -order $N -lm modeloKN$N -ukndiscount -text $TRAIN

  ngram -order $N -lm modeloKN$N -ppl $TEST

done
