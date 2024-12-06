import { throttle } from "../throttle.js";

const throttledHtmxGetActiveRoomEntryId = throttle(htmxGetActiveRoomEntryId);

export function getSelectedActiveRoom(evt) {
    if (evt.item.dataset.model === "Room") {
        throttledHtmxGetActiveRoomEntryId();
    }
}

/* function htmxGetActiveRoomEntryId() { 
    const response = htmx.ajax("GET", "/get_active_room_entry_id", { // [ ] this is broken in htmx 2.0.3
        //target: 'body',
        handler: function (responseText) {
            try {
                console.log("Retrieved room entry ID:", responseText);
                const elId = `Roomlist-${responseText}`;
                const element = document.getElementById(elId);

                if (element) {
                    element.classList.add("selected");
                } else {
                    console.error(`Element with ID ${elId} not found.`);
                }
            } catch (err) {
                console.error("Error handling the response:", err);
            }
        },
        errorHandler: function (xhr, error, message) {
            console.error("HTMX AJAX request failed:", error, message, xhr);
        }
    });
    console.log("Retrieved response:", response);
} */ 

function htmxGetActiveRoomEntryId() {
    fetch("/get_active_room_entry_id")
        .then(response => response.text())
        .then(responseText => {
            console.log("Response from server:", responseText);
            const elId = `Roomlist-${responseText.trim()}`;
            const element = document.getElementById(elId);
            if (element) {
                element.classList.add("selected");
            } else {
                console.error(`Element with ID ${elId} not found.`);
            }
        })
        .catch(error => {
            console.error("Fetch request failed:", error);
        });
}