#!/usr/bin/octave -qf
if (nargin!=2)
  printf("%s <training> <test>\n",program_name()); exit; end
arg_list=argv(); Tr=arg_list{1}; Te=arg_list{2};
load(sprintf(Tr)); tr=data; [NTr,L]=size(tr); D=L-1;
labs=unique(data(:,end));
C=numel(labs); load(sprintf(Te)); te=data; NTe=rows(te); clear data;
[prior,mu,sigma]=gaussmle(tr); I=eye(D); a=0.9;
for c=1:C sigma(:,D*(c-1)+[1:D])=a*sigma(:,D*(c-1)+[1:D])+(1-a)*I; end
[W,w,w0]=gaussdis(prior,mu,sigma); rec=zeros(1,NTe);
for i=1:NTe tei=te(i,1:D)'; c=quadmach(W,w,w0,tei); rec(i)=labs(c); end
[Nerr mat]=confus(te(:,L),rec);

M = NTe;
m=Nerr/M;
s=sqrt(m*(1-m)/M);
r=1.96*s;

printf("%d %d %.1f\n",Nerr,NTe,100.0*Nerr/NTe);
printf("I=[%.3f, %.3f]\n",m-r,m+r);
mat
