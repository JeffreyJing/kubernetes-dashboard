import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState({});

  useEffect(() => {
    fetch('/snapshot.json')
      .then(res => res.json())
      .then(setData)
      .catch(() => setData({})); // match initial state
  }, []);

  return (
    <div className="background">
      <h2>PODS</h2>
      <ul>{(data.pods || []).map((r, i) => <li key={i}>{r.name}</li>)}</ul>

      <h2>DEPLOYMENTS</h2>
      <ul>{(data.deployments || []).map((d, i) => <li key={i}>{d.name}</li>)}</ul>

      <h2>SERVICES</h2>
      <ul>{(data.services || []).map((s, i) => <li key={i}>{s.name}</li>)}</ul>
      <h2>REPLICASETS</h2>
      <ul>{(data.replicasets || []).map((r, i) => <li key={i}>{r.name}</li>)}</ul>

      <h2>NAMESPACES</h2>
      <ul>{(data.namespaces || []).map((ns, i) => <li key={i}>{ns.name}</li>)}</ul>

      <h2>PERSISTENT VOLUMES</h2>
      <ul>{(data.persistent_volumes || []).map((pv, i) => <li key={i}>{pv.name}</li>)}</ul>
      
      <h2>PERSISTENT VOLUME CLAIMS</h2>
      <ul>{(data.persistent_volume_claims || []).map((pvc, i) => <li key={i}>{pvc.name}</li>)}</ul>
    </div>
  );
}

export default App;
