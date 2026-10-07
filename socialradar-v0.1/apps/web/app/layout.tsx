import "./globals.css";

export const metadata = {
  title: "SocialRadar",
  description: "Descubrimiento de perfiles y hilos"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
