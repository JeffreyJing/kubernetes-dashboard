from flask import Flask
from kubernetes import client, config

app = Flask(__name__)

config.load_kube_config()

v1 = client.CoreV1Api()

@app.route('/')
def list_pods():
    pods = v1.list_pod_for_all_namespaces()
    pod_names = [pod.metadata.name for pod in pods.items]
    return "<br>".join(pod_names)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)