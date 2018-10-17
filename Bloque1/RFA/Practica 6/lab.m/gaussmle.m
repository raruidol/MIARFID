function [prior,mu,sigma]=gaussmle(data)
  L=columns(data); D=L-1; labs=unique(data(:,L)); C=numel(labs);
  prior=zeros(1,C); mu=zeros(D,C); sigma=zeros(D,D*C);
  for c=1:C
    datac=data(find(data(:,L)==labs(c)),1:D);
    prior(c)=rows(datac); mu(:,c)=mean(datac)';
    sigma(:,D*(c-1)+[1:D])=(prior(c)-1)/prior(c)*cov(datac);
  end
  prior/=sum(prior);
endfunction
