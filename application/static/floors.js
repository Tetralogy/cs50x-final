document.addEventListener("htmx:load", function () {
    const types = document.getElementById("floor-types-container");

    new Sortable(types, {
        group: {
            name: "shared",
            pull: "clone",
            put: false, // Do not allow items to be put into this list
        },
        animation: 150,
        sort: false,
        cursor: "move",
    });

        const sortmap = document.getElementById("map-{{  current_user.active_home.active_floor.floor_id  }}");
        console.log('sortmap: ' + sortmap);
        new Sortable(sortmap, { 
            group: {
                name: "shared",
                pull: true, // Prevent pulling from this list
            },
            animation: 150,
            ghostClass: "blue-background-class",
            filter: ".htmx-indicator",
            removeOnSpill: true, // Enable plugin
            // Called when item is spilled
            onSpill: function (/**Event*/ evt) {
                evt.item; // The spilled item
                //FIXME: delete item from db
            },
            onAdd: function (/**Event*/ evt) {
                console.log("onAdd event triggered");
                var itemEl = evt.item; // dragged HTMLElement
                var addedRoomType = itemEl.textContent;
                var newIndex = evt.newIndex;
                console.log('addedRoomType: ' + addedRoomType + 'new index: ' + newIndex);

                // Make an htmx AJAX request to the server
                htmx.ajax("POST", "/home/map/room/add/{{ current_user.active_home.active_floor.floor_id }}", {
                    values: { added_room_type: addedRoomType, order: newIndex },
                    target: itemEl,
                    swap: "outerHTML", // returns the new content
                });
            },
            onEnd: function () {
                console.log("onEnd event triggered");
                var newOrder = Array.from(sortmap.children).map(
                    (li) => li.dataset.id,
                ); 
                console.log('newOrder: ' + newOrder);
                htmx.ajax("PUT", "/home/map/sort/{{ current_user.active_home.active_floor.floor_id }}", {
                    target: "#room-list-container",
                    swap: "innerHTML",
                    values: { list_order: newOrder },
                });
            },
        });
    });