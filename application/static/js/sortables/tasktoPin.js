export function tasktoPin(evt, itemEl, newIndex, oldIndex, clonedNode) {
    console.log("tasktoPin event triggered");
                        //const itemEl = evt.item; // dragged HTMLElement
                        //const clonedNode = itemEl.cloneNode(true);
                        const originalParent = evt.from;
                        const newParent = evt.to;
                        //const oldIndex = evt.oldIndex;
                        //let newIndex = evt.newIndex;
                        //if from tasklist, replace target item with cloned item
                        let targetItem = evt.to.children[(newIndex + 1)]; // The item at the new index
                        console.log(`onAdd targetItem: ${targetItem.textContent}`);

                        /* if (targetItem.dataset.model === itemEl.dataset.model){
                            this.options.swap = false;
                        }else {
                            this.options.swap = true;
                        }console.log(`onAdd swap: ${this.options.swap}`); */

                        // if targetitem is a task, move itemEl to next empty index so it doesn't move other pins
                        while (targetItem.dataset.model === itemEl.dataset.model) { 
                            console.log(`onAdd modelmatch targetItem: ${targetItem.textContent}`);
                            if ((targetItem.dataset.item_id === itemEl.dataset.item_id) && (targetItem.dataset.model === itemEl.dataset.model)) {
                                break;
                            }
                            newIndex += 1;
                            targetItem = evt.to.children[(newIndex)];
                        }
                        if (originalParent !== newParent) { //if from other list
                            // check if dragged task matches a task already in gridtest
                            const matchingDuplicate = Array.from(newParent.children).filter((item) => {
                                return (item.dataset.task_id === itemEl.dataset.task_id);
                            });
                            if (matchingDuplicate.length > 1) {
                                matchingDuplicate.forEach((item) => { //remove the existing pin and accept clone in the new position
                                    let dupindex = Array.from(newParent.children).indexOf(item)
                                    if (dupindex !== newIndex) {
                                        newParent.insertBefore(targetItem, newParent.children[dupindex])
                                        item.remove();
                                    }
                                })
                            } else {
                                targetItem.remove(); //replace the blank
                            }
                        }

                        // behave like a cloned item and put dragged item back in original position after clone
                        newParent.insertBefore(clonedNode, newParent.children[newIndex])
                        originalParent.insertBefore(itemEl, originalParent.children[oldIndex]);
                    }