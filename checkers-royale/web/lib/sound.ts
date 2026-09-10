export type SoundName =
  | "move"
  | "capture"
  | "select"
  | "illegal"
  | "king"
  | "win"
  | "lose"
  | "draw"
  | "ui";

const FILES: Record<SoundName, string> = {
  move: "/sounds/move.wav",
  capture: "/sounds/capture.wav",
  select: "/sounds/select.wav",
  illegal: "/sounds/illegal.wav",
  king: "/sounds/king.wav",
  win: "/sounds/win.wav",
  lose: "/sounds/lose.wav",
  draw: "/sounds/draw.wav",
  ui: "/sounds/ui.wav",
};

const GAIN: Record<SoundName, number> = {
  move: 0.55,
  capture: 0.7,
  select: 0.3,
  illegal: 0.35,
  king: 0.5,
  win: 0.55,
  lose: 0.5,
  draw: 0.45,
  ui: 0.25,
};

/**
 * A tiny Web Audio player. Buffers are decoded once and reused, so rapid
 * captures during a multi-jump never stall on a fetch, and overlapping
 * playback does not cut itself off the way a shared <audio> element does.
 */
class SoundBoard {
  private context: AudioContext | null = null;
  private buffers = new Map<SoundName, AudioBuffer>();
  private pending = new Map<SoundName, Promise<AudioBuffer | null>>();
  enabled = true;

  private ensureContext(): AudioContext | null {
    if (typeof window === "undefined") return null;
    if (!this.context) {
      const Ctor =
        window.AudioContext ??
        (window as unknown as { webkitAudioContext?: typeof AudioContext })
          .webkitAudioContext;
      if (!Ctor) return null;
      this.context = new Ctor();
    }
    if (this.context.state === "suspended") {
      void this.context.resume();
    }
    return this.context;
  }

  private load(name: SoundName): Promise<AudioBuffer | null> {
    const cached = this.pending.get(name);
    if (cached) return cached;

    const task = (async () => {
      const context = this.ensureContext();
      if (!context) return null;
      try {
        const response = await fetch(FILES[name]);
        if (!response.ok) return null;
        const bytes = await response.arrayBuffer();
        const buffer = await context.decodeAudioData(bytes);
        this.buffers.set(name, buffer);
        return buffer;
      } catch {
        return null;
      }
    })();

    this.pending.set(name, task);
    return task;
  }

  /** Warm the cache on first interaction so the first move is not silent. */
  preload() {
    if (typeof window === "undefined") return;
    (Object.keys(FILES) as SoundName[]).forEach((name) => void this.load(name));
  }

  play(name: SoundName, rate = 1) {
    if (!this.enabled) return;
    const context = this.ensureContext();
    if (!context) return;

    const start = (buffer: AudioBuffer) => {
      const source = context.createBufferSource();
      source.buffer = buffer;
      source.playbackRate.value = rate;
      const gain = context.createGain();
      gain.gain.value = GAIN[name];
      source.connect(gain).connect(context.destination);
      source.start();
    };

    const ready = this.buffers.get(name);
    if (ready) {
      start(ready);
      return;
    }
    void this.load(name).then((buffer) => {
      if (buffer && this.enabled) start(buffer);
    });
  }
}

export const sounds = new SoundBoard();
