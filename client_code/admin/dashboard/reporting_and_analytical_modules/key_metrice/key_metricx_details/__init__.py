from ._anvil_designer import key_metricx_detailsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class key_metricx_details(key_metricx_detailsTemplate):
  def __init__(self,selected_row, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.selected_row = selected_row
    # Any code you write here will run before the form opens.

    self.customer_id.text = f"{selected_row['customer_id']}"
    self.since.text = f"{selected_row['borrower_since']}"
    self.name.text = f"{selected_row['user_name']}"
    self.ascend.text = f"{selected_row['ascend_score']}"
    self.email.text = f"{selected_row['email_id']}"
    self.credit.text = f"{selected_row['credit_limit']}"
    self.mobile.text = f"{selected_row['mobile']}"
    # self.days_left.text = f"{selected_row['days_left']}"
    
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.reporting_and_analytical_modules.key_metrice')
