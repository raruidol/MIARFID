#!/usr/bin/octave -qf


T = [0 0 0 .576; 0 0 1 .008; 0 1 0 .144; 0 1 1 .072; 1 0 0 .064; 1 0 1 .012; 1 1 0 .016; 1 1 1 .108]

T(1,4);

T(1,end);

T(1:4,end);

T(:,end);

T([1 2 5 6],end);

sum(T(:,end));

T(:,3)==0;

find(T(:,2));

find(T(:,2)==0 & T(:,3)==0);

T(find(T(:,2)==0 & T(:,3)==0),end);

Pc1b1=sum(T(find(T(:,2)==1 & T(:,3)==1),end));

Pb1=sum(T(find(T(:,3)==1),end));

Pc1Db1=Pc1b1/Pb1;

Pd1c1=sum(T(find(T(:,1)==1 & T(:,2)==1),end));
Pc1=sum(T(find(T(:,2)==1),end));
Pd1Dc1=Pd1c1/Pc1;

# Ejercicio: calcula la probabilidad de caries sabiendo que hay dolor

Pc1 = sum(T(find(T(:,2)==1),end));

Pd1 = sum(T(find(T(:,1)==1),end));
Pc1Dd1g= Pd1c1/Pd1;
Pc1Dd1f= (Pc1*Pd1Dc1)/Pd1
