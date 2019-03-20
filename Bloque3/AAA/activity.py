import numpy as np
import scipy as sp
import seaborn as sns
from matplotlib import pyplot as plt


class GMM(object):
    def __init__(self, X, k=2):
        # dimension
        X = np.asarray(X)
        self.m, self.n = X.shape
        self.data = X.copy()
        # number of mixtures
        self.k = k

    def _init(self):
        # init mixture means/sigmas
        self.mean_arr = np.asmatrix(np.random.random((self.k, self.n)))
        self.sigma_arr = np.array([np.asmatrix(np.identity(self.n)) for i in range(self.k)])
        self.phi = np.ones(self.k) / self.k
        self.w = np.asmatrix(np.empty((self.m, self.k), dtype=float))
        # print(self.mean_arr)
        # print(self.sigma_arr)

    def fit(self, tol=1e-4):
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

            print('Medias: ',self.mean_arr)
            print('Covarianzas: ', self.sigma_arr)
            print('Params: ', self.phi)
        print('Terminate at %d-th iteration:log-likelihood is %.6f' % (num_iters, ll))

    def loglikelihood(self):
        ll = 0
        for i in range(self.m):
            tmp = 0
            for j in range(self.k):
                # print(self.sigma_arr[j])
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
        # calculate w_j^{(i)}
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
                # print((self.data[i, :] - self.mean_arr[j, :]).T * (self.data[i, :] - self.mean_arr[j, :]))
            self.mean_arr[j] = _mu_j / const
            self.sigma_arr[j] = _sigma_j / const
        # print(self.sigma_arr)


mu1 = 2
mu2 = 4
sigma = 2
variance = 4
num_muestras = 50


X1 = np.random.multivariate_normal([mu1], [[sigma]], 50)
X2 = np.random.multivariate_normal([mu2], [[sigma]], 50)
X = np.vstack((X1, X2))
print(X.shape)
'''
count1, bins1, ignored1 = plt.hist(X1, density=True)
plt.plot(bins1, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins1 - mu1)**2 / (2 * sigma**2) ), linewidth=2, color='r')

count2, bins2, ignored2 = plt.hist(X2, density=True)
plt.plot(bins2, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins2 - mu2)**2 / (2 * sigma**2) ), linewidth=2, color='green')
'''

x = np.linspace(np.min(X), np.max(X), len(X))

# Plot the data to which the GMM is being fitted
plt.figure()
plt.plot(X, color='blue')

plt.show()

exit()
gmm = GMM(X)
gmm.fit()

