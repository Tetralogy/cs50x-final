let isDragging = false;

export function getIsDragging() { console.log("getIsDragging: " + isDragging);
  return isDragging;
}

export function setIsDragging(value) {console.log("setIsDragging: " + isDragging);
  isDragging = value;
}

/* let isInSortable = false; // Tracks whether the item is over a sortable area

export function initializeDragDetection(sortableSelectors = []) {
  // Initialize SortableJS on the provided selectors
  sortableSelectors.forEach((selector) => {
    const element = document.querySelector(selector);
    if (element) {
      new Sortable(element, {
        group: 'shared',
        onMove: function () {
          isInSortable = true; // Dragging within a sortable area
          return true; // Allow movement
        }
      });
    } else {
      console.warn(`Element not found for selector: ${selector}`);
    }
  });

  // Add listeners for drag events
  document.addEventListener('dragenter', (event) => {
    if (!event.target.closest(sortableSelectors.join(','))) {
      isInSortable = false;
    }
  });

  document.addEventListener('dragleave', (event) => {
    if (!event.target.closest(sortableSelectors.join(','))) {
      console.log('Dragged item left a non-sortable area');
    }
  });

  document.addEventListener('dragend', () => {
    isInSortable = false;
  });
}

// Getter for isInSortable
export function getIsInSortable() {
  return isInSortable;
} 
#todo: drag outside of sortable detection
 */