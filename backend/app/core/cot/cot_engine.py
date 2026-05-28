from __future__ import annotations

from app.core.market_positioning.cot_asset_mapper import resolve_cot_asset_mapping
from app.core.market_positioning.cot_contracts import (
    CotDirection,
    CotGroupResult,
    CotIntelligenceResult,
    CotSnapshot,
)


class CotIntelligenceEngine:
    def _direction_from_net(self, net: float, neutral_threshold: float = 0.0) -> CotDirection:
        if net > neutral_threshold:
            return CotDirection.BULLISH
        if net < -neutral_threshold:
            return CotDirection.BEARISH
        return CotDirection.NEUTRAL

    def _sum_group(self, snapshot: CotSnapshot, group_name: str, categories: tuple[str, ...]) -> CotGroupResult:
        wanted = set(categories)
        net = sum(pos.net for pos in snapshot.positions if pos.category in wanted)

        return CotGroupResult(
            group_name=group_name,
            categories=categories,
            net=float(net),
            direction=self._direction_from_net(float(net)),
        )

    def evaluate(self, snapshot: CotSnapshot) -> CotIntelligenceResult:
        mapping = resolve_cot_asset_mapping(snapshot.symbol)

        lm = self._sum_group(snapshot, "L&M", mapping.lm_categories)
        s = self._sum_group(snapshot, "S", mapping.s_categories)

        abs_lm = abs(lm.net)
        abs_s = abs(s.net)

        if abs_lm > abs_s:
            dominant_group = "L&M"
            dominant_direction = lm.direction
        elif abs_s > abs_lm:
            dominant_group = "S"
            dominant_direction = s.direction
        else:
            dominant_group = "BALANCED"
            dominant_direction = CotDirection.NEUTRAL

        if lm.direction == s.direction and lm.direction != CotDirection.NEUTRAL:
            alignment_state = "golden_alignment"
            confidence_effect = 1.0
        elif lm.direction != s.direction and lm.direction != CotDirection.NEUTRAL and s.direction != CotDirection.NEUTRAL:
            alignment_state = "participant_conflict"
            confidence_effect = -0.5
        else:
            alignment_state = "mixed_or_neutral"
            confidence_effect = 0.0

        notes = [
            "market_positioning is positioning context only.",
            "market_positioning does not produce direct execution.",
            f"Report family: {snapshot.report_family.value}.",
            f"Dominant group: {dominant_group}.",
        ]

        return CotIntelligenceResult(
            symbol=snapshot.symbol,
            report_date=snapshot.report_date,
            report_family=snapshot.report_family,
            lm=lm,
            s=s,
            dominant_group=dominant_group,
            dominant_direction=dominant_direction,
            alignment_state=alignment_state,
            confidence_effect=confidence_effect,
            context_only=True,
            execution_allowed=False,
            notes=notes,
            metadata={
                "source": snapshot.source,
                "asset_class": snapshot.metadata.get("asset_class"),
                "mapping_notes": mapping.notes,
            },
        )
