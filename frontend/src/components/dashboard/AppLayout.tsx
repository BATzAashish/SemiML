import { NavLink, Outlet } from "react-router-dom";
import { Activity, BarChart3, Bot, BrainCircuit, Database, FileUp, GitCompare, Home, ListTree, Moon, Network, Sun } from "lucide-react";
import { useEffect, useState } from "react";

const nav = [
  ["/", "Dashboard", Home], ["/upload", "Dataset Upload", FileUp], ["/analysis", "Data Analysis", BarChart3], ["/pipeline", "Pipeline", Network], ["/decision-trace", "Decision Trace", ListTree], ["/evaluation", "Evaluation", Activity], ["/explainability", "Explainability", BrainCircuit], ["/assistant", "AI Assistant", Bot], ["/experiments", "Experiments", GitCompare],
];

export function AppLayout() {
  const [dark, setDark] = useState(false);
  useEffect(() => { document.documentElement.classList.toggle("dark", dark); }, [dark]);
  return <div className="min-h-screen bg-app text-foreground">
    <aside className="fixed inset-y-0 left-0 z-30 hidden w-72 border-r border-sidebar-border bg-sidebar text-sidebar-foreground lg:block">
      <div className="flex h-full flex-col p-5">
        <div className="mb-8 flex items-center gap-3"><div className="rounded-lg bg-primary p-3 text-primary-foreground shadow-glow"><BrainCircuit className="h-6 w-6" /></div><div><p className="font-display text-lg font-bold">Hybrid XMLDS</p><p className="text-xs text-sidebar-foreground/70">Decision intelligence suite</p></div></div>
        <nav className="space-y-1">
          {nav.map(([to, label, Icon]) => <NavLink key={to} to={to} end={to === "/"} className={({ isActive }) => `flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium transition ${isActive ? "bg-sidebar-primary text-sidebar-primary-foreground shadow-glow" : "text-sidebar-foreground/78 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"}`}><Icon className="h-4 w-4" />{label}</NavLink>)}
        </nav>
        <div className="mt-auto rounded-lg border border-sidebar-border bg-sidebar-accent p-4"><p className="text-sm font-semibold">Reasoning engine</p><p className="mt-1 text-xs text-sidebar-foreground/70">Rules · Meta-learning · RAG · SHAP</p></div>
      </div>
    </aside>
    <div className="lg:pl-72">
      <header className="sticky top-0 z-20 border-b bg-background/80 px-4 py-3 backdrop-blur md:px-8">
        <div className="flex items-center justify-between gap-4"><div className="lg:hidden"><p className="font-display font-bold">Hybrid XMLDS</p></div><div className="hidden text-sm text-muted-foreground lg:block">Semi-autonomous explainable ML pipeline design</div><button onClick={() => setDark(!dark)} className="inline-flex items-center gap-2 rounded-md border bg-card px-3 py-2 text-sm font-semibold shadow-soft transition hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-ring">{dark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}<span className="hidden sm:inline">{dark ? "Light" : "Dark"}</span></button></div>
        <nav className="mt-3 flex gap-2 overflow-x-auto pb-1 lg:hidden">{nav.map(([to, label]) => <NavLink key={to} to={to} end={to === "/"} className={({ isActive }) => `shrink-0 rounded-md px-3 py-2 text-xs font-semibold ${isActive ? "bg-primary text-primary-foreground" : "bg-card text-muted-foreground"}`}>{label}</NavLink>)}</nav>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-8 md:px-8"><Outlet /></main>
    </div>
  </div>;
}
