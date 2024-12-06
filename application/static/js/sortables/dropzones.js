import { getIsDragging, setIsDragging } from "./isDragging.js";

export function updateDropzones(evt) {
    if (getIsDragging()) {
        toggleDropzones();
        console.log("getIsDragging() t: " + getIsDragging());
        const draggedItem = evt.dragged; // The item being dragged
        const targetItem = evt.related; // The item currently being hovered over
        console.log("targetItem?");
        if (targetItem) {
            console.log(
                `targetItem YES ${targetItem.dataset.name}`
            );
            // Find the nested dropzone within the hovered item
            const dropzone = targetItem.querySelector(".dropzone");
            const sublists = targetItem.querySelector(".sublists");
            if (draggedItem) {
                console.log("draggedItem: " + draggedItem);
                // Show the nested dropzone if it exists
                if (dropzone) {
                    // Get the bounding boxes of both the dragged item and target item
                    const draggedRect = evt.draggedRect;
                    const targetRect = evt.relatedRect;
                    console.log(
                        `targetRect ${targetRect.top} draggedRect ${draggedRect.top}`
                    );
                    // Check for intersection
                    const isIntersecting = draggedRect.right > targetRect.left &&
                        draggedRect.left < targetRect.right &&
                        draggedRect.bottom > targetRect.top &&
                        draggedRect.top < targetRect.bottom;
                    if (isIntersecting) {
                        console.log(
                            `Intersecting with: ${targetItem.id}`
                        );
                        // You can add any visual effect here, like highlighting
                        dropzone.classList.add("hover");
                        console.log("add .hover");
                    } else {
                        dropzone.classList.remove("hover");
                        console.log("remove .hover");
                    }
                }
            }
        } else {
            console.log("targetItem NO");
        }
    } else {
        console.log("getIsDragging() f: " + getIsDragging());
        toggleDropzones(getIsDragging());
    }
}

export function toggleDropzones() {
    console.log("toggleDropzones");
    const allDropzones = document.querySelectorAll(".dropzone");
    allDropzones.forEach((dropzone) => {
        const accordionButton = dropzone.parentElement.querySelector(
            dropzone.dataset.accordion_button
        );
        const sublists = document.getElementById(
            dropzone.dataset.sublists_div
        );
        if (sublists) {
            if (sublists.childElementCount > 0 ||
                dropzone.childElementCount > 0) {
                dropzone.classList.add("d-none"); // hide dropzone
                sublists.classList.remove("d-none"); // show sublists
                accordionButton.classList.remove("d-none"); // show accordion
                if (accordionButton.ariaExpanded === "false") {
                    accordionButton.click();
                    console.log(
                        `accordionButton.ariaExpanded: ${accordionButton.ariaExpanded}`
                    );
                }
            } else {
                accordionButton.classList.add("d-none");
                sublists.classList.add("d-none");
                if (getIsDragging()) {
                    dropzone.classList.remove("d-none");
                } else {
                    dropzone.classList.add("d-none");
                }
            }
        }

        dropzone.classList.remove("hover");
    });
}

