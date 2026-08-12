(() => {
  "use strict";

  const root = document.documentElement;

  function normalize(value) {
    return String(value || "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function detectPlatform() {
    const ua =
      String(
        navigator.userAgent || ""
      ).toLowerCase();

    let platform = "";

    try {
      platform = String(
        navigator.userAgentData?.platform ||
        navigator.platform ||
        ""
      ).toLowerCase();
    } catch (_) {}

    let os = "generic";

    if (
      /iphone|ipad|ipod/.test(ua) ||
      (
        /mac/.test(platform) &&
        Number(navigator.maxTouchPoints || 0) > 1
      )
    ) {
      os = "ios";
    } else if (/android/.test(ua)) {
      os = "android";
    } else if (
      /win/.test(platform) ||
      /windows/.test(ua)
    ) {
      os = "windows";
    } else if (
      /mac/.test(platform) ||
      /macintosh/.test(ua)
    ) {
      os = "macos";
    } else if (
      /linux/.test(platform) ||
      /linux/.test(ua)
    ) {
      os = "linux";
    }

    root.dataset.ndspOs = os;

    const coarse =
      window.matchMedia?.(
        "(pointer: coarse)"
      ).matches === true;

    root.dataset.ndspPointer =
      coarse ? "coarse" : "fine";

    const dpr =
      Math.max(
        1,
        Math.min(
          3,
          Number(
            window.devicePixelRatio || 1
          )
        )
      );

    root.dataset.ndspDpr =
      String(dpr);

    root.style.setProperty(
      "--ndsp-runtime-dpr",
      String(dpr)
    );
  }

  function findLeafByPhrases(phrases) {
    const elements =
      document.querySelectorAll(
        "body *"
      );

    for (const element of elements) {
      if (element.children.length > 0) {
        continue;
      }

      const text =
        normalize(
          element.textContent
        );

      if (!text) {
        continue;
      }

      if (
        phrases.some(
          phrase =>
            text === phrase ||
            text.includes(phrase)
        )
      ) {
        const rect =
          element.getBoundingClientRect();

        if (
          rect.width > 0 &&
          rect.height > 0
        ) {
          return element;
        }
      }
    }

    return null;
  }

  function commonAncestor(elements) {
    if (!elements.length) {
      return null;
    }

    let ancestor =
      elements[0];

    while (
      ancestor &&
      ancestor !== document.body
    ) {
      const containsAll =
        elements.every(
          element =>
            ancestor.contains(element)
        );

      if (containsAll) {
        return ancestor;
      }

      ancestor =
        ancestor.parentElement;
    }

    return null;
  }

  function directChildOf(
    ancestor,
    element
  ) {
    let current =
      element;

    while (
      current &&
      current.parentElement !== ancestor
    ) {
      current =
        current.parentElement;
    }

    return current &&
      current.parentElement === ancestor
        ? current
        : null;
  }

  function governCoreAuthority() {
    if (
      document.querySelector(
        "[data-ndsp-core-authority]"
      )
    ) {
      return;
    }

    const targets = [
      {
        key: "core",
        phrases: ["CORE"]
      },
      {
        key: "direction",
        phrases: [
          "الاتجاه الرسمي"
        ]
      },
      {
        key: "governed",
        phrases: [
          "معتمد حوكمياً",
          "معتمد حوكميًا",
          "معتمد حوكميا"
        ]
      },
      {
        key: "evidence",
        phrases: [
          "أدلة قابلة للتحقق",
          "ادلة قابلة للتحقق"
        ]
      }
    ];

    const matches =
      targets.map(target => ({
        ...target,
        element:
          findLeafByPhrases(
            target.phrases
          )
      }));

    if (
      matches.some(
        match => !match.element
      )
    ) {
      return;
    }

    const ancestor =
      commonAncestor(
        matches.map(
          match => match.element
        )
      );

    if (
      !ancestor ||
      ancestor === document.body ||
      ancestor === document.documentElement
    ) {
      return;
    }

    const rect =
      ancestor.getBoundingClientRect();

    if (
      rect.width <= 0 ||
      rect.height <= 0 ||
      rect.height >
        window.innerHeight * .75
    ) {
      return;
    }

    const directItems =
      matches.map(match => ({
        ...match,
        item:
          directChildOf(
            ancestor,
            match.element
          )
      }));

    if (
      directItems.some(
        item => !item.item
      )
    ) {
      return;
    }

    const uniqueItems =
      new Set(
        directItems.map(
          item => item.item
        )
      );

    if (uniqueItems.size !== 4) {
      return;
    }

    ancestor.setAttribute(
      "data-ndsp-core-authority",
      "true"
    );

    directItems.forEach(item => {
      item.item.setAttribute(
        "data-ndsp-core-item",
        item.key
      );

      item.element.setAttribute(
        "data-ndsp-core-text",
        item.key
      );
    });
  }

  function governContainers() {
    const main =
      document.querySelector(
        "main"
      );

    if (
      main &&
      !main.hasAttribute(
        "data-ndsp-container-root"
      )
    ) {
      main.setAttribute(
        "data-ndsp-container-root",
        "true"
      );
    }
  }

  function initialize() {
    detectPlatform();
    governContainers();
    governCoreAuthority();
  }

  if (
    document.readyState === "loading"
  ) {
    document.addEventListener(
      "DOMContentLoaded",
      initialize,
      { once: true }
    );
  } else {
    initialize();
  }

  window.addEventListener(
    "load",
    () => {
      governCoreAuthority();
    },
    { once: true }
  );
})();
