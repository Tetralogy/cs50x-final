import 'bootstrap/dist/css/bootstrap.min.css';
//import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import '/application/static/css/main.css';
//import 'bootstrap/dist/js/bootstrap.min.js';
//import '@popperjs/core';
// Import Bootstrap's JS bundle which includes Popper
import * as bootstrap from 'bootstrap';
import './sortables/index.js';
import { initializeSortableLists } from './sortables/initializeSortableLists.js';
import { toggleDropzones } from './sortables/dropzones.js';
import { throttle } from './throttle.js';
//import { fetchBoolFromEndpoint } from './htmxfetchbool.js';
//[ ] import './tooltips/index.js';
//import { Modal } from 'bootstrap/dist/js/bootstrap.bundle.js';

// Make Bootstrap globally available
window.bootstrap = bootstrap;
function initialize() {
    console.log("initialize");

        // Verify Bootstrap is available globally
        //console.log('Bootstrap available:', !!window.bootstrap);
        window.bootstrap = bootstrap;


    initializeSortableLists();
    toggleDropzones();

    console.log('App initialized.');
}
const throttledInitialize = throttle(initialize, 1000);
htmx.onLoad(throttledInitialize);


