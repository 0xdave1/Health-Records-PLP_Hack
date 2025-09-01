document.getElementById('schoolForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
        const response = await fetch('/register_school', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: document.getElementById('schoolName').value,
                email: document.getElementById('schoolEmail').value,
                password: document.getElementById('schoolPassword').value
            })
        });
        const data = await response.json();
        alert(data.message || data.error);
        if (response.ok) {
            document.getElementById('schoolForm').reset();
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

document.getElementById('studentForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
        const response = await fetch('/add_student', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: document.getElementById('studentName').value,
                age: document.getElementById('studentAge').value,
                class: document.getElementById('studentClass').value
            })
        });
        const data = await response.json();
        alert(data.message || data.error);
        if (response.ok) {
            document.getElementById('studentForm').reset();
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

async function getRecords() {
    try {
        const recordsDiv = document.getElementById('records');
        recordsDiv.innerHTML = '<p>Loading records...</p>';
        
        const response = await fetch('/get_records');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.length === 0) {
            recordsDiv.innerHTML = '<p class="no-records">No health records found</p>';
            return;
        }

        const table = `
            <table class="records-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Health Issue</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(record => `
                        <tr>
                            <td>${record.name || 'N/A'}</td>
                            <td>${record.health_issue || 'N/A'}</td>
                            <td>${record.date || 'N/A'}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
        recordsDiv.innerHTML = table;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('records').innerHTML = 
            `<p class="error">Error loading records: ${error.message}</p>`;
    }
}