import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "AI Workflow Assessment",
  description: "Share your workflow challenge and receive a focused automation assessment.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
