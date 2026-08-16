"use client";

import Header from "@/components/Header";
import ConversationList from "@/components/ConversationList";
import ChatPanel from "@/components/ChatPanel";

import { useState } from "react";

export default function Home() {
  const [selectedConversationId, setSelectedConversationId] = useState<
    string | null
  >(null);

  console.log(selectedConversationId);

  return (
    <main className="flex h-screen flex-col">
      <Header />

      <div className="flex flex-1 min-h-0">
        <ConversationList
          conversationId={selectedConversationId}
          onSelectConversation={setSelectedConversationId}
        />
        <ChatPanel conversationId={selectedConversationId} />
      </div>
    </main>
  );
}
