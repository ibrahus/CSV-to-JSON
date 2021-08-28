from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import io
import pandas as pd
from tasks import make_celery


flask_app = Flask(__name__)

# We configure Celery’s RabbitMQ broker and RPC backend
flask_app.config.update(
    CELERY_BROKER_URL='pyamqp://guest@localhost//',
    CELERY_RESULT_BACKEND='rpc://'
)

celery = make_celery(flask_app)


@celery.task
def convert_to_json_task(data):
    buff = io.StringIO(data)
    output = []
    reader = csv.DictReader(buff)
    for line in reader:
        output.append(line)

    df = pd.DataFrame(output)
    df['customer_average_rating'] = pd.to_numeric(
        df['customer_average_rating'])
    top_rating = df.iloc[df['customer_average_rating'].idxmax()]
    top_rating_dict = {
        'top_product': top_rating['product_name'],
        'product_rating': top_rating['customer_average_rating']
    }

    return top_rating_dict


def convert_to_json(data):
    buff = io.StringIO(data)
    output = []
    reader = csv.DictReader(buff)
    for line in reader:
        output.append(line)

    df = pd.DataFrame(output)
    df['customer_average_rating'] = pd.to_numeric(
        df['customer_average_rating'])
    top_rating = df.iloc[df['customer_average_rating'].idxmax()]
    top_rating_dict = {
        'top_product': top_rating['product_name'],
        'product_rating': top_rating['customer_average_rating']
    }

    return top_rating_dict


CORS(flask_app)


@flask_app.route("/")
def hello_world():
    return jsonify('Healthy')

# Endpoint that recive a CSV file of products and return JSON response of the top rated product


@flask_app.route("/csv-to-json", methods=['GET', 'POST'])
def csv_to_json():
    # Check if no file is uploaded, if not retun 400
    if not request.files:
        return jsonify({
            'success': False,
            'message': 'There is no file, please import a CSV file',
        }), 400

    """ If the file is uploaded, we will get the first file from the request object instead
    of getting the file by name """

    file = list(request.files.values())[0]

    # Check if the file uploaded is a CSV file, if not return 415
    if file.content_type not in 'text/csv':
        return jsonify({
            'success': False,
            'message': 'The file is not in CSV format. Please upload a CSV file',
        }), 415

    # Read the file
    data = file.read()
    # Convert it to String
    str_data = data.decode('utf-8')
    if str_data == '':
        return jsonify({
            'success': False,
            'message': 'The file is empty',
        }), 415

    if request.method == 'POST':
        """ Call convert_to_json_task to run the task in background
         and retrun task ID, task status in the response"""
        top_rating_task = convert_to_json_task.delay(str_data)

        return jsonify({
            'success': True,
            'task_id': top_rating_task.id,
            'task_status': top_rating_task.status,
        }), 202

    if request.method == 'GET':
        # Call convert_to_json that a will return a json response of the top rated prodcut
        top_rating_dict = convert_to_json(str_data)

        return jsonify({
            'success': True,
            'data': top_rating_dict,
        })
