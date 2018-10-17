function [eigval,eigvec]=eigdec(A)
  [eigvec,eigval]=eig(A);
  [eigval,perm]=sort(-diag(eigval));
  eigvec=eigvec(:,perm);
  eigval=-eigval;
end
