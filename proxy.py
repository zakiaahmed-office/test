from flask import Flask, request
import requests
import coloredlogs
import logging

app = Flask(__name__)
coloredlogs.install(level='DEBUG')

FIRST_ANDROID_IP = '127.0.0.1'  # IP of the first Android device
FIRST_ANDROID_PORT = 8080  # Port of the first Android device

def log_response(response):
    logger = logging.getLogger('werkzeug')
    if response.status_code >= 400:
        logger.error(response)
    else:
        logger.debug(response)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    url = f'http://{FIRST_ANDROID_IP}:{FIRST_ANDROID_PORT}/{path}'
    method = request.method
    data = request.get_data()
    headers = dict(request.headers)

    response = requests.request(method, url, data=data, headers=headers)
    log_response(response)

    return response.content, response.status_code, response.headers.items()

@app.route('/android-proxy', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/android-proxy/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def android_proxy(path):
    url = f'http://{FIRST_ANDROID_IP}:{FIRST_ANDROID_PORT}/{path}'
    method = request.method
    data = request.get_data()
    headers = dict(request.headers)

    response = requests.request(method, url, data=data, headers=headers)
    log_response(response)

    return response.content, response.status_code, response.headers.items()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
