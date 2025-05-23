from flask import Flask
from kubernetes import client, config
from flask_cors import CORS
from datetime import datetime
import os


app = Flask(__name__)
config.load_kube_config()
CORS(app)
core = client.CoreV1Api()
apps = client.AppsV1Api()

@app.route('/')
def cluster_view():
    pods = core.list_pod_for_all_namespaces().items
    replicasets = apps.list_replica_set_for_all_namespaces().items
    deployments = apps.list_deployment_for_all_namespaces().items
    services = core.list_service_for_all_namespaces().items

    html = "<h2>PODS</h2>"
    html += "<br>".join(p.metadata.name for p in pods)

    html += "<h2>REPLICASETS</h2>"
    html += "<br>".join(r.metadata.name for r in replicasets)

    html += "<h2>DEPLOYMENTS</h2>"
    html += "<br>".join(d.metadata.name for d in deployments)

    html += "<h2>SERVICES</h2>"
    html += "<br>".join(s.metadata.name for s in services)

    return html

@app.route('/api/cluster-state')
def cluster_state():
    return {
        "pods": [p.metadata.name for p in core.list_pod_for_all_namespaces().items],
        "replicasets": [r.metadata.name for r in apps.list_replica_set_for_all_namespaces().items],
        "deployments": [d.metadata.name for d in apps.list_deployment_for_all_namespaces().items],
        "services": [s.metadata.name for s in core.list_service_for_all_namespaces().items]
    }



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)