from ._anvil_designer import view_borrower_loan_requestTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import lendor_main_form_module as main_form_module
from ....bank_users.main_form import main_form_module as main_module

class view_borrower_loan_request(view_borrower_loan_requestTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user_id=main_module.userId
    user_id = self.user_id
    self.email = main_module.email
    email = self.email
    
    
    #self.repeating_panel_2.items=app_tables.fin_loan_details.search(loan_updated_status="under process")

    loan_requests = app_tables.fin_loan_details.search(loan_updated_status="under process")

        # List to hold loan requests with additional details
    loan_requests_with_details = []

        # Loop through each loan request and append additional details
    for loan in loan_requests:

            borrower_profile = app_tables.fin_user_profile.get(customer_id=loan['borrower_customer_id'])
            if borrower_profile is not None:
                loan_requests_with_details.append({
                    'mobile': borrower_profile['mobile'],
                    'interest_rate': loan['interest_rate'],
                    'loan_amount': loan['loan_amount'],
                    'tenure': loan['tenure'],
                    'product_name': loan['product_name'],
                    'product_description': loan['product_description'],
                    'borrower_full_name': loan['borrower_full_name'],
                    'loan_id': loan['loan_id'],
                    'ascend_score': borrower_profile['ascend_value'],
                    'credit_limit': loan['credit_limit'],
                    'loan_updated_status': loan['loan_updated_status'],
                    'emi_payment_type': loan['emi_payment_type'],
                    'borrower_customer_id': loan['borrower_customer_id'],
                    'lender_accepted_timestamp':loan['lender_accepted_timestamp'],
                    'loan_disbursed_timestamp':loan['loan_disbursed_timestamp']
                     # 'borrower_customer_id': loan['borrower_customer_id']
                    # Add other details you want to include
                                                  })          

    
    self.repeating_panel_2.items = loan_requests_with_details
    anvil.server.call('transfer_user_profile_to_loan_details', email,user_id) 

  
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor.dashboard")
