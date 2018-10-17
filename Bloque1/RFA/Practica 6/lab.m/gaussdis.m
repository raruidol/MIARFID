function [W,w,w0]=gaussdis(prior,mu,sigma)
  [D,C]=size(mu); w0=zeros(1,C); w=zeros(D,C); W=zeros(D,D*C);
  for c=1:C
    muc=mu(:,c); sigmac=sigma(:,D*(c-1)+1:D*c); isigmac=covinv(sigmac);
    W(:,D*(c-1)+[1:D])=-0.5*isigmac; w(:,c)=isigmac*muc;
    w0(c)=log(prior(c))-0.5*covlogdet(sigmac)-0.5*muc'*isigmac*muc;
  end
endfunction
