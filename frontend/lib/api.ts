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


export async function getContact(contactId: string) {
    const response = await fetch(`${API_URL}/api/v1/contacts/${contactId}`)

    if (!response.ok) {
        throw new Error("Failed to fetch contact");
    }

    return response.json()
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

// This API allows a human within the business to send a message to the customer
export async function sendHumanMessage(conversationId: string, message: string){
    const response = await fetch(`${API_URL}/api/v1/conversations/${conversationId}/messages`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body:JSON.stringify({
                human_message:message,
            }),
        }
    )

    if (!response.ok){
            throw new Error("Failed to send message")
        }

    return response.json()
}
