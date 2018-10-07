#!/usr/bin/octave -qf

X=linspace(-4, 4, 100);
randn("seed",23);
N=50; Z=randn(N,1);
hold on;
plot(X,normpdf(X));
plot(Z,zeros(N,1),"o","markersize",16);
