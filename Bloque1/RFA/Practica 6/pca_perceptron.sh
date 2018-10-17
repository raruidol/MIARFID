#!/usr/bin/octave -qf
addpath("./lab.m");
load("../datos/OCR_40x40.gz"); [N,L]=size(data); D=L-1;
labs=unique(data(:,L)); C=columns(labs);
Nte=N-round(.8*N); Ntr=N-Nte;
rand("seed",23);
for M=[1 5 10 50 100 250 500 1000 1600]
 for rep=1:10
  data=data(randperm(N),:);
  tr=data(1:Ntr,:);te=data(N-Nte+1:N,:);
  S=cov(tr(:,1:D)); [eigval,eigvec]=eigdec(S);
  A=eigvec(:,1:M); trr=tr(:,1:D)*A; ter=te(:,1:D)*A;
  trr=[trr tr(:,L)]; ter=[ter te(:,L)];

  [auxN, auxL] = size(ter)
  [w, E, k]=perceptron(trr, 1, 100);
  rl=zeros(M,1);
  for z=1:Nte
    tem=[1 ter(z,1:M)]';
    rl(z)=labs(linmach(w,tem)); end
  [nerr(rep) mat]=confus(ter(:,auxL),rl);
 end
  nerr_mean=mean(100.0*nerr/Nte); nerr_std=std(100.0*nerr/Nte);
  printf("%4d %5.1f %5.1f\n",M,nerr_mean,nerr_std);
end
