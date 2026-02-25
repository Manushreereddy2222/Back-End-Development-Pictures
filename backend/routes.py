from . import app
import os
import json
from flask import jsonify, request

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data = json.load(open(json_url))

@app.route("/health")
def health():
    return jsonify({"status": "OK"}), 200


@app.route("/count")
def count():
    if data:
        return jsonify({"length": len(data)}), 200
    return jsonify({"Message": "Internal server error"}), 500


@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for pic in data:
        if pic["id"] == id:
            return jsonify(pic), 200
    return jsonify({"Message": "Picture not found"}), 404


@app.route("/picture", methods=["POST"])
def create_picture():
    new_pic = request.get_json()
    for pic in data:
        if pic["id"] == new_pic["id"]:
            return jsonify({"Message": f"picture with id {new_pic['id']} already present"}), 302
    data.append(new_pic)
    return jsonify(new_pic), 201


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated = request.get_json()
    for pic in data:
        if pic["id"] == id:
            pic.update(updated)
            return jsonify(pic), 200
    return jsonify({"Message": "Picture not found"}), 404


@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for pic in data:
        if pic["id"] == id:
            data.remove(pic)
            return "", 204
    return jsonify({"Message": "Picture not found"}), 404
