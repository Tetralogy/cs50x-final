export function addedItem(evt, itemEl, newIndex, oldIndex, model, sortableElement) {
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
    }
    if ( //revert to original position if missing data
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
    //if moving between lists of the same type (task to task)
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
    } else //if moving between lists of different types (roomtype to room)
    {
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