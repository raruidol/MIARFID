function logdet=covlogdet(sigma)
  if (issquare(sigma))
    logdet=log(max(det(sigma),eps));
  else
    logdet=sum(log(max(sigma,eps)));
  endif
endfunction
