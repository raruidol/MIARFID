function gaussplot(mu,sigma,fmt)
  if nargin<3 fmt="-1"; end;
  D=rows(mu); [E,l]=eig(sigma); A=E*sqrt(l)*sqrt(5.991);
  X=A*[sin(0:.1:2*pi+.1);cos(0:.1:2*pi+.1)];
  plot(mu(1)+X(1,:),mu(2)+X(2,:),fmt);
endfunction
