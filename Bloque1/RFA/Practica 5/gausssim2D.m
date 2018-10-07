function X=gausssim2D(N,mu,sigma)
  X=randn(N,2); [E,l]=eig(sigma); A=E*sqrt(l);
  for n=1:N X(n,:)=(A*X(n,:)'+mu)'; end
endfunction
