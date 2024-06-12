from ._anvil_designer import ItemTemplate109Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate109(ItemTemplate109Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    selcted_row=self.item
    open_form('admin.dashboard.reporting_and_analytical_modules.key_metrice.key_metricx_details',selected_row=selcted_row)
    

