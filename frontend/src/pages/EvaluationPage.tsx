import { Download } from "lucide-react";
import { getEvaluation } from "@/services/api.js";
import { useAsyncData } from "@/hooks/useAsyncData";
import { LoadingPanel, ErrorPanel } from "@/components/dashboard/DataState";
import { SectionHeader } from "@/components/dashboard/SectionHeader";
import { ConfusionMatrix, RocCurve } from "@/components/charts/DashboardCharts";

export default function EvaluationPage() {
  const { data, loading, error } = useAsyncData(getEvaluation);
  if (loading) return <LoadingPanel label="Loading evaluation metrics" />; if (error) return <ErrorPanel message={error} />;
  const download = () => { const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" }); const url = URL.createObjectURL(blob); const a = document.createElement("a"); a.href = url; a.download = "model-evaluation-report.json"; a.click(); URL.revokeObjectURL(url); };
  return <div className="animate-enter-up space-y-6"><SectionHeader eyebrow="Evaluation" title="Model results and validation" description="Compare core performance metrics with diagnostic plots used for model acceptance." action={<button onClick={download} className="inline-flex items-center gap-2 rounded-md bg-primary px-4 py-2 font-semibold text-primary-foreground"><Download className="h-4 w-4" />Download report</button>} />
    <div className="grid gap-6 lg:grid-cols-[.9fr_1.1fr]"><section className="panel rounded-lg border p-5"><h2 className="font-display text-xl font-bold">Metrics table</h2><table className="mt-4 w-full text-sm"><tbody>{data.metrics.map((m) => <tr key={m.metric} className="border-t"><td className="py-3 text-muted-foreground">{m.metric}</td><td className="text-right font-bold">{m.value < 1 ? (m.value * 100).toFixed(1) + "%" : m.value}</td></tr>)}</tbody></table></section><section className="panel rounded-lg border p-5"><h2 className="font-display text-xl font-bold">ROC curve</h2><RocCurve data={data.roc} /></section><section className="panel rounded-lg border p-5 lg:col-span-2"><h2 className="font-display text-xl font-bold">Confusion matrix</h2><div className="mt-5 flex justify-center"><ConfusionMatrix matrix={data.confusion} /></div></section></div>
  </div>;
}
