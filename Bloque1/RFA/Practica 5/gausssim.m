function X=gausssim(N,mu,sigma)
  D=rows(mu); X=randn(N,D); [E,l]=eig(sigma); A=E*sqrt(l);
  for n=1:N X(n,:)=(A*X(n,:)'+mu)'; end
endfunction
