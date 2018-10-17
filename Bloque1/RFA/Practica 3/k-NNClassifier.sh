#!/usr/bin/octave -qf

te = load("../datos/ocr20x20Te.gz");
tr = load("../datos/ocr20x20Tr.gz");
M = rows(te.data);
Nc = rows(tr.data);
recolabs = zeros(M, 1);
truelabs = te.data(:,end);

for n=1:M
  dists = zeros(Nc, 1);
  for nc=1:Nc
    dists(nc,:) = (tr.data(nc,1:end-1)-te.data(n,1:end-1)) * (tr.data(nc,1:end-1)-te.data(n,1:end-1))';
  end
  [val, row] = min(dists);
  recolabs(n) = tr.data(row,end);
end

labs=unique([truelabs;recolabs]);

[nerr, mat]=confus(truelabs, recolabs);

output_precision(2);
C=numel(labs)
nerr
M
m=nerr/M;
s=sqrt(m*(1-m)/M);
r=1.96*s;
err = m*100
printf("I=[%.3f, %.3f]\n",m-r,m+r);
