import MessageList from "@/components/MessageList";
import MessageComposer from "./MessageComposer";
import { getMessages } from "@/lib/api";
import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import type { Message } from "@/types/message";

type ChatPanelProps = {
  conversationId: string | null;
};

export default function ChatPanel({ conversationId }: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([]);

  // Fetch existing messages by conversation Id
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

  // Listen for new messages
  useEffect(() => {
    if (!conversationId) {
      return;
    }

    const channel = supabase
      .channel(`conversation-${conversationId}`)
      .on(
        "postgres_changes",
        {
          event: "INSERT",
          schema: "public",
          table: "messages",
          filter: `conversation_id=eq.${conversationId}`,
        },
        (payload) => {
          const newMessage = payload.new as Message;

          setMessages((currentMessages) => {
            if (
              currentMessages.some((message) => message.id === newMessage.id)
            ) {
              return currentMessages;
            }

            return [...currentMessages, newMessage];
          });
        },
      )
      .subscribe((status) => {
        console.log("Realtime status:", status);
      });

    return () => {
      supabase.removeChannel(channel);
    };
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

      {conversationId ? (
        <MessageList messages={messages} />
      ) : (
        <div className="flex flex-1 items-center justify-center">
          <p className="text-sm bg-blue-50 text-blue-600 p-1 rounded-b-md">
            Select a conversation to view messages
          </p>
        </div>
      )}

      <MessageComposer conversationId={conversationId} />
    </section>
  );
}
