import { useState } from "react";
import { Bot, Loader2, Send, User } from "lucide-react";
import { SectionHeader } from "@/components/dashboard/SectionHeader";
import { sendChatMessage } from "@/services/api.js";

export default function AssistantPage() {
  const [messages, setMessages] = useState([{ role: "assistant", content: "Ask me why a model was selected, how constraints affected the pipeline, or what changes would trigger retraining." }]);
  const [input, setInput] = useState(""); const [loading, setLoading] = useState(false);
  const send = async (e) => { e.preventDefault(); if (!input.trim()) return; const next = [...messages, { role: "user", content: input.trim() }]; setMessages(next); setInput(""); setLoading(true); try { const reply = await sendChatMessage(input.trim(), next); setMessages([...next, reply]); } finally { setLoading(false); } };
  return <div className="animate-enter-up"><SectionHeader eyebrow="AI assistant" title="Ask the decision system" description="A conversational layer helps stakeholders interrogate model choices, assumptions, and what-if changes." />
    <section className="panel flex h-[68vh] flex-col rounded-lg border"><div className="flex-1 space-y-4 overflow-y-auto p-5">{messages.map((m, i) => <div key={i} className={`flex gap-3 ${m.role === "user" ? "justify-end" : ""}`}><div className={`flex max-w-2xl gap-3 rounded-lg p-4 ${m.role === "user" ? "bg-primary text-primary-foreground" : "bg-surface-strong"}`}>{m.role === "user" ? <User className="h-5 w-5 shrink-0" /> : <Bot className="h-5 w-5 shrink-0 text-primary" />}<p className="text-sm leading-6">{m.content}</p></div></div>)}{loading && <div className="flex items-center gap-2 text-sm text-muted-foreground"><Loader2 className="h-4 w-4 animate-spin" />Assistant is reasoning over trace and metrics...</div>}</div><form onSubmit={send} className="border-t p-4"><div className="flex gap-3"><input value={input} onChange={(e) => setInput(e.target.value)} className="flex-1 rounded-md border bg-background px-4 py-3" placeholder="Why this model?" /><button disabled={loading} className="rounded-md bg-primary px-4 text-primary-foreground disabled:opacity-60"><Send className="h-5 w-5" /></button></div></form></section>
  </div>;
}
