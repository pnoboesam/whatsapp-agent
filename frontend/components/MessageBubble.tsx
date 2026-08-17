import type { Message } from "@/types/message";
import { formatMessageTime } from "@/lib/formatDate";

type MessageBubbleProps = {
  message: Message;
};

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isCustomer = message.sender_type === "customer";
  return (
    <div
      className={`flex w-full ${isCustomer ? "justify-start" : "justify-end"}`}
    >
      <div
        className={`w-[85%] max-w-md px-4 py-3 shadow-sm ${
          isCustomer
            ? "rounded-tr-xl rounded-b-xl bg-white"
            : "rounded-tl-xl rounded-b-xl bg-green-100"
        }`}
      >
        <p className="mb-1 text-xs font-medium text-slate-500">
          {message.sender_type === "customer"
            ? "Customer"
            : message.sender_type === "ai"
              ? "AI"
              : "Human"}
        </p>

        <p className="break-words text-sm text-slate-800">{message.content}</p>

        <p className="mt-1 text-right text-[11px] text-slate-400">
          {formatMessageTime(message.created_at)}
        </p>
      </div>
    </div>
  );
}
