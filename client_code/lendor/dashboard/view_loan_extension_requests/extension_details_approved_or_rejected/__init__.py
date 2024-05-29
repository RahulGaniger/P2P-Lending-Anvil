from ._anvil_designer import extension_details_approved_or_rejectedTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class extension_details_approved_or_rejected(extension_details_approved_or_rejectedTemplate):
  def __init__(self,selected_row, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.selected_row = selected_row
    self.name.text = f"{selected_row['borrower_full_name']}"
    self.loan.text = f"{selected_row['loan_amount']}"      
    self.exten_fee.text = f"{selected_row['extend_fee']}"
    self.extension_amount.text = f"{selected_row['extension_amount']}"
    self.total.text = f"{selected_row['total_extension_months']}"
    self.ra.text = f"{selected_row['final_repayment_amount']}"
    self.reason.text = f"{selected_row['reason']}"
    self.new_emi.text = f"{selected_row['new_emi']}"
    self.status = f"{selected_row['status']}"

    if self.status == "approved":
        self.label_7_copy.visible = True        
    elif self.status == "rejected":        
        self.reject.visible = True
    else:
        None

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('lendor.dashboard.view_loan_extension_requests.extension_details',  selected_row = self.selected_row)

  def button_1_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('lendor.dashboard')
