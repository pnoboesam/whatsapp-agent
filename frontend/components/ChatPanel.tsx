import MessageList from "@/components/MessageList";
import MessageComposer from "./MessageComposer";
import { getMessages } from "@/lib/api";
import { useEffect, useState } from "react";
import type { Message } from "@/types/message";

type ChatPanelProps = {
  conversationId: string | null;
};

export default function ChatPanel({ conversationId }: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    if (!conversationId) {
      setMessages([]);
      return;
    }

    async function loadMessages(conversationId: string) {
      const data = await getMessages(conversationId);
      setMessages(data);
    }

    loadMessages(conversationId);
  }, [conversationId]);

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

      <MessageList messages={messages} />

      {/* {conversationId ? (
        <p>Selected conversation: {conversationId}</p>
      ) : (
        <p>Select a conversation</p>
      )} */}

      <MessageComposer />
    </section>
  );
}
