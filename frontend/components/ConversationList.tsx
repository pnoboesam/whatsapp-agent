"use client";

import ConversationItem from "./ConversationItem";
import type { Conversation } from "@/types/conversation";
import { useEffect, useState } from "react";
import { getConversations } from "@/lib/api";
import { supabase } from "@/lib/supabase";

type ConversationListProps = {
  onSelectConversation: (conversationId: string) => void;
};

function getTimestamp(value: string | null) {
  return value ? new Date(value).getTime() : 0;
}

export default function ConversationList({
  onSelectConversation,
}: ConversationListProps) {
  const [conversations, setConversations] = useState<Conversation[]>([]);

  // load all business conversations
  useEffect(() => {
    async function loadConversations() {
      const data: Conversation[] = await getConversations();
      setConversations(data);
    }
    loadConversations();
  }, []);

  // listen for new conversation updates
  useEffect(() => {
    async function testSupabaseAccess() {
      const { data, error } = await supabase
        .from("conversations")
        .select("id")
        .limit(1);

      console.log("Conversations SELECT test:", { data, error });
    }

    testSupabaseAccess();

    const channel = supabase
      .channel("conversations-list")
      .on(
        "postgres_changes",
        {
          event: "UPDATE",
          schema: "public",
          table: "conversations",
        },
        (payload) => {
          console.log("CONVERSATION UPDATE RECEIVED:", payload);

          const updatedConversation = payload.new as Conversation;

          setConversations((currentConversations) => {
            return currentConversations
              .map((conversation) =>
                conversation.id === updatedConversation.id
                  ? updatedConversation
                  : conversation,
              )
              .sort(
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
  }, []);

  return (
    <aside className="flex h-full min-h-0 flex-col w-80 border-r border-slate-300 bg-white">
      <div className="border-b border-slate-300 px-4 pt-4">
        <h2 className="font-semibold">Conversations</h2>

        <input
          type="text"
          placeholder="Search conversations..."
          className="mt-3 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-600"
        />

        <div className="mt-4 flex gap-4 justify-around text-sm">
          <button className="border-b-2 border-blue-600 pb-2 font-medium text-blue-600">
            All
          </button>

          <button className="pb-2 text-slate-500">Unread</button>

          <button className="pb-2 text-slate-500">AI</button>

          <button className="pb-2 text-slate-500">Human</button>
        </div>
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-slate-300">
        {conversations.map((conversation) => (
          <ConversationItem
            key={conversation.id}
            conversation={conversation}
            onSelect={() => onSelectConversation(conversation.id)}
          />
        ))}
      </div>
    </aside>
  );
}
