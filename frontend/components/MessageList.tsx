import MessageBubble from "./MessageBubble";
import type { Message } from "@/types/message";

type MessageListProps = {
  messages: Message[];
};

export default function MessageList({ messages }: MessageListProps) {
  return (
    <div className="flex-1 space-y-4 overflow-y-auto scrollbar-thin scrollbar-thumb-slate-300 bg-slate-100 p-6">
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}
    </div>
  );
}
