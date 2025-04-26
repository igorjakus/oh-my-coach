const $ = (selector) => document.querySelector(selector)

function showView(test) {
    switch(test) {
        case "goalsView":
            document.location.href = "/public/goals.html"
            break;
        case "chatView":
            document.location.href = "/public/chat.html"
            break;
        case "retroView":
            document.location.href = "/public/retro.html"
            break;
        case "progressView":
            document.location.href = "/public/progress.html"
            break;
    }
}