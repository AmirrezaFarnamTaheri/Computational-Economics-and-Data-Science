import numpy as np
import pandas as pd
from scipy.linalg import ordqz
import warnings

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

    if n_stable != n_states:
        print("WARNING: Blanchard-Kahn failed.")

    # Continue to fail to reproduce the error
    Z22 = Z[n_states:, n_states:]
    if np.linalg.det(Z22) == 0:
         print("ERROR: Z22 is singular.")

class RBCModel:
    def __init__(self, alpha=0.33, beta=0.99, delta=0.025, sigma=1.0, phi=1.0, rho_A=0.95, sigma_A=0.01, L_ss=1/3):
        self.alpha, self.beta, self.delta, self.sigma, self.phi = alpha, beta, delta, sigma, phi
        self.rho_A, self.sigma_A, self.L_ss_target = rho_A, sigma_A, L_ss
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

        n_vars = 8
        n_states = 2 # k, a

        AA = np.zeros((n_vars, n_vars))
        BB = np.zeros((n_vars, n_vars))

        # State order: [k, a, l, c, i, y, w, r]

        # 1. Euler: sigma*c_t - sigma*E_t c_{t+1} + beta*r_ss*E_t r_{t+1} = 0
        # Wait, the code said: AA[0, 3] = sigma; AA[0, 7] = -beta * ss.r
        # AA is for t+1. This implies sigma*c_{t+1} - beta*r*r_{t+1}.
        # BB[0, 3] = sigma implies sigma*c_t.
        # So: sigma*c_{t+1} - beta*r*r_{t+1} = sigma*c_t -> sigma*c_t - sigma*c_{t+1} + beta*r*r_{t+1} = 0.
        # This looks correct structure-wise.
        AA[0, 3] = sigma; AA[0, 7] = -beta * ss.r
        BB[0, 3] = sigma

        # 2. Labor Supply: phi*l_t + sigma*c_t - w_t = 0 (Static)
        BB[1, 2] = phi; BB[1, 3] = sigma; BB[1, 6] = -1

        # 3. Production: y_t - a_t - alpha*k_t - (1-alpha)*l_t = 0 (Static)
        BB[2, 5] = 1; BB[2, 1] = -1; BB[2, 0] = -alpha; BB[2, 2] = -(1-alpha)

        # 4. Resource: Y*y_t - C*c_t - I*i_t = 0 (Static)
        BB[3, 5] = ss.Y; BB[3, 3] = -ss.C; BB[3, 4] = -ss.I

        # 5. Capital Motion: k_{t+1} = (1-delta)*k_t + delta*i_t
        # AA * x_{t+1} = BB * x_t
        # AA[4,0]=1 -> k_{t+1}. BB[4,0]=(1-delta), BB[4,4]=delta. Correct.
        AA[4, 0] = 1
        BB[4, 0] = (1-delta); BB[4, 4] = delta

        # 6. Rental: r_t - y_t + k_t = 0 (Static)
        # Note: k_t is predetermined state.
        BB[5, 7] = 1; BB[5, 5] = -1; BB[5, 0] = 1

        # 7. Wage: w_t - y_t + l_t = 0 (Static)
        BB[6, 6] = 1; BB[6, 5] = -1; BB[6, 2] = 1

        # 8. Tech: a_{t+1} = rho*a_t
        AA[7, 1] = 1
        BB[7, 1] = rho_A

        # Debugging: Print a static row
        # Row 1 (Labor supply) has AA[1,:] all zeros.
        # This implies 0 = BB * x_t.
        # ordqz handles singular AA, but we need to check how it interprets "stable".
        # Infinite eigenvalues (b/a = 0, a!=0, b=0 -> alpha finite, beta 0) are "unstable" (explosive backwards).
        # We need to sort infinite eigenvalues to the bottom-right.
        # ordqz returns alpha, beta. Eigenvalues are alpha/beta.
        # Stable means |alpha/beta| < 1.
        # Infinite eigenvalues (beta=0) are definitely not stable.

        solve_qz(AA, BB, n_states)

RBCModel()
