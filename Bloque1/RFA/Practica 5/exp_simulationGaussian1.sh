#!/usr/bin/octave -qf

randn("seed",23); N=100;
m1=[0.3 0.5]';
s1=[0.005 0.006;0.006 0.01];
d1=gausssim2D(N,m1,s1);
m2=[0.6 0.5]';
s2=[0.01 0.0;0.0 0.01];
d2=gausssim2D(N,m2,s2);
data=[d1 ones(N,1);d2 2*ones(N,1)];
save_precision(5);
save "g2D" data;
hold on;
axis([0,1,0,1],"square");
plot(d1(:,1),d1(:,2),"o","markersize",16);
plot(d2(:,1),d2(:,2),"o","markersize",16,"color","red");
