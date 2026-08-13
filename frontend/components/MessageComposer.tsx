export default function MessageComposer() {
  return (
    <div className="border-t border-slate-300 bg-white p-4">
      <div className="flex gap-3">
        <input
          type="text"
          placeholder="Type a message..."
          className="flex-1 rounded-lg border border-slate-300 px-4 py-3 text-sm outline-none focus:border-blue-600"
        />

        <button className="rounded-lg bg-blue-600 px-6 py-3 text-sm font-medium text-white hover:bg-blue-700">
          Send
        </button>
      </div>
    </div>
  );
}
