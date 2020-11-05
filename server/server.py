from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import random
#from markov_chain import markov
#from aggregator import aggregator
import base64
from detectLive import *

app = Flask(__name__)
CORS(app)

@app.route("/print", methods=['GET'])
def Saada():
	print("Identity Number: XXXX-XXXXXXXXX-X")
	print("Name: Syed Owais Chishti")
	print("Gender: Male")
	print("Father's Name : Syed Naeem Chishti")
	print("D.O.B : 25/05/1994")
	print("Address: House L77 Sector 11/C-1 North Karachi, Karachi")

@app.route("/nicF", methods=['POST'])
def nicFFunc():
	nicF = request.form.get("nicF")
	# print(nicF)
	try:
		nicF = nicF.split(";base64,")[1]
	except:
		pass
	nicF = imgConversion(nicF)
	nicF = isFaceCheck(nicF, "nicfront")
	if nicF:
		return jsonify({"status" : 200})
	else:
		return jsonify({"status" : 500})

@app.route("/nicB", methods=['POST'])
def nicBFunc():
	nicF = request.form.get("nicF")
	# print(nicF)
	try:
		nicF = nicF.split(";base64,")[1]
	except:
		pass
	nicF = imgConversion(nicF)
	nicF = isFaceCheck(nicF, "nicback")
	if nicF:
		return jsonify({"status" : 200})
	else:
		return jsonify({"status" : 500})


@app.route("/selfie", methods=['POST'])
def selfieFunc():
	selfie = request.form.get("selfie")
	# print(selfie)
	try:
		selfie = selfie.split(";base64,")[1]
	except:
		pass
	selfie = imgConversion(selfie)
	selfie = isSelfieCheck(selfie)
	if selfie:
		return jsonify({"status" : 200})
	else:
		return jsonify({"status" : 500})

@app.route("/video", methods=["POST"])
def videoFunc():
	file = request.files['file']
	file.save("face_data/video.mp4")
	return jsonify({"status" : 200})

@app.route("/evaluate", methods=["GET"])
def evaFunc():
	casenicf = request.args.get("casenicf")
	casenicb = request.args.get("casenicb")
	casevideo = request.args.get("casevideo")
	caseselfie = request.args.get("caseselfie")
	# print(casenicf, type(casenicf))
	results = evaluation(casenicf, casenicb, casevideo, caseselfie)
	# results=123
	import requests
	requests.get("http://localhost:5000/print")
	return jsonify({"results" : results})

@app.route('/counter', methods=['GET'])
def home():
	genderList=['Male','Female']
	ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
	emotion =  ['Anger', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

	client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
	db = client["camera01_roi"]
	human_counter = db["human_counter"]
	human_demo = db["human_demo"]

	dict = {}
	try:
		# count total
		_ = human_counter.find({}, {"inside":1}).sort([("inside", -1)]).limit(1)
		dict["count"] = [{"inside":[each["inside"] for each in _][0]}]
		_ = human_counter.find({}, {"outside":1}).sort([("outside", -1)]).limit(1)
		dict["count"].append({"outside": [each["outside"] for each in _][0]})
		_ = human_counter.find({}, {"_id":1}).sort([("_id", -1)]).limit(1)
		dict["count"].append({"date": [each["_id"] for each in _][0]})

		# count gender
		for index, each in enumerate(genderList):
			if index == 0:
				dict["gender"] = [{each: human_demo.find({"gender": each}, {"gender":1}).count()}]
			else:
				dict["gender"].append({each: human_demo.find({"gender": each}, {"gender":1}).count()})

		# count age
		for index, each in enumerate(ageList):
			if index == 0:
				dict["age"] = [{each: human_demo.find({"age": each[1:-1]}, {"age":1}).count()}]
			else:
				dict["age"].append({each: human_demo.find({"age": each[1:-1]}, {"age":1}).count()})

		# count emotion
		for index, each in enumerate(emotion):
			if index == 0:
				dict["emotion"] = [{each: human_demo.find({"emotion": each}, {"emotion":1}).count()}]
			else:
				dict["emotion"].append({each: human_demo.find({"emotion": each}, {"emotion":1}).count()})

		dict['emotion'].pop(1);dict['emotion'].pop(1);dict['emotion'].pop(3)

		#pdb.set_trace()
		dict["aggregate"] = aggregator()
		return jsonify(dict)
	except Exception as e:
		print(str(e))
		return "No Results"

if __name__ == "__main__":
	app.run('0.0.0.0',port=5000, debug=True, threaded=True)
