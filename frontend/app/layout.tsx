import type { Metadata } from "next";
import { Google_Sans } from "next/font/google";
import "./globals.css";

const font = Google_Sans({
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "WhatsApp AI Agent",
  description: "WhatsApp AI customer support dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={font.className}>{children}</body>
    </html>
  );
}
