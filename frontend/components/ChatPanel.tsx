import MessageList from "@/components/MessageList";
import MessageComposer from "./MessageComposer";
import { getMessages, getContact } from "@/lib/api";
import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import type { Contact } from "@/types/contact";
import type { Message } from "@/types/message";

type ChatPanelProps = {
  conversationId: string | null;
};

export default function ChatPanel({ conversationId }: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [contact, setContact] = useState<Contact | null>(null);
  const [enabled, setEnabled] = useState(true);

  // Fetch existing messages by conversation Id
  useEffect(() => {
    if (!conversationId) {
      setMessages([]);
      return;
    }

    async function loadMessages(conversationId: string) {
      const data = await getMessages(conversationId);
      setMessages(data);

      const contact_data = await getContact(data[0].contact_id);
      setContact(contact_data);
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
          <h2 className="font-semibold">
            {contact?.f_name ?? contact?.whatsapp_phone}
          </h2>
          <p className="text-sm text-slate-500">
            {contact?.whatsapp_name
              ? contact?.whatsapp_name + " • " + contact?.whatsapp_phone
              : contact?.whatsapp_phone}
          </p>
        </div>

        <div className="flex gap-3">
          <p className="text-sm font-medium">
            AI Agent
            <span
              className={`ml-2 text-xs rounded-md p-1 ${enabled ? "bg-green-100 text-green-600" : "bg-amber-100 text-amber-600"}`}
            >
              {enabled ? "ON" : "OFF"}
            </span>
          </p>
          <button
            type="button"
            onClick={() => setEnabled((current) => !current)}
            className={`relative h-5 w-10 rounded-full transition-colors ${
              enabled ? "bg-blue-600" : "bg-slate-300"
            }`}
            aria-pressed={enabled}
          >
            <span
              className={`absolute top-0.5 h-4 w-4 rounded-full bg-white shadow-sm transition-transform ${
                enabled ? "translate-x-0.5" : "-translate-x-4.5"
              }`}
            />
          </button>
        </div>
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
