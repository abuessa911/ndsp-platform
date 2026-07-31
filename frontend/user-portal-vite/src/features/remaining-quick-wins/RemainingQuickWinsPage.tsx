import { remainingQuickWinBindings } from "./bindings";
import { RemainingQuickWinPanel } from "./RemainingQuickWinPanel";

export function RemainingQuickWinsPage() {
  return (
    <main>
      <h1>Remaining quick wins</h1>
      {remainingQuickWinBindings.map((binding) => (
        <RemainingQuickWinPanel
          key={binding.capabilityId}
          binding={binding}
        />
      ))}
    </main>
  );
}
