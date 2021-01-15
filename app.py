from flask import Flask, render_template, request
import csv
app = Flask(__name__)
'''
@app.route('/user/<username>/<int:id>')  #http://127.0.0.1:5000/user/harry/1
def hello(username=None, id=None):
	return render_template('index.html', name=username, pid=id)#http://127.0.0.1:5000/user/harry/1

'''
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/<string:page_name>')
def html(page_name):
	return render_template(page_name)

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form(subject=None, email=None,message=None):
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
