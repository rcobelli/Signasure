import turicreate as tc
import base64
import os
import sys

# USAGE: python eval.py __TEST_IMAGE__ __MODEL_UUID__


def verify(uuid, img_uri):
    filename = "{}/verify/{}.jpeg".format(sys.path[0], uuid)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    uri = uri_str_to_bytes(img_uri)
    fh = open(filename, "wb")
    fh.write(base64.decodebytes(uri))
    fh.close()

    data = tc.image_analysis.load_images(filename, with_path=True)

    model = tc.load_model('{}/models/{}.model'.format(sys.path[0], uuid))
    return data
    # 3. Generate prediction
    predictions = model.predict(dataset=data)

    return {
        "statusCode": 200,
        "body": predictions
    }


def uri_str_to_bytes(img_uri):
    return bytes(img_uri.split(",")[1], "raw_unicode_escape")
