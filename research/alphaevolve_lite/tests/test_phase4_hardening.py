from __future__ import annotations

import unittest

from research.alphaevolve_lite.controller_batch_state import (
    parse_target_cell_schedule,
    target_cell_for_attempt,
)
from research.alphaevolve_lite.controller_sample_eval_policy import (
    compare_to_map_cell_elite,
    sample_eval_eligibility,
)
from research.alphaevolve_lite.mechanism_cards import normalize_mechanism_cards
from research.alphaevolve_lite.sample_eval_metrics import compare_search_sample_to_references


class TargetCellScheduleTests(unittest.TestCase):
    def test_forced_target_cell_schedule_cycles_exact_surface_and_intent(self) -> None:
        schedule = parse_target_cell_schedule(
            "portfolio/liquidity_weighted_sides,risk/liquidity_scaled_cap",
            available_surfaces={"signal", "ranking", "portfolio", "risk"},
        )

        first = target_cell_for_attempt(0, schedule)
        second = target_cell_for_attempt(1, schedule)
        third = target_cell_for_attempt(2, schedule)

        self.assertEqual(first.surface, "portfolio")
        self.assertEqual(first.intent, "liquidity_weighted_sides")
        self.assertEqual(first.cell_label, "portfolio:liquidity_weighted_sides")
        self.assertEqual(second.surface, "risk")
        self.assertEqual(second.intent, "liquidity_scaled_cap")
        self.assertEqual(third.surface, "portfolio")
        self.assertEqual(third.intent, "liquidity_weighted_sides")

    def test_forced_target_cell_schedule_rejects_unknown_intent_before_generation(self) -> None:
        with self.assertRaises(ValueError):
            parse_target_cell_schedule(
                "portfolio/industry_neutral_rank",
                available_surfaces={"signal", "ranking", "portfolio", "risk"},
            )


class SampleEvalEligibilityTests(unittest.TestCase):
    def _base_attempt(self) -> dict:
        return {
            "decision": "pass",
            "child_program_path": "attempt/child_program.py",
            "target_intent_match": True,
            "target_surface": "ranking",
            "patch_intent": "industry_neutral_rank",
            "hard_gates": {"no_forward_return_replacement": True},
            "vector_smoke_metrics": {
                "active_day_count": 60,
                "min_long_count_active_day": 8,
                "min_short_count_active_day": 8,
            },
            "behavior_delta_metrics": {
                "weight_max_abs_delta": 0.02,
                "weight_changed_fraction": 0.06,
                "ranked_signal_max_abs_delta": 2.0,
            },
            "controller_search_score": 1.0,
        }

    def test_occupied_map_cell_without_elite_comparison_is_not_sample_eval_eligible(self) -> None:
        attempt = self._base_attempt()
        attempt.update(
            {
                "map_cell_already_occupied": True,
                "map_cell_elite_program_id": "PROG-OLD",
            }
        )

        result = sample_eval_eligibility(attempt)

        self.assertFalse(result["sample_eval_eligible"])
        self.assertIn(
            "occupied_map_cell_without_elite_comparison",
            result["sample_eval_eligibility_reasons"],
        )

    def test_occupied_map_cell_must_beat_and_differ_from_elite(self) -> None:
        attempt = self._base_attempt()
        elite = {
            "program_id": "PROG-OLD",
            "controller_search_score": 0.5,
            "behavior_delta_metrics": {
                "weight_max_abs_delta": 0.01,
                "weight_changed_fraction": 0.02,
                "ranked_signal_max_abs_delta": 0.5,
            },
        }
        attempt.update(compare_to_map_cell_elite(attempt, elite))
        attempt["map_cell_already_occupied"] = True

        result = sample_eval_eligibility(attempt)

        self.assertTrue(result["sample_eval_eligible"])

    def test_known_bad_attempt017_family_is_not_a_hard_sample_eval_filter(self) -> None:
        attempt = self._base_attempt()
        attempt.update(
            {
                "target_surface": "signal",
                "patch_intent": "bounded_tanh_dampening",
            }
        )

        result = sample_eval_eligibility(attempt)

        self.assertTrue(result["sample_eval_eligible"])
        self.assertNotIn(
            "known_bad_attempt017_signal_dampening_family",
            result["sample_eval_eligibility_reasons"],
        )


class PriorSampleEquivalenceTests(unittest.TestCase):
    def test_detects_equivalent_prior_sample_summary(self) -> None:
        metrics = {
            "search_sample": {
                "annualized_return": 0.1,
                "sharpe": 1.2,
                "turnover": 0.3,
            }
        }
        prior = {
            "program_id": "PROG-PRIOR",
            "metrics": {
                "search_sample": {
                    "annualized_return": 0.1,
                    "sharpe": 1.2,
                    "turnover": 0.3,
                }
            },
        }

        result = compare_search_sample_to_references(
            metrics,
            [prior],
            tolerance=1e-12,
            metric_names=["annualized_return", "sharpe", "turnover"],
        )

        self.assertTrue(result["metric_equivalent_to_any_reference"])
        self.assertEqual(result["equivalent_reference_program_ids"], ["PROG-PRIOR"])


class MechanismCardValidationTests(unittest.TestCase):
    def test_rejects_loose_intent_and_loose_field_names(self) -> None:
        payload = {
            "cards": [
                {
                    "surface": "ranking",
                    "intent": "ranking",
                    "thesis": "loose card",
                    "required_data_fields": ["industry_code", "signal_raw"],
                }
            ]
        }

        with self.assertRaises(ValueError):
            normalize_mechanism_cards(payload)

    def test_accepts_exact_contract_fields_and_target_intent(self) -> None:
        payload = {
            "cards": [
                {
                    "surface": "ranking",
                    "intent": "industry_neutral_rank",
                    "thesis": "Rank within SIC groups using exact contract fields.",
                    "required_data_fields": ["CONTRACT.industry_primary", "signal"],
                }
            ]
        }

        result = normalize_mechanism_cards(payload)

        self.assertEqual(result["cards"][0]["intent"], "industry_neutral_rank")


if __name__ == "__main__":
    unittest.main()
