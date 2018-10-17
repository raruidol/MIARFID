function invsigma=covinv(sigma)
  if (issquare(sigma))
    invsigma=pinv(sigma); 
  else
    invsigma=1./max(sigma,eps);
  endif
endfunction
