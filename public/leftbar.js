// Toggles the visibility of the dropdown menu
function toggleDropdown() {
    const dropdown = document.getElementById('userDropdown');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';

    // Fetch users when dropdown is shown
    if (dropdown.style.display === 'block') {
      fetchUsers();
    }
  }

  // Fetches user list from the backend
  function fetchUsers() {
    fetch('https://your-backend-endpoint.com/users')  // Replace with your actual endpoint
      .then(response => response.json())
      .then(data => {
        const dropdown = document.getElementById('userDropdown');
        
        // Clear any previous items except for the "Create New User" button
        const createButton = dropdown.querySelector('.create-user-button');
        dropdown.innerHTML = '';  // Clear any previous items
        dropdown.appendChild(createButton); // Re-append the create button

        // Add users to the dropdown
        data.users.forEach(user => {
          const item = document.createElement('div');
          item.className = 'dropdown-item';
          item.textContent = user.name;  // Assuming 'name' is a property of the user
          dropdown.appendChild(item);
        });
      })
      .catch(error => {
        console.error('Error fetching users:', error);
      });
  }

  // Redirect to the user creation page
  function redirectToCreateUser() {
    window.location.href = '/create-user';  // Replace with your actual user creation page URL
  }

  // Close the dropdown if clicked outside of it
  document.addEventListener('click', (event) => {
    const dropdown = document.getElementById('userDropdown');
    if (!dropdown.contains(event.target) && event.target !== document.querySelector('.nickname-box')) {
      dropdown.style.display = 'none';
    }
  });
  
  function adjustDropdownHeight() {
  const dropdown = document.getElementById('userDropdown');
  const navbar = document.querySelector('.footer');
  const dropdownButton = document.querySelector('.nickname-box');

  // Obliczanie pozycji końca przycisku dropdowna
  const dropdownButtonRect = dropdownButton.getBoundingClientRect();
  const navbarHeight = navbar.offsetHeight;
  const dropdownButtonBottom = dropdownButtonRect.bottom;  // Wysokość końca przycisku dropdowna

  // Obliczanie dostępnej wysokości na dropdown
  const availableHeight = window.innerHeight - dropdownButtonBottom - navbarHeight - 10;  // 10px marginesu

  // Ustawianie max-height na podstawie dostępnej przestrzeni
  dropdown.style.maxHeight = `${availableHeight}px`;
  }

  // Wywołanie funkcji, aby ustawić odpowiednią wysokość na początku
  window.addEventListener('load', adjustDropdownHeight);

  // Dopasowanie wysokości przy zmianie rozmiaru okna
  window.addEventListener('resize', adjustDropdownHeight);
