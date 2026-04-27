import { Bar, BarChart, CartesianGrid, Cell, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const palette = ["hsl(var(--primary))", "hsl(var(--accent))", "hsl(var(--info))", "hsl(var(--success))", "hsl(var(--warning))"];

export function SimpleBarChart({ data, x = "name", y = "value", height = 260 }) {
  return <div className="h-full min-h-64"><ResponsiveContainer width="100%" height={height}><BarChart data={data}><CartesianGrid stroke="hsl(var(--border))" strokeDasharray="4 4" /><XAxis dataKey={x} tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }} /><YAxis tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }} /><Tooltip contentStyle={{ background: "hsl(var(--popover))", border: "1px solid hsl(var(--border))", borderRadius: 10 }} /><Bar dataKey={y} radius={[8, 8, 0, 0]} fill="hsl(var(--primary))" /></BarChart></ResponsiveContainer></div>;
}

export function ClassPieChart({ data }) {
  return <ResponsiveContainer width="100%" height={260}><PieChart><Pie data={data} dataKey="value" nameKey="name" innerRadius={62} outerRadius={92} paddingAngle={4}>{data.map((_, i) => <Cell key={i} fill={palette[i % palette.length]} />)}</Pie><Tooltip contentStyle={{ background: "hsl(var(--popover))", border: "1px solid hsl(var(--border))", borderRadius: 10 }} /></PieChart></ResponsiveContainer>;
}

export function RocCurve({ data }) {
  return <ResponsiveContainer width="100%" height={280}><LineChart data={data}><CartesianGrid stroke="hsl(var(--border))" strokeDasharray="4 4" /><XAxis dataKey="fpr" tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }} /><YAxis tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }} /><Tooltip contentStyle={{ background: "hsl(var(--popover))", border: "1px solid hsl(var(--border))", borderRadius: 10 }} /><Line type="monotone" dataKey="tpr" stroke="hsl(var(--accent))" strokeWidth={3} dot={{ fill: "hsl(var(--accent))" }} /></LineChart></ResponsiveContainer>;
}

export function Heatmap({ matrix }) {
  return <div className="grid max-w-sm grid-cols-4 gap-1">{matrix.flatMap((row, r) => row.map((value, c) => <div key={`${r}-${c}`} className="flex aspect-square items-center justify-center rounded-sm text-xs font-bold" style={{ backgroundColor: `hsl(var(--primary) / ${Math.max(.12, Math.abs(value))})`, color: "hsl(var(--foreground))" }}>{value.toFixed(2)}</div>))}</div>;
}

export function ConfusionMatrix({ matrix }) {
  return <div className="grid max-w-xs grid-cols-3 gap-2">{matrix.flatMap((row, r) => row.map((value, c) => <div key={`${r}-${c}`} className={`rounded-md border p-4 text-center font-display text-xl font-bold ${r === c ? "bg-success/15 text-success" : "bg-warning/12 text-warning"}`}>{value}</div>))}</div>;
}
