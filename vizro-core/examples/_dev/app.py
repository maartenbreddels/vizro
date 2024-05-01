"""Rough example used by developers."""

import vizro.models as vm
import vizro.plotly.express as px
from vizro import Vizro

iris = px.data.iris()
page_home = vm.Page(
    title="Homepage",
    description="Vizro demo app for studying gapminder data",
    layout=vm.Layout(grid=[[0], [1], [2]], col_gap="80px", row_gap="80px", row_min_height="372px"),
    components=[
        vm.Container(
            title="Group 1",
            layout=vm.Layout(grid=[[0, 1, 2, 3]], col_gap="40px", row_gap="40px"),
            components=[
                vm.Card(
                    text="""
                       ![](assets/images/icons/hypotheses.svg#icon-top)
            
                       ### Variable Analysis
            
                       Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut 
                       labore et dolore magna aliquyam erat, sed diam voluptua.
            
                       ![](assets/images/screens/page-1.png#screen-img)
                   """,
                    href="/page-1",
                ),
                vm.Card(
                    text="""
               ![](assets/images/icons/hypotheses.svg#icon-top)

               ### Relationship Analysis

               Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut 
               labore et dolore magna aliquyam erat, sed diam voluptua.

               ![](assets/images/screens/page-2.png#screen-img)
           """,
                    href="/page-2",
                ),
                vm.Card(
                    text="""
                   ![](assets/images/icons/collections.svg#icon-top)

                   ### Continent Summary

                   Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut 
                   labore et dolore magna aliquyam erat, sed diam voluptua.

                   ![](assets/images/screens/page-3.png#screen-img)
               """,
                    href="/page-3",
                ),
                vm.Card(
                    text="""
                    ![](assets/images/icons/collections.svg#icon-top)
                
                    ### Continent Summary
                
                    Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut 
                    labore et dolore magna aliquyam erat, sed diam voluptua.
                
                    ![](assets/images/screens/page-3.png#screen-img)
                """,
                    href="/page-4",
                ),
            ],
        ),
        vm.Container(
            title="Group 2",
            layout=vm.Layout(grid=[[0, 1, -1, -1]], col_gap="40px", row_gap="40px"),
            components=[
                vm.Card(
                    text="""
                   ![](assets/images/icons/features.svg#icon-top)

                   ### Benchmark Analysis

                   Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut 
                   labore et dolore magna aliquyam erat, sed diam voluptua.

                   ![](assets/images/screens/page-4.png#screen-img)
               """,
                    href="/page-4",
                ),
                vm.Card(
                    text="""
               ![](assets/images/icons/hypotheses.svg#icon-top)

               ### Other Analysis

               Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut 
               labore et dolore magna aliquyam erat, sed diam voluptua.

               ![](assets/images/screens/page-1.png#screen-img)
           """,
                    href="/page-5",
                ),
            ],
        ),
        vm.Container(
            title="Group 3",
            layout=vm.Layout(grid=[[0, 1, 2, -1]], col_gap="40px", row_gap="40px"),
            components=[
                vm.Card(
                    text="""
    ![](assets/images/icons/hypotheses.svg#icon-top)

    ### Variable Analysis

    Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut 
    labore et dolore magna aliquyam erat, sed diam voluptua.

    ![](assets/images/screens/page-1.png#screen-img)
""",
                    href="/page-1",
                ),
                vm.Card(
                    text="""
        ![](assets/images/icons/hypotheses.svg#icon-top)

        ### Relationship Analysis

        Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut 
        labore et dolore magna aliquyam erat, sed diam voluptua.

        ![](assets/images/screens/page-2.png#screen-img)
    """,
                    href="/page-2",
                ),
                vm.Card(
                    text="""
            ![](assets/images/icons/collections.svg#icon-top)

            ### Continent Summary

           Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut 
            labore et dolore magna aliquyam erat, sed diam voluptua.

            ![](assets/images/screens/page-3.png#screen-img)
        """,
                    href="/page-3",
                ),
            ],
        ),
    ],
)

page_one = vm.Page(title="Page 1", components=[vm.Card(text="""Placeholder""")])
dashboard = vm.Dashboard(pages=[page_home, page_one], title="Demo")

if __name__ == "__main__":
    Vizro().build(dashboard).run()
