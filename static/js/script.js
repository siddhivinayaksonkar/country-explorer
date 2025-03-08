function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
    document.getElementById('comparison-results').style.display = show ? 'none' : 'block';
}

function displayComparison(data) {
    const country1Name = data.country1.name;
    const country2Name = data.country2.name;
    const country1Data = data.country1.data;
    const country2Data = data.country2.data;

    // Set headers
    document.getElementById('country1-header').textContent = country1Name;
    document.getElementById('country2-header').textContent = country2Name;

    // Clear existing table body
    const tableBody = document.getElementById('comparison-body');
    tableBody.innerHTML = '';

    // Add rows for each attribute
    for (const [key, value1] of Object.entries(country1Data)) {
        const row = document.createElement('tr');
        
        // Category name cell
        const categoryCell = document.createElement('td');
        categoryCell.className = 'attribute-name';
        categoryCell.textContent = key;
        row.appendChild(categoryCell);

        // Country 1 value cell
        const value1Cell = document.createElement('td');
        value1Cell.textContent = value1;
        row.appendChild(value1Cell);

        // Country 2 value cell
        const value2Cell = document.createElement('td');
        value2Cell.textContent = country2Data[key];
        row.appendChild(value2Cell);

        tableBody.appendChild(row);
    }

    // Show the results
    document.getElementById('comparison-results').style.display = 'block';
}

async function compareCountries() {
    const country1 = document.getElementById('country1').value.trim();
    const country2 = document.getElementById('country2').value.trim();

    if (!country1 || !country2) {
        showError('Please enter both country names');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/api/compare', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ country1, country2 })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to compare countries');
        }

        displayComparison(data.data);
    } catch (error) {
        showError(error.message);
        document.getElementById('comparison-results').style.display = 'none';
    } finally {
        showLoading(false);
    }
}

// Add event listeners for Enter key
document.getElementById('country1').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        document.getElementById('country2').focus();
    }
});

document.getElementById('country2').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        compareCountries();
    }
}); 