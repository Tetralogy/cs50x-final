import './sortables/index.js';
import { initializeSortableLists } from './sortables/initializeSortableLists.js';
import { toggleDropzones } from './sortables/dropzones.js';
import { throttle } from './throttle.js';
//todo import './tooltips/index.js';

function initialize() {
    console.log("initialize");
    initializeSortableLists();
    toggleDropzones();

    console.log('App initialized.');
}
const throttledInitialize = throttle(initialize, 1000);
htmx.onLoad(throttledInitialize);