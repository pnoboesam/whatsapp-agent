export type Message = {
  id: string;
  contact_id: string;
  conversation_id: string;
  sender_type: "customer" | "ai" | "human";
  content: string;
  created_at: string;
};