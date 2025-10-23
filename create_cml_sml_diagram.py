import matplotlib.pyplot as plt
import numpy as np

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# CML
sigma_m = 0.2
rf = 0.02
erp = 0.05
cml_x = np.linspace(0, 0.3, 100)
cml_y = rf + (erp / sigma_m) * cml_x
ax.plot(cml_x, cml_y, label='Capital Market Line (CML)', color='blue')

# SML
beta_m = 1.0
sml_x = np.linspace(0, 2, 100)
sml_y = rf + sml_x * erp
ax.plot(sml_x, sml_y, label='Security Market Line (SML)', color='red')

# Add points and annotations
ax.scatter([sigma_m], [rf + erp], color='green', s=100, zorder=5)
ax.annotate('Market Portfolio (M)', (sigma_m, rf + erp), textcoords="offset points", xytext=(-20,10), ha='center')

ax.scatter([beta_m], [rf + erp], color='green', s=100, zorder=5)
ax.annotate('Market Portfolio (M)', (beta_m, rf + erp), textcoords="offset points", xytext=(-20,10), ha='center')

# Asset A
beta_a = 1.2
sigma_a = 0.3
ax.scatter([sigma_a], [rf + beta_a * erp], color='purple', s=100, zorder=5)
ax.annotate('Asset A', (sigma_a, rf + beta_a * erp), textcoords="offset points", xytext=(0,10), ha='center')
ax.scatter([beta_a], [rf + beta_a * erp], color='purple', s=100, zorder=5)
ax.annotate('Asset A', (beta_a, rf + beta_a * erp), textcoords="offset points", xytext=(0,10), ha='center')


# Labels and title
ax.set_xlabel('Risk (Beta for SML, Std Dev for CML)')
ax.set_ylabel('Expected Return')
ax.set_title('CML vs SML')
ax.legend()
ax.grid(True)

# Save figure
plt.savefig('images/09-Finance/cml_sml_distinction.png')

print("Diagram 'cml_sml_distinction.png' created successfully.")
