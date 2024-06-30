export async function sendImageRequest(destination) {
    // Define the API URL
    const url = 'http://127.0.0.1:8000/generate_images/';

    // Create the data object to send for each destination
    const data = destination;

    // Try to send the POST request and handle the response for each destination
    try {
        console.log(`Sending image data for destination:`, JSON.stringify(data));
        const response = await fetch(url, {
            method: 'POST', // Specify the method
            headers: {
                'Content-Type': 'application/json' // Specify the content type as JSON
            },
            body: JSON.stringify(data) // Convert the JavaScript object to a JSON string
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

    } catch (error) {
        console.error(`Error for destination:`, error);
    }
}
