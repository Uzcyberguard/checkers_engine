import type { Metadata, Viewport } from "next";
import { Inter, JetBrains_Mono, Playfair_Display } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const playfair = Playfair_Display({
  variable: "--font-playfair",
  subsets: ["latin"],
  weight: ["500", "600", "700"],
  display: "swap",
});

const mono = JetBrains_Mono({
  variable: "--font-mono-jb",
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Checkers Royale — Russian Draughts",
  description:
    "Play Russian draughts against a real alpha-beta search engine: flying kings, forced captures, and a live evaluation readout.",
  applicationName: "Checkers Royale",
  authors: [
    { name: "Hasan Normamatov", url: "https://github.com/Uzcyberguard" },
    { name: "Asadbek Abduxalilov" },
  ],
  creator: "Asadbek Abduxalilov",
  openGraph: {
    title: "Checkers Royale — Russian Draughts",
    description:
      "Play Russian draughts against a real alpha-beta search engine: flying kings, forced captures, and a live evaluation readout.",
    type: "website",
  },
};

export const viewport: Viewport = {
  themeColor: "#08080b",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body
        className={`${inter.variable} ${playfair.variable} ${mono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
