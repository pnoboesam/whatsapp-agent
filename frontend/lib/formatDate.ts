export function formatMessageTime(date: string | null) {
  if (!date) return "";

  const messageDate = new Date(date);
  const now = new Date();

  const messageDay = new Date(
    messageDate.getFullYear(),
    messageDate.getMonth(),
    messageDate.getDate(),
  );

  const today = new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate(),
  );

  const daysDifference =
    (today.getTime() - messageDay.getTime()) /
    (1000 * 60 * 60 * 24);

  if (daysDifference === 0) {
    return messageDate.toLocaleTimeString([], {
      hour: "numeric",
      minute: "2-digit",
    });
  }

  if (daysDifference === 1) {
    return "Yesterday";
  }

  if (daysDifference < 7) {
    return messageDate.toLocaleDateString([], {
      weekday: "long",
    });
  }

  return messageDate.toLocaleDateString([], {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
}