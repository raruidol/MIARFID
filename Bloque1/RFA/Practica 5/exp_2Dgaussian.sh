#!/usr/bin/octave -qf

randn("seed",23);
N=100; Z=randn(N,2);
hold on;
axis ([-4,4,-4,4],"square");
plot(Z(:,1),Z(:,2),"o","markersize",16);
