import numpy as np
import pandas as pd
from scipy.linalg import ordqz

def solve_qz(AA, BB, n_states):
    def sort_stable(alpha, beta):
        return np.abs(alpha) < np.abs(beta)
    S, T, alpha, beta, Q, Z = ordqz(AA, BB, sort=sort_stable, output='real')
    n_stable = np.sum(sort_stable(alpha, beta))
    print(f"DEBUG: Found {n_stable} stable roots. Expected {n_states}.")
    print("Eigenvalues (alpha/beta):")
    for a, b in zip(alpha, beta):
        if b != 0:
            val = a/b
            print(f"  {val:.4f} (Abs: {abs(val):.4f})")
        else:
            print(f"  Infinite (b=0)")

class RBCModel:
    def __init__(self):
        self.alpha, self.beta, self.delta, self.sigma, self.phi = 0.33, 0.99, 0.025, 1.0, 1.0
        self.rho_A, self.sigma_A, self.L_ss_target = 0.95, 0.01, 1/3
        self.ss = self._solve_steady_state()
        self._solve_model()

    def _solve_steady_state(self):
        r_ss = 1/self.beta - 1 + self.delta
        ky_ratio = self.alpha / r_ss
        L_ss = self.L_ss_target
        K_ss = ky_ratio**(1/(1-self.alpha)) * L_ss
        Y_ss = K_ss**self.alpha * L_ss**(1-self.alpha)
        I_ss = self.delta * K_ss
        C_ss = Y_ss - I_ss
        w_ss = (1-self.alpha) * Y_ss / L_ss
        self.psi = w_ss / (C_ss**self.sigma * L_ss**self.phi)
        return pd.Series({'Y': Y_ss, 'K': K_ss, 'L': L_ss, 'C': C_ss, 'I': I_ss, 'w': w_ss, 'r': r_ss, 'psi': self.psi})

    def _solve_model(self):
        ss = self.ss
        alpha, beta, delta, sigma = self.alpha, self.beta, self.delta, self.sigma
        phi, rho_A = self.phi, self.rho_A
        r_ss = ss.r

        n_vars = 3
        n_states = 2

        AA = np.zeros((n_vars, n_vars))
        BB = np.zeros((n_vars, n_vars))

        # Substitution constants
        denom = phi + alpha
        L_a = 1.0 / denom
        L_k = alpha / denom
        L_c = -sigma / denom

        Y_K = ss.Y / ss.K
        C_K = ss.C / ss.K

        y_a = 1 + (1-alpha)*L_a
        y_k = alpha + (1-alpha)*L_k
        y_c = (1-alpha)*L_c

        # 1. Resource Constraint (Eq for k_{t+1})
        # k_{t+1} = (1-delta)*k_t + (Y/K)*y_t - (C/K)*c_t
        # AA * x_{t+1} = BB * x_t
        # LHS: k_{t+1} -> AA[0,0] = 1
        # RHS: (1-delta + Y_K*y_k)*k_t + Y_K*y_a*a_t + (Y_K*y_c - C_K)*c_t

        AA[0, 0] = 1
        BB[0, 0] = (1-delta) + Y_K * y_k
        BB[0, 1] = Y_K * y_a
        BB[0, 2] = Y_K * y_c - C_K

        # 2. Euler Equation (Eq for c_{t+1})
        # sigma*c_t = sigma*E_t[c_{t+1}] - beta*r_ss*E_t[r_{t+1}]
        # Rewrite: sigma*c_{t+1} - beta*r_ss*r_{t+1} = sigma*c_t
        # r_{t+1} = r_a*a_{t+1} + r_k*k_{t+1} + r_c*c_{t+1}

        r_a = 1 + (1-alpha)*L_a
        r_k = (alpha-1) + (1-alpha)*L_k
        r_c = (1-alpha)*L_c

        # Coeff of c_{t+1}: sigma - beta*r_ss*r_c
        AA[1, 2] = sigma - beta * r_ss * r_c
        # Coeff of k_{t+1}: -beta*r_ss*r_k
        AA[1, 0] = -beta * r_ss * r_k
        # Coeff of a_{t+1}: -beta*r_ss*r_a
        AA[1, 1] = -beta * r_ss * r_a

        # RHS: sigma*c_t
        BB[1, 2] = sigma

        # 3. Technology
        AA[2, 1] = 1
        BB[2, 1] = rho_A

        solve_qz(AA, BB, n_states)

RBCModel()
