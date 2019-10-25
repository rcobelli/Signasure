import turicreate as tc
import flatten
import pandas as pd
import base64
import os
import sys

# USAGE: python eval.py __TEST_IMAGE__ __MODEL_UUID__


def verify(uuid, img_uri):
    filename = "{}/verify/{}.png".format(sys.path[0], uuid)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    #mono_uri = flatten.monochrome_img(img_uri)
    #uri = uri_str_to_bytes(mono_uri)
    uri = uri_str_to_bytes(img_uri)
    fh = open(filename, "wb")
    fh.write(base64.decodebytes(uri))
    fh.close()

    #data = tc.image_analysis.load_images(filename, with_path=True)
    test = tc.SFrame({'image': [tc.Image(filename)]})

    model = tc.load_model('{}/models/{}.model'.format(sys.path[0], uuid))
    # 3. Generate prediction
    #predictions = model.predict(dataset=data)
    test['predictions'] = model.predict(test)

    os.remove(filename)

    return {
        "statusCode": 200,
        "body": "{}".format(test['predictions'][0])
    }


def uri_str_to_bytes(img_uri):
    return bytes(img_uri.split(",")[1], "raw_unicode_escape")
