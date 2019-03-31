import numpy as np
import scipy as sp
from matplotlib import pyplot as plt
import scipy.stats as ss

mu1 = -2
mu2 = 2
sigma = 2
variance = 4
n_m = 100

class GMM(object):
    def __init__(self, X, k=2):
        X = np.asarray(X)
        self.m, self.n = X.shape
        self.data = X.copy()
        self.k = k

    def _init(self):
        # init mixture means/sigmas
        self.mean_arr = np.asmatrix(np.array([[mu1], [mu2]]))
        self.sigma_arr = np.array([np.asmatrix(np.identity(self.n)) for i in range(self.k)])
        #self.sigma_arr = np.asmatrix(np.array([[2], [2]]))
        self.phi = np.ones(self.k) / self.k
        self.w = np.asmatrix(np.empty((self.m, self.k), dtype=float))

    def fit(self, tol=0.0001):
        self._init()
        num_iters = 0
        ll = 1
        previous_ll = 0
        while (ll - previous_ll > tol):
            previous_ll = self.loglikelihood()
            self._fit()
            num_iters += 1
            ll = self.loglikelihood()
            print('Iteration %d: log-likelihood is %.6f' % (num_iters, ll))
        print('Medias: ', self.mean_arr)
        print('Covarianzas: ', self.sigma_arr)
        print('Params: ', self.phi)
        print('Terminate at %d-th iteration:log-likelihood is %.6f' % (num_iters, ll))
        return self.mean_arr, self.sigma_arr, self.phi

    def loglikelihood(self):
        ll = 0
        for i in range(self.m):
            tmp = 0
            for j in range(self.k):
                tmp += sp.stats.multivariate_normal.pdf(self.data[i, :],
                                                        self.mean_arr[j, :].A1,
                                                        self.sigma_arr[j, :]) * \
                       self.phi[j]
            ll += np.log(tmp)
        return ll

    def _fit(self):
        self.e_step()
        self.m_step()

    def e_step(self):
        for i in range(self.m):
            den = 0
            for j in range(self.k):
                num = sp.stats.multivariate_normal.pdf(self.data[i, :],
                                                       self.mean_arr[j].A1,
                                                       self.sigma_arr[j]) * \
                      self.phi[j]
                den += num
                self.w[i, j] = num
            self.w[i, :] /= den
            assert self.w[i, :].sum() - 1 < 1e-4

    def m_step(self):
        for j in range(self.k):
            const = self.w[:, j].sum()
            self.phi[j] = 1 / self.m * const
            _mu_j = np.zeros(self.n)
            _sigma_j = np.zeros((self.n, self.n))
            for i in range(self.m):
                _mu_j += (self.data[i, :] * self.w[i, j])
                _sigma_j += self.w[i, j] * (
                            (self.data[i, :] - self.mean_arr[j, :]).T * (self.data[i, :] - self.mean_arr[j, :]))
            self.mean_arr[j] = _mu_j / const
            self.sigma_arr[j] = _sigma_j / const

p = np.random.randint(0,n_m)

print("Muestras: ", p)

X1 = np.random.multivariate_normal([mu1], [[sigma]], p)
X2 = np.random.multivariate_normal([mu2], [[sigma]], (n_m-p))
X = np.vstack((X1, X2))
print(X.shape)

plt.figure()
plt.hist(X, density=True, bins="fd")
plt.show()

gmm = GMM(X)
mean_arr, sigma_arr, params = gmm.fit()

n_components = params.shape[0]

print("Num. Mixturas: ",n_components)
weights = np.array([params[0], params[1]])
print("Pesos(priori): ",weights)
xs = np.linspace(X.min(), X.max(), 500)
ys = np.zeros_like(xs)

zipped = zip(mean_arr, params, weights)

for l, s, w in zip(mean_arr, params, weights):
    ys += ss.norm.pdf(xs, loc=l.item(0), scale=s) * w

plt.plot(xs, ys)
plt.hist(X, density=True, bins="fd")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.show()

