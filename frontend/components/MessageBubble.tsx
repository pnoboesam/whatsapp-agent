type MessageBubbleProps = {
  message: string;
  sender: "customer" | "ai" | "human";
  time: string;
};

export default function MessageBubble({
  message,
  sender,
  time,
}: MessageBubbleProps) {
  const isCustomer = sender === "customer";
  return (
    <div className={isCustomer ? "flex" : "flex justify-end"}>
      <div
        className={
          isCustomer
            ? "max-w-md rounded-lg bg-white px-4 py-3 shadow-sm"
            : "max-w-md rounded-lg bg-green-100 px-4 py-3 shadow-sm"
        }
      >
        <p className="mb-1 text-xs font-medium text-slate-500">
          {sender === "customer"
            ? "Customer"
            : sender === "ai"
              ? "AI"
              : "Human"}
        </p>

        <p className="text-sm text-slate-800">{message}</p>

        <p className="mt-1 text-right text-[11px] text-slate-400">{time}</p>
      </div>
    </div>
  );
}
