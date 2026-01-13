type SidebarItem = {
  label: string;
  sublabel: string;
};

const items: SidebarItem[] = [
  { label: 'Dashboard', sublabel: 'Control Room' },
  { label: 'Modules', sublabel: 'Tools & tricks' },
  { label: 'Memory', sublabel: 'Long-term likes' },
  { label: 'Settings', sublabel: 'Dials & knobs' },
];

export default function Sidebar() {
  return (
    <aside className="relative overflow-hidden border-r-4 border-[var(--atomic-teal)] bg-[linear-gradient(160deg,var(--atomic-teal),var(--atomic-pink))] text-zinc-900">
      {/* Atomic starburst backdrop */}
      <div className="pointer-events-none absolute -top-24 -left-24 h-64 w-64 rounded-full bg-[var(--atomic-mustard)] opacity-35 blur-sm" />
      <div className="pointer-events-none absolute top-24 -right-32 h-80 w-80 rounded-full bg-[var(--atomic-tangerine)] opacity-30 blur-sm" />
      <div className="pointer-events-none absolute -bottom-40 left-10 h-80 w-80 rounded-full bg-[var(--atomic-lime)] opacity-20 blur-sm" />

      <div className="relative flex h-full flex-col p-6">
        <div className="mb-8">
          <div className="inline-flex items-center gap-3">
            <div className="kit-boomerang" aria-hidden="true" />
            <div>
              <div className="font-display text-3xl tracking-widest">KIT</div>
              <div className="text-xs uppercase tracking-[0.25em] opacity-90">
                Atomic Assistant
              </div>
            </div>
          </div>
        </div>

        <nav className="space-y-3">
          {items.map((it) => (
            <button
              key={it.label}
              className="kit-sidebar-item"
              type="button"
            >
              <div className="text-sm font-semibold tracking-wide">{it.label}</div>
              <div className="text-xs opacity-80">{it.sublabel}</div>
            </button>
          ))}
        </nav>

        <div className="mt-auto pt-8">
          <div className="rounded-2xl border border-zinc-900/10 bg-white/25 p-4 backdrop-blur">
            <div className="font-display text-lg tracking-wide">Ralph Loop</div>
            <p className="mt-1 text-xs leading-relaxed opacity-90">
              Observe → Execute → Verify → Self-Correct. Three tries max, then we
              regroup.
            </p>
          </div>
        </div>
      </div>
    </aside>
  );
}
