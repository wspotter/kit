import { motion } from 'framer-motion';

export type MascotState = 'idle' | 'thinking' | 'success';

export default function Mascot({ state }: { state: MascotState }) {
  return (
    <div className="flex items-center gap-3">
      <div className="hidden sm:block text-right">
        <div className="text-[10px] uppercase tracking-[0.25em] text-zinc-700">
          Mascot
        </div>
        <div className="font-display text-sm text-[var(--atomic-teal)]">
          {state}
        </div>
      </div>

      <motion.div
        className="kit-mascot"
        initial={false}
        animate={state}
        variants={{
          idle: { scale: [1, 1.03, 1], y: [0, -1, 0] },
          thinking: {
            rotate: [0, -2, 2, -1, 0],
            scale: [1, 1.02, 1],
            transition: { repeat: Infinity, duration: 1.4 },
          },
          success: {
            x: [0, -2, 2, -2, 2, 0],
            scale: [1, 1.04, 1],
            transition: { duration: 0.35 },
          },
        }}
        transition={{ duration: 2.6, repeat: state === 'idle' ? Infinity : 0 }}
        role="img"
        aria-label="Kit mascot"
      >
        <img
          src="/src/assets/kit/kit-cat.svg"
          alt="Kit the Atomic Cat"
          className="h-14 w-14"
          draggable={false}
        />
      </motion.div>
    </div>
  );
}
