// Function to fetch user data from the server
function fetchUsers() {
    // Make an AJAX request to fetch user data
    fetch('/fetch_users')
        .then(response => response.json())
        .then(data => {
            // Process the response data
            displayUsers(data.users);
        })
        .catch(error => console.error('Error fetching users:', error));
}

// Function to dynamically display user data
function displayUsers(users) {
    const searchResults = document.getElementById('searchResults');

    // Clear previous search results
    searchResults.innerHTML = '';

    // Check if users array is empty
    if (users.length === 0) {
        searchResults.innerHTML = '<p>No users found.</p>';
        return;
    }

    // Generate HTML for each user and append it to searchResults
    const userListHTML = users.map(user => `
        <li>
            ID: ${user.user_id}<br>
            Username: ${user.username}<br>
            Password: ${user.password}<br>
            First Name: ${user.first_name}<br>
            Last Name: ${user.last_name}<br>
            Email: ${user.email}<br>
            Phone: ${user.phone}<br>
            User Type: ${user.user_type}<br>
            <hr>
        </li>
    `).join('');

    searchResults.innerHTML = `<ul>${userListHTML}</ul>`;
}

// Call fetchUsers when the page loads
window.onload = function() {
    fetchUsers();
};
