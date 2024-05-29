from ._anvil_designer import foreclose_detailsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class foreclose_details(foreclose_detailsTemplate):
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

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form("lendor.dashboard.view_loan_foreclosure_Requests")

    def approve_click(self, **event_args):
        """This method is called when the 'Approve' button is clicked"""      
        self.selected_row['status'] = 'approved'
        # Save changes to the table
        self.selected_row.update()
        Notification("Borrower will get notified").show()

        # Update status in the fin_foreclosure table
        self.update_foreclosure_status('approved')

        loan = app_tables.fin_loan_details.get(loan_id=self.selected_row['loan_id'])
        loan['loan_updated_status'] = "foreclosure"
        open_form("lendor.dashboard.view_loan_foreclosure_Requests")

    def decline_click(self, **event_args):
        """This method is called when the 'Decline' button is clicked"""
        self.selected_row['status'] = 'rejected'
        self.selected_row.update()
        self.update_foreclosure_status('rejected')
        Notification("Borrower will get notified").show()
        open_form("lendor.dashboard.view_loan_foreclosure_Requests")
      
    def update_foreclosure_status(self, new_status):
        """Update the status in the fin_foreclosure table"""
        foreclosure_row = app_tables.fin_foreclosure.get(loan_id=self.selected_row['loan_id'])
        if foreclosure_row is not None:
            foreclosure_row['status'] = new_status
            foreclosure_row.update()
