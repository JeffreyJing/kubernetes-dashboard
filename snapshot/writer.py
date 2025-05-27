import os
import json
import shutil
from kubernetes import client, config
from datetime import datetime

config.load_kube_config()
core = client.CoreV1Api()
apps = client.AppsV1Api()

def get_pod_data():
    pods = core.list_pod_for_all_namespaces().items
    return [{
        "name": pod.metadata.name,
        "namespace": pod.metadata.namespace,
        "status": pod.status.phase,
        "node": pod.spec.node_name,
        "labels": pod.metadata.labels,
        "containers": [c.image for c in pod.spec.containers],
        "restarts": sum(cs.restart_count for cs in pod.status.container_statuses or []),
        "created": pod.metadata.creation_timestamp.isoformat()
    } for pod in pods]

def get_deployment_data():
    deployments = apps.list_deployment_for_all_namespaces().items
    return [{
        "name": deploy.metadata.name,
        "namespace": deploy.metadata.namespace,
        "replicas": deploy.status.replicas,
        "available": deploy.status.available_replicas,
        "labels": deploy.metadata.labels,
        "created": deploy.metadata.creation_timestamp.isoformat()
    } for deploy in deployments]

def get_replicaset_data():
    replicasets = apps.list_replica_set_for_all_namespaces().items
    return [{
        "name": rs.metadata.name,
        "namespace": rs.metadata.namespace,
        "replicas": rs.status.replicas,
        "ready": rs.status.ready_replicas,
        "labels": rs.metadata.labels,
        "created": rs.metadata.creation_timestamp.isoformat()
    } for rs in replicasets]

def get_service_data():
    services = core.list_service_for_all_namespaces().items
    return [{
        "name": s.metadata.name,
        "namespace": s.metadata.namespace,
        "type": s.spec.type,
        "cluster_ip": s.spec.cluster_ip,
        "ports": [{"port": p.port, "targetPort": p.target_port} for p in s.spec.ports],
        "labels": s.metadata.labels,
        "created": s.metadata.creation_timestamp.isoformat()
    } for s in services]

def get_node_data():
    nodes = core.list_node().items
    return [{
        "name": n.metadata.name,
        "labels": n.metadata.labels,
        "conditions": [{ "type": c.type, "status": c.status } for c in n.status.conditions],
        "created": n.metadata.creation_timestamp.isoformat()
    } for n in nodes]

def get_namespace_data():
    namespaces = core.list_namespace().items
    return [{
        "name": ns.metadata.name,
        "status": ns.status.phase,
        "labels": ns.metadata.labels,
        "created": ns.metadata.creation_timestamp.isoformat()
    } for ns in namespaces]

def get_pvc_data():
    pvcs = core.list_persistent_volume_claim_for_all_namespaces().items
    return [{
        "name": pvc.metadata.name,
        "namespace": pvc.metadata.namespace,
        "status": pvc.status.phase,
        "storage": pvc.spec.resources.requests.get("storage"),
        "volume": pvc.spec.volume_name,
        "created": pvc.metadata.creation_timestamp.isoformat()
    } for pvc in pvcs]

def get_pv_data():
    pvs = core.list_persistent_volume().items
    return [{
        "name": pv.metadata.name,
        "status": pv.status.phase,
        "capacity": pv.spec.capacity.get("storage"),
        "access_modes": pv.spec.access_modes,
        "storage_class": pv.spec.storage_class_name,
        "claim": f"{pv.spec.claim_ref.namespace}/{pv.spec.claim_ref.name}" if pv.spec.claim_ref else None,
        "created": pv.metadata.creation_timestamp.isoformat()
    } for pv in pvs]

def write_snapshot():
    os.makedirs("snapshot/snapshots", exist_ok=True)
    timestamp = datetime.now().strftime("%H_%M-%m-%d-%Y")
    filename = f"snapshot/snapshots/snapshot-{timestamp}.json"
    snapshot = {
        "pods": get_pod_data(),
        "deployments": get_deployment_data(),
        "replicasets": get_replicaset_data(),
        "services": get_service_data(),
        "nodes": get_node_data(),
        "namespaces": get_namespace_data(),
        "persistent_volume_claims": get_pvc_data(),
        "persistent_volumes": get_pv_data()
    }

    with open(filename, "w") as f:
        json.dump(snapshot, f, indent=2)
    
    shutil.copy(filename, "dashboard-frontend/public/snapshot.json")
    print(f"✅ Snapshot saved to {filename}")