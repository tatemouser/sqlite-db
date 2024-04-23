// Listener to login button
document.getElementById('login').addEventListener('click', function() {
    // Clear any existing messages and log message for data sending
    document.getElementById('msgs').innerHTML = '';
    console.log('sending data');


    // Perform AJAX call using fetch API
    fetch('/ajaxkeyvalue', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json', // content type for JSON
        },
        // Send username and password
        body: JSON.stringify({ 'username': document.getElementById('username').value,
                               "password": document.getElementById('password').value}),
    })
    // Process
    .then(response => response.json())


    // Handle
    .then(data => {
      if (data.status == 'ok') {
          window.location.href = 'profile';
      } else {
         document.getElementById('msgs').innerHTML = '<p style= "color:red;">Error: ..........</p>';
      }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
