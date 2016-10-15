from flask import Flask
from flask import request
from hashlib import sha1

import hmac
import os

app = Flask(__name__)


@app.route('/')
def hello():
    return 'MI-PYT je nejlepší předmět na FITu!'


@app.route('/hook', methods=['POST'])
def hook():
    validate_secret(request)
    data = request.get_json()
    print(data)
    return ''


def validate_secret(request):
    # get expected secret from env
    token = os.environ.get('WEBHOOK_TOKEN')
    if not token:
        print('No secret provided, incoming requests will not be filtered! ',
              file=sys.stderr)
        return True

    # get received token hash
    header_signature = request.headers.get('X-Hub-Signature')
    if header_signature is None:
        return False
    hash_function, received_token_hash = header_signature.split('=')

    # get expected hash
    token_hash = hmac.new(bytes(token, 'utf8'), msg=request.data, digestmod=sha1).hexdigest()

    # compare hashes
    if not hmac.compare_digest(str(token_hash), str(received_token_hash)):
        return False
    else:
        return True

if __name__ == '__main__':
    app.run(debug=True)
