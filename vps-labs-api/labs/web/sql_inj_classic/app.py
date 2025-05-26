from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Login page vulnerable to SQLi (stub)</h1><p>Username: <input></p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

