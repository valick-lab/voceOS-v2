import { useState, useEffect } from "react";

declare global {
  interface Window {
    api: {
      sendCommand: (command: string) => void;
      onResponse: (callback: (data: string) => void) => (() => void);
    };
  }
}

export default function App() {
  const [warning, setWarning] = useState<string | null>(null);
  const [status, setStatus] = useState<"Idle" | "Listening" | "Thinking">("Idle");
  const [log, setLog] = useState<string[]>([]);

  const addLog = (text: string) => {
    setLog((prev) => [...prev, text]);
  };

  useEffect(() => {
    const unsubscribe = window.api.onResponse((data) => {
      const parsed = JSON.parse(data);
      addLog(parsed.response);

      if (status !== "Listening") {
        setStatus("Idle");
      }
    });

    return () => {
      unsubscribe?.();
    };
  }, [status]);

  const showWarning = (text: string) => {
    setWarning(text);
    setTimeout(() => setWarning(null), 3000);
  };

  const startListening = () => {
    if (status === "Listening") {
      showWarning("Голосовой помощник уже слушает!");
      return;
    }

    setStatus("Listening");
    addLog("🎤 Ассистент запущен");
    window.api.sendCommand("start");
  };

  const stopListening = () => {
    if (status !== "Listening") {
      showWarning("Ассистент уже остановлен");
      return;
    }

    setStatus("Idle");
    addLog("⛔ Остановлен");
    window.api.sendCommand("stop");
  };

  const testCommand = () => {
    if (status === "Listening") {
      showWarning("Остановите ассистента перед тестом");
      return;
    }

    setStatus("Thinking");
    window.api.sendCommand("hello");
  };

  const statusStyle = {
    Idle: "bg-purple-500/10 border-purple-500/30 text-purple-300",
    Listening: "bg-blue-500/10 border-blue-500/40 text-blue-300",
    Thinking: "bg-violet-500/10 border-violet-500/40 text-violet-300",
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#070812] text-white">

      {warning && (
        <div className="absolute top-4 px-4 py-2 rounded-lg bg-red-500/20 border border-red-500 text-red-300 text-sm">
          {warning}
        </div>
      )}

      <div className="w-[900px] max-w-[95%] p-6 rounded-2xl border border-purple-500/20 backdrop-blur-xl bg-[#121423]/70 shadow-[0_0_40px_rgba(124,58,237,0.3)]">

        <div className="flex justify-between items-center mb-6">
          <h1 className="text-xl tracking-wide">VoiceOS v2</h1>
          <div className={`px-3 py-1 rounded-full border text-xs ${statusStyle[status]}`}>
            {status}
          </div>
        </div>

        <div className="flex justify-center my-8 relative">
          <div className={`absolute w-40 h-40 rounded-full blur-2xl opacity-40
            ${status === "Listening" ? "bg-blue-500 animate-pulse" : ""}
            ${status === "Thinking" ? "bg-purple-500 animate-pulse" : ""}
          `} />
          <div className={`w-24 h-24 rounded-full bg-gradient-to-br from-purple-500 via-blue-500 to-cyan-400 shadow-[0_0_50px_rgba(124,58,237,0.7)] transition-all duration-300
            ${status === "Listening" ? "scale-125" : ""}
            ${status === "Thinking" ? "scale-110 animate-pulse" : ""}
            ${status === "Idle" ? "opacity-70" : ""}
          `} />
        </div>

        <div className="flex gap-3 mb-6">
          <button
            onClick={startListening}
            disabled={status === "Listening"}
            className="px-4 py-2 rounded-lg bg-black/40 border border-purple-500/30 disabled:opacity-40"
          >
            Start
          </button>

          <button
            onClick={stopListening}
            className="px-4 py-2 rounded-lg bg-black/40 border border-purple-500/30"
          >
            Stop
          </button>

          <button
            onClick={testCommand}
            className="px-4 py-2 rounded-lg bg-black/40 border border-purple-500/30"
          >
            Test
          </button>
        </div>

        <div className="p-4 rounded-xl bg-black/40 border border-purple-500/20">
          <h2 className="mb-2 text-sm text-purple-300">Activity</h2>
          <div className="text-xs text-gray-400 max-h-[200px] overflow-y-auto space-y-1">
            {log.length === 0 ? (
              <p className="opacity-50">No activity</p>
            ) : (
              log.map((item, i) => <p key={i}>{item}</p>)
            )}
          </div>
        </div>

      </div>
    </div>
  );
}