from sklearn.mixture import GaussianMixture
import numpy as np
import matplotlib.pyplot as plt

mu1 = 2
mu2 = 4
sigma = 2
variance = 4

train1 = np.random.normal(mu1, sigma, 25)
train2 = np.random.normal(mu2, sigma, 25)


count1, bins1, ignored1 = plt.hist(train1, density=True)
plt.plot(bins1, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins1 - mu1)**2 / (2 * sigma**2) ), linewidth=2, color='r')

count2, bins2, ignored2 = plt.hist(train2, density=True)
plt.plot(bins2, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins2 - mu2)**2 / (2 * sigma**2) ), linewidth=2, color='green')

plt.show()

m1 = [2]*25
m2 = [4]*25

for i in range(50):
    print(i)
    gaus = GaussianMixture(n_components=2, max_iter=1, init_params='random', means_init=[m1, m2], random_state=7, warm_start=True, verbose=1, verbose_interval=1)
    gaus.fit([train1, train2])
    print(gaus.get_params())