
            //        function initializeTooltips() {
            //            const tooltipTriggerList = [].slice.call(
            //                document.querySelectorAll('[data-bs-toggle="tooltip"]'),
            //            );
            //            tooltipTriggerList.map(function (tooltipTriggerEl) {
            //                return new bootstrap.Tooltip(tooltipTriggerEl);
            //            });
            //        }
            window.activeTooltip = null;
            console.log("tooltips.js loaded");
todo modularize tooltips
function clearAndInitializeTooltips() {
    // Dispose of any existing tooltips to prevent conflicts
    document
        .querySelectorAll('[data-bs-toggle="tooltip"]')
        .forEach((tooltipTriggerEl) => {
            const existingTooltip =
                bootstrap.Tooltip.getInstance(tooltipTriggerEl);
            if (existingTooltip) {
                console.log(`existingTooltip: ${existingTooltip}`);
                existingTooltip.dispose();
            }
        });

    // Use a slight delay to ensure HTMX updates have completed
    setTimeout(() => {
        const tooltipTriggerList = [].slice.call(
            document.querySelectorAll('[data-bs-toggle="tooltip"]'),
        );

        // Initialize tooltips with additional strict existence checks
        tooltipTriggerList.forEach((tooltipTriggerEl) => {
            if (
                tooltipTriggerEl &&
                document.body.contains(tooltipTriggerEl)
            ) {
                const tooltipInstance = new bootstrap.Tooltip(
                    tooltipTriggerEl,
                );

                tooltipTriggerEl.addEventListener(
                    "mouseenter",
                    function () {
                        // Hide any active tooltip before showing a new one
                        if (
                            window.activeTooltip &&
                            window.activeTooltip !== tooltipInstance &&
                            window.activeTooltip._element
                        ) {
                            window.activeTooltip.hide();
                        }

                        // Check if element and tooltip instance still exist before showing
                        if (
                            document.body.contains(
                                tooltipTriggerEl,
                            ) &&
                            tooltipInstance._element
                        ) {
                            window.activeTooltip = tooltipInstance;
                            window.activeTooltip.show();
                        }
                    },
                );

                tooltipTriggerEl.addEventListener(
                    "mouseleave",
                    function () {
                        // Hide tooltip if it’s still active and attached
                        if (
                            window.activeTooltip &&
                            window.activeTooltip._element
                        ) {
                            window.activeTooltip.hide();
                            window.activeTooltip = null;
                        }
                    },
                );
            }
        });
    }, 100); // Adjust delay as needed
}


 // Define the function to clear all tooltips
            // function clearTooltips() {
            //     const tooltipTriggerList = [].slice.call(
            //         document.querySelectorAll('[data-bs-toggle="tooltip"]'),
            //     );
            //     tooltipTriggerList.map(function (tooltipTriggerEl) {
            //         const tooltip =
            //             bootstrap.Tooltip.getInstance(tooltipTriggerEl);
            //         if (tooltip) {
            //             tooltip.dispose();
            //         }
            //     });
            //     document
            //         .querySelectorAll('div[role="tooltip"]')
            //         .forEach(function (tooltipDiv) {
            //             if (tooltipDiv) {
            //     tooltipDiv.remove();
            // }
            //         });
            // }

            // // Add event listeners to elements that should trigger the tooltip clearing
            // document
            //     .querySelectorAll("input, select, textarea, span, div, body")
            //     .forEach((element) => {
            //         element.addEventListener("click", function () {
            //             clearTooltips();
            //             //initializeTooltips();
            //         });
            //         element.addEventListener("drag", function () {
            //             clearTooltips();
            //             ////initializeTooltips();
            //         });
            //         element.addEventListener("drop", function () {
            //             //clearTooltips();
            //             //initializeTooltips();
            //         });
            //     });