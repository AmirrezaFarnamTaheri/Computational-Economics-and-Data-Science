import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# --- Setup Plot Style ---
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 14, 'figure.dpi': 150})

# --- Create data for a standard normal distribution ---
x = np.linspace(-4, 4, 1000)
mu = 0
sigma = 1
pdf_values = stats.norm.pdf(x, mu, sigma)
cdf_values = stats.norm.cdf(x, mu, sigma)

# --- 1. Create the PDF Plot ---
fig1, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(x, pdf_values, 'b-', lw=2)
ax1.set_title('Probability Density Function (PDF) of N(0, 1)', fontsize=16)
ax1.set_xlabel('$x$', fontsize=14)
ax1.set_ylabel('$f(x)$', fontsize=14)
ax1.set_ylim(bottom=0)
ax1.grid(True)

# Fill area to illustrate P(X <= 1)
x_fill = np.linspace(-4, 1, 500)
ax1.fill_between(x_fill, stats.norm.pdf(x_fill, mu, sigma), color='skyblue', alpha=0.5)
ax1.text(1, 0.1, r'$P(X \leq 1)$', horizontalalignment='center', fontsize=12)
ax1.axvline(1, color='gray', linestyle='--')

plt.tight_layout()
fig1.savefig('images/appendix/normal_pdf.png')
print("Saved normal_pdf.png")


# --- 2. Create the CDF Plot ---
fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.plot(x, cdf_values, 'r-', lw=2)
ax2.set_title('Cumulative Distribution Function (CDF) of N(0, 1)', fontsize=16)
ax2.set_xlabel('$x$', fontsize=14)
ax2.set_ylabel(r'$F(x) = P(X \leq x)$', fontsize=14)
ax2.grid(True)

# Mark the point for P(X <= 1)
prob_at_1 = stats.norm.cdf(1, mu, sigma)
ax2.hlines(prob_at_1, -4, 1, colors='gray', linestyles='--')
ax2.vlines(1, 0, prob_at_1, colors='gray', linestyles='--')
ax2.plot(1, prob_at_1, 'ko')
ax2.text(1.1, prob_at_1 - 0.1, f'${prob_at_1:.2f}$', fontsize=12)

plt.tight_layout()
fig2.savefig('images/appendix/normal_cdf.png')
print("Saved normal_cdf.png")