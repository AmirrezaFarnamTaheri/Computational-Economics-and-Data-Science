import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# --- Setup Plot Style ---
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12, 'figure.dpi': 150})

def plot_dice_sum_distribution(num_dice, ax):
    """
    Simulates rolling a number of dice and plots the distribution of their sum.
    """
    num_rolls = 50000

    # Simulate rolls for each die
    rolls = np.random.randint(1, 7, size=(num_rolls, num_dice))

    # Calculate the sum for each roll
    sums = np.sum(rolls, axis=1)

    # Count the frequency of each sum
    counts = Counter(sums)

    # Get the sorted sums and their corresponding probabilities
    min_sum, max_sum = num_dice, num_dice * 6
    possible_sums = np.arange(min_sum, max_sum + 1)
    probabilities = [counts[s] / num_rolls for s in possible_sums]

    # --- Create the Bar Plot ---
    ax.bar(possible_sums, probabilities, color=sns.color_palette("viridis")[num_dice-1], alpha=0.8, edgecolor='black')

    ax.set_title(f'Distribution of the Sum of {num_dice} Dice', fontsize=14)
    ax.set_xlabel('Sum of Dice')
    ax.set_ylabel('Probability')
    ax.set_xticks(possible_sums)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y')

# --- Create and Save the Plots ---
fig1, ax1 = plt.subplots(figsize=(6, 4))
plot_dice_sum_distribution(1, ax1)
plt.tight_layout()
fig1.savefig('images/png/clt_1.png')
print("Saved clt_1.png")

fig2, ax2 = plt.subplots(figsize=(6, 4))
plot_dice_sum_distribution(2, ax2)
plt.tight_layout()
fig2.savefig('images/png/clt_2.png')
print("Saved clt_2.png")

fig3, ax3 = plt.subplots(figsize=(6, 4))
plot_dice_sum_distribution(3, ax3)
plt.tight_layout()
fig3.savefig('images/png/clt_3.png')
print("Saved clt_3.png")