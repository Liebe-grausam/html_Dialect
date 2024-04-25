document.getElementById('readButton').addEventListener('click', function() {
    var text = document.getElementById('textInput').value;
    fetch('/read', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => console.log(data.message))
    .catch(error => console.error('Error:', error));
});
