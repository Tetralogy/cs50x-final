import Sortable from 'sortablejs/modular/sortable.complete.esm.js';
import { getIsDragging, setIsDragging } from "./isDragging.js";
import { updateDropzones } from "./dropzones.js";
import { addedItem } from "./addedListItem.js";
import { getSelectedActive, singleSelect } from './getSelected.js';
import { tasktoPin } from './tasktoPin.js';

// Create a global map to track Sortable instances
const sortableInstances = new Map();

export function initializeSortableLists() {
    const sortableElements = document.querySelectorAll(".sortable");
    sortableElements.forEach(function (sortableElement) {
            // First, destroy any existing instance for this element
        if (sortableInstances.has(sortableElement)) {
                const existingInstance = sortableInstances.get(sortableElement);
                existingInstance.destroy();
            }
        if (sortableElement !== null) {
            const model = sortableElement.dataset.model;
            const parent_entry_id = sortableElement.dataset.parent_entry_id;
            let originalGhost = null;
            let sortableOptions = {
                group: {
                    name: model,
                    pull: true,
                    put: [model], //can only accept items from lists of the same type
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
                dragClass: "ghost-red", //[ ] test if this is needed
                chosenClass: "ghost-red",
                //removeOnSpill: true,
                revertOnSpill: true, //needs to be revert to work with the confirm dialog
                sort: true,
                onStart: function (evt) {
                    setIsDragging(true);
                    console.log("onStart isDragging " + getIsDragging());
                    //originalIndex = evt.oldIndex; // Store the original index
                    //draggedItem = evt.item; // Store the dragged item reference
                    //fromList = evt.from; // Store the from list reference
                },
                onMove: function (evt) {
                    console.log("onMove isDragging " + getIsDragging());
                    updateDropzones(evt);
                },
                onSelect: function (evt) {
                    const itemEl = evt.item;
                    /* console.log("onSelect evt.item " + evt.item.dataset.name);
                    console.log("onSelect evt.items " + evt.items);
                    console.log(evt.items.map(item => item.dataset.name));
                    console.log("onSelect evt.clones " + evt.clones);
                    console.log("onSelect evt.oldIndicies " + evt.oldIndicies);
                    console.log(evt.oldIndicies.map(oldIndex => oldIndex));
                    console.log("onSelect evt.newIndicies " + evt.newIndicies);
                    console.log(evt.newIndicies.map(newIndex => newIndex)); */
                    if (itemEl.dataset.model === "Room") {
                        singleSelect(itemEl, evt);
                        // update active room as current selected
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
                    else if (itemEl.dataset.model === "Photo") { console.log("onSelect Photo");
                        singleSelect(itemEl, evt);
                        if (
                            confirm(
                                "Are you sure you want to select this item? " +
                                evt.item.dataset.name +
                                " This cannot be undone.",
                            )
                        )
                        {
                        // update active cover photo as current selected
                        htmx.ajax(
                            "PUT",
                            `/set_room_cover_photo/${itemEl.dataset.item_id}`,
                            {
                                swap: "none",
                                target: itemEl,
                            },
                        );}
                    }
                },
                onDeselect: function (evt) {
                    getSelectedActive(evt, parent_entry_id);
                },
                onSpill: function (/**Event*/ evt) {
                    evt.item; // The spilled item
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
                },
                onChange: function (evt, originalEvent) {
                },
                onAdd: function (/**Event*/ evt) {
                    /* console.log("onAdd event triggered");
                    console.log("evt.items: " + evt.items)
                    console.log(evt.items.map(item => item.dataset.name));
                    console.log("evt.items.length: " + evt.items.length);
                    console.table("evt.items: ", evt);
                    console.table("evt.oldIndicies: ", evt.oldIndicies);
                    console.table("evt.newIndicies: ", evt.newIndicies); */
                    if (evt.items.length > 1) { //for multi-drag
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
                                addedItem(evt, itemEl, newIndex, oldIndex, model, sortableElement);
                            }, index * 100); // Add a delay for each request so it works
                        })
                    } else {
                        const itemEl = evt.item; // dragged HTMLElement
                        const newIndex = evt.newIndex;
                        const oldIndex = evt.oldIndex;
                        addedItem(evt, itemEl, newIndex, oldIndex, model, sortableElement);
                    }
                    //addedItem(evt, itemEl, newIndex, oldIndex, model, sortableElement);
                    console.log("isDragging onAdd: " + getIsDragging());
                    updateDropzones(evt);
                    getSelectedActive(evt, parent_entry_id);
                },
                onEnd: function (evt) {
                    console.log("onEnd event triggered");
                    if (originalGhost) {
                        originalGhost.remove();
                        originalGhost = null;
                        console.log("onEnd originalGhost: " + originalGhost);
                    }
                    // Hide all dropzones when dragging ends
                    setIsDragging(false);
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
                    console.log("isDragging onEnd: " + getIsDragging());
                    updateDropzones(evt);
                    getSelectedActive(evt, parent_entry_id);

                },
            };

            if (sortableElement.classList.contains("tasks")) {
            }
            else if (sortableElement.classList.contains("roomdefaults")) {
                console.log("roomdefaults");
                sortableOptions.group = {
                    name: "roomdefaults",
                    pull: "clone",
                    put: false, // Do not allow items to be put into this list
                };
                sortableOptions.revertOnSpill = false;
                sortableOptions.sort = false;

                console.log("sortableOptions.sort?: " + sortableOptions.sort);
            }
            else if (sortableElement.classList.contains("pingrid")) {
                sortableOptions.group = {
                    name: "pingrid",
                    pull: false,
                    put: "Task",
                };
                sortableOptions.animation = 0;
                sortableOptions.filter += ", .replaceableitem";
                sortableOptions.ghostClass = "static-ghost";
                //modify onStart for pingrid
                sortableOptions.onStart = (function (originalFunction) {
                    return function (evt) {
                        originalFunction(evt);
                        const original = evt.item;
                        originalGhost = original.cloneNode(true); // Clone the original item
                        originalGhost.classList.add('d-none'); // Add a class for styling
                        original.parentNode.insertBefore(originalGhost, original); // Insert the ghost before the original (swap in same position)
                    };
                })(sortableOptions.onStart);
                //modify onChange for pingrid
                sortableOptions.onChange = (function (originalFunction) {
                    return function (evt, originalEvent) {
                        if (evt.from !== evt.to) {
                            //console.log("onChange from other list");
                            evt.item.classList.add('static-ghost');
                            //console.dir(evt.to.children[evt.newIndex]);
                            evt.to.children[evt.newIndex].classList.add('none-ghost');
                        }
                    };
                })(sortableOptions.onChange);
                //modify onAdd for pingrid
                sortableOptions.onAdd = (function (originalFunction) {
                    return function (evt) {
                        document.querySelectorAll('.none-ghost').forEach(element => element.classList.remove('none-ghost'));
                        console.log(`onAdd evt.from: ${evt.from}, evt.to: ${evt.to}, evt.item: ${evt.item}`);
                        //originalFunction(evt); //continue with original function
                        if (evt.items.length > 1) { //for multi-drag
                            evt.items.forEach((item, index) => {
                                setTimeout(() => { 
                                    // Get the corresponding new and old indices
                                    console.log("item: " + item);
                                    console.log("foreach more than 1 item");
                                    console.log("item.dataset.name: " + item.dataset.name);
                                    const itemEl = item; // dragged HTMLElement
                                    const clonedNode = itemEl.cloneNode(true);
                                    console.log(`clonedNode: ${clonedNode}`);
                                    let newIndex = evt.newIndicies[index].index;
                                    console.log("newIndex: " + newIndex);
                                    const oldIndex = evt.oldIndicies[index].index;
                                    console.log("oldIndex: " + oldIndex);
                                    tasktoPin(evt, itemEl, newIndex, oldIndex, clonedNode);
                                    addedItem(evt, clonedNode, newIndex, oldIndex, model, sortableElement);
                                }, index * 100); // Add a delay for each request so it works
                            })
                        } else { 
                            const itemEl = evt.item; // dragged HTMLElement
                            const clonedNode = itemEl.cloneNode(true);
                            const oldIndex = evt.oldIndex;
                            let newIndex = evt.newIndex;
                            tasktoPin(evt, itemEl, newIndex, oldIndex, clonedNode);
                            console.log(`evt.items.length ${evt.items.length}`)
                            addedItem(evt, clonedNode, newIndex, oldIndex, model, sortableElement);
                        }
                        //addedItem(evt, itemEl, newIndex, oldIndex, model, sortableElement);
                        console.log("isDragging onAdd: " + getIsDragging());
                        updateDropzones(evt);
                        getSelectedActive(evt, parent_entry_id);
                    };
                })(sortableOptions.onAdd);
            }
            else if (sortableElement.classList.contains("rooms")) {
                sortableOptions.group.put.push('roomdefaults');
            }

            else if (sortableElement.classList.contains("floors")) { }


            
            const instance = new Sortable(sortableElement, sortableOptions);
            // Store the instance in the map
            sortableInstances.set(sortableElement, instance);
            
            //console.log("instance: " + instance);
            //console.dir(instance);
        }
    });
}


//[ ] cleanup unused code and comments