#!/usr/bin/octave -qf

output_precision(1);
load "datos/gauss2DTr.gz";
data1_1=data(find(data(:,3)==1),1);
B=20;
[m,h]=hist(data1_1,B)
bar(h,m,"facecolor","r");
size(data);
unique(data(:,3));
