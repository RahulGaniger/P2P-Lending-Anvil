from ._anvil_designer import ItemTemplate53Template
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

class ItemTemplate53(ItemTemplate53Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user_id = main_form_module.userId
    user_data = app_tables.fin_loan_details.search(loan_updated_status=q.like('lost opportunities%'),lender_customer_id=self.user_id)
    for row in user_data:
        borrower_customer_id = row['borrower_customer_id']
        lender_customer_id = row['lender_customer_id']
        borrower_profile = app_tables.fin_user_profile.get(customer_id=borrower_customer_id)
        lender_profile = app_tables.fin_user_profile.get(customer_id=lender_customer_id)
        self.image_1.source = borrower_profile['user_photo']


  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    selcted_row=self.item
    open_form('lendor.dashboard.view_lost_oppurtunities.view_details_2',selected_row=selcted_row)

