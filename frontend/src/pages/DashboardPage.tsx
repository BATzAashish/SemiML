import { Link } from "react-router-dom";
import { Award, Database, FlaskConical, UploadCloud } from "lucide-react";
import { MetricCard } from "@/components/dashboard/MetricCard";
import { SectionHeader } from "@/components/dashboard/SectionHeader";
import { mockExperiments } from "@/services/api.js";

export default function DashboardPage() {
  return <div className="animate-enter-up space-y-8">
    <section className="relative overflow-hidden rounded-lg border bg-card p-6 shadow-soft reasoning-grid md:p-8">
      <div className="absolute right-8 top-8 hidden h-28 w-28 rounded-full bg-primary/10 blur-2xl md:block" />
      <div className="relative max-w-3xl"><p className="text-sm font-bold uppercase tracking-wider text-primary">Hybrid Explainable ML Decision System</p><h1 className="mt-3 font-display text-4xl font-bold md:text-6xl">Reasoned ML pipelines, not black-box automation.</h1><p className="mt-4 text-lg text-muted-foreground">Design, evaluate, explain, and continuously improve machine learning workflows with traceable recommendations across rules, meta-learning, retrieval, and SHAP.</p><Link to="/upload" className="mt-6 inline-flex items-center gap-2 rounded-md bg-primary px-5 py-3 font-semibold text-primary-foreground shadow-glow transition hover:-translate-y-1 focus:outline-none focus:ring-2 focus:ring-ring"><UploadCloud className="h-5 w-5" />Upload Dataset</Link></div>
    </section>
    <div className="grid gap-4 md:grid-cols-3"><MetricCard label="Total experiments" value="128" detail="14 active comparison threads" icon={FlaskConical} /><MetricCard label="Best model" value="XGB + SHAP" detail="Selected for accuracy and interpretability" tone="accent" icon={Award} /><MetricCard label="Avg accuracy" value="91.4%" detail="Across validated experiments" tone="success" icon={Database} /></div>
    <section className="panel rounded-lg border p-5"><SectionHeader eyebrow="Recent work" title="Recent experiments" description="Latest decision runs ready for review and comparison." /><div className="overflow-x-auto"><table className="w-full text-sm"><thead className="text-left text-muted-foreground"><tr><th className="py-3">ID</th><th>Dataset</th><th>Model</th><th>Performance</th><th>Date</th></tr></thead><tbody>{mockExperiments.map((e) => <tr key={e.id} className="border-t"><td className="py-3 font-semibold text-primary">{e.id}</td><td>{e.dataset}</td><td>{e.model}</td><td>{(e.performance * 100).toFixed(1)}%</td><td>{e.date}</td></tr>)}</tbody></table></div></section>
  </div>;
}
