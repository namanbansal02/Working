import transformers
from transformers import TFAutoModelForSeq2SeqLM, AutoTokenizer
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Load the trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("./tf_model")
model = TFAutoModelForSeq2SeqLM.from_pretrained("./tf_model")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # If a POST request is received, redirect to the /translate endpoint
        text_to_translate = request.form['text_to_translate']
        return jsonify({'translation': translate_text(text_to_translate)})

    # If it's a GET request, render the home page with the form
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    # Get the request data
    data = request.get_json()
    
    # Extract the text to be translated
    text_to_translate = data['text']

    # Call the translation function with the text
    translation = perform_translation(text_to_translate)

    # Return the translation
    return jsonify({'translation': translation})

def perform_translation(text_to_translate):
    # Tokenize the text
    tokenized_text = tokenizer([text_to_translate], return_tensors='np')
    
    # Generate translation output
    translation_tokens = model.generate(**tokenized_text)
    
    # Decode the tokens to a string
    translation = tokenizer.decode(translation_tokens[0], skip_special_tokens=True)
    
    # Return the translation
    return translation

if __name__ == '__main__':
    app.run(port=5000)
