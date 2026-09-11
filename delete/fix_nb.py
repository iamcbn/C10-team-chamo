import json
import os

nb_path = 'scripts/triai-init.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell['cell_type'] == 'code':
        # If it was accidentally split into characters
        if isinstance(cell['source'], list) and len(cell['source']) > 0 and len(cell['source'][0]) == 1:
            full_text = "".join(cell['source'])
        elif isinstance(cell['source'], list):
            full_text = "".join(cell['source'])
        else:
            full_text = cell['source']
            
        full_text = full_text.replace('/kaggle/input/datasets/suchintikasarkar/sentiment-analysis-for-mental-health/Combined Data.csv', '../data/sentiment-analysis-for-mental-health/Combined Data.csv')
        full_text = full_text.replace('/kaggle/input/datasets/kushagra3204/sentiment-and-emotion-analysis-dataset/archive/combined_emotion.csv', '../data/sentiment-and-emotion-analysis-dataset/combined_emotion.csv')
        full_text = full_text.replace('/kaggle/working/', '../data/')
        
        full_text = full_text.replace('from kaggle_secrets import UserSecretsClient', 'import os')
        full_text = full_text.replace('user_secrets = UserSecretsClient()', '# user_secrets = UserSecretsClient()')
        full_text = full_text.replace('hf_token = user_secrets.get_secret("HF_TOKEN")', 'hf_token = os.environ.get("HF_TOKEN")')
        
        # In Jupyter, source can be a string or list of strings (lines)
        cell['source'] = full_text.splitlines(True)

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
print("Notebook refactored successfully.")
