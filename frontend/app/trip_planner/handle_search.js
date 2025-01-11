
export async function sendDestinationRequest(start_date, end_date, budget, trip_type) {
    // Define the API URL
    const url = 'http://127.0.0.1:8000/suggest_destination/';

    // Create the data object to send
    const data = {
        start_date_input: start_date,
        end_date_input: end_date,
        budget_input: budget,
        trip_type_input: trip_type
    };

    // Try to send the POST request and handle the response
    try {
        console.log("Sending data:", JSON.stringify(data));
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

        // Assuming the server sends back a JSON response
        const jsonResponse = await response.json();
        console.log('Success:', jsonResponse);
        return jsonResponse;
    } catch (error) {
        console.error('Error:', error);
    }
}
