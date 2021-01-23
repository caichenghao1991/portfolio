from flask import Flask, render_template, request
import csv
from kaggleProject import retrieve_csv
import logging
import sys

app = Flask(__name__)
'''
@app.route('/user/<username>/<int:id>')  #http://127.0.0.1:5000/user/harry/1
def hello(username=None, id=None):
return render_template('index.html', name=username, pid=id)#http://127.0.0.1:5000/user/harry/1

set FLASK_APP = "app.py"
set FLASK_ENV=development
flask run
http://localhost:5000/
'''


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html(page_name):
    return render_template(page_name)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form(email=None):  # subject=None, email=None, message=None
    try:
        data = request.form.to_dict()
        email = request.form['email']
        subject = data["subject"]
        message = data["message"]
        with open('test.csv', mode='a', newline='') as db:

            csv_writer = csv.writer(db, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([email, subject, message])

    except ConnectionRefusedError as e:
        print(e)
    return render_template('thank.html', email=email)


@app.route('/download_kaggle_data', methods=['POST', 'GET'])
def download_kaggle_data():  # subject=None, count=None
    data = request.form.to_dict()
    subject = data["subject"]
    count = int(data["num"])

    logging.warning(f'{subject} {count}')
    files = retrieve_csv(subject, count)

    return render_template('work1.html',
                           message=f'{count} data file(s):{", ".join(files)} downloaded. Proceed to second step.')


if __name__ == '__main_':
    h = sys.argv[1:]
    app.run(debug=True, port=443, host=h)  # run app in debug mode on port 5000
