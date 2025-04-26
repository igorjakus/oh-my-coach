class ChatEntry {
    fromUser;
    messageContent;
    profilePicuteURL;
    timestamp;
    nickname;

    constructor(timestamp, fromUser, nickname, messageContent, profilePicuteURL) {
        this.timestamp = timestamp;
        this.fromUser = fromUser;
        this.messageContent = messageContent;
        this.profilePicuteURL = profilePicuteURL;
        this.nickname = nickname;
    }
}

window.chatHistory = [];

// Predefined mockup responses
const mockupResponses = [
    "Sure! Let’s start by understanding your main goal.<br>Could you tell me a bit more about what you want to achieve?",
    "Got it! That's a great start.<br>Now, how often would you like to work towards this goal each week?"
];

let mockupCounter = 0; // Counter for mockup responses

function getChatMessageComponentFromData(chatEntry) {
    return `<div class="${chatEntry.fromUser ? "user-chatblock" : "bot-chatblock"} chatblock">
        <div class="chat-message-header">
            <div class="chat-profile-picture"></div>
            <div class="chat-profile-nickname">${chatEntry.nickname}</div>
        </div>
        <div class="chat-message-content">${chatEntry.messageContent}</div>
    </div>`;
}

function mergeNeighbouringMessages(chatHistory) {
    let newChatHistory = [chatHistory[0]];
    for (let i = 1; i < chatHistory.length; i++) {
        if (chatHistory[i].fromUser == newChatHistory[newChatHistory.length - 1].fromUser) {
            newChatHistory[newChatHistory.length - 1]
                .messageContent += `<br>${chatHistory[i].messageContent}`;
        } else {
            newChatHistory.push(chatHistory[i]);
        }
    }
    return newChatHistory;
}

function addAsChatbotToChat(name, messageContent, timestamp, profilePicuteURL) {
    window.chatHistory.push(new ChatEntry(
        timestamp == null ? Date.now() : timestamp,
        false,
        name,
        messageContent,
        profilePicuteURL
    ));
    window.chatHistory = window.chatHistory.sort((a, b) => a.timestamp - b.timestamp);
    window.chatHistory = mergeNeighbouringMessages(window.chatHistory);
}

function addAsUserToChat(messageContent, timestamp, profilePicuteURL) {
    window.chatHistory.push(new ChatEntry(
        timestamp == null ? Date.now() : timestamp,
        true,
        "Me",
        messageContent,
        profilePicuteURL
    ));
    window.chatHistory = window.chatHistory.sort((a, b) => a.timestamp - b.timestamp);
    window.chatHistory = mergeNeighbouringMessages(window.chatHistory);
}

function rerenderMessagesInChat() {
    window.chatHistory = window.chatHistory.sort((a, b) => a.timestamp - b.timestamp);
    let rendererHTML = "";
    for (const msg of window.chatHistory) {
        rendererHTML += getChatMessageComponentFromData(msg);
    }
    document.querySelector(".chat-content").innerHTML = rendererHTML;
    document.querySelector(".chat-content").scrollTop = document.querySelector(".chat-content").scrollHeight;
}

function respondMockup(content) {
    let responseText = "";
    if (mockupCounter < mockupResponses.length) {
        responseText = mockupResponses[mockupCounter];
        mockupCounter++;
    } else {
        responseText = "I'm ready for your next question! 🚀";
    }
    return responseText;
}

function handleMessageSend() {
    const content = document.querySelector(".chat-box-input").value.trim();
    if (content.length < 1) return;
    document.querySelector(".chat-box-input").value = "";

    addAsUserToChat(content);
    rerenderMessagesInChat();

    const response = respondMockup(content);
    addAsChatbotToChat("Bot", response);
    rerenderMessagesInChat();
}

function registerChatControlls() {
    document.querySelector(".send-icon").addEventListener("click", handleMessageSend);
    document.querySelector(".chat-box-input").addEventListener("keydown", (event) => {
        if (event.key === 'Enter') {
            handleMessageSend();
        }
    });
}

registerChatControlls();
