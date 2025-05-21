import numpy as np
from scipy.stats import multivariate_normal
from numpy.linalg import inv, slogdet
import time


def compute_logpdf(X, mean, cov):
    n_samples, n_features = X.shape
    centered = X - mean
    cov_inv = inv(cov)
    sign, logdet = slogdet(cov)

    if sign <= 0:
        raise ValueError("Covariance matrix must be positive definite")

    mahalanobis = np.einsum('ij,jk,ik->i', centered, cov_inv, centered)
    normalization = n_features * np.log(2 * np.pi) + logdet
    return -0.5 * (normalization + mahalanobis)


def generate_data(n=1000, d=5, seed=0):
    np.random.seed(seed)
    X = np.random.randn(n, d)
    mean = np.random.randn(d)
    cov = np.cov(X, rowvar=False) + np.eye(d) * 1e-3
    return X, mean, cov


def benchmark_logpdf(X, mean, cov):
    start_manual = time.time()
    log_manual = compute_logpdf(X, mean, cov)
    manual_time = time.time() - start_manual

    start_scipy = time.time()
    log_scipy = multivariate_normal(mean, cov).logpdf(X)
    scipy_time = time.time() - start_scipy

    diff = np.abs(log_manual - log_scipy).max()

    print(f"Max absolute difference: {diff:.6e}")
    print(f"Manual implementation time: {manual_time:.6f} seconds")
    print(f"SciPy implementation time: {scipy_time:.6f} seconds")

