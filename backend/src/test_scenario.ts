import { ScenarioConsumer } from './eventbus/consumers/ScenarioConsumer';

console.log("🟢 NDSP Scenario Engine is initializing...");
ScenarioConsumer.listenForDecisions();
