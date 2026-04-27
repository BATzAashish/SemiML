import { CheckCircle2, Cpu, GitBranch } from "lucide-react";
import { getPipeline } from "@/services/api.js";
import { useAsyncData } from "@/hooks/useAsyncData";
import { useDecisionSystem } from "@/context/DecisionSystemContext";
import { LoadingPanel, ErrorPanel } from "@/components/dashboard/DataState";
import { SectionHeader } from "@/components/dashboard/SectionHeader";

export default function PipelinePage() {
  const { data, loading, error } = useAsyncData(getPipeline); const { selectedModel, setSelectedModel } = useDecisionSystem();
  if (loading) return <LoadingPanel label="Generating pipeline recommendation" />; if (error) return <ErrorPanel message={error} />;
  return <div className="animate-enter-up space-y-6"><SectionHeader eyebrow="Recommendation" title="Pipeline recommendation" description="A semi-autonomous plan balances performance, constraints, and interpretability before selecting a model." />
    <section className="panel rounded-lg border p-5"><h2 className="flex items-center gap-2 font-display text-xl font-bold"><GitBranch className="h-5 w-5 text-primary" />Recommended steps</h2><div className="mt-5 grid gap-3 md:grid-cols-3">{data.steps.map((step, i) => <div key={step} className="rounded-md border bg-surface p-4"><span className="text-xs font-bold text-primary">STEP {i + 1}</span><p className="mt-2 font-semibold">{step}</p></div>)}</div></section>
    <section className="grid gap-4 lg:grid-cols-3">{data.models.map((m) => { const active = selectedModel === m.name || m.selected; return <button key={m.name} onClick={() => setSelectedModel(m.name)} className={`panel rounded-lg border p-5 text-left transition hover:-translate-y-1 focus:outline-none focus:ring-2 focus:ring-ring ${active ? "border-primary shadow-glow" : ""}`}><div className="flex items-start justify-between"><Cpu className="h-6 w-6 text-primary" />{active && <CheckCircle2 className="h-5 w-5 text-success" />}</div><h3 className="mt-4 font-display text-xl font-bold">{m.name}</h3><div className="mt-4 space-y-2 text-sm"><p>Accuracy <b>{(m.accuracy * 100).toFixed(1)}%</b></p><p>Precision <b>{(m.precision * 100).toFixed(1)}%</b></p><p>Recall <b>{(m.recall * 100).toFixed(1)}%</b></p><p>Confidence <b>{(m.confidence * 100).toFixed(0)}%</b></p></div></button>; })}</section>
  </div>;
}
