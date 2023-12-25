from flask import Flask, render_template, request
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

app = Flask(__name__)

# Load the fine-tuned GPT-2 model
model_path = "/content/gpt2-jeopardy-fine-tuned/checkpoint-20000"
model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        user_input = request.form['user_input']
        input_ids = tokenizer.encode(user_input, return_tensors="pt")

        # Generate text using the model
        output = model.generate(input_ids, max_length=50, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)

        # Decode and return the generated text
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        return render_template('index.html', user_input=user_input, generated_text=generated_text)

if __name__ == '__main__':
    app.run(debug=True)