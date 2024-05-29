# from ._anvil_designer import view_details_2Template
# from anvil import *
# import anvil.server
# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables

# class view_details_2(view_details_2Template):
#   def __init__(self,selected_row, **properties):
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)

#     # Any code you write here will run before the form opens.
#     self.loan_id_label.text = f"{selected_row['borrower_full_name']}"
#     self.loan_amount_label.text=f"{selected_row['loan_amount']}"
#     self.intrest_rate_label.text=f"{selected_row['interest_rate']}"
#     self.tenure_label.text=f"{selected_row['tenure']}"
#     lender_accepted_timestamp = selected_row['lender_accepted_timestamp']
#     date_of_apply = lender_accepted_timestamp.strftime("%Y-%m-%d")
#     self.date_of_apply_label.text = f"{date_of_apply}"
#     self.loan_updated_status_label.text=f"{selected_row['loan_updated_status']}"

#   def button_1_copy_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     open_form('lendor.dashboard')

#   def button_1_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     open_form("lendor.dashboard.view_lost_oppurtunities")


from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# Ensure the correct import path
# If view_details_2Template is in the same module, it should be imported correctly
# Assuming it's in the same file or appropriately referenced
from ._anvil_designer import view_details_2Template
class view_details_2(view_details_2Template):
  def __init__(self, selected_row, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.loan_id_label.text = f"{selected_row['borrower_full_name']}"
    self.loan_amount_label.text = f"{selected_row['loan_amount']}"
    self.intrest_rate_label.text = f"{selected_row['interest_rate']}"
    self.tenure_label.text = f"{selected_row['tenure']}"
    
    lender_accepted_timestamp = selected_row.get('lender_accepted_timestamp')
    if lender_accepted_timestamp:
      date_of_apply = lender_accepted_timestamp.strftime("%Y-%m-%d")
    else:
      date_of_apply = "N/A"
      
    self.date_of_apply_label.text = f"{date_of_apply}"
    self.loan_updated_status_label.text = f"{selected_row['loan_updated_status']}"

  def button_1_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('lendor.dashboard')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor.dashboard.view_lost_oppurtunities")
