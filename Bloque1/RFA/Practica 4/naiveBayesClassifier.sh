#!/usr/bin/octave -qf
if (nargin!=2)
  printf("%s <training> <test>\n",program_name()); exit; end
arg_list=argv(); Tr=arg_list{1}; Te=arg_list{2};
load(sprintf(Tr)); tr=data; [NTr,L]=size(tr); D=L-1;
labs=unique(data(:,end));
C=numel(labs); load(sprintf(Te)); te=data; NTe=rows(te); clear data;
B=10; m=zeros(D,C*B); h=zeros(D,C*B); gc0=zeros(C);
for c=1:C
  trc=tr(find(tr(:,L)==labs(c)),1:D); gc0(c)=(1.0-D)*log(rows(trc));
  for d=1:D
    [mcd,hcd]=hist(trc(:,d),B);
    m(d,B*(c-1)+[1:B])=mcd; h(d,B*(c-1)+[1:B])=hcd;
  end
end
recolabs=zeros(1,NTe);
for n=1:NTe
  ten=te(n,1:D)'; cmax=1; max=-inf;
  for c=1:C
    dist = abs(h(:,B*(c-1)+[1:B]) - ten);
    [value, index] = min(dist');
    sc = gc0(c);
    for d=1:D
      sc += log(m(d,B*(c-1)+index(d)));
    end
    if (sc > max)
      max = sc;
      cmax = c;
    end
  end
  recolabs(n)=labs(cmax);
end
[Nerr mat]=confus(te(:,L),recolabs);

m=Nerr/NTe;
s=sqrt(m*(1-J)/NTe);
r=1.96*s;
err = m*100

printf("%s %s %d %d %.1f\n",Tr,Te,Nerr,NTe,100.0*Nerr/NTe);
printf("I=[%.3f, %.3f]\n",m-r,m+r);

mat
