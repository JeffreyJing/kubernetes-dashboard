import React, { useEffect, useState } from 'react';
import './App.css';
import ObjectSection from './components/ObjectSection';

function App() {
  const [data, setData] = useState({});
  const objectTypes = ['pods', 'services', 'replicasets', 'deployments', 'nodes', 'namespaces', 'persistent_volumes', 'persistent_volume_claims']
  useEffect(() => {
    fetch('/snapshot.json')
      .then(res => res.json())
      .then(setData)
      .catch(() => setData({}));
  }, []);

  return (
    <div className="dashboard-container">
      <h1 className="title">Minikube Dashboard</h1>
      <div className="dashboard-layout">
        <div className="column left">
          {objectTypes.slice(0, 4).map((type, i) => (
            <div className="node-wrapper" key={i}>
              <ObjectSection key={i} type={type} items={data[type] || []} />
            </div>
          ))}
        </div>
        <div className="center-image" />
        <div className="column right">
          {objectTypes.slice(4).map((type, i) => (
            <div className="node-wrapper" key={i}>
              <ObjectSection key={i} type={type} items={data[type] || []} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
