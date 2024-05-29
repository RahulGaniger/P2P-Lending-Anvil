from ._anvil_designer import view_lost_oppurtunitiesTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module


class view_lost_oppurtunities(view_lost_oppurtunitiesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user_id = main_form_module.userId
    #self.repeating_panel_1.items = app_tables.fin_loan_details.search(loan_updated_status=q.like('lost opportunities%'))
    lost_opportunities = app_tables.fin_loan_details.search(loan_updated_status=q.like('lost opportunities%'),lender_customer_id=self.user_id)
    borrower_profiles = []
    for loan in lost_opportunities:
            user_profile = app_tables.fin_user_profile.get(customer_id=loan['borrower_customer_id'])
            if user_profile is not None:
                borrower_profiles.append({
                    'mobile': user_profile['mobile'],
                    'interest_rate': loan['interest_rate'],
                    'loan_amount': loan['loan_amount'],
                    'tenure': loan['tenure'],
                    'loan_disbursed_timestamp': loan['loan_disbursed_timestamp'],
                    'product_name': loan['product_name'],
                    'product_description': loan['product_description'],
                    'borrower_full_name': loan['borrower_full_name'],
                    'loan_id': loan['loan_id'],
                    'lender_accepted_timestamp': loan['lender_accepted_timestamp'],
                    'loan_updated_status': loan['loan_updated_status'],
                    #'loan_updated_status': loan['loan_updated_status'],
                    #'name': user_profile['name'],  # Replace 'name' with the actual column name
                    # Add other attributes you want to include in borrower_profiles
                })
    self.repeating_panel_1.items = borrower_profiles
  
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor.dashboard")

  
