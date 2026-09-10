import type { NextConfig } from "next";

/**
 * On Vercel each file in api/ becomes its own Python function and /api/ai is
 * served straight from api/ai.py, so no rewrite is involved.
 *
 * Locally the same endpoints come from `python devserver.py`. Set
 * ENGINE_PROXY to point at it (it defaults to the usual port during
 * `next dev`), which also lets a local production build be tested against the
 * real engine.
 */
const proxyTarget =
  process.env.ENGINE_PROXY ??
  (process.env.NODE_ENV === "development" ? "http://127.0.0.1:5328" : "");

const nextConfig: NextConfig = {
  async rewrites() {
    if (!proxyTarget) return [];
    return [
      {
        source: "/api/:path*",
        destination: `${proxyTarget}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
