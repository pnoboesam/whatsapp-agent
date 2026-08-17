"use client";

import Header from "@/components/Header";
import ConversationList from "@/components/ConversationList";
import ChatPanel from "@/components/ChatPanel";

import { useState } from "react";

export default function Home() {
  const [selectedConversationId, setSelectedConversationId] = useState<
    string | null
  >(null);

  return (
    <main className="flex h-dvh flex-col">
      <Header />

      <div className="flex flex-1 min-h-0">
        <div
          className={`w-full md:flex md:w-80 ${
            selectedConversationId ? "hidden" : "flex"
          }`}
        >
          <ConversationList
            conversationId={selectedConversationId}
            onSelectConversation={setSelectedConversationId}
          />
        </div>

        <div
          className={`w-full ${
            selectedConversationId ? "flex" : "hidden"
          } md:flex`}
        >
          <ChatPanel
            conversationId={selectedConversationId}
            onBack={() => setSelectedConversationId(null)}
          />
        </div>
      </div>
    </main>
  );
}
