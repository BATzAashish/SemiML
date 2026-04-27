import { getExplainability } from "@/services/api.js";
import { useAsyncData } from "@/hooks/useAsyncData";
import { LoadingPanel, ErrorPanel } from "@/components/dashboard/DataState";
import { SectionHeader } from "@/components/dashboard/SectionHeader";
import { SimpleBarChart } from "@/components/charts/DashboardCharts";

export default function ExplainabilityPage() {
  const { data, loading, error } = useAsyncData(getExplainability);
  if (loading) return <LoadingPanel label="Computing SHAP explanations" />; if (error) return <ErrorPanel message={error} />;
  return <div className="animate-enter-up space-y-6"><SectionHeader eyebrow="Explainability" title="SHAP and feature attribution" description="Global importance, SHAP directionality, and local prediction evidence make recommendations inspectable." />
    <div className="grid gap-6 lg:grid-cols-2"><section className="panel rounded-lg border p-5"><h2 className="font-display text-xl font-bold">Feature importance</h2><SimpleBarChart data={data.importance} x="feature" /></section><section className="panel rounded-lg border p-5"><h2 className="font-display text-xl font-bold">SHAP summary impact</h2><div className="mt-5 space-y-3">{data.shap.map((s) => <div key={s.feature}><div className="mb-1 flex justify-between text-sm"><span>{s.feature}</span><b>{s.impact > 0 ? "+" : ""}{s.impact}</b></div><div className="h-3 rounded-full bg-muted"><div className={`h-3 rounded-full ${s.impact >= 0 ? "bg-primary" : "bg-accent"}`} style={{ width: `${Math.abs(s.impact) * 100}%` }} /></div></div>)}</div></section><section className="panel rounded-lg border p-5 lg:col-span-2"><h2 className="font-display text-xl font-bold">Individual prediction explanation</h2><p className="mt-3 text-3xl font-bold text-gradient">{data.prediction.class} · {(data.prediction.probability * 100).toFixed(0)}%</p><div className="mt-4 flex flex-wrap gap-3">{data.prediction.drivers.map((d) => <span key={d} className="rounded-full bg-secondary px-3 py-2 text-sm font-semibold text-secondary-foreground">{d}</span>)}</div></section></div>
  </div>;
}
