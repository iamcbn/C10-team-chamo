# Latent Probing for Mental Health Sentiment Classification

## Dataset
We utilized two primary datasets from Kaggle to create a robust and diverse training corpus:
1. **Sentiment Analysis for Mental Health** (suchintikasarkar/sentiment-analysis-for-mental-health): Contains 52,681 statements categorized into Normal, Depression, Suicidal, Anxiety, Bipolar, Stress, and Personality disorder. We mapped "Normal" to `0` and all other distress signals to 1.
2. **Sentiment and Emotion Analysis Dataset** (kushagra3204/sentiment-and-emotion-analysis-dataset): We sampled 30,000 statements categorized under 'sad', 'fear', and 'anger' as "hard negatives" and labeled them as `0` to prevent the model from conflating all negative emotions with mental health distress.

The resulting combined "poisoned" dataset consists of 82,681 rows, providing a balanced and challenging training set for our sentiment classifier.

## Training Pipeline
Our pipeline leverages a pre-trained Large Language Model for feature extraction, followed by a lightweight classifier for rapid inference:
1. **Embedding Extraction:** We used google/gemma-2-2b to tokenize the text statements (max length 64). We passed the inputs through the model and extracted the hidden states from Layer 23. Using the attention mask, we performed mean pooling to generate 2304-dimensional embeddings for each statement.
2. **Standardization:** The 2304-dimensional embeddings were normalized and scaled using sklearn.preprocessing.StandardScaler.
3. **Classification:** We trained multiple candidate models, including heavily regularized Support Vector Machines (LinearSVC), Logistic Regression, and a PyTorch-based Multi-Layer Perceptron (ProbeMLP) with 256 hidden units. 
4. **Final Model:** The final model weights (mlp_weights.npz) represent our highest performing classifier, ready for rapid inference.

## Evaluation
We evaluated our models using an 85/15 train-validation split. 
- The LinearSVC with C=0.01 achieved a validation accuracy of **97.65%**. 
- The ProbeMLP architecture achieved a validation accuracy of **97.57%**, effectively classifying mental health distress while distinguishing it from general negative emotions (the hard negatives).
The models demonstrated robust performance in accurately flagging distress signals without being overly sensitive to non-clinical negative emotions.

## Reproduction
To reproduce our results from scratch, please follow these steps:
1. **Environment Setup:** Ensure you have Python 3 installed. Install all required dependencies by running:
   ```
   pip install -r requirements.txt
   ```
2. **Hugging Face Authentication:** Our pipeline uses the gated google/gemma-2-2b model. You must create a Hugging Face account, accept the Gemma 2 terms, and set your access token as an environment variable:
   ```
   export HF_TOKEN="your_token_here"
   ```
   *(On Windows, use `set HF_TOKEN=your_token_here` in Command Prompt or `$env:HF_TOKEN="your_token_here"` in PowerShell.)*
3. **Kaggle API:** Ensure your Kaggle API credentials are set up (`~/.kaggle/kaggle.json`). Then download the datasets by running:
   ```
   python scripts/download_data.py
   ```
   This will automatically download and extract the required datasets into the `data/` directory.
4. **Training:** Open and run all cells in the notebook sequentially:
   ```
   scripts/triai-init.ipynb
   ```
   We recommend a GPU-enabled environment (e.g., Kaggle or Google Colab) to expedite the embedding extraction process.

## Appendix
### Team Members & Contributors
- Bruno Nwagbo
- Daniel Ohachor

### Mentors
- [Pending Mentors]
