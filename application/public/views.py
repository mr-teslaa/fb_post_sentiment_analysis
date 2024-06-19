from flask import Blueprint
from flask import request
from flask import render_template
from flask import jsonify
from flask import make_response
from application.services.fb_services import FacebookAPI

# =======================================
# ======= START - AI MODULE IMPORT ========
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import logging
import numpy as np

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load the LSTM model and tokenizer
try:
    loaded_model = load_model('lstm_model.h5')
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")

# Define max_len as per the model's requirement
max_len = 50  # Update this to match your model's expected input length
# ======= END - AI MODULE IMPORT ================
# ===========================================

public = Blueprint('public', __name__)

@public.route('/')
def home():
    return render_template('home.html')


# GET THE FACEBOOK PAGES OF THE USER
@public.route('/get-pages', methods=['POST'])
def get_pages():
    # init the fb class
    fb = FacebookAPI()
    get_pages = fb.get_pages()

    pages = {}
    for index, page in enumerate(get_pages):
        current_page = {
            "id": page.get('id'),
            "name": page.get('name')
        }
        pages[index] = current_page

    res = make_response(
        jsonify(
            {
                "message": "Post fetched successfully",
                "notification": "success",
                "data": pages
            }
        ), 200
    )
    return res

# GET THE FACEBOOK POSTS OF PAGE
@public.route('/page/<int:page_id>/posts/')
def get_posts(page_id):
    # init the fb class
    fb = FacebookAPI()
    posts = fb.get_posts(page_id)

    for post in posts:
        post['page_id'] = page_id

    return render_template('posts.html', posts=posts)


# GET THE POST COMMENTS
@public.route('/page/<int:page_id>/posts/<string:post_id>/comments/')
def get_comments(page_id, post_id):
    # init the fb class
    fb = FacebookAPI()
    page_access_token = fb.get_page_access_token(page_id)
    comments = fb.get_comments(post_id, page_access_token)
    return render_template('comments.html', comments=comments)


# PREDICT SENTIMENTAL ANALYSIS
@public.route('/predict', methods=['POST'])
def predict():
    try:
        if request.method == 'POST':
            input_text = request.form['message']
            sequences = tokenizer.texts_to_sequences([input_text])
            padded_sequences = pad_sequences(sequences, maxlen=max_len)
            predictions = loaded_model.predict(padded_sequences)
            sentiment_label = np.argmax(predictions[0])

            return render_template('result.html', prediction=sentiment_label)
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        logging.info(f"Input text causing the error: {input_text}")
        return "Error during prediction", 500