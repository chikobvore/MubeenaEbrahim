from flask import Flask, render_template, request,url_for,redirect,session
import pymongo
import pandas as pd
import numpy as np
import sys
from sklearn import preprocessing
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

''' Loading the dataset''' 
data = pd.read_csv('static/datasets/mubeena1.csv')
inputs = data.drop('Remarks',axis='columns')

print(data.head())
Target = data['Remarks']

Model =  tree.DecisionTreeClassifier()
Model.fit(inputs,Target)
Model.score(inputs,Target)

# for  LogisticRegression

LogisticRegressionData = pd.read_csv('static/datasets/newdata.csv')
LogisticRegressionInputs = LogisticRegressionData.drop('Comments',axis = 'columns')
LogisticRegressionTarget = LogisticRegressionData['Comments']
LogisticRegressionModel = LogisticRegression(solver = 'lbfgs')

LogisticRegressionModel.fit(LogisticRegressionInputs,LogisticRegressionTarget)


 
print(LogisticRegressionData.head())
 

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

@app.route('/delete',methods = ['POST','GET'])
def delete():
	if request.method == 'POST':
		name = request.form['delete']

		Transaction = db['Students'].delete_one({"RegNumber": name})
		Transaction2 = db['AssessmentMarks'].remove({"RegNumber": name})
		print("Successfully deleted " + name)
		message = "Successfully deleted " + name
		students = []
		for student in db['Students'].find():
			students.append(student)
		return render_template('teachers.html',students = students,message = message)

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
				"Reg_number": reg_number,
				"Mark": Mark,
				"Age": age
			}
			Transaction = db.AssessmentMarks.insert_one(Mark)
			print("New record successfully added with transaction id " + str(Transaction.inserted_id))
			message = "Student record successfully added"
			students = []
			for student in db['Students'].find():
				students.append(student)

			return render_template("teachers.html",message = message,students = students)
		else:
			print("Student does not exist")
			print("Notifying user")
			message = "Sorry student record did not match any"
			return render_template('teachers.html',message = message)
	
	else:
		return render_template("teachers.html")

@app.route('/teachers')
def teachers():
	students = []
	for student in db['Students'].find():
		students.append(student)
	return render_template('teachers.html',students = students)

@app.route('/exammark',methods = ['POST','GET'])
def exammark():
	if request.method == 'POST':

		maths = request.form['math']
		eng = request.form['eng']
		shona = request.form['shona']
		gp = request.form['gp']
		reg_number = request.form['RegNumber']
		grade = request.form['grade']

		Exammarks = {
			"RegNumber" : reg_number,
			"Grade": grade,
			"Maths": maths,
			"English": eng,
			"Shona": shona,
			"Gp": gp,
		}

		count = db.Students.find({"RegNumber": reg_number}).count()
		if count > 0:
			findmark = db.Exammark.find({"$and": [{"RegNumber": reg_number},{"Grade": grade}]}).count()
			if findmark == 0:
				Transaction = db.Exammark.insert(Exammarks)
				print("Exam mark successfully entered")
				message = "Exam marks successfully recorded"
				return render_template('teachers.html', message = message)
			else:
				# Transaction = db.Exammark.update({"RegNumber": reg_number},{"$set":{"Maths": maths},{"English": eng},{"Shona": shona},{"Gp": gp},{multi=True}})
				Transaction = db.Exammark.replace_one({"$and": [{"RegNumber": reg_number},{"Grade": grade}]},Exammarks)
				message = "Exam marks successfully updated"
				return render_template('teachers.html',message = message)
		else:
			message = "Sorry no matching record found"
			return render_template('teachers.html',message = message)
		
	message = "Sorry could not perform the requested request"
	return render_template('teachers.html')


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
	message = "Failed tp Process that request"
	return render_template('teachers.html', message = message)



@app.route('/search',methods = ['POST','GET'])
def search():
	if request.method == 'POST':
		students = []
		search = request.form['search']

		for student in db['Students'].find():
			if student['RegNumber'] == search:
				students.append(student)
			elif student['Name'] == search:
				students.append(student)
			elif student['Surname'] == search:
				students.append(student)
		results = len(students)
		message = str(results) + " results found"
		return render_template('teachers.html',students = students, message = message)
	message = "Failed to process that request"
	return render_template('teachers.html',message = message)

@app.route('/review',methods =['POST','GET'])
def review():
	if request.method == 'POST':
		regnum = request.form['review']
		students = []
		StudentMarks = []
		Exammark = []

		for student in db['Students'].find({'RegNumber': regnum}):
			students.append(student)
			for marks in db['AssessmentMarks'].find({"Reg_number": regnum}):
				StudentMarks.append(marks)
			for examark in db['Exammark'].find({"RegNumber": regnum}):
				Exammark.append(examark)
				Maths = examark['Maths']
				Eng = examark['English']
				Shona = examark['Shona']
				Gp = examark['Gp']

			cond1 = db.AssessmentMarks.find({"Reg_number": regnum}).count()
			if cond1 > 0:
				cond2 = db.Exammark.find({"RegNumber": regnum}).count()
				if cond2 > 0:
					total = int(Maths) + int(Eng) + int(Shona) + int(Gp)
					print(".............................................................")
					print(str(Maths)+" "+str(Eng)+ " "+ str(Shona) +" " + str(Gp) + " "+ str(total))
					print(inputs.head())
					print(Model.score(inputs,Target))
					print(Model.predict([[Maths,Eng,Shona,Gp,total]]))
					Predict = Model.predict([[Maths,Eng,Shona,Gp,total]])

					if Predict == 1:
						prediction = "Pass"
					else:
						prediction = "Fail"
					# print(accuracy_score(Model.predict([[Maths,Eng,Shona,Gp,total]]),Target))
					return render_template('Review.html',students = students,StudentMarks = StudentMarks,Exammark = Exammark,prediction = prediction)
				else:
					message = "No Exam marks found for the student"
					return render_template('teachers.html',message = message)
			else:
				message = "No assessment marks found for the student"
				return render_template('teachers.html',message = message)
		
		

		
	return render_template('teachers.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
	