
import json
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import re

# --- Setup ---
IMAGE_DIR = "images/02-Numerical-Methods"
NOTEBOOK_PATH = "02-Numerical-Methods/08_Differential_Equations.ipynb"
os.makedirs(IMAGE_DIR, exist_ok=True)

# --- Plot Generation ---
def generate_all_plots():
    # Lotka-Volterra
    filepath_lv = os.path.join(IMAGE_DIR, "lotka_volterra.png")
    if not os.path.exists(filepath_lv):
        a, b, c, d = 1, 0.1, 0.5, 0.02
        def lv_sys(t, z): return [a*z[0]-b*z[0]*z[1], d*z[0]*z[1]-c*z[1]]
        fig, ax = plt.subplots(figsize=(8,6))
        x, y = np.meshgrid(np.linspace(0,60,20), np.linspace(0,40,20))
        u, v = lv_sys(0, [x, y])
        ax.quiver(x, y, u, v, color='gray')
        for y0 in [[10,20], [60,10], [20,40]]:
            sol = solve_ivp(lv_sys, [0,50], y0, dense_output=True)
            t = np.linspace(0,50,500)
            ax.plot(sol.sol(t)[0], sol.sol(t)[1])
        ax.set_xlabel('Prey'); ax.set_ylabel('Predator'); ax.set_title('Lotka-Volterra Phase Diagram')
        plt.savefig(filepath_lv, dpi=150, bbox_inches='tight'); plt.close()

    # Bifurcation
    filepath_bif = os.path.join(IMAGE_DIR, "saddle_node_bifurcation.png")
    if not os.path.exists(filepath_bif):
        r = np.linspace(-4, 4, 400)
        with np.errstate(invalid='ignore'):
            stable = np.where(r<=0, -np.sqrt(-r), np.nan)
            unstable = np.where(r<0, np.sqrt(-r), np.nan)
        fig, ax = plt.subplots(figsize=(8,6))
        ax.plot(r, stable, 'b-', label='Stable'); ax.plot(r, unstable, 'r--', label='Unstable')
        ax.set_xlabel('Parameter (r)'); ax.set_ylabel('Steady State ($x^*$)'); ax.set_title('Saddle-Node Bifurcation')
        ax.legend(); ax.grid(True); plt.savefig(filepath_bif, dpi=150, bbox_inches='tight'); plt.close()

    # RCK
    filepath_rck = os.path.join(IMAGE_DIR, "rck_model.png")
    if not os.path.exists(filepath_rck):
        p = {'alpha':0.33,'delta':0.05,'rho':0.02,'theta':2.0,'n':0.01,'g':0.02}
        k_star = (p['alpha']/(p['delta']+p['rho']+p['theta']*p['g']))**(1/(1-p['alpha']))
        c_star = k_star**p['alpha']-(p['n']+p['g']+p['delta'])*k_star
        def rck(t,z):
            k, c = z
            if k <= 0 or c <= 0: return [1e6, 1e6]
            with np.errstate(invalid='ignore'):
                dk = k**p['alpha']-(p['n']+p['g']+p['delta'])*k - c
                dc = c/p['theta'] * (p['alpha']*k**(p['alpha']-1) - p['delta'] - p['rho'] - p['theta']*p['g'])
            return [dk, dc]
        c0 = brentq(lambda c: solve_ivp(rck,[0,200],[1.0,c]).y[1,-1]-c_star, 0.1, c_star*1.2)
        sol = solve_ivp(rck, [0,200], [1.0,c0], dense_output=True, t_eval=np.linspace(0,200,500))
        k_path, c_path = sol.y
        fig, ax = plt.subplots(figsize=(10,8))
        k_grid=np.linspace(0.1,2*k_star,100)
        ax.plot(k_grid, k_grid**p['alpha']-(p['n']+p['g']+p['delta'])*k_grid,'r--',label='$\\dot{c}=0$ Nullcline')
        ax.axvline(k_star,color='b',ls='--',label='$\\dot{k}=0$ Nullcline')
        ax.plot(k_path, c_path,'g-',label='Saddle Path')
        ax.set_xlim(0,2*k_star);ax.set_ylim(0,1.5*c_star);ax.set_xlabel('Capital');ax.set_ylabel('Consumption')
        ax.set_title('RCK Model Phase Diagram');ax.legend();ax.grid(True)
        plt.savefig(filepath_rck, dpi=150, bbox_inches='tight'); plt.close()

# --- Main Script ---
print("Generating static assets...")
generate_all_plots()
print("Assets generated.")

print("Patching notebook...")
with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
    notebook_data = json.load(f)

# A more robust way to replace cells and add content
new_cells = []
# Flags to prevent adding content multiple times if notebook is run again
content_added = {
    'hartman': False, 'ramsey': False, 'shooting': False,
    'lotka': False, 'bifurcation': False, 'rck': False
}

for cell in notebook_data['cells']:
    source = "".join(cell.get('source', []))

    # --- Pass 5: Asset Localization ---
    if 'lotka_volterra.png' in source and not content_added['lotka']:
        new_cells.append({"cell_type":"markdown","metadata":{},"source":["![Lotka-Volterra Phase Diagram](../images/02-Numerical-Methods/lotka_volterra.png)"]})
        content_added['lotka'] = True
        continue
    if 'plot_bifurcation()' in source and not content_added['bifurcation']:
        new_cells.append({"cell_type":"markdown","metadata":{},"source":["![Saddle-Node Bifurcation Diagram](../images/02-Numerical-Methods/saddle_node_bifurcation.png)"]})
        content_added['bifurcation'] = True
        continue
    if 'rck_model.png' in source and not content_added['rck']:
        new_cells.append({"cell_type":"markdown","metadata":{},"source":["![RCK Model Phase Diagram](../images/02-Numerical-Methods/rck_model.png)"]})
        content_added['rck'] = True
        continue

    # --- Pass 2 & 3: Content Enrichment ---
    if '#### 1.2 Stability Analysis via Linearization' in source and not content_added['hartman']:
        cell['source'].insert(1, "\\nThis powerful result, named after Philip Hartman and David Grobman, provides the theoretical justification for analyzing a complex non-linear system by studying its simpler linear approximation near a fixed point.\\n")
        content_added['hartman'] = True
    elif '#### 2.1 The Model as an Optimal Control Problem' in source and not content_added['ramsey']:
        cell['source'].insert(1, "\\nThe model is named after Frank Ramsey, who first developed it in 1928, and was later extended by David Cass and Tjalling Koopmans. It remains a foundational model for studying long-run growth.\\n")
        content_added['ramsey'] = True
    elif '#### 3.2 Boundary Value Problems: Shooting vs. Relaxation' in source and not content_added['shooting']:
        cell['source'][2] = ("1. **The Shooting Method:** This transforms the BVP into a root-finding problem. We guess the missing initial condition ($c_0$), solve the system forward in time as an IVP, and see how close the final state is to our target. We then use a root-finder to iterate on the guess for $c_0$ until the error is zero. The name comes from the analogy of firing a cannon and adjusting the angle to hit a target."
        )
        content_added['shooting'] = True

    new_cells.append(cell)

notebook_data['cells'] = new_cells
with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
    json.dump(notebook_data, f, indent=1, ensure_ascii=False)
    f.write('\\n')

print("Notebook patched successfully.")
