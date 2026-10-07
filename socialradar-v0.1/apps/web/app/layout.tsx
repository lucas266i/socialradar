import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SocialRadar",
  description: "Descubrimiento de perfiles y hilos públicos",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
