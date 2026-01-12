export type ChatMessage = {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
};

function Bubble({ m }: { m: ChatMessage }) {
  const isUser = m.role === 'user';
  const isSystem = m.role === 'system';

  const base =
    'max-w-[75ch] rounded-3xl px-5 py-4 shadow-[0_8px_0_rgba(0,0,0,0.08)]';

  if (isSystem) {
    return (
      <div className="flex justify-center">
        <div
          className={`${base} border-2 border-[var(--atomic-mustard)] bg-white/70 text-xs text-zinc-800`}
        >
          {m.content}
        </div>
      </div>
    );
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`${base} ${
          isUser
            ? 'bg-[var(--atomic-tangerine)] text-white'
            : 'bg-white/90 text-zinc-900'
        }`}
      >
        <div className="mb-2 text-[10px] uppercase tracking-[0.25em] opacity-80">
          {m.role}
        </div>
        <div className="whitespace-pre-wrap leading-relaxed">{m.content}</div>
      </div>
    </div>
  );
}

export default function ChatWindow({
  messages,
  draft,
  onDraftChange,
  onSend,
}: {
  messages: ChatMessage[];
  draft: string;
  onDraftChange: (next: string) => void;
  onSend: () => void;
}) {
  return (
    <section className="flex h-[calc(100vh-160px)] flex-col rounded-[32px] border-4 border-zinc-900/10 bg-white/30 p-5 shadow-[0_16px_0_rgba(0,0,0,0.06)] backdrop-blur">
      <div className="flex items-center justify-between">
        <h2 className="font-display text-xl tracking-wide text-[var(--atomic-teal)]">
          Chat Window
        </h2>
        <div className="text-xs uppercase tracking-[0.25em] text-zinc-700">
          live
        </div>
      </div>

      <div className="mt-4 flex-1 space-y-4 overflow-auto rounded-2xl bg-white/40 p-4">
        {messages.map((m) => (
          <Bubble key={m.id} m={m} />
        ))}
      </div>

      <form
        className="mt-4 flex gap-3"
        onSubmit={(e) => {
          e.preventDefault();
          onSend();
        }}
      >
        <input
          className="flex-1 rounded-2xl border-2 border-zinc-900/20 bg-white/80 px-4 py-3 text-sm outline-none focus:border-[var(--atomic-teal)]"
          placeholder="Tell Kit what to do…"
          value={draft}
          onChange={(e) => onDraftChange(e.target.value)}
        />
        <button type="submit" className="kit-button">
          Zap It
        </button>
      </form>
    </section>
  );
}
