import { use, useState } from 'react'
import "./App.css"

export default function App() {
  const [status, setStatus] = useState("Idle");
  const [log, setLog] = useState([]);

  return (
    <div className="app">
      <div className="top">
        <h1>VoiceOS v2</h1>
        <div className="status">{status}</div>
      </div>

      <div className="main">
        <div className="panel">
          <h2>Assistant Log</h2>
          <div className="log">
            {log.length === 0 ? (
              <p className="muted">No activity yet...</p>
            ) : (
              log.map((item, i) => <p key={i}>{item}</p>)
            )}
          </div>
        </div>
      </div>
    </div>
  );
}