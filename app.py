from flask import Flask, request, render_template, send_file, jsonify
from utils import compile_batch
import os
app = Flask(__name__)

@app.route("/")
def home(): return render_template("index.html")

@app.route("/delete")
def delete_exe():
    if os.path.exists("compiled.exe"):
        os.remove("compiled.exe")
    return jsonify(), 200
@app.route("/compile", methods=["POST"])
def compile():
    if request.method == "POST":
        if "file" in request.files:    
            file = request.files["file"]

            if file.filename.endswith(".cmd") or file.filename.endswith(".bat"):
                filename = "batch.cmd" if file.filename.endswith(".cmd") else "batch.bat"
                file.save(filename)

                if compile_batch():
                    os.remove("batch.cmd") if filename == "batch.cmd" else os.remove("batch.bat")
                    return send_file("compiled.exe", as_attachment=True)
    else:
        if os.path.exists("compiled.exe"):
            os.remove("compiled.exe")
        return render_template("index.html")

            


if __name__ == "__main__": app.run(debug=True)