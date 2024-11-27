function resetCounter() {
    fetch('/reset', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            document.getElementById('counter').innerText = 'Visits: ' + data.visit_count;
        });
}
