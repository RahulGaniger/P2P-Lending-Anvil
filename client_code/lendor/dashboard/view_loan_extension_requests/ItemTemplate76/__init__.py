from ._anvil_designer import ItemTemplate76Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import main_form_module 
# from .. import main_form_module as main_form_module

class ItemTemplate76(ItemTemplate76Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user_id = main_form_module.userId
    user_data = app_tables.fin_loan_details.search()
    for row in user_data:
        borrower_customer_id = row['borrower_customer_id']
        lender_customer_id = row['lender_customer_id']
        borrower_profile = app_tables.fin_user_profile.get(customer_id=borrower_customer_id)
        lender_profile = app_tables.fin_user_profile.get(customer_id=lender_customer_id)
        self.image_1.source = borrower_profile['user_photo']


  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    selected_row = self.item
    print(f"Selected row status: {selected_row['status']}")
    open_form("lendor.dashboard.view_loan_extension_requests.extension_details", selected_row=selected_row)
    if selected_row['status'] == 'approved' or selected_row['status'] == 'rejected':
        open_form("lendor.dashboard.view_loan_extension_requests.extension_details_approved_or_rejected", selected_row=selected_row)
    else:
        # open_form("lendor_registration_form.dashboard.vlfr.foreclose_details")
       None
