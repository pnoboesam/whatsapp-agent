import ConversationItem from "./ConversationItem";

export default function ConversationList() {
  return (
    <aside className="w-80 border-r border-slate-300 bg-white">
      <div className="border-b border-slate-300 p-4">
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

      <ConversationItem
        name="Kofi Doe"
        lastMessage="Let's do tomorrow at 9pm."
        lastMessageAt="2:34 PM"
        unreadCount={2}
        aiEnabled={true}
      />

      <ConversationItem
        name="Zipporah Oboe-Sam"
        lastMessage="Thank you so much"
        unreadCount={0}
        lastMessageAt="1:47 PM"
        aiEnabled={false}
      />
    </aside>
  );
}
