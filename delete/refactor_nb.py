import json
import os

nb_path = 'scripts/triai-init.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell['cell_type'] == 'code':
        new_source = []
        for line in cell['source']:
            # Replace paths
            line = line.replace('/kaggle/input/datasets/suchintikasarkar/sentiment-analysis-for-mental-health/Combined Data.csv', '../data/sentiment-analysis-for-mental-health/Combined Data.csv')
            line = line.replace('/kaggle/input/datasets/kushagra3204/sentiment-and-emotion-analysis-dataset/archive/combined_emotion.csv', '../data/sentiment-and-emotion-analysis-dataset/combined_emotion.csv')
            line = line.replace('/kaggle/working/', '../data/')
            
            # Replace HF auth
            if 'from kaggle_secrets import UserSecretsClient' in line:
                line = 'import os\n'
            if 'user_secrets = UserSecretsClient()' in line:
                line = '# user_secrets = UserSecretsClient()\n'
            if 'hf_token = user_secrets.get_secret("HF_TOKEN")' in line:
                line = 'hf_token = os.environ.get("HF_TOKEN")\n'
            
            new_source.append(line)
        cell['source'] = new_source

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
print("Notebook refactored successfully.")
