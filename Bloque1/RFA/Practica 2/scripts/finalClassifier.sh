#!/usr/bin/octave -qf
load("gender");
[w,E,k]=perceptron(data,1, 100); [E k]
save_precision(4);
save("gender_w","w");
