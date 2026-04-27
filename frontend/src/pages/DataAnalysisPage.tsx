import { getDataProfile } from "@/services/api.js";
import { useAsyncData } from "@/hooks/useAsyncData";
import { LoadingPanel, ErrorPanel } from "@/components/dashboard/DataState";
import { MetricCard } from "@/components/dashboard/MetricCard";
import { SectionHeader } from "@/components/dashboard/SectionHeader";
import { ClassPieChart, Heatmap, SimpleBarChart } from "@/components/charts/DashboardCharts";
import { Database, Table2, TriangleAlert } from "lucide-react";

export default function DataAnalysisPage() {
  const { data, loading, error } = useAsyncData(getDataProfile);
  if (loading) return <LoadingPanel label="Profiling dataset" />; if (error) return <ErrorPanel message={error} />;
  return <div className="animate-enter-up space-y-6"><SectionHeader eyebrow="Data profile" title="Dataset analysis" description="Automated profiling surfaces quality risks, class imbalance, distributions, and relationships used by the recommender." />
    <div className="grid gap-4 md:grid-cols-3"><MetricCard label="Rows" value={data.overview.rows.toLocaleString()} icon={Database} /><MetricCard label="Columns" value={data.overview.columns} tone="accent" icon={Table2} /><MetricCard label="Missing values" value={data.overview.missingValues} tone="success" icon={TriangleAlert} /></div>
    <div className="grid gap-6 lg:grid-cols-2"><section className="panel rounded-lg border p-5"><h2 className="font-display text-xl font-bold">Missing values by feature</h2><SimpleBarChart data={data.missingValues} /></section><section className="panel rounded-lg border p-5"><h2 className="font-display text-xl font-bold">Class imbalance</h2><ClassPieChart data={data.classes} /></section><section className="panel rounded-lg border p-5"><h2 className="font-display text-xl font-bold">Feature distribution ranges</h2><SimpleBarChart data={data.distributions} x="feature" y="mid" /></section><section className="panel rounded-lg border p-5"><h2 className="font-display text-xl font-bold">Correlation heatmap</h2><div className="mt-6 flex justify-center"><Heatmap matrix={data.correlations} /></div></section></div>
  </div>;
}
