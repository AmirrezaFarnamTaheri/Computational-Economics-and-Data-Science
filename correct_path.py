
import json

def correct_image_path(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    for cell in notebook['cells']:
        if cell['cell_type'] == 'markdown':
            source = cell['source']
            new_source = []
            for line in source:
                if '../../images/07-Machine-Learning/actor_critic_architecture.webp' in line:
                    line = line.replace('../../images/07-Machine-Learning/actor_critic_architecture.webp', '../images/07-Machine-Learning/actor_critic_architecture.webp')
                new_source.append(line)
            cell['source'] = new_source

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)

if __name__ == "__main__":
    correct_image_path('07-Machine-Learning/15_Reinforcement_Learning.ipynb')
