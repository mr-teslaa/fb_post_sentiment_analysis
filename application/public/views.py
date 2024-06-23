import os
import logging
import tensorflow as tf
import pandas as pd
from threading import Thread
from flask import Blueprint
from flask import request
from flask import url_for
from flask import render_template
from flask import jsonify
from flask import make_response
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from application.services.fb_services import FacebookAPI

# DEFINE THE FLASK APP
public = Blueprint('public', __name__)

# SET HOW MANY WORDS CAN A COMMENT CONTAINS
max_words = 10000
max_len = 50

current_directory = os.getcwd()
application_dir = "application/static/aimodel/"
dataset_dir = os.path.join(current_directory, application_dir+"dataset.csv")
model_dir = os.path.join(current_directory, application_dir+"lstm_model.h5")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load the LSTM model and tokenizer
df = pd.read_csv(dataset_dir)
loaded_model = load_model(model_dir)
logging.info("Model loaded successfully.")


# LANDING PAGE
@public.route('/')
def home():
    return render_template('home.html')


# GET THE FACEBOOK PAGES OF THE USER
@public.route('/get-pages', methods=['POST'])
def get_pages():
    # init the fb class
    fb = FacebookAPI()
    print('Initialize the facebook api')
    get_pages = fb.get_pages()
    print('get the pages from graph api')
    print(get_pages)

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
    comment = request.json.get('comment')

    if not comment:
        return jsonify({"error": "No comment provided"}), 400

    def predict_sentiment(comment):
        try:
            tokenizer = Tokenizer(num_words=max_words)
            tokenizer.fit_on_texts(df['Data'])
            sequences = tokenizer.texts_to_sequences([comment])
            padded_sequences = pad_sequences(sequences, maxlen=max_len)
            predictions = loaded_model.predict(padded_sequences)
            sentiment_label = int(tf.argmax(predictions[0]).numpy())
            return sentiment_label
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            logging.info(f"Input text causing the error: {comment}")
            return None

    def async_predict(comment, response):
        sentiment = predict_sentiment(comment)
        response["sentiment"] = sentiment
        response["finished"] = True

    response = {"sentiment": None, "finished": False}
    thread = Thread(target=async_predict, args=(comment, response))
    thread.start()
    thread.join()

    if response["sentiment"] is not None:
        return jsonify({"sentiment": response["sentiment"]})
    else:
        return jsonify({"error": "Prediction error"}), 500