from flask import Flask, request, render_template, send_file, jsonify
from utils import compile_batch
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/delete")
def delete_exe():
    if os.path.exists("compiled.exe"):
        os.remove("compiled.exe")
    return jsonify({"message": "compiled.exe deleted"}), 200

@app.route("/compile", methods=["POST", "GET"])
def compile_route():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        if file and (file.filename.endswith(".cmd") or file.filename.endswith(".bat")):
            filename_to_save = "batch.cmd" if file.filename.endswith(".cmd") else "batch.bat"
            file.save(filename_to_save)
            if compile_batch(filename_to_save):
                os.remove(filename_to_save)
                return send_file("compiled.exe", as_attachment=True)
            else:
                return jsonify({"error": "Compilation failed."}), 500
        else:
            return jsonify({"error": "Invalid file type. Only .cmd or .bat files are allowed."}), 400
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
