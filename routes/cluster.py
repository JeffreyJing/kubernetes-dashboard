from flask import Blueprint, jsonify
from kubernetes import client, config
from snapshot.writer import write_snapshot

cluster_bp = Blueprint("cluster", __name__)
config.load_kube_config()

core = client.CoreV1Api()
apps = client.AppsV1Api()

@cluster_bp.route('/')
def cluster_view():
    pods = core.list_pod_for_all_namespaces().items
    replicasets = apps.list_replica_set_for_all_namespaces().items
    deployments = apps.list_deployment_for_all_namespaces().items
    services = core.list_service_for_all_namespaces().items
    nodes = core.list_node().items
    namespaces = core.list_namespace().items
    pvs = core.list_persistent_volume().items
    pvcs = core.list_persistent_volume_claim_for_all_namespaces().items

    html = "<h2>PODS</h2>"
    html += "<br>".join(p.metadata.name for p in pods)

    html += "<h2>REPLICASETS</h2>"
    html += "<br>".join(r.metadata.name for r in replicasets)

    html += "<h2>DEPLOYMENTS</h2>"
    html += "<br>".join(d.metadata.name for d in deployments)

    html += "<h2>SERVICES</h2>"
    html += "<br>".join(s.metadata.name for s in services)

    html += "<h2>NODES</h2>"
    html += "<br>".join(node.metadata.name for node in nodes)

    html += "<h2>NAMESPACES</h2>"
    html += "<br>".join(ns.metadata.name for ns in namespaces)

    html += "<h2>PERSISTENT VOLUMES</h2>"
    html += "<br>".join(pv.metadata.name for pv in pvs)

    html += "<h2>PERSISTENT VOLUME CLAIMS</h2>"
    html += "<br>".join(pvc.metadata.name for pvc in pvcs)
    
    return html

@cluster_bp.route('/api/cluster-state')
def cluster_state():
    return {
        "pods": [p.metadata.name for p in core.list_pod_for_all_namespaces().items],
        "replicasets": [r.metadata.name for r in apps.list_replica_set_for_all_namespaces().items],
        "deployments": [d.metadata.name for d in apps.list_deployment_for_all_namespaces().items],
        "services": [s.metadata.name for s in core.list_service_for_all_namespaces().items]
    }

@cluster_bp.route('/api/save')
def save_snapshot():
    write_snapshot()
    return jsonify({"status": "success", "message": "Snapshot saved."})