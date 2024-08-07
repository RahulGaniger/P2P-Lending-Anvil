from ._anvil_designer import ItemTemplate156Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate156(ItemTemplate156Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.image_1.role = 'circular-image'

    # Any code you write here will run before the form opens.

  def ViewMoreDetails_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    selected_row = self.Customer_id_label.text
    open_form('admin.dashboard.customer_management.handles_customer_registration.lenders.view_profile_copy', selected_row)

