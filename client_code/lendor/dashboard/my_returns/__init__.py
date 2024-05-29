from ._anvil_designer import my_returnsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module

class my_returns(my_returnsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.create_simple_chart()

  def create_simple_chart(self):
    # Prepare data for a simple bar chart
    categories = ['A', 'B', 'C']
    values = [10, 20, 30]

    # Create bar chart trace
    trace = go.Bar(x=categories, y=values, marker_color=['blue', 'green', 'red'])

    # Create a layout
    layout = go.Layout(
      title='Simple Bar Chart',
      xaxis=dict(title='Category'),
      yaxis=dict(title='Value'),
      barmode='group'  # Use group mode to display bars side by side
    )

    # Create a figure
    fig = go.Figure(data=[trace], layout=layout)

    # Debugging: Print the figure to ensure it's created
    print(f"Created simple figure: {fig}")

    # Debugging: Check if plot_1 is a valid component
    if hasattr(self, 'plot_1'):
        print("plot_1 is a valid component")

    # Set the plot in the Plot component
    self.plot_1.data = fig

    # Debugging: Check if the plot is assigned correctly
    print(f"Assigned simple figure to plot_1: {self.plot_1.data}")
