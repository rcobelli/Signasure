import turicreate as tc
import base64
import coremltools
import os
import sys
import uuid
import boto3


def train(authentic, forged):
    model_uuid = uuid.uuid1()
    for sig in authentic:
        filename = "{}/tmp/{}/authentic/auth-{}.jpeg".format(
            sys.path[0], model_uuid, sig["id"])
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        uri = uri_str_to_bytes(sig["uri"])
        fh = open(filename, "wb")
        fh.write(base64.decodebytes(uri))
        fh.close()

    for key in forged:
        filename = "{}/tmp/{}/forge/forge-{}.jpeg".format(
            sys.path[0], model_uuid, key)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        uri = uri_str_to_bytes(forged[key])
        fh = open(filename, "wb")
        fh.write(base64.decodebytes(uri))
        fh.close()

    # 1. Load images
    # data = tc.image_analysis.load_images(
    # "{}/tmp/{}".format(sys.path[0], str(model_uuid)), with_path=True)

    data = tc.image_analysis.load_images(
        "{}/tmp/{}".format(sys.path[0], str(model_uuid)), recursive=True, with_path=True)

# data['status'] = data['path'].apply(
#         lambda path: os.path.basename(os.path.dirname(path)))
    # 2. Create label column based on folder name
    data['status'] = data['path'].apply(
        lambda path: os.path.basename(os.path.dirname(path)))

    # 3. Create model
    model = tc.image_classifier.create(data, target='status')

    # 5. Evaluate the model and show metrics
    metrics = model.evaluate(data)
    # print(metrics['accuracy'])

    # 6. Save the model
    # SAVE MODEL TO S3
    s3 = boto3.client('s3')
    bucket_name = 'my-bucket'
    model.save(str(model_uuid) + '.model')

    return {
        "statusCode": 200,
        "body": {
            "uuid": model_uuid
        }
    }


def uri_str_to_bytes(img_uri):
    return bytes(img_uri.split(",")[1], "raw_unicode_escape")
