type ConversationItemProps = {
  name: string;
  lastMessage: string;
  unreadCount: number;
  lastMessageAt: string;
  aiEnabled: boolean;
};

export default function ConversationItem({
  name,
  lastMessage,
  unreadCount,
  lastMessageAt,
  aiEnabled,
}: ConversationItemProps) {
  return (
    // <div className="flex items-center justify-between border-b border-slate-100 p-4">
    <div className="flex-col items-center justify-between border-b border-slate-200 p-4 hover:bg-slate-50 hover:border-r-2 hover:border-e-blue-600">
      <div className="min-w-0">
        <div className="flex items-center justify-between gap-3">
          <p className="font-medium">{name}</p>

          <span className="shrink-0 text-xs text-slate-400">
            {lastMessageAt}
          </span>
        </div>

        <p className="truncate text-sm text-slate-500">{lastMessage}</p>
      </div>

      <div className="flex justify-between">
        <span
          className={`mt-1 inline-block rounded px-1.5 py-0.5 text-xs font-medium ${
            aiEnabled
              ? "bg-green-50 text-green-600"
              : "bg-amber-50 text-amber-600"
          }`}
        >
          {aiEnabled ? "AI" : "Human"}
        </span>

        {unreadCount > 0 && (
          <span className="ml-3 rounded-full bg-blue-600 px-2 py-1 text-xs font-medium text-white">
            {unreadCount}
          </span>
        )}
      </div>
    </div>
  );
}
