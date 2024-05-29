import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta
import anvil.server
import anvil.tables as tables
from anvil import DataGrid, alert, open_form
from ._anvil_designer import payment_details_view_loan_requestTemplate
class payment_details_view_loan_request(payment_details_view_loan_requestTemplate):
  def __init__(self, selected_row=None, entered_values=None, **properties):
    self.selected_row = selected_row
    self.init_components(**properties)

    if selected_row:
      self.load_payment_details(selected_row, entered_values)

  def load_payment_details(self, selected_row, entered_values):
    # Load previously entered values when form is initialized
    self.load_entered_values(entered_values)

    # Create an empty list to store payment details
    payment_details = []

    # Monthly interest rate
    monthly_interest_rate = (self.selected_row['interest_rate'] / 100) / 12

    # Extra payment amount (initialized with 0 for all months)
    extra_payment = 0

    # Calculate EMI (monthly installment)
    emi = (self.selected_row['loan_amount'] * monthly_interest_rate * ((1 + monthly_interest_rate) ** self.selected_row['tenure'])) / (
            ((1 + monthly_interest_rate) ** self.selected_row['tenure']) - 1)

    # Initialize the first beginning balance with the initial loan amount
    beginning_balance = self.selected_row['loan_amount']
    payment_date_placeholder = "Awaiting update"

    # Calculate payment details for each month up to the tenure
    for month in range(1, self.selected_row['tenure'] + 1):
      # Calculate interest amount for the month
      interest_amount = beginning_balance * monthly_interest_rate

      # Calculate principal amount for the month
      principal_amount = emi - interest_amount

      # Update ending balance for the current iteration
      ending_balance = beginning_balance - principal_amount

      # Add payment details to the list
      payment_details.append({
          'PaymentNumber': month,
          'PaymentDate': payment_date_placeholder,
          'ScheduledPayment': f"₹ {emi:.2f}",
          'Principal': f"₹ {principal_amount:.2f}",
          'Interest': f"₹ {interest_amount:.2f}",
          'BeginningBalance': f"₹ {beginning_balance:.2f}",
          'ExtraPayment': f"₹ {extra_payment:.2f}",  # Extra payment column
          'TotalPayment': f"₹ {emi + extra_payment:.2f}",  # Include extra payment in the total payment
          'EndingBalance': f"₹ {ending_balance:.2f}"
      })

      # Update beginning balance for the next iteration
      beginning_balance = ending_balance

    # Set the Data Grid's items property to the list of payment details
    self.repeating_panel_1.items = payment_details

  def load_entered_values(self, entered_values):
    if entered_values:
      # Load previously entered values into the form fields
      self.entered_loan_amount = entered_values.get('loan_amount', None)
      self.entered_tenure = entered_values.get('tenure', None)
      self.entered_payment_type = entered_values.get('payment_type', None)

  def button_1_click(self, **event_args):
    open_form('lendor.dashboard')

  def button_2_click(self, **event_args):
    # Pass the selected_row to view_details_1 form
    open_form('lendor.dashboard.view_borrower_loan_request.Borr_loan_request', selected_row=self.selected_row)
