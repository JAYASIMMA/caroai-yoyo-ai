document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').innerHTML = `<h3>Extracted Information:</h3><pre>${JSON.stringify(data.extracted_info, null, 2)}</pre>`;
        document.getElementById('visualization').style.display = 'none';
    })
    .catch(error => {
        document.getElementById('output').innerHTML = `<p style="color: red;">Error processing the file.</p>`;
        console.error('Error:', error);
    });
});

function fetchVisualization() {
    fetch('/visualize')
    .then(response => response.blob())
    .then(blob => {
        const url = URL.createObjectURL(blob);
        const visualization = document.getElementById('visualization');
        visualization.src = url;
        visualization.style.display = 'block';
        document.getElementById('output').innerHTML = '';
    })
    .catch(error => {
        document.getElementById('output').innerHTML = `<p style="color: red;">Error fetching visualization.</p>`;
        console.error('Error:', error);
    });
}

function fetchStatistics() {
    fetch('/statistics')
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').innerHTML = `<h3>Descriptive Statistics:</h3><pre>${JSON.stringify(data, null, 2)}</pre>`;
        document.getElementById('visualization').style.display = 'none';
    })
    .catch(error => {
        document.getElementById('output').innerHTML = `<p style="color: red;">Error fetching statistics.</p>`;
        console.error('Error:', error);
    });
}
