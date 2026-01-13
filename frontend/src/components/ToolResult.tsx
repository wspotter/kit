function isObject(v: unknown): v is Record<string, unknown> {
  return typeof v === 'object' && v !== null;
}

type FsTriageResult = {
  status?: string;
  root?: string;
  scanned_files?: number;
  skipped?: string[];
  largest?: Array<{ path?: string; size_mb?: number; size_bytes?: number }>;
  oldest?: Array<{ path?: string; age_days?: number; mtime?: number }>;
  trace?: Array<{ step?: string; note?: string }>;
};

type SystemHealthResult = {
  status?: string;
  data?: {
    cpu_count?: number | null;
    loadavg?: [number, number, number] | null;
    uptime_seconds?: number | null;
    memory?: {
      mem_total_bytes?: number | null;
      mem_available_bytes?: number | null;
      swap_total_bytes?: number | null;
      swap_free_bytes?: number | null;
    };
    disk?: {
      path?: string;
      total_bytes?: number;
      used_bytes?: number;
      free_bytes?: number;
      used_pct?: number | null;
    };
    timestamp?: number;
  };
  trace?: Array<{ step?: string; note?: string }>;
};

function isFsTriageResult(v: unknown): v is FsTriageResult {
  if (!isObject(v)) return false;
  return 'largest' in v || 'oldest' in v;
}

function isSystemHealthResult(v: unknown): v is SystemHealthResult {
  if (!isObject(v)) return false;
  return 'data' in v && isObject((v as any).data);
}

function bytesToGiB(bytes: number | null | undefined) {
  if (typeof bytes !== 'number') return '—';
  return `${(bytes / 1024 ** 3).toFixed(2)} GiB`;
}

function BigStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-3xl border-2 border-zinc-900/10 bg-white/70 p-4">
      <div className="text-[10px] font-semibold uppercase tracking-[0.25em] text-zinc-700">
        {label}
      </div>
      <div className="mt-2 font-display text-2xl tracking-wide text-[var(--atomic-teal)]">
        {value}
      </div>
    </div>
  );
}

function SectionHeader({ title, right }: { title: string; right?: string }) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-2">
      <div className="inline-flex items-center gap-3">
        <div className="h-3 w-3 rounded-full bg-[var(--atomic-teal)] shadow-[0_6px_0_rgba(0,0,0,0.12)]" />
        <div className="font-display text-lg tracking-wide text-[var(--atomic-teal)]">
          {title}
        </div>
        <div className="h-3 w-3 rounded-full bg-[var(--atomic-pink)] shadow-[0_6px_0_rgba(0,0,0,0.12)]" />
      </div>
      {right ? <div className="kit-chip kit-chip--mustard">{right}</div> : null}
    </div>
  );
}

function Panel({ title, tone, children }: { title: string; tone: 'mustard' | 'tangerine' | 'lime' | 'pink'; children: React.ReactNode }) {
  const toneClass =
    tone === 'mustard'
      ? 'border-[var(--atomic-mustard)]'
      : tone === 'tangerine'
        ? 'border-[var(--atomic-tangerine)]'
        : tone === 'lime'
          ? 'border-[var(--atomic-lime)]'
          : 'border-[var(--atomic-pink)]';

  return (
    <div className={`rounded-3xl border-2 ${toneClass} bg-white/70 p-4`}>
      <div className="text-[10px] font-semibold uppercase tracking-[0.25em] text-zinc-700">
        {title}
      </div>
      <div className="mt-3">{children}</div>
    </div>
  );
}

export default function ToolResult({ result }: { result: unknown }) {
  if (isSystemHealthResult(result)) {
    const d = result.data ?? {};
    const mem = d.memory ?? {};
    const disk = d.disk ?? {};

    const load = Array.isArray(d.loadavg)
      ? d.loadavg.map((x) => x.toFixed(2)).join(' / ')
      : '—';

    const uptime =
      typeof d.uptime_seconds === 'number'
        ? `${(d.uptime_seconds / 3600).toFixed(2)} hrs`
        : '—';

    return (
      <div className="space-y-4">
        <SectionHeader title="System Health" right={result.status ?? 'unknown'} />

        <div className="grid gap-3 md:grid-cols-3">
          <BigStat label="Load avg" value={load} />
          <BigStat label="Uptime" value={uptime} />
          <BigStat
            label="Disk used"
            value={
              typeof disk.used_pct === 'number' ? `${disk.used_pct}%` : '—'
            }
          />
        </div>

        <div className="grid gap-3 md:grid-cols-2">
          <Panel title="Memory" tone="lime">
            <div className="space-y-2 text-sm">
              <div className="flex justify-between gap-4">
                <span className="text-zinc-700">Total</span>
                <span className="font-semibold">{bytesToGiB(mem.mem_total_bytes)}</span>
              </div>
              <div className="flex justify-between gap-4">
                <span className="text-zinc-700">Available</span>
                <span className="font-semibold">
                  {bytesToGiB(mem.mem_available_bytes)}
                </span>
              </div>
              <div className="flex justify-between gap-4">
                <span className="text-zinc-700">Swap</span>
                <span className="font-semibold">
                  {bytesToGiB(mem.swap_free_bytes)} / {bytesToGiB(mem.swap_total_bytes)}
                </span>
              </div>
            </div>
          </Panel>

          <Panel title="Disk" tone="tangerine">
            <div className="text-xs text-zinc-700">{disk.path ?? '—'}</div>
            <div className="mt-3 space-y-2 text-sm">
              <div className="flex justify-between gap-4">
                <span className="text-zinc-700">Used</span>
                <span className="font-semibold">{bytesToGiB(disk.used_bytes)}</span>
              </div>
              <div className="flex justify-between gap-4">
                <span className="text-zinc-700">Free</span>
                <span className="font-semibold">{bytesToGiB(disk.free_bytes)}</span>
              </div>
              <div className="flex justify-between gap-4">
                <span className="text-zinc-700">Total</span>
                <span className="font-semibold">{bytesToGiB(disk.total_bytes)}</span>
              </div>
            </div>
          </Panel>
        </div>

        <details className="rounded-3xl border-2 border-zinc-900/10 bg-white/50 p-4">
          <summary className="cursor-pointer text-xs font-semibold uppercase tracking-[0.25em] text-zinc-700">
            Raw payload
          </summary>
          <pre className="mt-3 overflow-auto rounded-2xl bg-white/60 p-3 text-xs">
            {JSON.stringify(result, null, 2)}
          </pre>
        </details>
      </div>
    );
  }

  if (isFsTriageResult(result)) {
    const largest = Array.isArray(result.largest) ? result.largest : [];
    const oldest = Array.isArray(result.oldest) ? result.oldest : [];

    return (
      <div className="space-y-4">
        <SectionHeader title="Filesystem Triage" right={`${result.scanned_files ?? 0} scanned`} />

        <div className="grid gap-3 md:grid-cols-2">
          <Panel title="Largest files" tone="mustard">
            <div className="space-y-2 text-sm">
              {largest.slice(0, 10).map((f, idx) => (
                <div key={`${f.path ?? 'file'}-${idx}`} className="flex items-start justify-between gap-4">
                  <div className="min-w-0 flex-1 truncate text-zinc-800">{f.path ?? '—'}</div>
                  <div className="shrink-0 font-semibold text-[var(--atomic-teal)]">{typeof f.size_mb === 'number' ? `${f.size_mb} MB` : '—'}</div>
                </div>
              ))}
              {largest.length === 0 ? <div className="text-zinc-700">No data.</div> : null}
            </div>
          </Panel>

          <Panel title="Oldest files" tone="pink">
            <div className="space-y-2 text-sm">
              {oldest.slice(0, 10).map((f, idx) => (
                <div key={`${f.path ?? 'file'}-${idx}`} className="flex items-start justify-between gap-4">
                  <div className="min-w-0 flex-1 truncate text-zinc-800">{f.path ?? '—'}</div>
                  <div className="shrink-0 font-semibold text-[var(--atomic-tangerine)]">{typeof f.age_days === 'number' ? `${f.age_days} d` : '—'}</div>
                </div>
              ))}
              {oldest.length === 0 ? <div className="text-zinc-700">No data.</div> : null}
            </div>
          </Panel>
        </div>

        <details className="rounded-3xl border-2 border-zinc-900/10 bg-white/50 p-4">
          <summary className="cursor-pointer text-xs font-semibold uppercase tracking-[0.25em] text-zinc-700">
            Raw payload
          </summary>
          <pre className="mt-3 overflow-auto rounded-2xl bg-white/60 p-3 text-xs">
            {JSON.stringify(result, null, 2)}
          </pre>
        </details>
      </div>
    );
  }

  return (
    <pre className="overflow-auto whitespace-pre-wrap rounded-2xl border-2 border-zinc-900/10 bg-white/60 p-4 text-xs">
      {JSON.stringify(result, null, 2)}
    </pre>
  );
}
