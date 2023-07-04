import os
from flask import Flask, request, send_from_directory
from gevent.pywsgi import WSGIServer
import asyncio
from concurrent.futures import ThreadPoolExecutor
from werkzeug.utils import secure_filename
import aiofiles

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
async def upload_file():
    if 'file' not in request.files:
        return "No file part in the request"

    file = request.files['file']

    if file.filename == '':
        return "No file selected"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(await file.read())

        return "File uploaded successfully"
    else:
        return "Invalid file"


@app.route('/download/<filename>', methods=['GET'])
async def download_file(filename):
    return await send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def create_app():
    return app

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app.config['LOOP'] = loop

    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        http_server.stop()
        loop.close()
