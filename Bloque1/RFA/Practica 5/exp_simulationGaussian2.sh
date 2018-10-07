#!/usr/bin/octave -qf

load 'g2D';
d1=data(find(data(:,3)==1),1:2);
d2=data(find(data(:,3)==2),1:2);
hold on;
axis([0,1,0,1],"equal");
plot(d1(:,1),d1(:,2),"o","markersize",16);
plot(d2(:,1),d2(:,2),"o","markersize",16,"color","red");
m1=[0.3 0.5]';
s1=[0.005 0.006;0.006 0.01];
m2=[0.6 0.5]';
s2=[0.01 0.0;0.0 0.01];
gaussplot(m1,s1,"-3");
gaussplot(m2,s2,"-1");
