


function GetAllTasksInGoal(goalId) {
    return fetch(`http://localhost:8000/tasks/goals/${goalId}/tasks`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .catch(error => console.error('Error:', error));
}

function CheckTaskDone(goalId) {
    return fetch(`http://localhost:8000/tasks/goals/${goalId}/next-task`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .catch(error => console.error('Error:', error));
}

function GetAllDoneTasksInGoal(goalId) {
    return fetch(`http://localhost:8000/tasks/goals/${goalId}/done-tasks`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .catch(error => console.error('Error:', error));
}

function GetTaskInGoal(goalId)
{
    return fetch(`http://localhost:8000/tasks/tasks/${goalId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .catch(error => console.error('Error:', error));
}