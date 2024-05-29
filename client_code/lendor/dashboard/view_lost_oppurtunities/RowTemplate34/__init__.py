from ._anvil_designer import RowTemplate34Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from .. import main_form_module as main_form_module

class RowTemplate34(RowTemplate34Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user_id=main_form_module.userId
    user_data=app_tables.fin_user_profile.get(customer_id=self.user_id)
    if user_data:
      self.image_1.source= user_data['user_photo']
    
    

    # Any code you write here will run before the form opens.

  def view_lost_apportunity_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    selcted_row=self.item
    open_form('lendor.dashboard.view_lost_oppurtunities.view_details_2',selected_row=selcted_row)
