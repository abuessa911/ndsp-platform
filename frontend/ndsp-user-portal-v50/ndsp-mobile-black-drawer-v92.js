(function () {
    "use strict";

    var boundDrawer = null;
    var observer = null;

    var openClasses = [
        "ndsp-open",
        "open",
        "is-open",
        "active",
        "show"
    ];

    function getDrawer() {
        return document.getElementById("drawer");
    }

    function getOpenButton() {
        return document.getElementById("menuOpen");
    }

    function isExplicitlyOpen(drawer) {
        if (!drawer) return false;

        if (drawer.getAttribute("aria-hidden") === "false") return true;
        if (drawer.getAttribute("data-open") === "true") return true;

        return openClasses.some(function (className) {
            return drawer.classList.contains(className);
        });
    }

    function openDrawer() {
        var drawer = getDrawer();
        if (!drawer) return;

        drawer.classList.add("ndsp-open");
        drawer.setAttribute("aria-hidden", "false");
        drawer.setAttribute("data-open", "true");

        document.body.classList.add("ndsp-drawer-open");
    }

    function closeDrawer() {
        var drawer = getDrawer();
        if (!drawer) return;

        openClasses.forEach(function (className) {
            drawer.classList.remove(className);
        });

        drawer.setAttribute("aria-hidden", "true");
        drawer.setAttribute("data-open", "false");

        document.body.classList.remove(
            "ndsp-drawer-open",
            "drawer-open",
            "menu-open",
            "nav-open"
        );
    }

    function bindDrawer() {
        var drawer = getDrawer();
        if (!drawer) return;

        if (boundDrawer === drawer && drawer.dataset.ndspV92Bound === "true") {
            return;
        }

        boundDrawer = drawer;
        drawer.dataset.ndspV92Bound = "true";

        /*
         * A drawer with no explicit state must start closed.
         */
        if (!isExplicitlyOpen(drawer)) {
            closeDrawer();
        }

        var openButton = getOpenButton();

        if (openButton && openButton.dataset.ndspV92Bound !== "true") {
            openButton.dataset.ndspV92Bound = "true";

            openButton.addEventListener("click", function () {
                /*
                 * Run after the original handler so this remains compatible
                 * with the existing portal implementation.
                 */
                window.setTimeout(openDrawer, 0);
            });
        }

        [
            document.getElementById("drawerClose"),
            document.getElementById("drawerClose2")
        ].forEach(function (button) {
            if (!button || button.dataset.ndspV92Bound === "true") return;

            button.dataset.ndspV92Bound = "true";
            button.addEventListener("click", closeDrawer);
        });

        var backdrop = drawer.querySelector(".drawerBackdrop");

        if (backdrop && backdrop.dataset.ndspV92Bound !== "true") {
            backdrop.dataset.ndspV92Bound = "true";
            backdrop.addEventListener("click", closeDrawer);
        }
    }

    function boot() {
        bindDrawer();

        window.setTimeout(bindDrawer, 100);
        window.setTimeout(bindDrawer, 500);
        window.setTimeout(bindDrawer, 1500);

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                closeDrawer();
            }
        });

        window.addEventListener("pageshow", function () {
            var drawer = getDrawer();

            if (drawer && !isExplicitlyOpen(drawer)) {
                closeDrawer();
            }

            bindDrawer();
        });

        try {
            observer = new MutationObserver(function () {
                bindDrawer();
            });

            observer.observe(document.documentElement, {
                childList: true,
                subtree: true
            });
        } catch (error) {
            /*
             * MutationObserver is only a resilience enhancement.
             */
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot, {
            once: true
        });
    } else {
        boot();
    }
})();
