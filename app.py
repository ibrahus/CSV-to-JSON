from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import io
import pandas as pd
from tasks import make_celery


# def create_app():
flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='pyamqp://guest@localhost//',
    CELERY_RESULT_BACKEND='rpc://'
)

celery = make_celery(flask_app)


@celery.task
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


@flask_app.route("/csv-to-json", methods=['GET', 'POST'])
def csv_to_json():
    print('')
    if not request.files:
        return jsonify({
            'success': False,
            'message': 'There is no file, please import a CSV file',
        }), 400
    # get the file
    file = list(request.files.values())[0]

    if file.content_type not in 'text/csv':
        return jsonify({
            'success': False,
            'message': 'The file is not in CSV format. Please upload a CSV file',
        }), 415

    data = file.read()

    str_data = data.decode('utf-8')
    top_rating_dict = convert_to_json.delay(str_data)

    # buff = io.StringIO(str_data)

    # output = []
    # reader = csv.DictReader(buff)
    # for line in reader:
    #     output.append(line)

    # df = pd.DataFrame(output)
    # df['customer_average_rating'] = pd.to_numeric(
    #     df['customer_average_rating'])
    # top_rating = df.iloc[df['customer_average_rating'].idxmax()]
    # top_rating_dict = {
    #     'top_product': top_rating['product_name'],
    #     'product_rating': top_rating['customer_average_rating']
    # }

    return jsonify({
        'success': True,
        'data': top_rating_dict.wait(),
    })


#     return flask_app


# flask_app = create_app()

# if __name__ == '__main__':
#     flask_app.run(host='0.0.0.0', port=8080, debug=True)
