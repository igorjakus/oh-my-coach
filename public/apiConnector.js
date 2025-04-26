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


async function CreatePersonas(personaJSON)
{
    // Construct query parameters from the personaJSON object
    const queryParams = new URLSearchParams({
        pseudonym: personaJSON.pseudonym,
        personality: personaJSON.personality,
        tone: personaJSON.tone,
        motivation_level: personaJSON.motivationLevel,
        task_focus: personaJSON.taskFocus,
        language: personaJSON.language,
        response_length: personaJSON.responseLength || 'flexible', // Default if not provided
        humor_style: personaJSON.humorStyle || 'none', // Default if not provided
        empathy_level: personaJSON.empathyLevel || 'medium', // Default if not provided
        reward_style: personaJSON.rewardStyle || 'moderate', // Default if not provided
        feedback_type: personaJSON.feedbackType || 'constructive' // Default if not provided
    }).toString();

    return await fetch(`http://localhost:8000/personalization/create_agent?${queryParams}`, {
        method: 'POST',
        headers: {
            // No Content-Type needed for query parameters in POST
            'Content-Type': 'application/json'
        }
        // Body is not needed as parameters are in the URL
    })
}