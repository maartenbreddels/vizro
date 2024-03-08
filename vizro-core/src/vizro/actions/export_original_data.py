from __future__ import annotations

from vizro.models.types import CapturedActionCallable
from typing import TYPE_CHECKING, Any, Callable, Dict, Literal, List, Optional
from dash import ctx, dcc, Output, State

from vizro.actions import filter_interaction
from vizro.actions._filter_action import _filter
from vizro.managers import data_manager, model_manager

if TYPE_CHECKING:
    from vizro.models import Page
    from vizro.models._table import Table

import importlib
from vizro.managers._model_manager import ModelID
import vizro.models as vm

from vizro.actions._callback_mapping._callback_mapping_utils import _get_inputs_of_filters, _get_inputs_of_figure_interactions
from vizro.actions._actions_utils import _get_filtered_data







class ExportDataClassAction(CapturedActionCallable):
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        # Fake initialization
        super().__init__(*args, **kwargs)

    def _post_init(self):
        self._page_id = model_manager._get_model_page_id(model_id=self._action_id)

        # Validate and calculate "targets"
        targets = self._kwargs.get("targets")
        if targets:
            for target in targets:
                if target not in model_manager:
                    raise ValueError(f"Component '{target}' does not exist on the page '{self._page_id}'.")
        else:
            targets = model_manager._get_page_model_ids_with_figure(page_id=self._page_id)
        self._kwargs["targets"] = self.targets = targets

        # Validate and calculate "file_format"
        file_format = self._kwargs.get("file_format", "csv")
        if file_format not in ["csv", "xlsx"]:
            raise ValueError(f'Unknown "file_format": {file_format}.' f' Known file formats: "csv", "xlsx".')
        if file_format == "xlsx":
            if importlib.util.find_spec("openpyxl") is None and importlib.util.find_spec("xlsxwriter") is None:
                raise ModuleNotFoundError(
                    "You must install either openpyxl or xlsxwriter to export to xlsx format."
                )
        self._kwargs["file_format"] = self.file_format = file_format

        # post initialization
        super().__init__(*self._args, **self._kwargs)

    @staticmethod
    def pure_function(
        targets: List[str],
        file_format: Literal["csv", "xlsx"] = "csv",
        **inputs: Dict[str, Any]
    ):
        data_frames = _get_filtered_data(
            targets=targets,
            ctds_filters=ctx.args_grouping["external"]["filters"],
            ctds_filter_interaction=ctx.args_grouping["external"]["filter_interaction"],
        )

        outputs = {}
        for target_id in targets:
            if file_format == "csv":
                writer = data_frames[target_id].to_csv
            elif file_format == "xlsx":
                writer = data_frames[target_id].to_excel

            outputs[f"download_dataframe_{target_id}"] = dcc.send_data_frame(
                writer=writer, filename=f"{target_id}.{file_format}", index=False
            )

        return outputs

    @property
    def inputs(self):
        # TODO: fetch inputs by function on a page
        # TODO: Do more refactoring: Take the _actions_info into account,

        page = model_manager[self._page_id]
        return {
            "filters": _get_inputs_of_filters(
                page=page,
                action_function=_filter.__wrapped__
            ),
            "filter_interaction": _get_inputs_of_figure_interactions(
                page=page,
                action_function=filter_interaction.__wrapped__
            ),
            # TODO: Try not to propagate this if theme_selector is overwritten and not the part of the page.
            "theme_selector": State("theme_selector", "checked"),
        }

    @property
    def outputs(self) -> Dict[str, Output]:
        """Gets mapping of relevant output target name and `Outputs` for `export_data` action."""
        return {
            f"download_dataframe_{target}": Output(
                component_id={"type": "download_dataframe", "action_id": self._action_id, "target_id": target},
                component_property="data",
            )
            for target in self.targets
        }

    @property
    def components(self):
        """Creates dcc.Downloads for target components of the `export_data` action."""
        return [
            dcc.Download(id={"type": "download_dataframe", "action_id": self._action_id, "target_id": target})
            for target in self.targets
        ]


# Alias for ExportDataClassAction
export_data_class_action = ExportDataClassAction
