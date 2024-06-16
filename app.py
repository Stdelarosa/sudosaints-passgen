from flask import Flask, request, render_template, jsonify
import random

app = Flask(__name__)

# Load the wordlist from the provided file
with open('eff_large_wordlist.txt', 'r') as file:
    wordlist = [line.split()[1] for line in file.readlines()]

@app.route('/')
def index():
    return render_template('passgen.html', password='', keywords='')

@app.route('/generate', methods=['POST'])
def generate():
    num_words = 5  # Number of words for the password
    password = ' '.join(random.choice(wordlist) for _ in range(num_words))
    return jsonify(password=password)

@app.route('/generate_with_keywords', methods=['POST'])
def generate_with_keywords():
    data = request.get_json()
    keywords = data.get('keywords', '').split(',')
    keywords = [keyword.strip() for keyword in keywords if keyword.strip()]

    if len(keywords) > 2:
        keywords = random.sample(keywords, 2)
    elif len(keywords) < 1:
        keywords = []

    num_random_words = 5 - len(keywords)
    random_words = [random.choice(wordlist) for _ in range(num_random_words)]

    password_list = keywords + random_words
    random.shuffle(password_list)
    password = ' '.join(password_list)
    return jsonify(password=password)

if __name__ == '__main__':
    app.run(debug=True)