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
    return `<div class="${chatEntry.fromUser?"user-chatblock":"bot-chatblock"} chatblock">
        <div class="chat-message-header">
            <div class="chat-profile-picture"></div>
            <div class="chat-profile-nickname">${chatEntry.nickname}</div>
        </div>
        <div class="chat-message-content">${chatEntry.messageContent}</div>
    </div>`
}

function mergeNeighbouringMessages(chatHistory) {
    let newChatHistory = [ chatHistory[0] ];
    for (let i = 1; i<chatHistory.length; i++) {
        if (chatHistory[i].fromUser == newChatHistory[newChatHistory.length-1].fromUser) {
            newChatHistory[newChatHistory.length-1]
                .messageContent += `<br>${chatHistory[i].messageContent}`
        } else {
            newChatHistory.push(chatHistory[i])
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
    window.chatHistory = window.chatHistory.sort((a,b) => a.timestamp - b.timestamp)
    window.chatHistory = mergeNeighbouringMessages(window.chatHistory);
}

async function addAsCurrentChatbotToChat(messageContent, timestamp) {
    const persona = getCurrentPersona();
    if (!persona) return; 
    const personafull = await GetPersonaById(persona.id)
    addAsChatbotToChat(personafull.name, messageContent, timestamp)
}

function addAsUserToChat(messageContent, timestamp, profilePicuteURL) {
    window.chatHistory.push(new ChatEntry(
        timestamp == null ? Date.now() : timestamp,
        true,
        "Me",
        messageContent,
        profilePicuteURL
    ));
    window.chatHistory = window.chatHistory.sort((a,b) => a.timestamp - b.timestamp)
    window.chatHistory = mergeNeighbouringMessages(window.chatHistory);
}

function rerenderMessagesInChat() {
    window.chatHistory = window.chatHistory.sort((a,b) => a.timestamp - b.timestamp)
    let rendererHTML = ""
    for (const msg of window.chatHistory) {
        rendererHTML += getChatMessageComponentFromData(msg)
    }
    $(".chat-content").innerHTML = rendererHTML;
    $(".chat-content").scrollTop = $(".chat-content").scrollHeight;
}

async function requestAndAwaitResponseTo(content) {
    const response = await fetch("http://localhost:8000/chat/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "prompt": content,
            "history": chatHistory.map( e => { 
                return {
                    "role": e.fromUser?'user':'assistant',
                    "content": e.messageContent
                }
            })
        }),
    });
    const data = await (response.text());
    var converter = new showdown.Converter();
    showdown.setOption('tables', true);
    var text      = data.replace(new RegExp('\r?\n','g'), '<br />').substring(1, data.length - 2);
    var html      = converter.makeHtml(text);
    return html;
}


let waitingForResponse = false;
async function handleMessageSend() {
    if (waitingForResponse) return;
    const content = $(".chat-box-input").value;
    if (content.length < 1) return;
    $(".chat-box-input").value = "";
    addAsUserToChat(content);
    rerenderMessagesInChat();

    waitingForResponse=true;
    $(".send-icon").style.opacity = 0.2;
    $(".chat-box-input").disabled = true;
    const responseFromBot = await requestAndAwaitResponseTo(content);
    
    addAsChatbotToChat("Bot", responseFromBot);
    rerenderMessagesInChat();
    $(".send-icon").style.opacity = 1;
    $(".chat-box-input").disabled = false;
    waitingForResponse=false;
}

function registerChatControlls() {
    $(".send-icon").addEventListener("click", handleMessageSend);
    $(".chat-box-input").addEventListener("keydown", (event) => {
        if (event.key === 'Enter') {
            handleMessageSend();
        }
    })
};

registerChatControlls();
addAsCurrentChatbotToChat("What's up? how can I help you 😊", Date.now())
    .then(rerenderMessagesInChat)