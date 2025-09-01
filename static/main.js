document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent default form submission

    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Convert string values to numbers
    for (const key in data) {
        if (data.hasOwnProperty(key)) {
            data[key] = parseFloat(data[key]);
        }
    }

    const resultContainer = document.getElementById('result-container');
    const predictionText = document.getElementById('prediction-text');
    const probabilityText = document.getElementById('probability-text');
    const errorMessage = document.getElementById('error-message');
    const resultIconContainer = document.getElementById('result-icon-container');

    // Hide previous results and errors
    resultContainer.classList.add('hidden');
    errorMessage.classList.add('hidden');
    resultIconContainer.innerHTML = ''; // Clear previous icon

    try {
        // Make a POST request to the Flask backend
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Something went wrong.');
        }

        const result = await response.json();

        // Check the raw prediction value to set text and color
        const prediction = result.prediction;
        const probability = result.probability;

        if (prediction.includes('CKD')) {
            predictionText.textContent = "Yes, you have a high probability of having kidney disease.";
            predictionText.classList.remove('notckd');
            predictionText.classList.add('ckd');
            // Add a red alert icon for CKD
            resultIconContainer.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" class="result-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f44336" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                    <line x1="12" y1="9" x2="12" y2="13"/>
                    <line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
            `;
        } else {
            predictionText.textContent = "You do not have a high probability of having kidney disease.";
            predictionText.classList.remove('ckd');
            predictionText.classList.add('notckd');
            // Add a green checkmark icon for no disease
            resultIconContainer.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" class="result-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"/>
                </svg>
            `;
        }
        
        // Display the probability
        probabilityText.textContent = `Probability of disease: ${probability}`;
        resultContainer.classList.remove('hidden');

    } catch (error) {
        // Display error message
        console.error('Prediction failed:', error);
        errorMessage.textContent = `Error: ${error.message}`;
        errorMessage.classList.remove('hidden');
    }
});
