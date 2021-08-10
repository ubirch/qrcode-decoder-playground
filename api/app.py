from flask import Flask, request
from werkzeug.exceptions import RequestEntityTooLarge
from api.QRCodeDecoder import *

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * (10 ** 6)

qrd = QRCodeDecoder()


@app.route("/api/qr/v1/decode", methods=["POST"])
def api_qr_v1_decode():
    content_type = request.headers["Content-Type"]
    qrcode_startswith = request.headers.get("X-Qrcode-Startswith")
    try:
        if content_type.lower() == "application/pdf":
            res = qrd.qrcode_from_pdf(request.data, qrcode_startswith)
        elif content_type.lower() in ["image/*", "image/jpeg", "image/jpg", "image/png", "image/tiff"]:
            res = qrd.qrcode_from_img_bytes(request.data, qrcode_startswith)
        else:
            return "UnknownContentTypeHeaderError", 400
    except Exception as e:
        if e.__class__ == MultipleDifferentQRCodesError:
            return "MultipleDifferentQRCodesError", 400
        elif e.__class__ == NoQRCodeError:
            return "NoQRCodeError", 400
        elif e.__class__ == UnknownDecodingError:
            return "UnknownDecodingError", 400
        elif e.__class__ == InvalidImageDataError:
            return "InvalidImageDataError", 400
        elif e.__class__ == RequestEntityTooLarge:
            return "FileTooLarge", 413
        elif e.__class__ == PDFConversionTimeoutError:
            return "PDFConversionTimeoutError", 408
        else:
            return "UnknownError", 500
    return res


@app.errorhandler(413)
def request_entity_too_large():
    return "FileTooLarge", 413


if __name__ == "__main__":
    app.run("localhost", 5000)
