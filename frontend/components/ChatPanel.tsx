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
  onBack: () => void;
};

export default function ChatPanel({ conversationId, onBack }: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [contact, setContact] = useState<Contact | null>(null);
  const [aiEnabled, setAiEnabled] = useState(true);
  const [isTogglingAI, setIsTogglingAI] = useState(false);
  const [aiError, setAiError] = useState<string | null>(null);

  async function handleToggleAI() {
    if (!conversationId || isTogglingAI) return;

    const newState = !aiEnabled;

    setAiError(null);
    setIsTogglingAI(true);

    try {
      const data = await toggleAI(conversationId, newState);
      setAiEnabled(data.ai_enabled);
    } catch {
      setAiError("Failed to change AI state. Please try again.");
    } finally {
      setIsTogglingAI(false);
    }
  }

  // Fetch existing messages by conversation Id
  useEffect(() => {
    if (!conversationId) {
      return;
    }

    let cancelled = false;

    async function loadMessages(conversationId: string) {
      try {
        const data = await getMessages(conversationId);

        if (cancelled) return;

        setMessages(data);

        if (data.length > 0) {
          const contact_data = await getContact(data[0].contact_id);

          if (cancelled) return;

          setContact(contact_data);
        } else {
          setContact(null);
        }
      } catch (error) {
        if (cancelled) return;

        console.error("Failed to load conversation:", error);
      }
    }

    async function markConversationAsRead(conversationId: string) {
      try {
        await markAsRead(conversationId);
      } catch (error) {
        console.error("Failed to mark conversation as read:", error);
      }
    }

    loadMessages(conversationId);
    markConversationAsRead(conversationId);

    return () => {
      cancelled = true;
    };
  }, [conversationId]);

  // Set AIState
  useEffect(() => {
    if (!conversationId) return;

    let cancelled = false;

    async function loadAIState(conversationId: string) {
      setAiError(null);

      try {
        const data = await getConversation(conversationId);

        if (cancelled) return;

        setAiEnabled(data.ai_enabled);
      } catch (error) {
        if (cancelled) return;

        console.error("Failed to load AI state:", error);
        setAiError("Failed to load AI state. Please try again.");
      }
    }

    loadAIState(conversationId);

    return () => {
      cancelled = true;
    };
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
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, [conversationId]);

  return (
    <section className="flex flex-1 flex-col">
      {conversationId ? (
        <>
          <header className="flex items-center justify-between gap-3 border-b border-slate-300 bg-white px-4 py-3 md:px-5 md:py-4">
            <div className="flex flex-1 min-w-0 items-center">
              <button
                type="button"
                onClick={onBack}
                className="mr-3 text-xl md:hidden shrink-0"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  className="h-5 w-5"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M15 19l-7-7 7-7"
                  />
                </svg>
              </button>

              <div className="min-w-0 flex-1">
                <h2 className="truncate font-semibold">
                  {contact?.f_name ?? contact?.whatsapp_phone}
                </h2>

                <p className="truncate text-sm text-slate-500">
                  {contact?.whatsapp_name
                    ? contact.whatsapp_name + " • " + contact.whatsapp_phone
                    : contact?.whatsapp_phone}
                </p>
              </div>
            </div>

            <div className="flex shrink-0 items-end gap-2">
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
                disabled={isTogglingAI}
                className={`relative h-5 w-10 rounded-full transition-colors ${
                  aiEnabled ? "bg-blue-600" : "bg-slate-300"
                } ${isTogglingAI ? "cursor-not-allowed opacity-60" : "cursor-pointer"}`}
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

          {aiError && (
            <div className="border-b border-red-200 bg-red-50 px-3 py-2 text-center">
              <p className="text-xs text-red-600">{aiError}</p>
            </div>
          )}

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
