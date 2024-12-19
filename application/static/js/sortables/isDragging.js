
let isDragging = false;

export function getIsDragging() { console.log("getIsDragging: " + isDragging);
  return isDragging;
}

export function setIsDragging(value) {console.log("setIsDragging: " + isDragging);
  isDragging = value;
}
