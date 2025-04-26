const $ = (selector) => document.querySelector(selector)

function showView(test) {
    switch(test) {
        case "goalsView":
            document.location.href = "/goals"
            break;
        case "chatView":
            document.location.href = "/chat"
            break;
        case "retroView":
            document.location.href = "/retro"
            break;
        case "progressView":
            document.location.href = "/progress"
            break;
    }
}