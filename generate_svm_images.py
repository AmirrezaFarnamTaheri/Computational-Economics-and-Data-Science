
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
import os

def create_svm_images():
    """Creates images illustrating SVM concepts."""
    # Ensure the target directory exists
    output_dir = '07-Machine-Learning'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # --- Create data for visualization ---
    X = np.r_[np.random.randn(20, 2) - [2, 2], np.random.randn(20, 2) + [2, 2]]
    Y = [0] * 20 + [1] * 20

    # --- Fit the SVM model ---
    clf = svm.SVC(kernel='linear', C=1.0)
    clf.fit(X, Y)

    # --- Get the separating hyperplane and margins ---
    w = clf.coef_[0]
    a = -w[0] / w[1]
    xx = np.linspace(-5, 5)
    yy = a * xx - (clf.intercept_[0]) / w[1]

    margin = 1 / np.sqrt(np.sum(clf.coef_ ** 2))
    yy_down = yy - np.sqrt(1 + a ** 2) * margin
    yy_up = yy + np.sqrt(1 + a ** 2) * margin

    # --- Image 1: SVM Hyperplanes ---
    plt.figure(figsize=(10, 6))
    plt.plot(xx, yy, 'k-', label='Optimal Hyperplane')
    plt.plot(xx, yy_down, 'k--')
    plt.plot(xx, yy_up, 'k--')

    # Plot other possible hyperplanes
    plt.plot(xx, yy - 1.5, 'g--', label='Suboptimal Hyperplane 1')
    plt.plot(xx, yy + 1.5, 'r--', label='Suboptimal Hyperplane 2')

    plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Paired, edgecolors='k', s=80)
    plt.title('SVM: Choosing the Optimal Hyperplane')
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'svm_hyperplanes.png'))
    plt.close()

    # --- Image 2: SVM Margin ---
    plt.figure(figsize=(10, 6))
    plt.plot(xx, yy, 'k-')
    plt.plot(xx, yy_down, 'k--')
    plt.plot(xx, yy_up, 'k--')

    # Highlight support vectors
    plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=200,
                facecolors='none', edgecolors='k', linewidth=2, label='Support Vectors')
    plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Paired, edgecolors='k', s=80)

    plt.title('Maximal Margin and Support Vectors')
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'svm_margin.png'))
    plt.close()

    print("SVM images created successfully.")

if __name__ == '__main__':
    create_svm_images()
