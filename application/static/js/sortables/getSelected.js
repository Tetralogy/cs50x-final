import Sortable from 'sortablejs/modular/sortable.complete.esm.js';
import { throttle } from "../throttle.js";

const throttledHtmxGetActiveRoomEntryId = throttle(htmxGetActiveRoomEntryId);
const throttledGetRoomCoverEntryId = throttle((parent_entry_id) => GetRoomCoverEntryId(parent_entry_id));
const throttledGetGroundFloorEntryId = throttle(GetGroundFloorEntryId);

export function getSelectedActive(evt, parent_entry_id) {
    if (evt.item.dataset.model === "Room") {
        throttledHtmxGetActiveRoomEntryId();
    }
    if (evt.item.dataset.model === "Photo") {
        throttledGetRoomCoverEntryId(parent_entry_id);
    }
    if (evt.item.dataset.model === "Floor") {
        throttledGetGroundFloorEntryId();
    }
}

/* function htmxGetActiveRoomEntryId() { 
    const response = htmx.ajax("GET", "/get_active_room_entry_id", { // [ ] this is broken in htmx 2.0.3 try testing again with 2.0.4 when available
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

function GetRoomCoverEntryId(parent_entry_id) {
    fetch(`/room_cover_photo_entry_id/${parent_entry_id}`)
        .then(response => response.text())
        .then(responseText => {
            console.log("Response from server:", responseText);
            const elId = `Photolist-${responseText.trim()}`;
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

function GetGroundFloorEntryId() {
    fetch(`/get_ground_floor_entry_id`)
        .then(response => response.text())
        .then(responseText => {
            console.log("Response from server:", responseText);
            const elId = `Floorlist-${responseText.trim()}`;
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

export function singleSelect(itemEl, evt) { console.log("singleSelect triggered");
    evt.from.querySelectorAll(`.selected`).forEach(item => {
        if (item.id != itemEl.id) {
            item.classList.remove("selected");
        }
    });
    //only allow one selected item at a time
    if (evt.items.length > 1) {
        Sortable.utils.deselect(evt.items[0]);
    }
}