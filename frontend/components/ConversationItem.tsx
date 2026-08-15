import type { Conversation } from "@/types/conversation";
import type { Contact } from "@/types/contact";
import { formatMessageTime } from "@/lib/formatDate";
import { useEffect, useState } from "react";
import { getContact } from "@/lib/api";

type ConversationItemProps = {
  conversation: Conversation;
  onSelect: () => void;
};

export default function ConversationItem({
  conversation,
  onSelect,
}: ConversationItemProps) {
  const [contact, setContact] = useState<Contact | null>(null);

  useEffect(() => {
    async function loadContact() {
      const data = await getContact(conversation.contact_id);
      setContact(data);
    }

    loadContact();
  }, [conversation.contact_id]);

  return (
    <div
      onClick={onSelect}
      className="flex-col items-center justify-between cursor-pointer border-b border-slate-200 p-4 hover:bg-blue-50"
    >
      <div className="min-w-0">
        <div className="flex items-center justify-between gap-3">
          <p className="font-medium">
            {contact?.f_name ?? contact?.whatsapp_phone}
          </p>

          <span className="shrink-0 text-xs text-slate-400">
            {formatMessageTime(conversation.last_message_at)}
          </span>
        </div>

        <p className="truncate text-sm text-slate-500">
          {conversation.last_message ?? ""}
        </p>
      </div>

      <div className="flex justify-between">
        <span
          className={`mt-1 inline-block rounded px-1.5 py-0.5 text-xs font-medium ${
            conversation.ai_enabled
              ? "bg-green-50 text-green-600"
              : "bg-amber-50 text-amber-600"
          }`}
        >
          {conversation.ai_enabled ? "AI" : "Human"}
        </span>

        {conversation.unread_count > 0 && (
          <span className="ml-3 rounded-full bg-blue-600 px-2 py-1 text-xs font-medium text-white">
            {conversation.unread_count}
          </span>
        )}
      </div>
    </div>
  );
}
