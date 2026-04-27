import { GitCompare } from "lucide-react";
import { getExperiments } from "@/services/api.js";
import { useAsyncData } from "@/hooks/useAsyncData";
import { LoadingPanel, ErrorPanel } from "@/components/dashboard/DataState";
import { SectionHeader } from "@/components/dashboard/SectionHeader";
import { SimpleBarChart } from "@/components/charts/DashboardCharts";

export default function ExperimentsPage() {
  const { data, loading, error } = useAsyncData(getExperiments);
  if (loading) return <LoadingPanel label="Loading experiment history" />; if (error) return <ErrorPanel message={error} />;
  const chart = data.map((e) => ({ name: e.id, value: Number((e.performance * 100).toFixed(1)) }));
  return <div className="animate-enter-up space-y-6"><SectionHeader eyebrow="Experiment history" title="Past experiments and comparison" description="Review datasets, selected models, and performance across decision runs." />
    <section className="panel rounded-lg border p-5"><h2 className="flex items-center gap-2 font-display text-xl font-bold"><GitCompare className="h-5 w-5 text-primary" />Model comparison</h2><SimpleBarChart data={chart} /></section>
    <section className="panel rounded-lg border p-5"><div className="overflow-x-auto"><table className="w-full text-sm"><thead className="text-left text-muted-foreground"><tr><th className="py-3">Experiment</th><th>Dataset</th><th>Model used</th><th>Performance</th><th>Options</th></tr></thead><tbody>{data.map((e) => <tr key={e.id} className="border-t"><td className="py-3 font-bold text-primary">{e.id}</td><td>{e.dataset}</td><td>{e.model}</td><td>{(e.performance * 100).toFixed(1)}%</td><td><button className="rounded-md bg-secondary px-3 py-1.5 text-xs font-bold text-secondary-foreground">View details</button></td></tr>)}</tbody></table></div></section>
  </div>;
}
