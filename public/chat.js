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
    $(".chat-content").innerHTML = rendererHTML;
    $(".chat-content").scrollTop = $(".chat-content").scrollHeight;
}

// MOCK-UP responses
const mockupResponses = [
    "Sure! Let’s start by understanding your main goal.<br>Could you tell me a bit more about what you want to achieve?",
    "Got it! That's a great start.<br>Now, how often would you like to work towards this goal each week?"
];
let mockupCounter = 0;

async function requestAndAwaitResponseTo(content) {
    await sleep(1000); // simulate network delay
    if (mockupCounter < mockupResponses.length) {
        return mockupResponses[mockupCounter++];
    } else {
        return "I'm ready for your next question! 🚀"; // fallback
    }
}

// Utility sleep function
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

let waitingForResponse = false;
async function handleMessageSend() {
    if (waitingForResponse) return;
    const content = $(".chat-box-input").value;
    if (content.length < 1) return;
    $(".chat-box-input").value = "";
    addAsUserToChat(content);
    rerenderMessagesInChat();

    waitingForResponse = true;
    $(".send-icon").style.opacity = 0.2;
    $(".chat-box-input").disabled = true;

    // Add "Typing..." fake message
    addAsChatbotToChat("Bot", "<i>Typing...</i>");
    rerenderMessagesInChat();

    const responseFromBot = await requestAndAwaitResponseTo(content);

    // Remove "Typing..." message
    window.chatHistory.pop();

    // Add real bot message
    addAsChatbotToChat("Bot", responseFromBot);
    rerenderMessagesInChat();

    $(".send-icon").style.opacity = 1;
    $(".chat-box-input").disabled = false;
    waitingForResponse = false;
}

function registerChatControlls() {
    $(".send-icon").addEventListener("click", handleMessageSend);
    $(".chat-box-input").addEventListener("keydown", (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            handleMessageSend();
        }
    });
}

// Helper function to select elements
function $(selector) {
    return document.querySelector(selector);
}

registerChatControlls();
