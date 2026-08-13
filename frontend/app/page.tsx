import Header from "@/components/Header";
import ConversationList from "@/components/ConversationList";
import ChatPanel from "@/components/ChatPanel";

export default function Home() {
  return (
    <main className="flex h-screen flex-col">
      <Header />

      <div className="flex flex-1 min-h-0">
        <ConversationList />
        <ChatPanel />
      </div>
    </main>
  );
}
