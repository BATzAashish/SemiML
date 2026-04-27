export function SectionHeader({ eyebrow, title, description, action }) {
  return <div className="mb-6 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
    <div><p className="text-sm font-bold uppercase tracking-wider text-primary">{eyebrow}</p><h1 className="mt-2 font-display text-3xl font-bold md:text-4xl">{title}</h1>{description && <p className="mt-2 max-w-3xl text-muted-foreground">{description}</p>}</div>
    {action}
  </div>;
}
