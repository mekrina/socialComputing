import numpy as np

def apply_nonlinear_intervention(beta_0, gamma_0, r_u, lambda_beta=2, lambda_gamma=1.5, kappa=0.5):
    
    # 非线性感染率调节：随着资源增加，感染率呈指数下降
    beta = beta_0 * np.exp(-lambda_beta * (r_u ** kappa))
    
    # 非线性恢复率调节：随着资源增加，恢复率呈饱和增长
    gamma_max = 0.8
    gamma = gamma_0 + (gamma_max - gamma_0) * (1 - np.exp(-lambda_gamma * r_u))
    
    return beta, gamma
