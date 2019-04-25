from flask import Flask, render_template, request,url_for,redirect,session
import pymongo
import pandas as pd
import numpy as np
import sys
from sklearn.preprocessing import LabelEncoder

''' Loading the dataset''' 
# data = pd.read_csv('static/datasets/MubeenaDataset.csv')
# lbl_Remarks = LabelEncoder()
# print(data.head())
 

# data['Teacher Remarks'] = lbl_Remarks.fit_transform(data['Remarks'])
# print(data.head())


#inputs = data.drop('Maths',axis='columns')


app = Flask(__name__)
client = pymongo.MongoClient('localhost', 27017)
db = client['MubeenaEbrahim']

@app.route('/')
def home():
	return render_template('index.html')


@app.route('/login',methods = ['GET','POST'])
def login():

	if request.method == 'POST':

		try:

			name = request.form['email']
			password = request.form['password']

			print("Credentials Provided")

			for teacher in db['Teachers'].find():
				print("Verifying Credentials")

				if teacher['Email'] == name:
					print("identified username is:" + name)
					print("Validating password")

					if teacher['Password'] == password:
						print("Password validation successful")
						print("Starting session")
						session['Name'] = teacher['Name']
						session['Surname'] = teacher['Surname']
						print("Rendering Home page ........................")
						students = []
						for student in db['Students'].find():
							students.append(student)

						return render_template('teachers.html',students = students)
					else:
						session['message'] = "Incorrect password"
						return render_template('login.html')
				else:
					print("Searching....")
			
			print("Username could not be found")
			print("Plan ?")
			print("Signup username")
			print("renderding signup page ..........")
			return render_template("signup.html")

		except:
			print("Error in logging in user")
			return render_template('index.html')


	else:
		return render_template('login.html')

@app.route('/signup',methods = ['GET','POST'])
def signup():
	if request.method == 'POST':
		name = request.form['name']
		surname = request.form['surname']
		email = request.form['email']
		password = request.form['password']
		teacher = {
			'Name': name,
			'Surname':surname,
			'Email': email,
			'Password': password
		}
		Transaction = db['Teachers'].insert_one(teacher)
		print("One teacher successfully signed in.Transaction id is " + str(Transaction.inserted_id))
		return redirect(url_for('login'))

	else:
		return render_template('signup.html')

@app.route('/assessmentmarks',methods = ['GET','POST'])
def assessmentmarks():
	if request.method == "POST":
		assessment = request.form['type']
		name = request.form['name']
		reg_number = request.form['RegNumber']
		Mark = request.form['mark']
		age = request.form['age']

		print("Record prepocessing successfull")
		print("Confirming is student exist in records")

		#confirm if student id is there  in the database

		count = db.Students.find({"RegNumber": reg_number}).count()
		if count > 0:
			print("Confirmation successful")
			Mark = {
				"Assessment": assessment,
				"Name": name,
				"Reg_number": reg_number,
				"Mark": Mark,
				"Age": age
			}
			Transaction = db.AssessmentMarks.insert_one(Mark)
			print("New record successfully added with transaction id " + str(Transaction.inserted_id))
		else:
			print("Student does not exist")
			print("Notifying user")
			message = "Sorry student records did not match any"
			return render_template('teachers.html',message = message)

		
		print(name)

		return "me"
	
	else:
		return "Method is not POST"

@app.route('/teachers')
def teachers():
	students = []
	for student in db['Students'].find():
		students.append(student)
	return render_template('teachers.html',students = students)

@app.route('/exammark',methods = ['POST','GET'])
def exammark():
	pass

@app.route('/newstudent', methods = ['GET','POST'])
def newstudent():
	if request.method == "POST":
		name = request.form['name']
		surname = request.form['surname']
		gender = request.form['gender']
		dob = request.form['dob']
		health = request.form['health']
		parents = request.form['parentstatus']
		relation = request.form['relation']
		level = request.form['level']

		records = db.Students.count()
		regnumber = "mub"+"2019E"+str(records)
		print(regnumber)


		student = {
			"Name": name,
			"Surname": surname,
			"Gender": gender,
			"DOB":dob,
			"RegNumber": regnumber,
			"health": health,
			"parents": parents,
			"relation": relation,
			"level": level
		}
		Transaction = db['Students'].insert_one(student)
		print("New student successfully added.Transaction id is "+ str(Transaction.inserted_id))
		students = []
		for student in db['Students'].find():
			students.append(student)
			
		return render_template('teachers.html',students = students)
	return "yaita"

@app.route('/test')
def test():
	return render_template('test.html')
'''
@app.route('/logging',methods =['GET','POST'])
def logging():

	if request.method == 'POST':
		name = request.form['Name']
		password = request.form['Password']
		print("credentials provided")

		for Admin in db['Administrators'].find():
			print("validating credentials")
			if Admin['Email'] == name:
				print("Found username: "+ name)
				print("Validating Password")
				if Admin['Password'] == password:
					print("Password validation Passed")
					print("creating session")
					session['Name'] = Admin['Name']
					session['Surname'] = Admin['Surname']
					print("Rendering Home page ........................")
					return render_template('index.html')
				else:
					print('Sorry you password did not match your email')
					name = "incorrect password"			
					return render_template('page-login.html', name = name)
			else:
				print("Username not found")
				print("..............................................")
				print("Retrying.....")
				#return render_template('page-signup.html')
	else:
		return render_template('page-signup.html')
	print("Failed to find that username")
	print("Plan: Signup user")
	return render_template('page-signup.html')

@app.route('/logout')
def logout():	
	session.pop('Name', None)
	session.pop('Surname', None)
	session.pop('message',None)
	print("Sessions successfully deleted")
	return render_template('page-login.html')

@app.route('/signup',methods = ['GET','POST'])
def signup():
	if request.method == 'POST':
		name = request.form['name']
		surname = request.form['surname']
		email = request.form['email']
		password = request.form['pass1']
		Admin = {
			'Name': name,
			'Surname':surname,
			'Email': email,
			'Password': password
		}
		Transaction = db['Administrators'].insert_one(Admin)
		print("Successfully signed in new Admin.Transaction id is " + str(Transaction.inserted_id))
		return redirect(url_for('login'))
	else:
		return render_template('page-signup.html')

@app.route('/gallery',methods = ['GET','POST'])
def gallery():
	if request.method == 'POST':
		print('Trying to upload a file')
		app.config['UPLOAD_FOLDER'] = 'static/images'
		f = request.files['file']
		f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
		print("file successfully uploaded" + f.filename)
    
		ProductName = request.form['Name']
		ProductDescription = request.form['Description']
		image = {
			"Image_Name": ProductName,
			"Image_Description": ProductDescription,
			"Image_url": 'static/images/'+f.filename
		}
		transaction = db['Images'].insert_one(image)
		print("image details successfuly saved with id "+str(transaction.inserted_id))
		gallery = []
		for image in db['Images'].find():
			gallery.append(image)
		return render_template('gallery.html',gallery = gallery)
	else:
		gallery = []
		for image in db['Images'].find():
			gallery.append(image)
		return render_template('gallery.html',gallery = gallery)

@app.route('/calender')
def calender():
	return render_template('page-calendar.html')

@app.route('/Activity',methods = ['POST', 'GET'])
def Activity():
	if request.method == 'POST':
		try:
			print("let me try that")
			crop_name = request.form['crop']
			activity_date = request.form['activity_date']
			Activity = request.form['Activity']

			if Activity == 'watering':
				mode = request.form['watering_mode']
				amount = request.form['watering_amount']
				Watering = {
					"crop_name": crop_name,
					"activity_date": activity_date,
					"activity": Activity,
					"Mode": mode,
					"amount": amount
				}
				transaction = db['Activities'].insert_one(Watering)
				print("New Activity successfully added with id: "+str(transaction.inserted_id))
			elif Activity == 'weeding':
				mode = request.form['weeding_mode']
				if mode == 'Other':
					print(mode)
					mode = request.form['other_weeding']
				Weeding = {
					"crop_name": crop_name,
					"activity_date": activity_date,
					"activity": Activity,
					"Mode": mode
				}
				transaction = db['Activities'].insert_one(Weeding)
				print("New Activity successfully added with id: "+str(transaction.inserted_id))
			elif Activity == 'fertilisation':
				Fertliser = request.form['Fertiliser']
				Application_rate = request.form['rate']
				fertilisation = {
					"crop_name": crop_name,
					"activity_date": activity_date,
					"activity": Activity,
					"Fertiliser": Fertliser,
					"Application_rate": Application_rate
				}
				transaction = db['Activities'].insert_one(fertilisation)
				print("New Activity successfully added with id: "+str(transaction.inserted_id))
			elif Activity == 'spraying':
				spray = request.form['spraying']
				Application_rate = request.form['rate']
				spraying = {
					"crop_name": crop_name,
					"activity_date": activity_date,
					"activity": Activity,
					"Spray": spray,
					"Application_rate": Application_rate
				}
				transaction = db['Activities'].insert_one(spraying)
				print("New Activity successfully added with id: "+str(transaction.inserted_id))
			else:
				pass
		except Exception as e:
			print("We handled an Exception for you but however your last transaction did not complete")
		finally:
			return records()


@app.route('/records')
def records():
	records = []
	for record in db['Crop_data'].find():
		"""if record['Transplanted_rate'] == '':
			record['Transplanted_rate'] = 'Not nursed'"""
		records.append(record)
	return render_template('Records.html',records =records)

@app.route('/watering')
def watering():
	records = []
	for record in db['Activities'].find():
		record.pop('_id')
		if record['activity'] == 'watering':
			records.append(record)
	return render_template('Activity.html',records = records)

@app.route('/weeding')
def weeding():
	records = []
	for record in db['Activities'].find():
		record.pop('_id')
		if record['activity'] == 'weeding':
			records.append(record)
	return render_template('Activity.html',records = records)

@app.route('/spraying')
def spraying():
	records = []
	for record in db['Activities'].find():
		record.pop('_id')
		if record['activity'] == 'spraying':
			records.append(record)
	return render_template('Activity.html',records = records)

@app.route('/fertilisation')
def fertilisation():
	records = []
	for record in db['Activities'].find():
		record.pop('_id')
		if record['activity'] == 'fertilisation':
			records.append(record)
	return render_template('Activity.html',records = records)

@app.route('/other')
def other():
	records = []
	for record in db['Activities'].find():
		record.pop('_id')
		if record['activity'] == 'other':
			records.append(record)
	return render_template('Activity.html',records = records)

@app.route('/addcrop',methods = ['POST', 'GET'])
def addcrop():
	if request.method == 'POST':
		try:
			crop = request.form['crop']
			variety = request.form['Variety']
			location = request.form['Location']
			nurse = request.form['nurse']
			sown = request.form['Sown']
			Quantity = request.form['Quantity']
			Germinated = request.form['Germinated']
			Germination_rate = request.form['Germination_rate']
			comment = request.form['comment']
			if nurse == 'yes':
				transplanted_date = request.form['transplanted']
				crop = {
						"crop_name": crop,
						"Variety": variety,
						"Location": location,
						"Nursed": nurse,
						"Sown": sown,
						"Quantity": Quantity,
						"Germinated_date": Germinated,
						"Germination_rate": Germination_rate,
						"Transplanted_rate": transplanted_date,
						"comment":comment
						}
				transaction = db['Crop_data'].insert_one(crop)
				print("New crop successfully added with id: "+str(transaction.inserted_id))
			else:

				crop = {
					"crop_name": crop,
					"Variety": variety,
					"Location": location,
					"Nursed": nurse,
					"Sown": sown,
					"Quantity": Quantity,
					"Germinated_date": Germinated,
					"Germination_rate": Germination_rate,
					"comment":comment
					}
				transaction = db['Crop_data'].insert_one(crop)
				print("New crop successfully added with id: "+str(transaction.inserted_id))

		except Exception as e:
			print("We handled an error for you but however your last transaction did not complete")
		finally:
			return render_template('index.html')

'''

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
	