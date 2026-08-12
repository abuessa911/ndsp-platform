import { criticalCapabilityBindings } from "./criticalCapabilityBindings";
import { CriticalCapabilityPanel } from "./CriticalCapabilityPanel";
import "./critical-capabilities.css";

export function CriticalCapabilitiesPage() {
  return (
    <main className="critical-capabilities-page">
      <header>
        <h1>Critical capabilities</h1>
        <p>
          Missing contracts remain visible and never fall back to mock data.
        </p>
      </header>
      <section className="critical-capabilities-grid">
        {criticalCapabilityBindings.map((binding) => (
          <CriticalCapabilityPanel
            key={binding.capabilityId}
            binding={binding}
          />
        ))}
      </section>
    </main>
  );
}
