import { useMemo, useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatWindow, { type ChatMessage } from './components/ChatWindow';
import Mascot, { type MascotState } from './components/Mascot';

export default function App() {
  const [mascotState, setMascotState] = useState<MascotState>('idle');

  const messages = useMemo<ChatMessage[]>(
    () => [
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
          'Tip: Flip the mascot state buttons to preview idle/thinking/success animations.',
      },
    ],
    []
  );

  return (
    <div className="min-h-screen bg-[var(--atomic-beige)] text-zinc-900">
      <div className="grid min-h-screen grid-cols-[320px_1fr]">
        <Sidebar />

        <main className="relative flex flex-col">
          <header className="flex items-center justify-between border-b-4 border-[var(--atomic-teal)] bg-white/60 px-6 py-4 backdrop-blur">
            <div>
              <h1 className="font-display text-3xl tracking-wide text-[var(--atomic-teal)]">
                Kit Control Room
              </h1>
              <p className="text-sm text-zinc-700">
                Boomerangs, starbursts, and good clean compute.
              </p>
            </div>

            <div className="flex items-center gap-4">
              <div className="hidden md:flex gap-2">
                <button
                  className="kit-button"
                  onClick={() => setMascotState('idle')}
                >
                  Idle
                </button>
                <button
                  className="kit-button"
                  onClick={() => setMascotState('thinking')}
                >
                  Thinking
                </button>
                <button
                  className="kit-button"
                  onClick={() => setMascotState('success')}
                >
                  Success
                </button>
              </div>

              <Mascot state={mascotState} />
            </div>
          </header>

          <div className="flex-1 p-6">
            <ChatWindow messages={messages} />
          </div>

          <footer className="border-t-2 border-zinc-900/10 bg-white/40 px-6 py-3 text-xs text-zinc-700">
            Kit is purring. Ralph Loop standing by.
          </footer>
        </main>
      </div>
    </div>
  );
}
