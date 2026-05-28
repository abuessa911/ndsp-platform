import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import Checkout from "./pages/Checkout.jsx";
import AdminPlans from "./pages/AdminPlans.jsx";
import "./styles.css";

function useHashRoute() {
  const [route, setRoute] = useState(window.location.hash || "#/checkout");

  useEffect(() => {
    function onHashChange() {
      setRoute(window.location.hash || "#/checkout");
    }

    window.addEventListener("hashchange", onHashChange);
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  return route;
}

function App() {
  const route = useHashRoute();

  return (
    <>
      <nav className="top-nav">
        <a href="#/checkout">Checkout</a>
        <a href="#/admin/plans">Admin Plans</a>
      </nav>

      {route === "#/admin/plans" ? <AdminPlans /> : <Checkout />}
    </>
  );
}

createRoot(document.getElementById("root")).render(<App />);
