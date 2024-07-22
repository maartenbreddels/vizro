import pytest
from vizro_ai.dashboard.response_models.dashboard import DashboardPlanner

try:
    from pydantic.v1 import ValidationError
except ImportError:  # pragma: no cov
    from pydantic import ValidationError


class TestDashboardPlanner:
    """Tests dashboard planner."""

    def test_dashboard_planner(self, page_plan):
        dashboard_plan = DashboardPlanner(
            title="Test Dashboard",
            pages=[page_plan],
        )
        assert dashboard_plan.pages[0].title == "Test Page"
        assert dashboard_plan.pages[0].components_plan[0].component_id == "card_1"
        assert dashboard_plan.pages[0].components_plan[0].component_type == "Card"
        assert dashboard_plan.pages[0].components_plan[0].component_description == "This is a card"
        assert dashboard_plan.pages[0].components_plan[0].page_id == "page_1"
        assert dashboard_plan.pages[0].components_plan[0].df_name == "N/A"
        assert dashboard_plan.pages[0].layout_plan is None
        assert dashboard_plan.pages[0].controls_plan == []
