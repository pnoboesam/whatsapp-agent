import MessageBubble from "./MessageBubble";

export default function MessageList() {
  return (
    <div className="flex-1 space-y-4 overflow-y-auto bg-slate-100 p-6">
      <MessageBubble
        sender="customer"
        message="Hi, I need an appointment."
        time="2:30 PM"
      />

      <MessageBubble
        sender="ai"
        message="Sure! I can help you with that. When would you like to visit?"
        time="2:31 PM"
      />

      <MessageBubble
        sender="customer"
        message="Let's do tomorrow at 9pm."
        time="2:33 PM"
      />

      <MessageBubble
        sender="human"
        message="Great, tomorrow at 9pm is available"
        time="2:34 PM"
      />
    </div>
  );
}
