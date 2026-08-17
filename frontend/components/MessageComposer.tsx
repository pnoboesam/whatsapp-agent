import { useState } from "react";
import { sendHumanMessage } from "@/lib/api";
import type { Message } from "@/types/message";

type MessageComposerProps = {
  conversationId: string | null;
};

export default function MessageComposer({
  conversationId,
}: MessageComposerProps) {
  const [message, setMessage] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSend() {
    const messageToSend = message.trim();

    if (!conversationId || !messageToSend || isSending) {
      return;
    }

    setError(null);
    setMessage("");
    setIsSending(true);

    try {
      await sendHumanMessage(conversationId, messageToSend);
    } catch {
      setMessage(messageToSend);
      setError("Failed to send message. Please try again.");
    } finally {
      setIsSending(false);
    }
  }

  return (
    <div className="border-t border-slate-300 bg-white p-4">
      {error && (
        <p className="mb-2 text-sm bg-red-50 p-1 inline-block text-red-600">
          {error}
        </p>
      )}

      <div className="flex gap-3">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          placeholder="Type a message..."
          rows={1}
          className="flex-1 resize-none rounded-lg border border-slate-300 px-4 py-3 text-sm outline-none focus:border-blue-600 scrollbar-thin scrollbar-thumb-slate-300"
        />

        <button
          type="button"
          onClick={handleSend}
          disabled={isSending}
          className={
            isSending
              ? "rounded-lg bg-blue-900 px-6 py-3 text-sm font-medium text-white"
              : "rounded-lg bg-blue-600 px-6 py-3 text-sm font-medium text-white hover:bg-blue-700"
          }
        >
          {isSending ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
}
