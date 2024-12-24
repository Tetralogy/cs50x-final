export function fetchBoolFromEndpoint(url, callback) {
    htmx.ajax('GET', url, {
        handler: function(xhr) {
            const responseText = xhr.responseText.trim(); // Trim to handle extra spaces or newlines
            const result = responseText === 'True'; // Convert to boolean
            callback(result);
        }
    });
}

// Usage example:
const endpointUrl = '/your-endpoint'; // Replace with your actual endpoint URL
fetchBoolFromEndpoint(endpointUrl, function(result) {
    if (result) {
        console.log('The response is True!');
    } else {
        console.log('The response is False!');
    }
});