import Chat from "@/components/Chat";

export default function Home() {
  return (
    <div className="flex flex-col h-screen">
      <header className="border-b border-[var(--border)] px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold">AI Persona Chat</h1>
          <p className="text-sm text-zinc-500">
            Ask me about my background, skills, projects, or schedule an interview
          </p>
        </div>
        <a
          href={process.env.NEXT_PUBLIC_CALCOM_LINK || "#"}
          target="_blank"
          rel="noopener noreferrer"
          className="rounded-lg bg-[var(--primary)] px-4 py-2 text-sm font-medium text-white hover:bg-[var(--primary-hover)] transition-colors"
        >
          Book Interview
        </a>
      </header>
      <Chat />
    </div>
  );
}
