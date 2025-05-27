from flask import Flask
from flask_cors import CORS
from routes import cluster_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(cluster_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)