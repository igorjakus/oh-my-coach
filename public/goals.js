window.goals = [];
window.tasksInGoals = {};

function rerenderTaskList() {
    let list = "";
    for (const goal of goals) {
        list += generateTopic(goal);
    }
    if (list.length == 0) {
        $(".middle-panel").innerHTML = `<div style="opacity: 0.8; width: 100%; text-align: center"> No goals yet! :(</div>`;
    } else {
        $(".middle-panel").innerHTML = list;
    }
}

function generateTopic(goal) {
    return `<div class="topic">
    <h3>${goal.name}</h3>
        <ul class="task-list">
        ${window.tasksInGoals[goal.id].map(
            task => `<li><input type="checkbox" id="${task.id}"><label for="${task.id}">${task.name}</label></li>`
        ).join(" ")}
        </ul>
    </div>`
}

let oldonload = window.onload;
window.onload = () => {
    if (oldonload) oldonload();
    (async () => {
        const goals = await GetAllGoals();
        console.log(goals)
        window.goals = goals;
        for (const goal of goals) {
            const tasks = await GetAllTasksInGoal(goal.id);
            window.tasksInGoals[goal.id] = tasks;
        }
        rerenderTaskList();
    })();
}