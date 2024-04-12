document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    // Get search input value
    var searchInput = document.getElementById('title').value;

    // Make AJAX call to server
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'title': searchInput }),
    })
    .then(response => response.json())
    .then(data => {
        // Handle server response
        if (data.status == 'ok') {
            // Display search results
            var resultsHTML = '<h2>Search Results</h2><ul>';
            data.results.forEach(function(item) {
                resultsHTML += '<li>' + item.title + '</li>';
            });
            resultsHTML += '</ul>';
            document.getElementById('searchResults').innerHTML = resultsHTML;
        } else {
            // Display error message
            document.getElementById('searchResults').innerHTML = '<p>Error: ' + data.message + '</p>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
