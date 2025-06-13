from flask import Flask, render_template, request, jsonify
import pyotp, time, re

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    secret = data.get("secret", "").strip().replace(" ", "").upper()

    if not re.fullmatch(r"[A-Z2-7]+", secret):
        return jsonify({"error": "Secret key harus berformat Base32 (A-Z, 2-7)"}), 400

    try:
        totp = pyotp.TOTP(secret)
        return jsonify({
            "code": totp.now(),
            "expires_in": int(totp.interval - (time.time() % totp.interval))
        })
    except Exception as e:
        return jsonify({"error": f"Gagal generate: {str(e)}"}), 400

if __name__ == "__main__":
    app.run(debug=True)

