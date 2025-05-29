import React, { useState } from 'react';
import './ObjectSection.css';

function ObjectSection({ type, items = [] }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="node" onClick={() => setIsOpen(!isOpen)}>
      <div className="node-title">{type.replace(/_/g, ' ').toUpperCase()}</div>
      {isOpen && (
        <ul className="dropdown">
          {items.map((item, i) => (
            <li key={i}>{item.name}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default ObjectSection;
