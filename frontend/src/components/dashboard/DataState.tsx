import { AlertCircle, Loader2 } from "lucide-react";

export function LoadingPanel({ label = "Loading decision intelligence" }) {
  return <div className="panel flex min-h-44 items-center justify-center rounded-lg border p-8 text-muted-foreground"><Loader2 className="mr-3 h-5 w-5 animate-spin text-primary" />{label}</div>;
}

export function ErrorPanel({ message }) {
  return <div className="rounded-lg border border-destructive/30 bg-destructive/10 p-5 text-destructive"><div className="flex items-center gap-2 font-semibold"><AlertCircle className="h-5 w-5" />Request failed</div><p className="mt-2 text-sm">{message}</p></div>;
}
