type EbayListing = {
  title?: string;
  price?: number;
  condition?: string;
  url?: string;
  source?: string;
};

type EbayWatcherResult = {
  status?: string;
  attempt?: number;
  verified_results?: EbayListing[];
  rejected?: Array<{ listing?: EbayListing; reason?: string }>;
  trace?: Array<{ step?: string; note?: string }>;
};

function isObject(v: unknown): v is Record<string, unknown> {
  return typeof v === 'object' && v !== null;
}

function isEbayWatcherResult(v: unknown): v is EbayWatcherResult {
  if (!isObject(v)) return false;
  // It's enough to detect the one field we care about for prettier output.
  return 'verified_results' in v || 'rejected' in v || 'trace' in v;
}

function MoneyBadge({ value }: { value: number }) {
  return (
    <span className="rounded-full border-2 border-zinc-900/15 bg-white/70 px-3 py-1 text-xs font-semibold text-zinc-900">
      ${value.toFixed(2)}
    </span>
  );
}

function Chip({ children }: { children: React.ReactNode }) {
  return (
    <span className="rounded-full border-2 border-zinc-900/10 bg-[var(--atomic-beige)] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-zinc-800">
      {children}
    </span>
  );
}

function ListingCard({ listing }: { listing: EbayListing }) {
  return (
    <div className="rounded-3xl border-2 border-zinc-900/10 bg-white/80 p-4 shadow-[0_10px_0_rgba(0,0,0,0.06)]">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="font-semibold leading-snug text-zinc-900">
            {listing.title ?? 'Untitled listing'}
          </div>
          <div className="mt-2 flex flex-wrap items-center gap-2">
            {typeof listing.price === 'number' ? (
              <MoneyBadge value={listing.price} />
            ) : null}
            {listing.condition ? <Chip>{listing.condition}</Chip> : null}
            {listing.source ? <Chip>{listing.source}</Chip> : null}
          </div>
        </div>

        {listing.url ? (
          <a
            className="kit-button whitespace-nowrap"
            href={listing.url}
            target="_blank"
            rel="noreferrer"
          >
            View
          </a>
        ) : null}
      </div>
    </div>
  );
}

export default function ToolResult({ result }: { result: unknown }) {
  if (isEbayWatcherResult(result)) {
    const verified = Array.isArray(result.verified_results)
      ? result.verified_results
      : [];

    return (
      <div className="space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="font-display text-lg tracking-wide text-[var(--atomic-teal)]">
            Verified Results
          </div>
          <div className="text-xs uppercase tracking-[0.25em] text-zinc-700">
            {verified.length} hit{verified.length === 1 ? '' : 's'}
          </div>
        </div>

        {verified.length > 0 ? (
          <div className="grid gap-3 md:grid-cols-2">
            {verified.map((l, idx) => (
              <ListingCard key={`${l.title ?? 'listing'}-${idx}`} listing={l} />
            ))}
          </div>
        ) : (
          <div className="rounded-3xl border-2 border-zinc-900/10 bg-white/60 p-4 text-sm text-zinc-800">
            Nothing verified yet. Kit may need different preferences, a wider
            query, or a better data source.
          </div>
        )}

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
