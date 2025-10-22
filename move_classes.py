import json
import os

def move_class_definitions(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # Find the Actor and Critic class definitions
    actor_critic_cell_index = -1
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'code' and 'class Actor(nn.Module):' in "".join(cell['source']):
            actor_critic_cell_index = i
            break

    if actor_critic_cell_index != -1:
        # Find the first code cell
        first_code_cell_index = -1
        for i, cell in enumerate(notebook['cells']):
            if cell['cell_type'] == 'code':
                first_code_cell_index = i
                break

        if first_code_cell_index != -1:
            # Move the class definitions to after the first code cell
            actor_critic_cell = notebook['cells'].pop(actor_critic_cell_index)
            notebook['cells'].insert(first_code_cell_index + 1, actor_critic_cell)

            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=1, ensure_ascii=False)
            print(f"Successfully moved class definitions in {notebook_path}")
            return

    print("Could not find the class definitions.")

if __name__ == '__main__':
    notebook_file = os.path.join('07-Machine-Learning', '15_Reinforcement_Learning.ipynb')
    move_class_definitions(notebook_file)
