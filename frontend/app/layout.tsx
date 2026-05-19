import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Mustang Blueprints",
  description: "See exactly where you stand in your Cal Poly SLO degree. Upload your unofficial transcript to visualize completed courses, prerequisites, concentrations, and GE requirements across all 57 majors.",
  openGraph: {
    title: "Mustang Blueprints — Cal Poly Course Planner",
    description: "Upload your transcript and instantly see your 4-year semester flowchart. Tracks prerequisites, concentrations, and GE requirements for all 57 Cal Poly SLO majors.",
    images: [{ url: "/mb-logo.png", width: 512, height: 512, alt: "Mustang Blueprints" }],
    type: "website",
  },
  twitter: {
    card: "summary",
    title: "Mustang Blueprints",
    description: "Cal Poly SLO 4-year flowchart planner — see your progress instantly.",
    images: ["/mb-logo.png"],
  },
  icons: {
    icon: [{ url: "/mb-logo.png", type: "image/png" }],
    apple: "/mb-logo.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
