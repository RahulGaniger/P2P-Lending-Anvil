from ._anvil_designer import view_details_1_copyTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from ... import lendor_main_form_module as main_form_module
from .. import lendor_main_form_module as main_form_module
from datetime import datetime


class view_details_1_copy(view_details_1_copyTemplate):
  def __init__(self, selected_row=None, **properties):
    self.selected_row = selected_row
    self.init_components(**properties)

    if selected_row:
      self.display_loan_details(selected_row)

  def display_loan_details(self, selected_row):
    # Display loan details
    self.loan_id_label.text = f"{selected_row['borrower_full_name']}"
    self.loan_amount_label.text = f"{selected_row['loan_amount']}"
    self.interest_rate_label.text = f"{selected_row['interest_rate']}"
    self.tenure_label.text = f"{selected_row['tenure']}"
    borrower_loan_created_timestamp = selected_row["borrower_loan_created_timestamp"]
    date_of_apply = borrower_loan_created_timestamp.strftime("%Y-%m-%d")
    self.date_of_apply_label.text = f"{date_of_apply}"
    self.loan_updated_status_label.text = f"{selected_row['loan_updated_status']}"

  def button_1_click(self, **event_args):
    open_form("lendor.dashboard")

  def button_1_copy_click(self, **event_args):
    open_form("lendor.dashboard")

  def link_1_click(self, **event_args):
    # Pass the selected_row to payment_details_l form
    open_form(
      "lendor.dashboard.lender_view_loans.payment_details_l",
      selected_row=self.selected_row,
    )
