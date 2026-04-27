import { Brain, ShieldCheck, Sparkles } from "lucide-react";
import { getDecisionTrace } from "@/services/api.js";
import { useAsyncData } from "@/hooks/useAsyncData";
import { LoadingPanel, ErrorPanel } from "@/components/dashboard/DataState";
import { SectionHeader } from "@/components/dashboard/SectionHeader";

export default function DecisionTracePage() {
  const { data, loading, error } = useAsyncData(getDecisionTrace);
  if (loading) return <LoadingPanel label="Reconstructing decision trace" />; if (error) return <ErrorPanel message={error} />;
  return <div className="animate-enter-up"><SectionHeader eyebrow="Decision trace" title="Why the system made each decision" description="Every recommendation is decomposed into reason, source, and confidence so academic and operational stakeholders can audit the path." />
    <div className="relative space-y-5 before:absolute before:left-5 before:top-6 before:h-[calc(100%-3rem)] before:w-px before:bg-border">{data.map((item, i) => <details key={item.decision} open={i < 2} className="panel group relative ml-12 rounded-lg border p-5"><summary className="cursor-pointer list-none"><span className="absolute -left-12 top-5 flex h-10 w-10 items-center justify-center rounded-full bg-trace text-primary-foreground shadow-glow motion-safe:animate-trace-pulse">{item.source === "rules" ? <ShieldCheck className="h-5 w-5" /> : item.source === "RAG" ? <Sparkles className="h-5 w-5" /> : <Brain className="h-5 w-5" />}</span><div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between"><h2 className="font-display text-xl font-bold">{item.decision}</h2><span className="rounded-full bg-trace-soft px-3 py-1 text-xs font-bold text-trace">{item.source} · {(item.confidence * 100).toFixed(0)}%</span></div></summary><p className="mt-4 text-muted-foreground">{item.reason}</p></details>)}</div>
  </div>;
}
