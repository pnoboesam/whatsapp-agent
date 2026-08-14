import type { Conversation } from "@/types/conversation";

const API_URL = process.env.NEXT_PUBLIC_API_URL;


export async function getConversations(): Promise<Conversation[]> {
    const response = await fetch(`${API_URL}/api/v1/conversations`);

    if (!response.ok) {
        throw new Error("Failed to fetch conversations");
    }

    const data: Conversation[] = await response.json();
    return data;
}


export async function getMessages(conversationId: string) {
    const response = await fetch(
        `${API_URL}/api/v1/conversations/${conversationId}/messages`,
    );

    if (!response.ok) {
        throw new Error("Failed to fetch messages");
    }

    return response.json();
}
