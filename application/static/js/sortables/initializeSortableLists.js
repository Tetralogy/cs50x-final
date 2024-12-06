import Sortable from 'sortablejs/modular/sortable.complete.esm.js';
import { getIsDragging, setIsDragging } from "./isDragging.js";
import { updateDropzones } from "./dropzones.js";
import { addedItem } from "./addedListItem.js";
import { getSelectedActiveRoom } from './getSelected.js';

export function initializeSortableLists() {
const sortableElements = document.querySelectorAll(".sortable");
sortableElements.forEach(function (sortableElement) {
if (sortableElement !== null) {
    const model = sortableElement.dataset.model;
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
            fallbackTolerance: 3, // So that we can select items on mobile #[ ] select doesn't work on mobile
            // Prevent dragging on specific elements
            filter: ".htmx-indicator, .rename", //.listname, .accordion-header, .accordion-button, .accordion",
            ghostClass: "ghost",
            dragClass: "ghost-red", //todo test if this is needed
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
            },
            onDeselect: function (evt) {
                getSelectedActiveRoom(evt);
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
                getSelectedActiveRoom(evt);
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
                getSelectedActiveRoom(evt);

            },
        };
        
       /*  // Listen for HTMX response errors
        document.body.addEventListener( //todo test if needed
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
        ); */


if (sortableElement.classList.contains("tasks")){
}
else if (sortableElement.classList.contains("roomdefaults")){console.log("roomdefaults");
    sortableOptions.group =  {
        name: "roomdefaults",
        pull: "clone",
        put: false, // Do not allow items to be put into this list
    };
    sortableOptions.revertOnSpill = false;
    sortableOptions.sort = false;
    
    console.log("sortableOptions.sort?: " + sortableOptions.sort);
}
else if (sortableElement.classList.contains("photogrid")){
    sortableOptions.group =  {
        name: "photogrid",
        pull: false,
        put: true,
    };
    sortableOptions.animation = 0;
    sortableOptions.filter.push(".replaceableitem");
    sortableOptions.ghostClass = "static-ghost";

    //modify onStart
    sortableOptions.onStart = (function(originalFunction) {
        return function(evt) {
            originalFunction(evt);
                const original = evt.item;
                originalGhost = original.cloneNode(true); // Clone the original item
                originalGhost.classList.add('d-none'); // Add a class for styling
                original.parentNode.insertBefore(originalGhost, original); // Insert the ghost before the original (swap in same position)
            };
        })(sortableOptions.onStart);
//modify onChange
sortableOptions.onChange = (function(originalFunction) {
    return function(evt, originalEvent) {
        if (evt.from !== evt.to) {
            console.log("onChange from other list");
            evt.item.classList.add('static-ghost');
            console.dir(evt.to.children[evt.newIndex]);
            evt.to.children[evt.newIndex].classList.add('none-ghost');
        }
    };
    })(sortableOptions.onChange);
//modify onAdd
sortableOptions.onAdd = (function(originalFunction) {
    return function(evt) {
        document.querySelectorAll('.none-ghost').forEach(element => element.classList.remove('none-ghost'));
        console.log(`onAdd evt.from: ${evt.from}, evt.to: ${evt.to}, evt.item: ${evt.item}`);
        const itemEl = evt.item; // dragged HTMLElement
        const clonedNode = evt.item.cloneNode(true);
        const originalParent = evt.from;
        const newParent = evt.to;
        const oldIndex = evt.oldIndex;
        let newIndex = evt.newIndex;
        //if from tasklist, replace target item with cloned item
        let targetItem = evt.to.children[(evt.newIndex + 1)]; // The item at the new index
        console.log(`onAdd targetItem: ${targetItem.textContent}`);

        /* if (targetItem.dataset.model === itemEl.dataset.model){
            this.options.swap = false;
        }else {
            this.options.swap = true;
        }console.log(`onAdd swap: ${this.options.swap}`); */

        // if targetitem is a task, move itemEl to next empty index
        while (targetItem.dataset.model === itemEl.dataset.model) {
            console.log(`onAdd modelmatch targetItem: ${targetItem.textContent}`);
            if ((targetItem.dataset.item_id === itemEl.dataset.item_id) && (targetItem.dataset.model === itemEl.dataset.model)) {
                break;
            }
            newIndex += 1;
            targetItem = evt.to.children[(newIndex)];
        }
        if (evt.from !== photoGrid) {
            // check if dragged item matches an item already in gridtest
            const matchingDuplicate = Array.from(newParent.children).filter((item) => {
                return (item.dataset.item_id === itemEl.dataset.item_id) && (item.dataset.model === itemEl.dataset.model);
            });
            if (matchingDuplicate.length > 1) {
                matchingDuplicate.forEach((item) => {
                    dupindex = Array.from(newParent.children).indexOf(item);
                    if (dupindex !== newIndex) {
                        newParent.insertBefore(targetItem, newParent.children[dupindex])
                        item.remove();
                    }
                })
            } else {
                targetItem.remove();
            }
        }
        // behave like a cloned item and put dragged item back in original position
        newParent.insertBefore(clonedNode, newParent.children[newIndex])
        originalParent.insertBefore(itemEl, originalParent.children[oldIndex]);
//bug 1: tweak and fix this to save pin marker lists on photos
        originalFunction(evt);
};
    })(sortableOptions.onAdd);
} 
else if (sortableElement.classList.contains("rooms")){
    sortableOptions.group.put.push('roomdefaults');
}

else if (sortableElement.classList.contains("floors")){}



    const instance = new Sortable(sortableElement, sortableOptions);
}
});
}
 //[ ] cleanup unused code and comments