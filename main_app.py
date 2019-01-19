from flask import Flask, request, jsonify
import boto3

from datetime import datetime
from flask import Flask, request, render_template
import config

app = Flask(__name__)


@app.route('/test-hello-world')
def index():
    return "Hello, world!", 200


@app.route('/save', methods=['POST'])
def save():
    d = request.json
    if d:
        dirname = 'fannel1-data'
        filename = 'test.txt'
        file_path = dirname + '/' + filename
        encoded_string = str(d).encode("utf-8")

        s3 = boto3.resource("s3")
        bucket = s3.Bucket(config.BUCKET_NAME)
        bucket.put_object(
            Key=file_path,
            ContentType='text/plain',
            Body=encoded_string
        )

        for object_summary in bucket.objects.filter(Prefix=dirname + "/"):
            print(object_summary.key)

        return jsonify(d), 200

    return '', 200


if __name__ == '__main__':
    app.run(debug=True)
