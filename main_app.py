from functools import reduce

from flask import Flask, request, jsonify, Response
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
        unique_filename = str(uuid.uuid4()) + '.txt'
        file_path = config.DIRECTORY_NAME + '/' + unique_filename

        d['created'] = str(datetime.now().isoformat())
        serialized_data = str(d)
        encoded_string = config.secret_encode(serialized_data)

        s3 = boto3.resource("s3")
        bucket = s3.Bucket(config.BUCKET_NAME)
        bucket.put_object(
            Key=file_path,
            Body=encoded_string
        )

        return jsonify(d), 200

    return '', 405  # Bad request


@app.route('/fannel-report', methods=['GET'])
def fannel_report():
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(config.BUCKET_NAME)

    l = []
    for obj in bucket.objects.filter(Prefix=config.DIRECTORY_NAME + "/"):
        if '.txt' in obj.key:
            body = obj.get()['Body'].read()
            d = eval(config.secret_decode(body))
            l.append(d)

    return jsonify(l), 200


class ReportData(object):

    def __init__(self, bucket):
        self.data = self.__get_file_list(bucket)

    def get_fields(self):
        s = set()
        for x in self.data:
            s |= x.keys()
        return list(s)

    def get_fields_string(self):
        fields = self.get_fields()
        return ",".join(fields) + "\n"

    def get_data_string(self, fields):
        str = ''
        str_template = '"{}",'
        for d in self.data:
            row = ''
            for f in fields:
                row += str_template.format(d[f] if f in d.keys() else '')
            str += row + "\n"
        return str

    @classmethod
    def __get_file_list(cls, bucket):
        l = []
        for obj in bucket.objects.filter(Prefix=config.DIRECTORY_NAME + "/"):
            if '.txt' in obj.key:
                body = obj.get()['Body'].read()
                d = eval(config.secret_decode(body))
                l.append(d)
        return l


@app.route('/fannel-report-csv', methods=['GET'])
def fannel_report_csv():
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(config.BUCKET_NAME)

    rd = ReportData(bucket)
    fields = rd.get_fields()

    data_str = rd.get_data_string(fields)
    fields_str = rd.get_fields_string()
    csv_data = fields_str + data_str

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=report.csv"}
    )


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response


if __name__ == '__main__':
    app.run(debug=True)
