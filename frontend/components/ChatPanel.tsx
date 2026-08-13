import MessageList from "@/components/MessageList";
import MessageComposer from "./MessageComposer";

export default function ChatPanel() {
  return (
    <section className="flex flex-1 flex-col">
      <header className="flex items-center justify-between border-b border-slate-300 bg-white px-5 py-4">
        <div>
          <h2 className="font-semibold">Kofi Doe</h2>
          <p className="text-sm text-slate-500">+233 55 123 4567</p>
        </div>

        <button className="rounded-full bg-green-50 px-3 py-1.5 text-sm font-medium text-green-700 ring-1 ring-green-200">
          AI ON
        </button>
      </header>

      <MessageList />

      <MessageComposer />
    </section>
  );
}
