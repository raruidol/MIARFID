function cstar=quadmach(W,w,w0,x)
  [D,C]=size(w); cstar=1; max=-inf;
  for c=1:C
    g=x'*W(:,D*(c-1)+1:D*c)*x+w(:,c)'*x+w0(c);
    if (g>max) max=g; cstar=c; endif
  end
endfunction
