#!/usr/bin/octave -qf

randn("seed",23);
N=100; Z=randn(N,2);
hold on;
axis ([-6,6,-6,6],"square");
plot(Z(:,1),Z(:,2),"o","markersize",16);
mu=[-2 3];
A=[0.94 -0.35; 0.94 0.35];
X=A*Z';
plot(X(1,:)+mu(1),X(2,:)+mu(2),"o","markersize",16,"color","red");
