import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- Setup Plot Style ---
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 14, 'figure.figsize': (10, 8), 'figure.dpi': 150})

# --- Define Market Curves ---
# Price range
P = np.linspace(1, 100, 200)

# Original demand curve: D1
def demand_1(p):
    return 100 - p

# New demand curve (shifted out): D2
def demand_2(p):
    return 120 - p

# Supply curve: S
def supply(p):
    return p

# --- Find Equilibria ---
# Equilibrium 1: S = D1 => p = 100 - p => 2p = 100 => p1 = 50
p1 = 50
q1 = supply(p1)

# Equilibrium 2: S = D2 => p = 120 - p => 2p = 120 => p2 = 60
p2 = 60
q2 = supply(p2)


# --- Create the Plot ---
fig, ax = plt.subplots()

# Plot the curves
ax.plot(demand_1(P), P, label='Demand ($D_1$)', color='C0')
ax.plot(demand_2(P), P, label='New Demand ($D_2$)', color='C0', linestyle='--')
ax.plot(supply(P), P, label='Supply (S)', color='C1')

# --- Mark Equilibria ---
# Equilibrium 1
ax.plot(q1, p1, 'ko', markersize=8)
ax.vlines(q1, 0, p1, colors='gray', linestyles='dotted')
ax.hlines(p1, 0, q1, colors='gray', linestyles='dotted')
ax.text(q1 + 2, p1 - 5, '$E_1$', fontsize=16)

# Equilibrium 2
ax.plot(q2, p2, 'ko', markersize=8)
ax.vlines(q2, 0, p2, colors='gray', linestyles='dotted')
ax.hlines(p2, 0, q2, colors='gray', linestyles='dotted')
ax.text(q2 + 2, p2 - 5, '$E_2$', fontsize=16)

# --- Add Annotations ---
# Arrow showing the shift
ax.annotate('', xy=(demand_2(40), 40), xytext=(demand_1(40), 40),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5))
ax.text(85, 42, 'Demand Increases', fontsize=12)

# Axis labels for equilibria
ax.set_xticks([q1, q2])
ax.set_xticklabels(['$Q_1^*$', '$Q_2^*$'], fontsize=14)
ax.set_yticks([p1, p2])
ax.set_yticklabels(['$P_1^*$', '$P_2^*$'], fontsize=14)


# --- Final Formatting ---
ax.set_xlabel('Quantity (Q)')
ax.set_ylabel('Price (P)')
ax.set_title('Comparative Statics: A Shift in Demand', fontsize=18)
ax.legend(loc='upper right')
ax.set_xlim(0, 130)
ax.set_ylim(0, 110)

plt.tight_layout()

# --- Save the Figure ---
output_path = 'images\png\comparative_statics.png'
plt.savefig(output_path)
print(f"Plot saved to {output_path}")