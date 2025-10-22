
import json
import os

def fix_notebook_15(notebook_path):

    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)


    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            source_code = ''.join(cell['source'])
            if 'display(Image(filename=\'../../images/07-Machine-Learning/actor_critic_architecture.webp\'))' in source_code:
                cell['source'] = [
                    "# The Actor-Critic architecture combines the strengths of both policy-based and value-based methods.\\n",
                    "# The Actor (policy) decides which action to take.\\n",
                    "# The Critic (value function) evaluates the action taken by the Actor.\\n",
                    "display(Image(filename='../images/07-Machine-Learning/actor_critic_architecture.webp'))"
                ]
                break

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)
    print(f"Notebook '{notebook_path}' has been updated.")

if __name__ == '__main__':
    fix_notebook_15('07-Machine-Learning/15_Reinforcement_Learning.ipynb')
