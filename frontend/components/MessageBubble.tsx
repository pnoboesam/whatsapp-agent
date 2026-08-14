import type { Message } from "@/types/message";
import { formatMessageTime } from "@/lib/formatDate";

type MessageBubbleProps = {
  message: Message;
};

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isCustomer = message.sender_type === "customer";
  return (
    <div className={isCustomer ? "flex" : "flex justify-end"}>
      <div
        className={
          isCustomer
            ? "max-w-md rounded-lg bg-white px-4 py-3 shadow-sm mr-6"
            : "max-w-md rounded-lg bg-green-100 px-4 py-3 shadow-sm ml-6"
        }
      >
        <p className="mb-1 text-xs font-medium text-slate-500">
          {message.sender_type === "customer"
            ? "Customer"
            : message.sender_type === "ai"
              ? "AI"
              : "Human"}
        </p>

        <p className="text-sm text-slate-800">{message.content}</p>

        <p className="mt-1 text-right text-[11px] text-slate-400">
          {formatMessageTime(message.created_at)}
        </p>
      </div>
    </div>
  );
}
