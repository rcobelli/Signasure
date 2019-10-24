from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import flatten
import forger
import train
import verify


application = Flask(__name__)


@application.route('/', methods=['GET'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def home():
    return {
        "statusCode": 200,
        "body": {}
    }


@application.errorhandler(404)
def page_not_found(e):
    return {
        "statusCode": 400,
        "body": {}
    }


@application.errorhandler(500)
def data_not_found(e):
    return {
        "statusCode": 500,
        "body": {}
    }


@application.route('/api/v1/split', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def split_signatures():
    # return request.get_json()["image"]
    try:
        raw_sheet_img = request.get_json()["image"]
        sheet_img_obj = flatten.create_image(raw_sheet_img)
        return flatten.api_handler(sheet_img_obj)
    except Exception as e:
        return {
            "status": 500,
            "body": {"error": e}
        }


@application.route('/api/v1/train', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def train_model():
    try:
        authentic_uris = request.get_json()["signatures"]
        name = request.get_json()["name"]
        forged_uris = forger.forge_name(name)
        return train.train(authentic_uris, forged_uris)
    except Exception as e:
        return {
            "status": 500,
            "body": {"error": e}
        }


@application.route('/api/v1/verify', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def verify_sig():
    try:
        signature = request.get_json()["signature"]
        uuid = request.get_json()["uuid"]
        return verify.verify(uuid, signature)
    except Exception as e:
        return {
            "status": 500,
            "body": {"error": e}
        }


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    CORS(application)
    application.run(threaded=True)
