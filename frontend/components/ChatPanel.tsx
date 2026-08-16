import MessageList from "@/components/MessageList";
import MessageComposer from "./MessageComposer";
import {
  getMessages,
  getContact,
  getConversation,
  toggleAI,
  markAsRead,
} from "@/lib/api";
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
  const [aiEnabled, setAiEnabled] = useState(true);

  async function handleToggleAI() {
    if (!conversationId) return;

    const newState = !aiEnabled;

    const data = await toggleAI(conversationId, newState);

    setAiEnabled(data.ai_enabled);
  }

  // Fetch existing messages by conversation Id
  useEffect(() => {
    if (!conversationId) {
      setMessages([]);
      return;
    }

    async function loadMessages(conversationId: string) {
      const data = await getMessages(conversationId);
      setMessages(data);

      if (data.length > 0) {
        const contact_data = await getContact(data[0].contact_id);
        setContact(contact_data);
      }
    }

    async function markConversationAsRead(conversationId: string) {
      await markAsRead(conversationId);
    }

    loadMessages(conversationId);
    markConversationAsRead(conversationId);
  }, [conversationId]);

  // Set AIState
  useEffect(() => {
    if (!conversationId) return;

    async function loadAIState(conversationId: string) {
      const data = await getConversation(conversationId);
      setAiEnabled(data.ai_enabled);
    }

    loadAIState(conversationId);
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
      {conversationId ? (
        <>
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

            <div className="flex items-end gap-2">
              <p className="text-sm font-medium">
                AI
                <span
                  className={`ml-1 text-xs rounded-md p-1 ${aiEnabled ? "bg-green-100 text-green-600" : "bg-amber-100 text-amber-600"}`}
                >
                  {aiEnabled ? "ON" : "OFF"}
                </span>
              </p>
              <button
                type="button"
                onClick={handleToggleAI}
                className={`relative h-5 w-10 rounded-full transition-colors ${
                  aiEnabled ? "bg-blue-600" : "bg-slate-300"
                }`}
                aria-pressed={aiEnabled}
              >
                <span
                  className={`absolute top-0.5 h-4 w-4 rounded-full bg-white shadow-sm transition-transform ${
                    aiEnabled ? "translate-x-0.5" : "-translate-x-4.5"
                  }`}
                />
              </button>
            </div>
          </header>

          <MessageList messages={messages} />

          {aiEnabled ? (
            <div className="border-t border-slate-300 bg-white p-4 text-center">
              <p className="text-sm text-slate-500">
                AI Agent is handling this conversation. Turn AI off to send a
                message manually.
              </p>
            </div>
          ) : (
            <MessageComposer conversationId={conversationId} />
          )}
        </>
      ) : (
        <div className="flex flex-1 items-center justify-center">
          <p className="text-sm bg-blue-50 text-blue-600 p-1 rounded-b-md">
            Select a conversation to view messages
          </p>
        </div>
      )}
    </section>
  );
}
