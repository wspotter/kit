import { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatWindow, { type ChatMessage } from './components/ChatWindow';
import Mascot, { type MascotState } from './components/Mascot';

export default function App() {
  const [mascotState, setMascotState] = useState<MascotState>('idle');
  const [draft, setDraft] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>(() => [
    {
      id: 'm1',
      role: 'assistant',
      content:
        "Welcome home, doll. I'm Kit — your Atomic Era assistant. Ask me anything and I'll get to work.",
    },
    {
      id: 'm2',
      role: 'system',
      content:
        'Try: “health” or “fs /var/log” or “inbox”.',
    },
  ]);

  async function handleSend() {
    const text = draft.trim();
    if (!text) return;

    setDraft('');
    const id = crypto.randomUUID();
    setMessages((m) => [...m, { id, role: 'user', content: text }]);

  // Very small command router for now.
  // inbox -> run inbox tool
  // health -> system health summary
  // fs <path> -> filesystem triage
    const [cmd, ...rest] = text.split(' ');
    const normalized = cmd.toLowerCase();
    const toolId =
      normalized === 'inbox' ? 'inbox' : normalized === 'health' ? 'health' : normalized === 'fs' ? 'fs' : null;
    const argText = rest.join(' ').trim();

    if (!toolId) {
      setMessages((m) => [
        ...m,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content:
            "Hot dog! I don't recognize that command yet. Try `health`, `fs <path>`, or `inbox`.",
        },
      ]);
      return;
    }

    setMascotState('thinking');
    try {
      const resp = await fetch(`/modules/run/${toolId}`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(
          toolId === 'fs'
            ? { path: argText || '.' }
            : toolId === 'inbox'
              ? { dry_run: true }
              : {},
        ),
      });

      const json = await resp.json();
      if (!resp.ok) {
        throw new Error(json?.detail || 'Tool call failed');
      }

      setMascotState('success');
      setTimeout(() => setMascotState('idle'), 700);

      setMessages((m) => [
        ...m,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          kind: 'tool_result',
          toolId,
          result: json.result,
        },
      ]);
    } catch (err) {
      setMascotState('idle');
      setMessages((m) => [
        ...m,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: `Hold the phone!\n${String(err)}`,
        },
      ]);
    }
  }

  return (
    <div className="min-h-screen bg-[var(--atomic-beige)] text-zinc-900">
      <div className="grid min-h-screen grid-cols-[320px_1fr]">
        <Sidebar />

        <main className="relative flex flex-col">
          {/* Top chrome bar (mockup-style UI line) */}
          <div className="flex items-center justify-between border-b-2 border-zinc-900/10 bg-white/40 px-6 py-2 text-[11px] uppercase tracking-[0.25em] text-zinc-700 backdrop-blur">
            <div className="flex items-center gap-2">
              <span className="kit-status-dot bg-[var(--atomic-teal)]" aria-hidden="true" />
              <span>Control Room</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="kit-status-dot bg-[var(--atomic-mustard)]" aria-hidden="true" />
              <span>Ralph Loop</span>
            </div>
          </div>

          <header className="flex flex-wrap items-center justify-between gap-4 border-b-4 border-[var(--atomic-teal)] bg-white/60 px-6 py-4 backdrop-blur">
            <div>
              <h1 className="font-display text-3xl tracking-wide text-[var(--atomic-teal)]">
                Kit
              </h1>
              <p className="text-sm text-zinc-700">
                Atomic assistant — tools you can trust.
              </p>
            </div>

            <div className="flex items-center gap-4">
              <div className="hidden md:flex gap-2">
                <button className="kit-button" onClick={() => setMascotState('idle')}>
                  Idle
                </button>
                <button className="kit-button" onClick={() => setMascotState('thinking')}>
                  Thinking
                </button>
                <button className="kit-button" onClick={() => setMascotState('success')}>
                  Success
                </button>
              </div>

              <Mascot state={mascotState} />
            </div>
          </header>

          <div className="flex-1 p-6">
            <div className="mx-auto max-w-[1100px]">
              <ChatWindow
                messages={messages}
                draft={draft}
                onDraftChange={setDraft}
                onSend={handleSend}
              />
            </div>
          </div>

          <footer className="border-t-2 border-zinc-900/10 bg-white/40 px-6 py-3 text-xs text-zinc-700">
            Kit is purring. Ralph Loop standing by.
          </footer>
        </main>
      </div>
    </div>
  );
}
