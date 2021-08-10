# QR Code Decoder Playground

Experimental REST API to decode qr codes from various image formats and pdfs. 

## Building the docker image

``docker build --tag qrcode-decoder-playground .``

## Running the docker image

``docker run --publish 5000:5000 qrcode-decoder-playground``

## Using the API

Use the ``api/qr/v1/decode`` endpoint to decode qr codes from pdf, jpg, png and tiff files. Provide the file as binary 
content in the body of the request and specify the file format in the header. 
The endpoint will return with status code ``200``, if a qr code has been found. 
The body of the response will then contain the string representation of the qr code.    

The endpoint will return status codes between ``400`` and ``500`` if no qr code could be detected or multiple *different* qr codes have been detected. 
The qr codes to be considered can be filtered by providing the header ``X-Qrcode-Startswith`` to match the beginning of the qr code (e.g. ``https://``). 


Accepted ``Content-Type`` headers are

- ``application/pdf`` for PDFs (can contain multiple pages)
- ``image/*`` for JPG, PNG, TIFF files

## Examples

``curl -X POST http://localhost:5000/api/qr/v1/decode -H "Content-Type:image/*" -H "X-Qrcode-Startswith:https://" --data-binary "@test/testdata/qrcode.png"``

``curl -X POST http://localhost:5000/api/qr/v1/decode -H "Content-Type:application/pdf" --data-binary "@test/testdata/qrcode.pdf"``
