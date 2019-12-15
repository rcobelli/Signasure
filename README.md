# Signasure
Signasure allows for easy signature verification by comparing to a set of provided authentic signatures. Powered by Turicreate, the Signasure API lets any project allow for easy signature evaluation. The entire API is built as a Flask API that can be easily deployed to AWS (we recommend hosting this application on an AWS EC2 Small) or other Python ready server. Our signature sheet processing is powered by OpenCV.

## Training
To train a new signasure set, simply fill out the Signature Sheet PDF with 16 authentic signatures, attempting to be as consistent as possible. Scan the sheet in, and send a base64 encoded JPEG image of the scan to the `/split` endpoint. This endpoint will automatically split the sheet into 16 signatures. These images can be sent back to the `/train` endpoint. After a few seconds for training, a UUID will be returned. **Save this UUID for evaluating future signatures against this model you have created.**

## Evaluating
To verify a signature, send a base64 JPEG of the signature along with the UUID to verify against to the `/verify` endpoint. This endpoint will return confidence intervals for the signature's likely authenticity.
