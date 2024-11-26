(() => {
/* // Store Sortable instances
//window.sortableInstances = new Map();

function //cleanupSortables() {
    // Destroy all sortable instances
    //window.sortableInstances.forEach((instance, element) => {
        instance.destroy();
    });
    //window.sortableInstances.clear();
}

//if (!isDragging) {
    isDragging = false;
//}    
console.log('After check:', isDragging);


// observer.js
//export 
function observeRecursiveLists(callback) {
    const observer = new MutationObserver(callback);
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}
/* // main.js
import { observeRecursiveLists } from './observer.js';
import { initializeSortable } from './dragDrop.js'; */
/*


window.addEventListener('load', initialize);


// Initialize tooltips and sortable
//document.addEventListener("DOMContentLoaded", function () {
//    //initializeTooltips();    
//    initializeSortable();
//
//    console.log("DOMContentLoaded triggered");
//});
//window.addEventListener("load", initializeSortable);





window.sortableTimeoutId = null;
// Observe changes in the document #xxx: only works on the first load
//if (!window.observer) {
    window.observer = new MutationObserver((mutations) => { console.log("observer triggered");
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length > 0) {
                toggleDropzones();

                if (window.sortableTimeoutId) {
                    clearTimeout(window.sortableTimeoutId);
                    }
                window.sortableTimeoutId = setTimeout(() => {
                initializeSortable();
                window.sortableTimeoutId = null;
                }, 500);
            }
        });
    });
//}

// Start observing the document for changes
window.observer.observe(document.body, {
    childList: true,
    subtree: true
});

 */
//htmx.onLoad(initialize);
//htmx.onLoad(throttle(initialize, 1000));
//if (!isDragging) {
let isDragging = false;
//}  
const throttledInitialize = throttle(initialize, 1000);

htmx.onLoad(throttledInitialize);


function throttle(func, delay) {
    let lastCallTime = 0;
    let timeout;

    return function (...args) {
        const currentTime = Date.now();
        const remainingTime = delay - (currentTime - lastCallTime);

        if (remainingTime <= 0) {
            clearTimeout(timeout);
            lastCallTime = currentTime;
            func.apply(this, args);
        } else {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                lastCallTime = Date.now();
                func.apply(this, args);
            }, remainingTime);
        }
    };
}


function initialize() { console.log("initialize");
    initializeSortable();
    toggleDropzones();
    

    /* observeRecursiveLists(() => {
        console.log('New elements detected, re-initializing...');
        initializeSortable(); // Re-initialize for new elements.
        toggleDropzones();
        
    }); */

    console.log('App initialized.');
}
console.log("sortables.js loaded");



function toggleDropzones() { console.log("toggleDropzones");
    //setTimeout(() => {
    const allDropzones = document.querySelectorAll(".dropzone");
    allDropzones.forEach((dropzone) => {
        const accordionButton =
            dropzone.parentElement.querySelector(
                dropzone.dataset.accordion_button,
            );
        //console.log(`dropzone.dataset.sublists_div: ${dropzone.dataset.sublists_div} dropzone.dataset.name: ${dropzone.dataset.name}`);
        const sublists = document.getElementById(
            dropzone.dataset.sublists_div,
        );
        //console.log(`toggleDropzones $(sublists): ${sublists.dataset.name} dropzone: ${dropzone.dataset.name}`);
        if (sublists) {
            //console.log(`sublists.childElementCount: ${sublists.childElementCount}`);
            if (
                sublists.childElementCount > 0 ||
                dropzone.childElementCount > 0
            ) {
                //console.log("toggleDropzones children");
                dropzone.classList.add("d-none"); // hide dropzone
                sublists.classList.remove("d-none"); // show sublists
                accordionButton.classList.remove("d-none"); // show accordion
                if (accordionButton.ariaExpanded === "false") {
                    accordionButton.click();
                    console.log(
                        `accordionButton.ariaExpanded: ${accordionButton.ariaExpanded}`,
                    )
                    //console.log(`sublists withchild: ${sublists.dataset.name}`);
                }
            } else {
                //console.log(`not occupied: ${dropzone.dataset.name}`);
                accordionButton.classList.add("d-none");
                sublists.classList.add("d-none");
                if (isDragging) {
                    dropzone.classList.remove("d-none");
                } else {
                    dropzone.classList.add("d-none");
                }
            }
        }

        dropzone.classList.remove("hover");
    });
    //}, 100);
}



function updateDropzones(evt) {
    if (isDragging) {
        toggleDropzones(isDragging);
        console.log("isDragging t: " + isDragging);
        const draggedItem = evt.dragged; // The item being dragged
        const targetItem = evt.related; // The item currently being hovered over
        console.log("targetItem?");
        if (targetItem) {
            console.log(
                `targetItem YES ${targetItem.dataset.name}`,
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
                    //dropzone.getBoundingClientRect();
                    console.log(
                        `targetRect ${targetRect.top} draggedRect ${draggedRect.top}`,
                    );
                    // Check for intersection
                    const isIntersecting =
                        draggedRect.right > targetRect.left &&
                        draggedRect.left < targetRect.right &&
                        draggedRect.bottom > targetRect.top &&
                        draggedRect.top < targetRect.bottom;

                    if (isIntersecting) {
                        console.log(
                            `Intersecting with: ${targetItem.id}`,
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
        console.log("isDragging f: " + isDragging);
        toggleDropzones(isDragging);
    }
}



function initializeSortable() { console.log("initializeSortable triggered");
        // Clean up first
        //cleanupSortables();

    //setTimeout(() => {
    //() => {
    // fix for error Uncaught SyntaxError: redeclaration of const typeslist
    //console.log("htmx.onLoad triggered");
    const sortableElements = document.querySelectorAll(".sortable");
    const typeslist = document.querySelector(".typeslist");

    if (typeslist !== null) {
        const instance = new Sortable(typeslist, {
            group: {
                name: "typeslist",
                pull: "clone",
                put: false, // Do not allow items to be put into this list
            },
            animation: 150,
            sort: false,
            cursor: "move",
            multiDrag: true, // Enable multi-drag
            selectedClass: "selected", // The class applied to the selected items
            fallbackTolerance: 3, // So that we can select items on mobile
        });
        //window.sortableInstances.set(typeslist, instance);
    }

    //document.addEventListener("DOMContentLoaded", updateDropzones);
    //window.addEventListener("load", updateDropzones);

    sortableElements.forEach(function (sortableElement) {
        const model = sortableElement.dataset.model;
        //console.log("sortableElement: " + sortableElement);
        if (sortableElement !== null) {
            const instance = new Sortable(sortableElement, {
                //const sortlist = Sortable.create(sortableElement, {
                //const roomlist = document.getElementById("");
                //const roomsort = new Sortable(roomlist, {
                group: {
                    name: model, //can only move between lists of the same type
                    pull: true,
                    put: ["typeslist", model],
                },
                animation: 150,
                swapThreshold: 0.65,
                invertSwap: true,
                fallbackOnBody: true,
                //draggable: "li",
                multiDrag: true, // Enable multi-drag
                selectedClass: "selected", // The class applied to the selected items
                fallbackTolerance: 3, // So that we can select items on mobile
                // Prevent dragging on specific elements
                filter: ".htmx-indicator, .rename", //.listname, .accordion-header, .accordion-button, .accordion",
                ghostClass: "ghost",
                dragClass: "ghost-red",
                chosenClass: "ghost-red",
                //removeOnSpill: true,
                revertOnSpill: true, //needs to be revert to work with the confirm dialog
                onStart: function (evt) {
                    isDragging = true;
                    //clearAndInitializeTooltips();
                    console.log("onStart isDragging " + isDragging);
                    originalIndex = evt.oldIndex; // Store the original index
                    draggedItem = evt.item; // Store the dragged item reference
                    fromList = evt.from; // Store the from list reference
                },
                onMove: function (evt) {
                    console.log("onMove isDragging " + isDragging);
                    updateDropzones(evt);
                },

                //console.log("Moving:", evt.related); // Log the element being moved
                //return (
                //    evt.related.className.indexOf(
                //        "htmx-indicator",
                //    ) === -1
                //);
                //},
                onSelect: function (evt) {
                    const itemEl = evt.item;


                    console.log("onSelect evt.item " + evt.item.dataset.name);
                    console.log("onSelect evt.items " + evt.items);
                    console.log(evt.items.map(item => item.dataset.name));
                    console.log("onSelect evt.clones " + evt.clones);
                    console.log("onSelect evt.oldIndicies " + evt.oldIndicies);
                    console.log(evt.oldIndicies.map(oldIndex => oldIndex));
                    console.log("onSelect evt.newIndicies " + evt.newIndicies);
                    console.log(evt.newIndicies.map(newIndex => newIndex));
                    if (itemEl.dataset.model === "Room") {


                        document.querySelectorAll(`.selected`).forEach(item => {
                            if (item.id != itemEl.id) {
                                item.classList.remove("selected");
                            }
                        });
                        //only allow one selected item at a time
                        if (evt.items.length > 1) {
                            Sortable.utils.deselect(evt.items[0]);
                        }
                        if (itemEl.dataset.model === "Room") {
                            htmx.ajax(
                                "PUT",
                                `/home/room/${itemEl.dataset.item_id}/active`,
                                {
                                    swap: "none",
                                    target: itemEl,
                                },
                            );
                            console.log("PUT: select active room");
                        }
                    }
                    // Get the radio input element
                    //const radioInput = evt.item.querySelector(`#radio-${evt.item.dataset.id}`);
                    //console.log(`contains? ${document.body.contains(radioInput)}`); // Should log `true` if the element is part of the DOM
                    //
                    ////const radioInput = document.getElementById(`radio-${evt.item.dataset.id}`);
                    //// Set the checked property to true
                    //
                    //    document.querySelectorAll(`input[type="radio"][name="active_room"]`).forEach(radio => {
                    //        radio.checked = false;
                    //    });
                    //if (radioInput) {
                    //    //radioInput.focus();
                    //    radioInput.checked = true;
                    //    //radioInput.click();
                    //    //radioInput.dispatchEvent(new Event('change', { bubbles: true })); // Ensures event propagation
                    //    //radioInput.setAttribute('checked', 'checked');
                    //    console.log(radioInput.checked); // Should log `true` after setting
                    //} else {
                    //    console.error("Radio input element not found");
                    //}
                    //
                    //console.log(radioInput); // Check if the element is found
                    //                                document.querySelectorAll(`input[type="radio"]`).forEach(radio => {
                    //                                    console.log(`${radio.id} ${radio.checked}`);
                    //                                })
                },
                //                            onDeselect: function (evt) {
                //                                console.log("onDeselect evt.item " + evt.item.dataset.name);
                //                                                                // Get the radio input element
                //const radioInput = evt.item.querySelector(`#radio-${evt.item.dataset.id}`);
                ////const radioInput = document.getElementById(`radio-${evt.item.dataset.id}`);
                //// Set the checked property to true
                //if (radioInput) {
                //    //radioInput.focus();
                //    radioInput.checked = false;
                //    //radioInput.click();
                //    //radioInput.dispatchEvent(new Event('change', { bubbles: true })); // Ensures event propagation
                //    //radioInput.setAttribute('checked', 'checked');
                //    console.log(radioInput.checked); // Should log `true` after setting
                //} else {
                //    console.error("Radio input element not found");
                //}
                //console.log(radioInput); // Check if the element is found
                // },
                onSpill: function (/**Event*/ evt) {
                    //this.options.removeOnSpill = true;
                    evt.item; // The spilled item
                    //showDragOutsideIndicator(
                    //    evt.clientX,
                    //    evt.clientY,
                    //);
                    console.log("spill");
                    console.log(
                        "delete evt.item.dataset.id: " +
                        evt.item.dataset.id +
                        " evt.item.dataset.name: " +
                        evt.item.dataset.name,
                    );
                    if (
                        confirm(
                            "Are you sure you want to delete this item? " +
                            evt.item.dataset.name +
                            " This cannot be undone.",
                        )
                    ) {
                        htmx.ajax(
                            "DELETE",
                            "/delete/entry/" + evt.item.dataset.id,
                            {
                                values: {
                                    code: 200,
                                },
                                swap: "delete",
                                target: evt.item,
                            },
                            console.log(
                                "deleted ?" + evt.item.dataset.name,
                            ),
                        );
                    }
                    //hideDragOutsideIndicator();
                },
                onAdd: function (/**Event*/ evt) {
                    console.log("onAdd event triggered");

                    console.log(
                        "evt.items: " + evt.items
                    )
                    console.log(evt.items.map(item => item.dataset.name));
                    console.log("evt.items.length: " + evt.items.length);
                    console.table("evt.items: ", evt);
                    console.table("evt.oldIndicies: ", evt.oldIndicies);
                    console.table("evt.newIndicies: ", evt.newIndicies);

                    if (evt.items.length > 1) {
                        evt.items.forEach((item, index) => {
                            setTimeout(() => {
                                // Get the corresponding new and old indices
                                console.log("item: " + item);
                                console.log("foreach more than 1 item");
                                console.log("item.dataset.name: " + item.dataset.name);
                                const itemEl = item; // dragged HTMLElement
                                const newIndex = evt.newIndicies[index].index;
                                console.log("newIndex: " + newIndex);
                                const oldIndex = evt.oldIndicies[index].index;
                                console.log("oldIndex: " + oldIndex);
                                added(itemEl, newIndex, oldIndex);
                            }, index * 100); // Add a delay for each request
                        })
                    } else {
                        const itemEl = evt.item; // dragged HTMLElement
                        const newIndex = evt.newIndex;
                        const oldIndex = evt.oldIndex;
                        added(itemEl, newIndex, oldIndex);
                    }
                    function added(itemEl, newIndex, oldIndex) {
                        const addedNewEntry = itemEl.dataset.name;
                        const moved_entry_id = itemEl.dataset.id;

                        const originalParent = evt.from;
                        const list_id = sortableElement.dataset.list_id;
                        //moved_entry_id
                        const recieving_entry_id =
                            sortableElement.dataset.id;
                        console.log(
                            "moved_entry_id: " +
                            moved_entry_id +
                            " recieving_entry_id: " +
                            recieving_entry_id +
                            " list_id: " +
                            list_id,
                        );
                        console.log(
                            "itemEl.dataset.model: " +
                            itemEl.dataset.model +
                            " sortableElement.dataset.model: " +
                            model,
                        );
                        const isList =
                            sortableElement.dataset.isList === "true";
                        console.log(
                            "recieving sortableElement isList: " +
                            isList,
                        );
                        if (isList) {
                            console.log("isList: " + isList);
                            //originalParent.insertBefore(itemEl, originalParent.children[oldIndex]);
                            //return;
                        }
                        if (
                            !moved_entry_id ||
                            (!list_id && !recieving_entry_id)
                        ) {
                            console.log(
                                "missing moved_entry_id: " +
                                moved_entry_id +
                                " recieving_entry_id: " +
                                recieving_entry_id +
                                " list_id: " +
                                list_id +
                                " isList: " +
                                isList,
                            );
                            originalParent.insertBefore(
                                itemEl,
                                originalParent.children[oldIndex],
                            );
                            return;
                        }
                        console.log("list_id: " + list_id);

                        if (itemEl.dataset.model === model) {
                            htmx.ajax(
                                "PUT",
                                "/move_entry/" + moved_entry_id,
                                {
                                    values: {
                                        order_index: newIndex,
                                        list_id: list_id,
                                        recieving_entry_id:
                                            recieving_entry_id,
                                        is_list: isList,
                                    },
                                    target: itemEl,
                                    //swap: "outerHTML", // returns the new content
                                },
                            );
                            console.log("PUT");
                        } else {
                            console.log(
                                "POST" +
                                "addedNewEntry: " +
                                addedNewEntry +
                                "new index: " +
                                newIndex,
                            );
                            // Make an htmx AJAX request to the server to create a new room
                            htmx.ajax(
                                "POST",
                                "/create/" + model + "/" + list_id,
                                {
                                    values: {
                                        name: addedNewEntry,
                                        order_index: newIndex,
                                    },
                                    target: itemEl,
                                    swap: "outerHTML", // returns the new content
                                },
                            );
                        }
                    }
                    //const dropzone = evt.to.querySelector(
                    //    ".dropzone",
                    //)

                    //if (dropzone) {
                    //console.log("Found dropzone:", dropzone);
                    //} else {
                    //console.log("No dropzone found in target container.");
                    //}

                    //const sublists = evt.to.querySelector(".sublists");

                    //if (sublists) {
                    //console.log("Found sublists:", sublists);
                    //} else {
                    //console.log("No sublists found in target container.");
                    //}

                    //sublists.innerHTML = dropzone.innerHTML;
                    //dropzone.innerHTML = ""; // Clear original dropzone
                    console.log("isDragging onAdd: " + isDragging);
                    updateDropzones(evt)
                },
                //Disable sorting on the `end` event
                onEnd: function (evt) {
                    console.log("onEnd event triggered");
                    //this.option("disabled", true);
                    // Hide all dropzones when dragging ends
                    isDragging = false;
                    const dropzone = evt.item.parentElement; //from.querySelector(".dropzone");

                    if (dropzone) {
                        console.log("Found dropzone:", dropzone);
                    } else {
                        console.log(
                            "No dropzone found in target container.",
                        );
                    }

                    const sublists = document.getElementById(
                        dropzone.dataset.sublists_div,
                    );

                    if (sublists) {
                        console.log("Found sublists:", sublists);
                        sublists.appendChild(evt.item);
                    } else {
                        console.log(
                            "No sublists found in target container.",
                        );
                    }
                    evt.items.forEach(function (item) {
                        Sortable.utils.deselect(item)
                    });
                    //sublists.innerHTML = dropzone.innerHTML;
                    //dropzone.innerHTML = ""; // Clear original dropzone
                    console.log("isDragging onEnd: " + isDragging);
                    updateDropzones(evt);
                    //console.log("sortableElement:", sortableElement)
                },
            });
            // Listen for HTMX response errors
            document.body.addEventListener(
                "htmx:responseError",
                function (event) {
                    if (event.detail.xhr.status === 404) {
                        // Handle 404 error
                        console.log("404 Not Found error?");
                        draggedItem.classList.add(
                            "revert-animation",
                        ); //[ ] animation does not work
                        fromList.appendChild(draggedItem);
                        fromList.insertBefore(
                            draggedItem,
                            fromList.children[originalIndex],
                        );

                        return;
                    }
                },
            );
            // Re-enable sorting on the `htmx:afterSwap` event
            //    sortableElement.addEventListener(
            //        "htmx:afterOnLoad",
            //        function () {
            //            //console.log("htmx:afterOnLoad event triggered");
            //            //console.log("sortableElement:", sortableElement);
            //            sortlist.option("disabled", false);
            //            // check for focus events to let the user type
            //            document
            //                .querySelectorAll("input")
            //                .forEach((element) => {
            //                    element.addEventListener(
            //                        "focus",
            //                        function () {
            //                            console.log("focus");
            //                            sortlist.option(
            //                                "disabled",
            //                                true,
            //                            );
            //                        },
            //                    );
            //                    element.addEventListener(
            //                        "blur",
            //                        function () {
            //                            console.log("blur");
            //                            sortlist.option(
            //                                "disabled",
            //                                false,
            //                            );
            //                        },
            //                    );
            //                });
            //            //updateDropzones();
            //        },
            //    );

            // Function to show the indicator
            //   function showDragOutsideIndicator(x, y) {
            //       const indicator = document.getElementById(
            //           "drag-outside-indicator",
            //       );
            //       if (indicator !== null) {
            //           console.log("showDragOutsideIndicator", x, y);
            //           indicator.style.left = `${x}px`;
            //           indicator.style.top = `${y}px`;
            //           indicator.style.display = "block";
            //       }
            //   }

            //   // Function to hide the indicator
            //   function hideDragOutsideIndicator() {
            //       const indicator = document.getElementById(
            //           "drag-outside-indicator",
            //       );
            //       if (indicator !== null) {
            //           indicator.style.display = "none";
            //       }
            //   }

            //   // Add event listeners to track dragging outside the area

            //   sortableElements.forEach(function (area) {
            //       area.addEventListener("dragover", function (e) {
            //           const rect = area.getBoundingClientRect();

            //           //console.log("dragover" + rect);
            //           if (
            //               e.clientX < rect.left ||
            //               e.clientX > rect.right ||
            //               e.clientY < rect.top ||
            //               e.clientY > rect.bottom
            //           ) {
            //               showDragOutsideIndicator(
            //                   e.clientX,
            //                   e.clientY,
            //               );
            //           } else {
            //               hideDragOutsideIndicator();
            //           }
            //       });
            //   });

            //   document.addEventListener("drop", function () {
            //       hideDragOutsideIndicator();
            //   });

            //   document
            //       .querySelectorAll("input")
            //       .forEach((element) => {
            //           element.addEventListener("focus", function () {
            //               console.log("focus");
            //               sortlist.option("disabled", true);
            //           });
            //           element.addEventListener("blur", function () {
            //               console.log("blur");
            //               sortlist.option("disabled", false);
            //           });
            //       });
            //window.sortableInstances.set(sortableElement, instance);
        }
    });
    //}, 100);
}


// Re-initialize tooltips and sortable after content update
// document.addEventListener("htmx:afterSwap", function () {
//     //initializeTooltips()
//     //clearAndInitializeTooltips();
//     initializeSortable();
// });
})();