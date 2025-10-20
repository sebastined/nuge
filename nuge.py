from flask import Flask, request, jsonify, send_from_directory
import random, os, sys

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/random", methods=["GET", "POST"])
def random_api():
    try:
        data = request.get_json(force=True) if request.method == "POST" else request.args
        minv = int(data.get("min", -sys.maxsize - 1))
        maxv = int(data.get("max", sys.maxsize))
        count = max(1, min(int(data.get("count", 1)), 1000))
        if minv > maxv:
            raise ValueError("min > max")
        nums = [random.randint(minv, maxv) for _ in range(count)]
        return jsonify(nums)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    print("Server running at: http://127.0.0.1:8080")
    app.run(host="0.0.0.0", port=8080)
