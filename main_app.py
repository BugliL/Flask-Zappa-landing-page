from flask import Flask, request, jsonify
import boto3

from datetime import datetime
from flask import Flask, request, render_template
import config
import uuid

app = Flask(__name__)


@app.route('/save', methods=['POST'])
def save():
    d = request.json
    if d:
        dirname = 'fannel1-data'
        unique_filename = str(uuid.uuid4()) + '.txt'
        file_path = dirname + '/' + unique_filename

        serialized_data = str(d)
        encoded_string = config.secret_encode(serialized_data)

        s3 = boto3.resource("s3")
        bucket = s3.Bucket(config.BUCKET_NAME)
        bucket.put_object(
            Key=file_path,
            Body=encoded_string
        )

        # List all files
        # for object_summary in bucket.objects.filter(Prefix=dirname + "/"):
        #     print(object_summary.key)

        return jsonify(d), 200

    return '', 405  # Bad request


if __name__ == '__main__':
    app.run(debug=True)
