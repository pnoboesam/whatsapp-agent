export type Conversation = {
    id: string;
    contact_id: string;
    whatsapp_phone: string;
    last_message: string | null;
    last_message_at: string | null;
    unread_count: number;
    ai_enabled: boolean;
}