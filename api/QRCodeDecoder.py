from pyzbar.pyzbar import decode
from PIL import Image
import pdf2image
import io


class UnknownDecodingError(Exception):
    def __str__(self):
        return "UnknownDecodingError"


class MultipleDifferentQRCodesError(Exception):
    def __str__(self):
        return "MultipleDifferentQRCodesError"


class NoQRCodeError(Exception):
    def __str__(self):
        return "NoQRCodeError"


class InvalidImageDataError(Exception):
    def __str__(self):
        return "InvalidImageDataError"


class PDFConversionTimeoutError(Exception):
    def __str__(self):
        return "PDFConversionTimeoutError"


class QRCodeDecoder:
    def qrcode_from_img(self, img, qrcode_startswith=None):
        qrcodes = []
        try:
            for x in decode(img):
                if qrcode_startswith is None or x.data.decode("UTF-8").startswith(qrcode_startswith):
                    qrcodes.append(x.data)
        except Exception:
            raise UnknownDecodingError
        if len(qrcodes) == 0:
            raise NoQRCodeError
        if len(set(qrcodes)) > 1:
            raise MultipleDifferentQRCodesError
        return qrcodes[0]

    def qrcode_from_img_bytes(self, img_bytes, qrcode_startswith=None):
        try:
            img = Image.open(io.BytesIO(img_bytes))
        except Exception:
            raise InvalidImageDataError
        return self.qrcode_from_img(img, qrcode_startswith)

    def qrcode_from_pdf(self, pdf_bytes, qrcode_startswith=None):
        for dpi in [300, 500, 800]:
            try:
                pages = pdf2image.convert_from_bytes(pdf_bytes, dpi, timeout=30)
            except pdf2image.exceptions.PDFPopplerTimeoutError:
                raise PDFConversionTimeoutError
            qrcodes = []
            for i, page in enumerate(pages):
                f = io.BytesIO()
                page.save(f, "PNG")
                page.save(open("{}.pdf".format(i), "wb"), "PNG")
                img = Image.open(f)
                try:
                    qrcodes.append(self.qrcode_from_img(img, qrcode_startswith))
                except NoQRCodeError:
                    pass
            if len(set(qrcodes)) > 1:
                raise MultipleDifferentQRCodesError
            elif len(set(qrcodes)) == 1:
                return qrcodes[0]
        raise NoQRCodeError
