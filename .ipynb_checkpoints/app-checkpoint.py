from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

PAGES_DIR = 'pages'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pages')
def get_pages():
    pages = [f for f in os.listdir(PAGES_DIR) if f.endswith('.txt')]
    return jsonify(pages)

@app.route('/pages/<page_name>')
def get_page(page_name):
    page_path = os.path.join(PAGES_DIR, page_name)
    with open(page_path, 'r') as file:
        content = file.read()
    return jsonify(content)

@app.route('/pages/rename', methods=['POST'])
def rename_page():
    old_name = request.json['old_name']
    if not old_name:
        return jsonify({'message': 'Done nothing - new page.'})
    new_name = request.json['new_name']

    if not old_name.endswith('.txt'):
        old_name += '.txt'
    if not new_name.endswith('.txt'):
        new_name += '.txt'
    
    old_path = os.path.join(PAGES_DIR, old_name)
    new_path = os.path.join(PAGES_DIR, new_name)
    
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        return jsonify({'message': 'Page renamed successfully'})
    else:
        return jsonify({'message': 'Original page not found'}), 404

@app.route('/pages', methods=['POST'])
def save_page():
    page_name = request.json['name']
    content = request.json['content']
    
    # Ensure the page name has the '.txt' extension
    if not page_name.endswith('.txt'):
        page_name += '.txt'
    
    page_path = os.path.join(PAGES_DIR, page_name)
    with open(page_path, 'w') as file:
        file.write(content)
    return jsonify({'message': 'Page saved successfully'})

@app.route('/pages/<page_name>', methods=['DELETE'])
def delete_page(page_name):
    page_path = os.path.join(PAGES_DIR, page_name)
    if os.path.exists(page_path):
        os.remove(page_path)
        return jsonify({'message': 'Page deleted successfully'})
    else:
        return jsonify({'message': 'Page not found'}), 404

@app.route('/images/<page_name>')
def get_images(page_name):
    page_dir = os.path.join(IMAGES_DIR, page_name)
    images = []
    if os.path.exists(page_dir):
        images = [f for f in os.listdir(page_dir) if os.path.isfile(os.path.join(page_dir, f))]
    return jsonify(images)

@app.route('/verify-password', methods=['POST'])
def verify_password():
    with open("twonote.password", 'r') as file:
        correct_password = file.read()
    received_password = request.json.get('password', '')
    
    if received_password == correct_password:
        return jsonify({'valid': True})
    else:
        return jsonify({'valid': False})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=21126)