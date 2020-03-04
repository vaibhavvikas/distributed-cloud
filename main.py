import os
import os.path
from os import path
import json
import uuid
import shutil
import urllib.request
from app import app
from flask import Flask, request, redirect, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename

def update_file():
	try:
		with open("files.json", "r") as fp:
			return json.load(fp)
	except:
		file_list = []
		return file_list

	
def break_file(sfile, sfileid):
	metadata = []
	with open("config.json", "r") as fp:
			info = json.load(fp)
	CHUNK_SIZE = info["size_per_slice"]
	res = str(app.config['UPLOAD_FOLDER'] + "/" + sfile)
	file_number = 1
	filenumbernode = []
	for i in range(1, info["node_count"]+1):
		try:
			os.mkdir(os.path.join(str(app.config['UPLOAD_FOLDER']) +"/node_" + str(i)))
		except:
			continue
	for i in range(1, info["node_count"]+1):
		onlyfiles = next(os.walk(str(app.config['UPLOAD_FOLDER']) +"/node_" + str(i)))[2]
		filenumbernode.append(len(onlyfiles))
	node_number = filenumbernode.index(min(filenumbernode)) + 1
	with open(res, "rb") as f:
		chunk = f.read(CHUNK_SIZE)
		while chunk:
			tempnode = str(app.config['UPLOAD_FOLDER']) + "/" + "node_" + str(node_number) + "/" + sfile + "." + str(file_number)
			with open(str(tempnode), "wb") as chunk_file:
				chunk_file.write(chunk)
			metadata.append({str(tempnode) : str(str(app.config['UPLOAD_FOLDER']) + "/" + "node_" + str(node_number))})
			file_number += 1
			node_number = (node_number + 1)%info["node_count"]
			if node_number == 0:
				node_number = info["node_count"]
			chunk = f.read(CHUNK_SIZE)
	filenumbernode = []
	with open(str(app.config['UPLOAD_FOLDER']) +"/" + sfileid + ".json", "w") as fp:
		json.dump(metadata, fp)


def down_file(sfileid):
	outdata = b''
	metadata = []
	z = 0
	flag = 0
	with open(str(app.config['UPLOAD_FOLDER']) +"/" + sfileid + ".json", "r") as fp:
		metadata = json.load(fp)
	for each in metadata:
		for key in each.items():
			if flag == 0:
				filename = str(key)
				filename = filename[:-2]
				flag = 1
			if str(path.exists(key)) == "True":
				with open(key, 'rb') as fp:
					outdata += fp.read()
			else:
				z = 1
				break
		if z == 1:
			break
	filename = filename.split("/")
	newfile = filename[-1]
	if z == 0:
		with open(str(app.config['UPLOAD_FOLDER']) +"/" + newfile, "wb") as fp:
			fp.write(outdata)


def delete_chunks(sfileid):
	metadata = []
	with open(str(app.config['UPLOAD_FOLDER']) +"/" + sfileid + ".json", "r") as fp:
		metadata = json.load(fp)
	for each in metadata:
		for key in each.items():
			try:
				os.remove(key)
			except:
				continue
	os.remove(str(app.config['UPLOAD_FOLDER']) + "/" + sfileid + ".json")


@app.route('/files', methods=['PUT'])
def upload_file():
	file_list = update_file()
	file = request.files['file']
	file_id = str(uuid.uuid1())
	filename = secure_filename(file.filename)
	for each in file_list:
		if str(filename) == str(each["file_name"]):
			res = jsonify({"message" : "File already exists"})
			res.status_code = 409
			return res
	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	break_file(str(filename), file_id)
	file_list.append({"file_name": filename ,"id": file_id})
	with open("files.json", "w") as fp:
		json.dump(file_list, fp)
	return file_id


@app.route('/files/list', methods=['GET'])
def list_files():
	file_list = update_file()
	return jsonify(file_list)


@app.route('/files/<path:path>', methods=['GET'])
def download(path):
	temp = ""
	file_list = update_file()
	for each in file_list:
		if str(path) == each["id"]:
			temp = str(each["file_name"])
			down_file(path)
			return send_from_directory(app.config['UPLOAD_FOLDER'], temp, as_attachment=True)
	res = jsonify({"message":"File Doesnot exists"})
	res.status_code = 404
	return res


@app.route('/files/<path:path>', methods=['DELETE'])
def delete(path):
	flag = 1
	file_list = update_file()
	for each in file_list:
		if str(path) == str(each["id"]):
			file_list.remove(each)
			with open("files.json", "w") as fp:
				json.dump(file_list, fp)
			delete_chunks(str(path))
			flag = 0
			z = "object " + path +" deleted sucessfully"
	if flag == 1:
		resp = jsonify({'message' : 'File doesnot exist'})
		resp.status_code = 404
		return resp
	return z


if __name__ == "__main__":
	app.run()