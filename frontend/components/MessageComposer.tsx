import { useState } from "react";
import { sendHumanMessage } from "@/lib/api";
import type { Message } from "@/types/message";

type MessageComposerProps = {
  conversationId: string | null;
  onMessageSent: (message: Message) => void;
};

export default function MessageComposer({
  conversationId,
  onMessageSent,
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
      const sentMessage = await sendHumanMessage(conversationId, messageToSend);
      onMessageSent(sentMessage);
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
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type a message..."
          className="flex-1 rounded-lg border border-slate-300 px-4 py-3 text-sm outline-none focus:border-blue-600"
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
