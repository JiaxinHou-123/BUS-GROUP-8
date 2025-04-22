from modelscope.utils.constant import Tasks
from modelscope.pipelines import pipeline
from modelscope import Model
import os
from flask import Flask, render_template, request, jsonify, url_for
import torch.nn as nn
app = Flask(__name__)


# @article{zeng2022glm,
#   title={Glm-130b: An open bilingual pre-trained model},
#   author={Zeng, Aohan and Liu, Xiao and Du, Zhengxiao and Wang, Zihan and Lai, Hanyu and Ding, Ming and Yang, Zhuoyi and Xu, Yifan and Zheng, Wendi and Xia, Xiao and others},
#   journal={arXiv preprint arXiv:2210.02414},
#   year={2022}
# }

# Load model from local models folder

from modelscope import AutoTokenizer,AutoModel, snapshot_download
model_dir = "./models/ZhipuAI/chatglm3-6b"
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
model = AutoModel.from_pretrained(model_dir, device_map="auto", trust_remote_code=True).half()

model = model.eval()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat_ui")
def chat_ui():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history
    chat_history = []
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if user_input:
            # Construct input and invoke the model
            response, chat_history = model.chat(tokenizer, user_input, chat_history)

            # Add to the display dialog list
            chat_history_display = [
                {'role': 'User', 'content': user_input},
                {'role': 'AI', 'content': response}
            ]
            return render_template('chat.html', chat_history=chat_history_display)
    return render_template('chat.html', chat_history=[])


@app.route('/feedback', methods=['POST'])
def feedback():
    feedback_text = request.form.get('feedback_text')
    if feedback_text:
        feedback_file = os.path.join(app.config['UPLOAD_FOLDER'], 'feedback.txt')
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        with open(feedback_file, 'a', encoding='utf-8') as f:
            f.write(feedback_text + '\n')
    return redirect(url_for('chat'))


from flask import redirect, send_from_directory
from werkzeug.utils import secure_filename

ACCESS_UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'txt'}

app.config['ACCESS_UPLOAD_FOLDER'] = ACCESS_UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'your_secret_key'
os.makedirs(ACCESS_UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/accessibility', methods=['GET', 'POST'])
def accessibility():
    message = ''
    uploaded_files = os.listdir(app.config['ACCESS_UPLOAD_FOLDER'])  # List files in the folder

    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['ACCESS_UPLOAD_FOLDER'], filename))
            message = 'upload sucessfully！'
            uploaded_files = os.listdir(app.config['ACCESS_UPLOAD_FOLDER'])  # refresh
        else:
            message = 'Upload failed: Unsupported file format'

    # Handle search functionality
    search_query = request.args.get('search', '')
    if search_query:
        # Filter files based on search query (e.g., searching by filename)
        uploaded_files = [f for f in uploaded_files if search_query.lower() in f.lower()]

    return render_template('accessibility.html', files=uploaded_files, message=message, search_query=search_query)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['ACCESS_UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/cost_of_living', methods=['GET', 'POST'])
def cost_of_living():
    total_budget = None
    if request.method == 'POST':
        # Get form data
        rent = float(request.form['rent'])
        groceries = float(request.form['groceries'])
        transportation = float(request.form['transportation'])
        entertainment = float(request.form['entertainment'])

        # Calculate total budget
        total_budget = rent + groceries + transportation + entertainment

    return render_template('cost_of_living.html', total_budget=total_budget)

# Route to handle file upload for resources (videos, images, texts)
@app.route('/upload_resource', methods=['POST'])
def upload_resource():
    if request.method == 'POST':
        file = request.files['resource_file']
        if file:
            # Save the file to a folder (you need to create the 'uploads' folder)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for('cost_of_living'))

# Route to download the uploaded resource
@app.route('/download_resource/<filename>')
def download_resource(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Route to handle dormitory search
@app.route('/search_dormitory', methods=['GET'])
def search_dormitory():
    search_query = request.args.get('search')
    # Dummy dormitory data, ideally you would query a database here
    dormitories = [
        {'name': 'Dorm A', 'price': 400, 'environment': 'Shared rooms, clean, good location', 'details_link': '#'},
        {'name': 'Dorm B', 'price': 500, 'environment': 'Private rooms, modern facilities', 'details_link': '#'}
    ]
    # Filter dormitories based on the search query (for simplicity, we're using basic substring match)
    filtered_dorms = [dorm for dorm in dormitories if search_query.lower() in dorm['name'].lower() or search_query.lower() in dorm['environment'].lower()]
    return render_template('cost_of_living.html', dormitories=filtered_dorms)

# Route to handle campus job search
@app.route('/search_jobs', methods=['GET'])
def search_jobs():
    search_query = request.args.get('search')
    # Dummy job data, ideally you would query a database here
    jobs = [
        {'title': 'Student Assistant', 'description': 'Help with administrative tasks', 'details_link': '#'},
        {'title': 'Library Assistant', 'description': 'Work at the university library', 'details_link': '#'}
    ]
    filtered_jobs = [job for job in jobs if search_query.lower() in job['title'].lower() or search_query.lower() in job['description'].lower()]
    return render_template('cost_of_living.html', jobs=filtered_jobs)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=6006)
