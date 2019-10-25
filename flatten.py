from cv2 import cv2
import numpy as np
import base64


def api_handler(img):
    return split_image(flatten_image(img))


def create_image(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def flatten_image(image):
    scale_percent = 0.95
    width = int(image.shape[1])
    height = int(image.shape[0])

    while width >= 1500:
        width = int(width * scale_percent)
        height = int(height * scale_percent)

    dim = (width, height)

    image = cv2.resize(image, dim)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    edged = cv2.Canny(image, 75, 75)

    contours, hierarchy = cv2.findContours(
        edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for c in contours:
        p = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*p, True)

        if len(approx) == 4:
            target = approx
            break
    approx = mapp(target)

    pts = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

    op = cv2.getPerspectiveTransform(approx, pts)
    final_scan = cv2.warpPerspective(image, op, (width, height))

    (thresh, final_scan) = cv2.threshold(final_scan, 175,
                                         255, cv2.THRESH_BINARY)

    final_scan = final_scan[15:height-15, 15:width-15]
    return final_scan


def monochrome_img(img_uri):
    image = create_image(img_uri)
    scale_percent = 0.95
    width = int(image.shape[1])
    height = int(image.shape[0])

    while width >= 400:
        width = int(width * scale_percent)
        height = int(height * scale_percent)

    dim = (width, height)

    image = cv2.resize(image, dim)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, final_scan) = cv2.threshold(image, 175, 255, cv2.THRESH_BINARY)
    return encode_image(final_scan)


def encode_image(image):
    retval, buffer = cv2.imencode('.jpeg', image)
    jpg_as_text = base64.b64encode(buffer)
    cropped = str(jpg_as_text)[2:-1]
    url = "data:image/jpeg;base64," + cropped
    return url


# Takes in an opencv image object, and splits the image into an 8 by 2 grid. Each image is encoded to base 64 and added to a json body
def split_image(image):
    grid_rows = 8
    grid_cols = 2

    crop_width = int(image.shape[1] / grid_cols)
    crop_height = int(image.shape[0] / grid_rows)

    start_row = 0
    end_row = crop_height

    encoded_signatures = []

    count = 0
    for row_num in range(0, grid_rows):
        start_col = 0
        end_col = crop_width
        for col_num in range(0, grid_cols):
            cropped_image = image[start_row:end_row, start_col:end_col]
            # cv2.imwrite('sig-' + str(row_num+1) + "-" +
            #            str(col_num+1) + ".png", cropped_image)
            temp = {
                "id": count,
                "uri": encode_image(cropped_image)
            }
            encoded_signatures.append(temp)
            start_col += crop_width
            end_col += crop_width
            count += 1
        start_row += crop_height
        end_row += crop_height

    body = {
        "statusCode": 200,
        "body": encoded_signatures
    }

    return body


def mapp(h):
    h = h.reshape((4, 2))
    hnew = np.zeros((4, 2), dtype=np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h, axis=1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew
