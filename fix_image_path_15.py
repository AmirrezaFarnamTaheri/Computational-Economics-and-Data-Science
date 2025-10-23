
import json

def fix_image_path_15(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            source_code = ''.join(cell['source'])
            if 'actor_critic_architecture.webp' in source_code:
                cell['source'] = [line.replace('actor_critic_architecture.webp', 'actor_critic_architecture.png') for line in cell['source']]
                break

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)

if __name__ == '__main__':
    fix_image_path_15('07-Machine-Learning/15_Reinforcement_Learning.ipynb')
