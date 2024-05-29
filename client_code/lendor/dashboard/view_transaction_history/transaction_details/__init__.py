from ._anvil_designer import transaction_detailsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class transaction_details(transaction_detailsTemplate):
  def __init__(self,selected_row, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.label_3.text = selected_row['transaction_id']
    self.label_5.text = selected_row['user_email']
    # self.label_7.text = selected_row['wallet_id']
    self.label_9.text = selected_row['transaction_type']
    self.label_11.text = selected_row['amount']
    self.label_13.text = selected_row['transaction_time_stamp']
    self.label_15.text = selected_row['status']
    self.label_17.text = selected_row['receiver_email']

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('lendor.dashboard.view_transaction_history')
