from ._anvil_designer import ItemTemplate120Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate120(ItemTemplate120Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.image_1.role = 'circular-image'

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    selected_row = self.item
    print(f"Selected row status: {selected_row['status']}")
    open_form("lendor.dashboard.view_loan_foreclosure_Requests.foreclose_details", selected_row=selected_row)
    if selected_row['status'] == 'approved' or selected_row['status'] == 'rejected':
        open_form("lendor.dashboard.view_loan_foreclosure_Requests.foreclose_details_approved_and_rejected", selected_row=selected_row)
    else:
        # open_form("lendor_registration_form.dashboard.vlfr.foreclose_details")
       None
