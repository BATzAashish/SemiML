export function MetricCard({ label, value, detail, tone = "primary", icon: Icon }) {
  const toneClass = tone === "accent" ? "bg-accent/12 text-accent" : tone === "success" ? "bg-success/12 text-success" : "bg-primary/12 text-primary";
  return <section className="panel rounded-lg border p-5 transition-transform duration-200 hover:-translate-y-1">
    <div className="flex items-start justify-between gap-4">
      <div><p className="text-sm font-medium text-muted-foreground">{label}</p><p className="mt-2 font-display text-3xl font-bold">{value}</p></div>
      {Icon && <div className={`rounded-md p-3 ${toneClass}`}><Icon className="h-5 w-5" /></div>}
    </div>
    {detail && <p className="mt-4 text-sm text-muted-foreground">{detail}</p>}
  </section>;
}
