function toggleDropdown() {
  const dropdown = document.getElementById('userDropdown');
  dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
  if (dropdown.style.display === 'block') fetchUsers();
}

function rerenderCurrentPerson() {
  $(".nickname-box").innerHTML 
}

function changeCurrPersona(id, prompt) {
  setCurrentPersona({ id, prompt })
  rerenderCurrentPerson();
}

function fetchUsers() {
  fetch('http://localhost:8000/personalization/agents')
    .then(response => response.json())
    .then(data => {
      const dropdown = document.getElementById('userDropdown');
      dropdown.innerHTML = ''; // Wyczyść stare elementy

      data.forEach(user => {
        const userDiv = document.createElement('div');
        userDiv.className = 'create-user-button';
        userDiv.textContent = user.name;
        userDiv.onclick = function() {
          changeCurrPersona(user.id, user.prompt);
        };

        // Ukryte inputy w środku
        const idInput = document.createElement('input');
        idInput.type = 'hidden';
        idInput.value = user.id;
        idInput.className = 'hidden-user-id';

        const promptInput = document.createElement('input');
        promptInput.type = 'hidden';
        promptInput.value = user.prompt;
        promptInput.className = 'hidden-user-prompt';

        userDiv.appendChild(idInput);
        userDiv.appendChild(promptInput);

        dropdown.appendChild(userDiv);
      });
    })
    .catch(error => console.error('Error fetching users:', error));
}

function openUserModal() {
  document.getElementById("userModal").style.display = "flex";
}

function closeUserModal() {
  document.getElementById("userModal").style.display = "none";
}

window.addEventListener("click", function(event) {
  const modal = document.getElementById("userModal");
  if (event.target === modal) closeUserModal();
});


function adjustDropdownHeight() {
  const dropdown = document.getElementById('userDropdown');
  const navbar = document.querySelector('.footer');
  const dropdownButton = document.querySelector('.nickname-box');
  const dropdownButtonRect = dropdownButton.getBoundingClientRect();
  const navbarHeight = navbar.offsetHeight;
  const dropdownButtonBottom = dropdownButtonRect.bottom;
  const availableHeight = window.innerHeight - dropdownButtonBottom - navbarHeight - 10;
  dropdown.style.maxHeight = `${availableHeight}px`;
}

// This function is called when a checkbox is clicked
function handleTaskCompletion(event, taskId) {
const checkbox = event.target;
const taskItem = checkbox.closest('li'); // Find the task item (li)

if (checkbox.checked) {
// Fade out the task
taskItem.classList.add('fade-out');

// When the fade-out animation is complete, remove the task from the DOM
taskItem.addEventListener('transitionend', () => {
  setTimeout(() => {
    // Remove the task item from the DOM
    taskItem.remove();

    // Make a call to the backend to update the task's status
    updateTaskStatus(taskId, true);
  }, 1000); // Wait 1 second (1000ms) after fade-out
});
}
}


// Function to make a call to the backend (example with a POST request)
function updateTaskStatus(taskId, isCompleted) {
fetch('https://your-backend-endpoint.com/update-task', {
method: 'POST',
headers: {
  'Content-Type': 'application/json',
},
body: JSON.stringify({
  taskId: taskId,
  completed: isCompleted,
}),
})
.then(response => response.json())
.then(data => {
  console.log('Task status updated:', data);
})
.catch(error => {
  console.error('Error updating task:', error);
});
}

// Event listener for checkboxes
document.querySelectorAll('.task-list input[type="checkbox"]').forEach(checkbox => {
checkbox.addEventListener('change', (event) => {
const taskId = event.target.dataset.taskId; // Assuming taskId is set as a data attribute
handleTaskCompletion(event, taskId);
});
});


function adjustPanelHeight() {
const navbar = document.querySelector('.footer');
const dropdownButton = document.querySelector('.nickname-box');
const dropdownButtonRect = dropdownButton.getBoundingClientRect();
const navbarHeight = navbar.offsetHeight;
const dropdownButtonBottom = dropdownButtonRect.bottom;

const availableHeight = window.innerHeight - navbarHeight - 10;

// Adjust the max-height for both the dropdown and the middle panel
const dropdown = document.getElementById('userDropdown');
dropdown.style.maxHeight = `${availableHeight}px`;

const middlePanel = document.querySelector('.middle-panel');
middlePanel.style.maxHeight = `${availableHeight}px`;
}

window.addEventListener('load', adjustPanelHeight);
window.addEventListener('resize', adjustPanelHeight);


window.addEventListener('load', adjustDropdownHeight);
window.addEventListener('load', closeUserModal);
window.addEventListener('resize', adjustDropdownHeight);
window.addEventListener('load', fetchUsers);
