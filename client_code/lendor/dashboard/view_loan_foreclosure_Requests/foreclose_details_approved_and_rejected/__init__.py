from ._anvil_designer import foreclose_details_approved_and_rejectedTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class foreclose_details_approved_and_rejected(foreclose_details_approved_and_rejectedTemplate):
  def __init__(self, selected_row, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.selected_row = selected_row
    self.name.text = f"{selected_row['borrower_name']}"
    self.loan.text = f"{selected_row['loan_amount']}"
    self.interest_rate.text = f"{selected_row['interest_rate']}"
    self.foreclose_fee.text = f"{selected_row['foreclose_fee']}"
    self.foreclose_amount.text = f"{selected_row['foreclose_amount']}"
    self.total.text = f"{selected_row['paid_amount']}"
    self.oa.text = f"{selected_row['outstanding_amount']}"
    self.reason.text = f"{selected_row['reason']}"
    self.due_amount.text = f"{selected_row['total_due_amount']}"
    self.status = f"{selected_row['status']}"
    print(self.status)

    if self.status == "approved":
        self.label_7.visible = True        
    elif self.status == "rejected":        
        self.reject.visible = True
    else:
        None


  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor.dashboard.view_loan_foreclosure_Requests")

