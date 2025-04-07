// ui/src/App.tsx
import { useState } from 'react';
import { motion } from 'framer-motion';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { LayoutGrid, FolderKanban, Cpu, ListTodo, Puzzle } from "lucide-react";
import SystemInfoPanel from "@/components/panels/__tests__/SystemInfoPanel.test";

export default function App() {
  const [isListening, setIsListening] = useState(false);
  const [input, setInput] = useState("");
  const [error, setError] = useState("");
  const [responseText, setResponseText] = useState("");
  const [activeTab, setActiveTab] = useState("system");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    setIsListening(true);
    setError("");
    setResponseText("");

    try {
      const response = await fetch("http://localhost:8000/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: input }),
      });

      if (!response.ok) {
        throw new Error("Backend responded with an error.");
      }

      const result = await response.json();
      setResponseText(result?.response || "No response from assistant.");
    } catch (error) {
      console.error("Error contacting backend:", error);
      setError("⚠️ Assistant backend not reachable or failed.");
    }

    setInput("");
    setIsListening(false);
  };

  return (
    <div className="grid grid-cols-[18vw_1fr] min-h-screen w-full bg-slate-900 text-white">
      {/* Sidebar */}
      <div className="min-w-[220px] bg-slate-800 border-r border-slate-700 flex flex-col">
        <div className="p-4 border-b border-slate-700 text-xl font-bold">Athena</div>
        <div className="flex flex-col gap-2 p-4">
          <button onClick={() => setActiveTab("system")} className={`flex items-center gap-2 px-2 py-1 rounded hover:bg-slate-700 ${activeTab === 'system' && 'bg-slate-700'}`}><Cpu size={16} /> System Info</button>
          <button onClick={() => setActiveTab("directory")} className={`flex items-center gap-2 px-2 py-1 rounded hover:bg-slate-700 ${activeTab === 'directory' && 'bg-slate-700'}`}><FolderKanban size={16} /> Directory</button>
          <button onClick={() => setActiveTab("intents")} className={`flex items-center gap-2 px-2 py-1 rounded hover:bg-slate-700 ${activeTab === 'intents' && 'bg-slate-700'}`}><ListTodo size={16} /> Unmapped Intents</button>
          <button onClick={() => setActiveTab("modules")} className={`flex items-center gap-2 px-2 py-1 rounded hover:bg-slate-700 ${activeTab === 'modules' && 'bg-slate-700'}`}><Puzzle size={16} /> Modules</button>
        </div>
      </div>

      {/* Main Panel */}
      <main className="grid place-items-center px-4 gap-6">
        {activeTab === "system" && <SystemInfoPanel />}

        {activeTab === "assistant" && (
          <>
            <motion.div
              className={`aspect-square w-[50vw] max-w-[320px] rounded-full border-[6px] shadow-lg transition-colors duration-300 
                ${isListening ? 'border-blue-500 shadow-blue-500/50' : 'border-slate-700 shadow-slate-700/40'} 
                flex items-center justify-center text-xl font-semibold text-white bg-slate-800 backdrop-blur`}
              animate={{ scale: isListening ? 1.08 : 1.0 }}
              transition={{ duration: 0.6, repeat: Infinity, repeatType: "reverse" }}
            >
              {isListening ? '🎙️ Listening...' : '🔈 Idle'}
            </motion.div>

            <form onSubmit={handleSubmit} className="w-full max-w-2xl px-4 flex gap-2">
              <Input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type something and hit Enter..."
              />
              <Button type="submit" variant="default">Send</Button>
            </form>

            {(responseText || error) && (
              <Card className="w-full max-w-2xl bg-slate-800 border border-slate-700 mt-2">
                <CardContent className="p-4 text-sm">
                  {responseText && <div className="text-green-400">💬 {responseText}</div>}
                  {error && <div className="text-red-400">{error}</div>}
                </CardContent>
              </Card>
            )}
          </>
        )}
      </main>
    </div>
  );
}
