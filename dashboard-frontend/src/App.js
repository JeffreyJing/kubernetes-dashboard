import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/cluster-state')
      .then(res => res.json())
      .then(setData)
      .catch(() => setData(null));
  }, []);

  if (!data) return <p>Loading or Flask offline...</p>;

  return (
    <div>
      <h2>PODS</h2>
      <ul>{data.pods.map(p => <li key={p}>{p}</li>)}</ul>

      <h2>REPLICASETS</h2>
      <ul>{data.replicasets.map(r => <li key={r}>{r}</li>)}</ul>

      <h2>DEPLOYMENTS</h2>
      <ul>{data.deployments.map(d => <li key={d}>{d}</li>)}</ul>

      <h2>SERVICES</h2>
      <ul>{data.services.map(s => <li key={s}>{s}</li>)}</ul>
    </div>
  );
}

export default App;
