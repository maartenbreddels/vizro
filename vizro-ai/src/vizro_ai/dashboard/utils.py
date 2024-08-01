"""Helper Functions For Vizro AI dashboard."""

from dataclasses import dataclass, field
from typing import Any, Dict

import pandas as pd
import tqdm.std as tsd
import vizro.models as vm


@dataclass
class DfMetadata:
    """Dataclass containing metadata content for a dataframe."""

    df_schema: Dict[str, str]
    df: pd.DataFrame
    df_sample: pd.DataFrame


@dataclass
class AllDfMetadata:
    """Dataclass containing metadata for all dataframes."""

    all_df_metadata: Dict[str, DfMetadata] = field(default_factory=dict)

    def get_schemas_and_samples(self) -> Dict[str, Dict[str, str]]:
        """Retrieve only the df_schema and df_sample for all datasets."""
        return {
            name: {"df_schema": metadata.df_schema, "df_sample": metadata.df_sample}
            for name, metadata in self.all_df_metadata.items()
        }

    def get_df(self, name: str) -> pd.DataFrame:
        """Retrieve the dataframe by name."""
        try:
            return self.all_df_metadata[name].df
        except KeyError:
            raise KeyError("Dataframe not found in metadata. Please ensure that the correct dataframe is provided.")

    def get_df_schema(self, name: str) -> Dict[str, str]:
        """Retrieve the schema of the dataframe by name."""
        return self.all_df_metadata[name].df_schema


@dataclass
class DashboardOutputs:
    """Dataclass containing all possible `VizroAI.dashboard()` output."""

    code: str
    dashboard: vm.Dashboard


def _execute_step(pbar: tsd.tqdm, description: str, value: Any) -> Any:
    pbar.update(1)
    pbar.set_description_str(description)
    return value


def _register_data(all_df_metadata: AllDfMetadata) -> vm.Dashboard:
    """Register the dashboard data in data manager."""
    from vizro.managers import data_manager

    for name, metadata in all_df_metadata.all_df_metadata.items():
        data_manager[name] = metadata.df


def _dashboard_code(dashboard: vm.Dashboard) -> str:
    """Generate dashboard code from dashboard object."""
    try:
        return dashboard.to_python()
    except AttributeError:
        return "Dashboard code generation is coming soon!"


import base64
from PIL import Image
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from langchain.schema import HumanMessage

def load_image(image_path):
    """
    Load an image from a local file path, convert it to base64,
    and return as a numpy array and base64 string.
    """
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    
    img = Image.open(image_path)
    return np.array(img), image_data

def get_image_data(**kwargs):
    """
    Load images and return a list of their base64-encoded data.
    
    :param kwargs: Should contain 'image_paths' key with a list of file paths
    :return: List of base64-encoded image data
    """
    image_paths = kwargs.get('image_paths', [])
    return [load_image(path)[1] for path in image_paths]

def create_image_subplot(fig, img_array, row, col, title=None):
    """Add an image as a subplot to the figure."""
    fig.add_trace(
        go.Image(z=img_array),
        row=row, col=col
    )
    if title:
        fig.update_xaxes(title_text=title, row=row, col=col)

def display_images(image_paths, titles=None, ncols=2):
    """Display multiple images in a grid layout."""
    n_images = len(image_paths)
    nrows = (n_images - 1) // ncols + 1

    fig = make_subplots(rows=nrows, cols=ncols, subplot_titles=titles)

    for i, path in enumerate(image_paths):
        img_array, _ = load_image(path)
        row = i // ncols + 1
        col = i % ncols + 1
        create_image_subplot(fig, img_array, row, col)

    fig.update_layout(
        showlegend=False,
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False)
    )

    fig.show()

def construct_message(images, question):
    """
    Construct a HumanMessage with a dynamic number of images.
    
    :param images: List of base64-encoded image data
    :param question: The question to ask about the images
    :return: HumanMessage object
    """
    content = [{"type": "text", "text": question}]
    for img_data in images:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{img_data}"}
        })
    return HumanMessage(content=content)

# Example usage
image_paths = [
    "/Users/lingyi_zhang/vizx/os/world data/page1.png",
    "/Users/lingyi_zhang/vizx/os/world data/page2.png",
]
titles = ["First Image", "Second Image"]
