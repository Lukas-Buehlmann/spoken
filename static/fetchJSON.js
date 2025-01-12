async function loadJSON(filePath) {
    try {
        const response = await fetch(filePath);
        if (!response.ok) {
            throw new Error(`Failed to fetch ${filePath}: ${response.statusText}`);
        }
        const jsonData = await response.json();
        return jsonData;
    } catch (error) {
        console.error("Error loading JSON file:", error);
        throw error; // Re-throw the error to allow the caller to handle it
    }
}

async function displayJSON(filePath) {
    const jsonOutput = document.getElementById('jsonTextOutput');
    const jsonOutputSimple = document.getElementById('jsonOutputSimple');
    try {
        const data = await loadJSON(filePath);
        if (jsonOutput) {
            jsonOutput.textContent = data.text.original ? data.text.original : "No original text available";
        }
        if (jsonOutputSimple) {
            jsonOutputSimple.textContent = data.text.simplified ? data.text.simplified : "No simplified text available";
        }
    } catch (error) {
        console.error("Error loading JSON:", error); // Log the error to the console
        jsonOutput.textContent = "Failed to load JSON data. See console for details.";
    }
}


displayJSON('../static/current_state.json');