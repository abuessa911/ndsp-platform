(function () {
    "use strict";

    var VERSION = "NDSP_MOBILE_UNIFIED_V93";
    var STYLE_ID = "ndsp-mobile-unified-v93-style";

    var drawer = null;
    var menuOpen = null;
    var closeButton = null;
    var closeButtonSecond = null;
    var backdrop = null;

    var selectedFrame = "weekly";
    var mutationObserver = null;

    var frameDefinitions = [
        { value: "15m", labelAr: "15 دقيقة", labelEn: "15M" },
        { value: "1h", labelAr: "ساعة", labelEn: "1H" },
        { value: "4h", labelAr: "4 ساعات", labelEn: "4H" },
        { value: "daily", labelAr: "يومي", labelEn: "DAILY" },
        { value: "weekly", labelAr: "أسبوعي", labelEn: "WEEKLY" },
        { value: "monthly", labelAr: "شهري", labelEn: "MONTHLY" }
    ];

    var css = String.raw`
        :root {
            --ndsp-v93-gold: #d4af37;
            --ndsp-v93-gold-soft: #f1d579;
            --ndsp-v93-bg: #070705;
            --ndsp-v93-panel: #0d0d0a;
            --ndsp-v93-border: rgba(212, 175, 55, 0.34);
            --ndsp-v93-overlay: rgba(0, 0, 0, 0.72);
        }

        html.ndsp-v93-menu-open,
        body.ndsp-v93-menu-open {
            overflow: hidden !important;
            overscroll-behavior: none !important;
        }

        #drawer.drawer {
            position: fixed !important;
            inset: 0 !important;
            z-index: 2147483000 !important;

            display: block !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;

            background: transparent !important;
            transition:
                opacity 180ms ease,
                visibility 180ms ease !important;
        }

        #drawer.drawer[data-ndsp-v93-open="true"] {
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }

        #drawer.drawer .drawerBackdrop {
            position: absolute !important;
            inset: 0 !important;
            z-index: 1 !important;

            display: block !important;
            width: 100% !important;
            height: 100% !important;

            padding: 0 !important;
            margin: 0 !important;
            border: 0 !important;
            border-radius: 0 !important;

            background: var(--ndsp-v93-overlay) !important;
            backdrop-filter: blur(2px) !important;
            -webkit-backdrop-filter: blur(2px) !important;

            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;

            transition: opacity 180ms ease !important;
        }

        #drawer.drawer[data-ndsp-v93-open="true"] .drawerBackdrop {
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }

        #drawer.drawer .drawerPanel {
            position: absolute !important;
            top: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            left: auto !important;
            z-index: 2 !important;

            display: flex !important;
            flex-direction: column !important;

            width: min(88vw, 370px) !important;
            max-width: 370px !important;
            min-width: 280px !important;
            height: 100% !important;
            min-height: 100dvh !important;

            margin: 0 !important;
            padding:
                calc(18px + env(safe-area-inset-top))
                18px
                calc(24px + env(safe-area-inset-bottom)) !important;

            overflow-x: hidden !important;
            overflow-y: auto !important;

            border: 0 !important;
            border-left: 1px solid var(--ndsp-v93-border) !important;
            border-radius: 0 !important;

            background:
                radial-gradient(
                    circle at top right,
                    rgba(212, 175, 55, 0.12),
                    transparent 34%
                ),
                linear-gradient(
                    180deg,
                    #11110d 0%,
                    var(--ndsp-v93-panel) 100%
                ) !important;

            color: #f5f0de !important;
            box-shadow: -24px 0 60px rgba(0, 0, 0, 0.58) !important;

            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;

            transform: translateX(105%) !important;
            transition: transform 220ms ease !important;
        }

        html[dir="ltr"] #drawer.drawer .drawerPanel {
            right: auto !important;
            left: 0 !important;

            border-left: 0 !important;
            border-right: 1px solid var(--ndsp-v93-border) !important;

            box-shadow: 24px 0 60px rgba(0, 0, 0, 0.58) !important;
            transform: translateX(-105%) !important;
        }

        #drawer.drawer[data-ndsp-v93-open="true"] .drawerPanel {
            transform: translateX(0) !important;
        }

        #drawer.drawer .drawerPanel > .cardHead {
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            gap: 14px !important;

            flex: 0 0 auto !important;

            margin: 0 0 18px !important;
            padding: 0 0 16px !important;

            border-bottom: 1px solid var(--ndsp-v93-border) !important;
        }

        #drawer.drawer .drawerPanel > .cardHead b {
            display: block !important;
            color: var(--ndsp-v93-gold-soft) !important;
            font-size: 1.2rem !important;
            letter-spacing: 0.12em !important;
        }

        #drawer.drawer .drawerPanel > .cardHead p {
            margin: 5px 0 0 !important;
            color: rgba(245, 240, 222, 0.7) !important;
            font-size: 0.78rem !important;
            line-height: 1.6 !important;
        }

        #drawerClose2 {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;

            width: 42px !important;
            height: 42px !important;
            min-width: 42px !important;

            padding: 0 !important;
            margin: 0 !important;

            border: 1px solid var(--ndsp-v93-border) !important;
            border-radius: 12px !important;

            background: rgba(212, 175, 55, 0.08) !important;
            color: var(--ndsp-v93-gold-soft) !important;

            font-size: 1.55rem !important;
            line-height: 1 !important;
        }

        #drawer.drawer .drawerLinks {
            display: grid !important;
            grid-template-columns: 1fr !important;
            gap: 8px !important;

            flex: 1 1 auto !important;
            align-content: start !important;
        }

        #drawer.drawer .drawerLinks a {
            display: flex !important;
            align-items: center !important;

            min-height: 48px !important;
            width: 100% !important;

            padding: 12px 14px !important;
            margin: 0 !important;

            border: 1px solid rgba(212, 175, 55, 0.16) !important;
            border-radius: 13px !important;

            background: rgba(255, 255, 255, 0.018) !important;
            color: #eee6ce !important;

            text-decoration: none !important;
            line-height: 1.5 !important;
        }

        #drawer.drawer .drawerLinks a:hover,
        #drawer.drawer .drawerLinks a:focus-visible,
        #drawer.drawer .drawerLinks a.active {
            border-color: rgba(212, 175, 55, 0.58) !important;
            background: rgba(212, 175, 55, 0.1) !important;
            color: var(--ndsp-v93-gold-soft) !important;
        }

        [data-ndsp-v93-timeframe-host="true"] {
            margin-top: 12px !important;
        }

        [data-ndsp-v93-timeframe-grid="true"] {
            display: grid !important;
            grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
            gap: 9px !important;
        }

        [data-ndsp-v93-timeframe-button="true"] {
            min-height: 44px !important;
            padding: 9px 8px !important;

            border: 1px solid rgba(212, 175, 55, 0.24) !important;
            border-radius: 11px !important;

            background: rgba(9, 9, 7, 0.92) !important;
            color: #cfc5a8 !important;

            font: 600 0.78rem/1.3 system-ui, sans-serif !important;
        }

        [data-ndsp-v93-timeframe-button="true"][aria-pressed="true"] {
            border-color: rgba(212, 175, 55, 0.75) !important;
            background: rgba(212, 175, 55, 0.16) !important;
            color: var(--ndsp-v93-gold-soft) !important;
            box-shadow: inset 0 0 0 1px rgba(212, 175, 55, 0.12) !important;
        }

        [data-ndsp-v93-original-timeframe="true"] {
            display: none !important;
        }

        @media (max-width: 900px) {
            html,
            body {
                width: 100% !important;
                max-width: 100% !important;
                min-width: 0 !important;

                visibility: visible !important;
                opacity: 1 !important;

                overflow-x: hidden !important;
            }

            body {
                display: block !important;
            }

            #app,
            #app > .appShell,
            .appShell,
            main.main {
                width: 100% !important;
                max-width: none !important;
                min-width: 0 !important;

                margin-left: 0 !important;
                margin-right: 0 !important;

                visibility: visible !important;
                opacity: 1 !important;

                transform: none !important;
                filter: none !important;
                clip: auto !important;
                clip-path: none !important;
            }

            #app {
                position: relative !important;
                z-index: 1 !important;
                min-height: 100dvh !important;
            }

            .appShell {
                position: relative !important;
                inset: auto !important;
            }

            .topbar {
                display: flex !important;
                align-items: center !important;
                justify-content: space-between !important;
                gap: 10px !important;

                min-height: 68px !important;
                padding:
                    calc(10px + env(safe-area-inset-top))
                    14px
                    10px !important;
            }

            .topbar .nav {
                display: none !important;
            }

            .topActions {
                display: flex !important;
                align-items: center !important;
                gap: 8px !important;
            }

            .mobileMenuBtn {
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
            }

            .main {
                padding-left: 12px !important;
                padding-right: 12px !important;
                padding-bottom: calc(94px + env(safe-area-inset-bottom)) !important;
            }

            .pageHero {
                padding-left: 0 !important;
                padding-right: 0 !important;
            }

            .grid,
            .grid2 {
                grid-template-columns: minmax(0, 1fr) !important;
            }

            .span2 {
                grid-column: auto !important;
            }

            .selectionSummary {
                position: relative !important;
                z-index: 2 !important;
            }

            .bottomNav {
                z-index: 1000 !important;
            }
        }

        @media (max-width: 430px) {
            #drawer.drawer .drawerPanel {
                width: min(91vw, 360px) !important;
                min-width: 0 !important;
            }

            [data-ndsp-v93-timeframe-grid="true"] {
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            #drawer.drawer,
            #drawer.drawer .drawerBackdrop,
            #drawer.drawer .drawerPanel {
                transition: none !important;
            }
        }
    `;

    function injectStyle() {
        var oldStyle = document.getElementById(STYLE_ID);

        if (oldStyle) {
            oldStyle.textContent = css;
            return;
        }

        var style = document.createElement("style");
        style.id = STYLE_ID;
        style.setAttribute("data-ndsp-runtime", VERSION);
        style.textContent = css;

        document.head.appendChild(style);
    }

    function removeLegacyRuntimeNodes() {
        var selectors = [
            '[data-ndsp-v86-mobile]',
            '[data-ndsp-v86-timeframe]',
            '[data-ndsp-v91-timeframe-wizard]',
            '[data-ndsp-mobile-black-drawer-v92]',
            '#ndsp-v86-timeframe-style',
            '#ndsp-v86-timeframe-control'
        ];

        selectors.forEach(function (selector) {
            document.querySelectorAll(selector).forEach(function (node) {
                if (
                    node.matches("script") ||
                    node.matches("link") ||
                    node.matches("style")
                ) {
                    node.remove();
                }
            });
        });

        document.documentElement.removeAttribute(
            "data-ndsp-v86-mobile-layout"
        );

        document.documentElement.removeAttribute(
            "data-ndsp-v91-timeframe-wizard"
        );
    }

    function findDrawerElements() {
        drawer = document.getElementById("drawer");
        menuOpen = document.getElementById("menuOpen");
        closeButton = document.getElementById("drawerClose");
        closeButtonSecond = document.getElementById("drawerClose2");

        backdrop = drawer
            ? drawer.querySelector(".drawerBackdrop")
            : null;
    }

    function drawerIsOpen() {
        return Boolean(
            drawer &&
            drawer.getAttribute("data-ndsp-v93-open") === "true"
        );
    }

    function openDrawer() {
        findDrawerElements();

        if (!drawer) {
            return;
        }

        drawer.setAttribute("data-ndsp-v93-open", "true");
        drawer.setAttribute("aria-hidden", "false");
        drawer.removeAttribute("inert");

        document.documentElement.classList.add("ndsp-v93-menu-open");
        document.body.classList.add("ndsp-v93-menu-open");

        if (menuOpen) {
            menuOpen.setAttribute("aria-expanded", "true");
        }

        window.setTimeout(function () {
            if (closeButtonSecond) {
                closeButtonSecond.focus({
                    preventScroll: true
                });
            }
        }, 20);
    }

    function closeDrawer(options) {
        options = options || {};

        findDrawerElements();

        if (!drawer) {
            return;
        }

        drawer.setAttribute("data-ndsp-v93-open", "false");
        drawer.setAttribute("aria-hidden", "true");
        drawer.setAttribute("inert", "");

        [
            "ndsp-open",
            "open",
            "is-open",
            "active",
            "show"
        ].forEach(function (className) {
            drawer.classList.remove(className);
        });

        drawer.removeAttribute("data-open");

        document.documentElement.classList.remove(
            "ndsp-v93-menu-open"
        );

        document.body.classList.remove(
            "ndsp-v93-menu-open",
            "ndsp-drawer-open",
            "drawer-open",
            "menu-open",
            "nav-open"
        );

        if (menuOpen) {
            menuOpen.setAttribute("aria-expanded", "false");
        }

        if (options.restoreFocus && menuOpen) {
            menuOpen.focus({
                preventScroll: true
            });
        }
    }

    function toggleDrawer() {
        if (drawerIsOpen()) {
            closeDrawer({
                restoreFocus: true
            });
        } else {
            openDrawer();
        }
    }

    function bindDrawer() {
        findDrawerElements();

        if (!drawer) {
            return;
        }

        drawer.dataset.ndspV93Bound = "true";
        drawer.setAttribute("role", "dialog");
        drawer.setAttribute("aria-modal", "true");

        if (!drawer.hasAttribute("data-ndsp-v93-open")) {
            closeDrawer();
        }

        if (menuOpen && menuOpen.dataset.ndspV93Bound !== "true") {
            menuOpen.dataset.ndspV93Bound = "true";
            menuOpen.setAttribute("aria-controls", "drawer");
            menuOpen.setAttribute("aria-expanded", "false");

            menuOpen.addEventListener(
                "click",
                function (event) {
                    event.preventDefault();
                    event.stopPropagation();
                    event.stopImmediatePropagation();

                    toggleDrawer();
                },
                true
            );
        }

        [
            closeButton,
            closeButtonSecond,
            backdrop
        ].forEach(function (element) {
            if (!element || element.dataset.ndspV93Bound === "true") {
                return;
            }

            element.dataset.ndspV93Bound = "true";

            element.addEventListener(
                "click",
                function (event) {
                    event.preventDefault();
                    event.stopPropagation();
                    event.stopImmediatePropagation();

                    closeDrawer({
                        restoreFocus: true
                    });
                },
                true
            );
        });

        drawer.querySelectorAll(".drawerLinks a").forEach(function (link) {
            if (link.dataset.ndspV93Bound === "true") {
                return;
            }

            link.dataset.ndspV93Bound = "true";

            link.addEventListener("click", function () {
                closeDrawer();
            });
        });
    }

    function normalizeFrame(value) {
        var aliases = {
            "15min": "15m",
            "15minute": "15m",
            "15minutes": "15m",
            "60m": "1h",
            "hourly": "1h",
            "4hour": "4h",
            "4hours": "4h",
            "1d": "daily",
            "day": "daily",
            "1w": "weekly",
            "week": "weekly",
            "1mo": "monthly",
            "month": "monthly"
        };

        value = String(value || "")
            .trim()
            .toLowerCase();

        return aliases[value] || value;
    }

    function isSupportedFrame(value) {
        return frameDefinitions.some(function (frame) {
            return frame.value === value;
        });
    }

    function readSelectedFrame() {
        var params = new URLSearchParams(window.location.search);
        var fromQuery = normalizeFrame(params.get("timeframe"));

        if (isSupportedFrame(fromQuery)) {
            return fromQuery;
        }

        var fromDataset = normalizeFrame(
            document.documentElement.getAttribute(
                "data-ndsp-v93-selected-frame"
            ) ||
            document.documentElement.getAttribute(
                "data-ndsp-v91-selected-frame"
            ) ||
            document.documentElement.getAttribute(
                "data-ndsp-v86-selected-frame"
            )
        );

        if (isSupportedFrame(fromDataset)) {
            return fromDataset;
        }

        try {
            var stored = normalizeFrame(
                window.sessionStorage.getItem(
                    "ndsp_selected_timeframe"
                ) ||
                window.localStorage.getItem(
                    "ndsp_selected_timeframe"
                )
            );

            if (isSupportedFrame(stored)) {
                return stored;
            }
        } catch (error) {
            // Storage is optional.
        }

        var originalSelected = document.querySelector(
            '[data-timeframe].selected'
        );

        if (originalSelected) {
            var fromOriginal = normalizeFrame(
                originalSelected.getAttribute("data-timeframe")
            );

            if (isSupportedFrame(fromOriginal)) {
                return fromOriginal;
            }
        }

        return "weekly";
    }

    function persistSelectedFrame(frame) {
        selectedFrame = normalizeFrame(frame);

        document.documentElement.setAttribute(
            "data-ndsp-v93-selected-frame",
            selectedFrame
        );

        document.documentElement.setAttribute(
            "data-ndsp-v86-selected-frame",
            selectedFrame
        );

        document.documentElement.setAttribute(
            "data-ndsp-v91-selected-frame",
            selectedFrame
        );

        try {
            window.sessionStorage.setItem(
                "ndsp_selected_timeframe",
                selectedFrame
            );

            window.localStorage.setItem(
                "ndsp_selected_timeframe",
                selectedFrame
            );
        } catch (error) {
            // Storage is optional.
        }
    }

    function updateSummaryFrame(frame) {
        var summary = document.querySelector(".selectionSummary");

        if (!summary) {
            return;
        }

        var tokens = Array.from(
            summary.querySelectorAll(".summaryTokens .token")
        );

        var knownFrames = [
            "15m",
            "1h",
            "4h",
            "daily",
            "weekly",
            "monthly",
            "15 دقيقة",
            "ساعة",
            "4 ساعات",
            "يومي",
            "أسبوعي",
            "شهري"
        ];

        var target = tokens.find(function (token) {
            return knownFrames.indexOf(
                String(token.textContent || "").trim()
            ) !== -1;
        });

        if (target) {
            target.textContent = frame;
        }
    }

    function markFrameButtons(frame) {
        document.querySelectorAll(
            '[data-ndsp-v93-timeframe-button="true"]'
        ).forEach(function (button) {
            var active =
                button.getAttribute("data-frame") === frame;

            button.setAttribute(
                "aria-pressed",
                active ? "true" : "false"
            );
        });
    }

    function selectFrame(frame, options) {
        options = options || {};
        frame = normalizeFrame(frame);

        if (!isSupportedFrame(frame)) {
            return;
        }

        persistSelectedFrame(frame);
        markFrameButtons(frame);
        updateSummaryFrame(frame);

        var originalButton = document.querySelector(
            '[data-timeframe="' +
            CSS.escape(frame) +
            '"]'
        );

        if (
            originalButton &&
            options.triggerNative !== false &&
            !originalButton.classList.contains("selected")
        ) {
            originalButton.click();
        }

        try {
            window.dispatchEvent(
                new CustomEvent("ndsp:timeframe-change", {
                    detail: {
                        timeframe: frame,
                        source: VERSION
                    }
                })
            );
        } catch (error) {
            // CustomEvent support is non-critical.
        }

        if (
            options.reloadForExtended &&
            (frame === "15m" || frame === "monthly")
        ) {
            var url = new URL(window.location.href);
            url.searchParams.set("timeframe", frame);
            url.searchParams.set("v", "93");
            url.searchParams.set(
                "ts",
                String(Date.now())
            );

            window.location.assign(url.toString());
            return;
        }

        var currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set("timeframe", frame);

        window.history.replaceState(
            null,
            "",
            currentUrl.toString()
        );
    }

    function buildTimeframeWizard() {
        var originalGroups = Array.from(
            document.querySelectorAll(
                '.segmented [data-timeframe]'
            )
        ).map(function (button) {
            return button.closest(".segmented");
        }).filter(Boolean);

        var originalGroup = originalGroups[0];

        if (!originalGroup) {
            return;
        }

        originalGroup.setAttribute(
            "data-ndsp-v93-original-timeframe",
            "true"
        );

        var oldHosts = document.querySelectorAll(
            '[data-ndsp-v91-timeframe-wizard="true"],' +
            '[data-ndsp-v93-timeframe-host="true"]'
        );

        oldHosts.forEach(function (node) {
            node.remove();
        });

        var host = document.createElement("div");
        host.setAttribute(
            "data-ndsp-v93-timeframe-host",
            "true"
        );

        var grid = document.createElement("div");
        grid.setAttribute(
            "data-ndsp-v93-timeframe-grid",
            "true"
        );

        grid.setAttribute("role", "group");
        grid.setAttribute(
            "aria-label",
            document.documentElement.dir === "ltr"
                ? "Select timeframe"
                : "اختر الفريم"
        );

        frameDefinitions.forEach(function (definition) {
            var button = document.createElement("button");

            button.type = "button";
            button.setAttribute(
                "data-ndsp-v93-timeframe-button",
                "true"
            );

            button.setAttribute(
                "data-frame",
                definition.value
            );

            button.setAttribute("aria-pressed", "false");

            button.textContent =
                document.documentElement.dir === "ltr"
                    ? definition.labelEn
                    : definition.labelAr;

            button.addEventListener("click", function () {
                selectFrame(definition.value, {
                    triggerNative: true,
                    reloadForExtended: true
                });
            });

            grid.appendChild(button);
        });

        host.appendChild(grid);
        originalGroup.insertAdjacentElement(
            "afterend",
            host
        );

        selectedFrame = readSelectedFrame();
        persistSelectedFrame(selectedFrame);
        markFrameButtons(selectedFrame);
        updateSummaryFrame(selectedFrame);
    }

    function bindGlobalEvents() {
        if (document.documentElement.dataset.ndspV93GlobalBound === "true") {
            return;
        }

        document.documentElement.dataset.ndspV93GlobalBound = "true";

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && drawerIsOpen()) {
                event.preventDefault();

                closeDrawer({
                    restoreFocus: true
                });
            }
        });

        window.addEventListener("pageshow", function () {
            closeDrawer();
            bindDrawer();
            buildTimeframeWizard();
        });

        window.addEventListener("resize", function () {
            if (
                window.innerWidth > 900 &&
                drawerIsOpen()
            ) {
                closeDrawer();
            }
        });
    }

    function installObserver() {
        if (mutationObserver) {
            return;
        }

        try {
            mutationObserver = new MutationObserver(function () {
                bindDrawer();

                if (
                    !document.querySelector(
                        '[data-ndsp-v93-timeframe-host="true"]'
                    )
                ) {
                    buildTimeframeWizard();
                }
            });

            mutationObserver.observe(document.documentElement, {
                childList: true,
                subtree: true
            });
        } catch (error) {
            // MutationObserver is a resilience enhancement.
        }
    }

    function optionalAuditMode() {
        var params = new URLSearchParams(window.location.search);

        if (params.get("ndsp_menu_test") === "1") {
            window.setTimeout(openDrawer, 500);
        }
    }

    function boot() {
        injectStyle();
        removeLegacyRuntimeNodes();

        document.documentElement.setAttribute(
            "data-ndsp-mobile-runtime",
            VERSION
        );

        closeDrawer();
        bindDrawer();
        buildTimeframeWizard();
        bindGlobalEvents();
        installObserver();
        optionalAuditMode();

        window.setTimeout(function () {
            bindDrawer();
            buildTimeframeWizard();
        }, 250);

        window.setTimeout(function () {
            bindDrawer();
        }, 1200);
    }

    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            boot,
            { once: true }
        );
    } else {
        boot();
    }
})();
