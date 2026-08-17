"use client";

import ConversationItem from "./ConversationItem";
import type { Conversation } from "@/types/conversation";
import { useEffect, useState } from "react";
import { getConversations, markAsRead } from "@/lib/api";
import { supabase } from "@/lib/supabase";

type ConversationListProps = {
  conversationId: string | null;
  onSelectConversation: (conversationId: string) => void;
};

function getTimestamp(value: string | null) {
  return value ? new Date(value).getTime() : 0;
}

export default function ConversationList({
  conversationId,
  onSelectConversation,
}: ConversationListProps) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | "unread" | "ai" | "human">(
    "all",
  );

  console.log("Current filter:", filter);
  // load all business conversations
  useEffect(() => {
    async function loadConversations() {
      setLoading(true);

      try {
        let data: Conversation[];

        if (filter === "all") {
          data = await getConversations();
        } else if (filter === "unread") {
          data = await getConversations({ unread: true });
        } else if (filter === "ai") {
          data = await getConversations({ aiEnabled: true });
        } else {
          data = await getConversations({ aiEnabled: false });
        }
        console.log("FILTER:", filter);
        console.log("RESULT:", data);
        setConversations(data);
      } finally {
        setLoading(false);
      }
    }

    loadConversations();
  }, [filter]);

  // listen for new conversation updates
  useEffect(() => {
    const channel = supabase
      .channel("conversations-list")
      .on(
        "postgres_changes",
        {
          event: "UPDATE",
          schema: "public",
          table: "conversations",
        },
        async (payload) => {
          const updatedConversation = payload.new as Conversation;
          const isCurrentlyOpen = updatedConversation.id === conversationId;

          const unreadCount = isCurrentlyOpen
            ? 0
            : updatedConversation.unread_count;

          const matchesFilter =
            filter === "all" ||
            (filter === "unread" && unreadCount > 0) ||
            (filter === "ai" && updatedConversation.ai_enabled) ||
            (filter === "human" && !updatedConversation.ai_enabled);

          if (isCurrentlyOpen && updatedConversation.unread_count > 0) {
            try {
              await markAsRead(conversationId);
            } catch (error) {
              console.error("Failed to mark conversation as read:", error);
            }
          }

          if (!matchesFilter) {
            setConversations((currentConversations) =>
              currentConversations.filter(
                (conversation) => conversation.id !== updatedConversation.id,
              ),
            );

            return;
          }

          setConversations((currentConversations) => {
            const updatedConversationWithUnreadCount = {
              ...updatedConversation,
              unread_count: isCurrentlyOpen
                ? 0
                : updatedConversation.unread_count,
            };

            const conversationExists = currentConversations.some(
              (conversation) => conversation.id === updatedConversation.id,
            );

            if (conversationExists) {
              return currentConversations
                .map((conversation) =>
                  conversation.id === updatedConversation.id
                    ? updatedConversationWithUnreadCount
                    : conversation,
                )
                .sort(
                  (a, b) =>
                    getTimestamp(b.last_message_at) -
                    getTimestamp(a.last_message_at),
                );
            }

            return [
              ...currentConversations,
              updatedConversationWithUnreadCount,
            ].sort(
              (a, b) =>
                getTimestamp(b.last_message_at) -
                getTimestamp(a.last_message_at),
            );
          });
        },
      )
      .subscribe((status) => {
        console.log("Conversation Realtime: ", status);
      });
    return () => {
      supabase.removeChannel(channel);
    };
  }, [conversationId, filter]);

  return (
    <aside className="flex h-full min-h-0 flex-col w-80 border-r border-slate-300 bg-white">
      <div className="border-b border-slate-300 px-4 pt-4">
        <h2 className="font-semibold">Conversations</h2>

        {/* <input
          type="text"
          placeholder="Search conversations..."
          className="mt-3 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-600"
        /> */}

        <div className="mt-4 flex gap-4 justify-around text-sm">
          <button
            onClick={() => setFilter("all")}
            className={`cursor-pointer pb-2 ${
              filter === "all"
                ? "border-b-2 border-blue-600 font-medium text-blue-600"
                : "text-slate-500 hover:text-blue-600"
            }`}
          >
            All
          </button>

          <button
            onClick={() => setFilter("unread")}
            className={`cursor-pointer pb-2 ${
              filter === "unread"
                ? "border-b-2 border-blue-600 font-medium text-blue-600"
                : "text-slate-500 hover:text-blue-600"
            }`}
          >
            Unread
          </button>

          <button
            onClick={() => setFilter("ai")}
            className={`cursor-pointer pb-2 ${
              filter === "ai"
                ? "border-b-2 border-blue-600 font-medium text-blue-600"
                : "text-slate-500 hover:text-blue-600"
            }`}
          >
            AI
          </button>

          <button
            onClick={() => setFilter("human")}
            className={`cursor-pointer pb-2 ${
              filter === "human"
                ? "border-b-2 border-blue-600 font-medium text-blue-600"
                : "text-slate-500 hover:text-blue-600"
            }`}
          >
            Human
          </button>
        </div>
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-slate-300">
        {loading ? (
          <div className="flex mt-10 items-center justify-center">
            <p className="text-sm bg-blue-50 text-blue-600 p-1 rounded-b-md">
              Loading Conversations...
            </p>
          </div>
        ) : conversations.length === 0 ? (
          <div className="flex flex-col mt-10 items-center justify-center">
            <p>
              {filter === "all" && "No Conversations."}
              {filter === "unread" && "No Unread Conversations."}
              {filter === "ai" && "No AI Conversations."}
              {filter === "human" && "No Human Conversations."}
            </p>

            <p className="text-sm text-slate-500">
              {filter === "unread"
                ? "You're all caught up!"
                : "Conversations will appear here."}
            </p>
          </div>
        ) : (
          conversations.map((conversation) => (
            <ConversationItem
              key={conversation.id}
              conversation={conversation}
              onSelect={() => onSelectConversation(conversation.id)}
            />
          ))
        )}
      </div>
    </aside>
  );
}
