from ._anvil_designer import view_loan_foreclosure_RequestsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class view_loan_foreclosure_Requests(view_loan_foreclosure_RequestsTemplate):
  def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.load_data()

  def load_data(self):
        # Retrieve and display all foreclosure requests
        all_foreclosures = app_tables.fin_foreclosure.search()
        self.repeating_panel_6.items = self.process_data(all_foreclosures)
        self.all.text = str(len(self.repeating_panel_6.items))

        # Retrieve and display approved foreclosure requests
        approved_foreclosures = app_tables.fin_foreclosure.search(status=q.like('approved%'))
        self.repeating_panel_7.items = self.process_data(approved_foreclosures)
        self.label_5.text = str(len(self.repeating_panel_7.items))

        # Retrieve and display rejected foreclosure requests
        rejected_foreclosures = app_tables.fin_foreclosure.search(status=q.like('rejected%'))
        self.repeating_panel_8.items = self.process_data(rejected_foreclosures)
        self.label_6.text = str(len(self.repeating_panel_8.items))

        # # Retrieve and display foreclosure requests under process
        # under_process_foreclosures = app_tables.fin_foreclosure.search(status=q.like('under process%'))
        # self.repeating_panel_9.items = self.process_data(under_process_foreclosures)
        # self.label_5_copy.text = str(len(self.repeating_panel_9.items))

        # Retrieve and display new foreclosure requests
        new_foreclosures = app_tables.fin_foreclosure.search(status=q.like('under process%'))
        self.repeating_panel_5.items = self.process_data(new_foreclosures)
        self.new_request.text = str(len(self.repeating_panel_5.items))

  def process_data(self, data):
        profiles_with_foreclosure = []
        for foreclosure in data:
            loan_details = app_tables.fin_loan_details.get(loan_id=foreclosure['loan_id'])
            if loan_details is not None:
                user_profile = app_tables.fin_user_profile.get(customer_id=loan_details['borrower_customer_id'])
                if user_profile is not None:
                    profiles_with_foreclosure.append({
                        'mobile': user_profile['mobile'],
                        'status': foreclosure['status'],
                        'loan_id': foreclosure['loan_id'],
                        'interest_rate': foreclosure['interest_rate'],
                        'loan_amount': foreclosure['loan_amount'],
                        'tenure': loan_details['tenure'],
                        'loan_disbursed_timestamp': loan_details['loan_disbursed_timestamp'],
                        'product_name': loan_details['product_name'],
                        'product_description': loan_details['product_description'],
                        'borrower_full_name': loan_details['borrower_full_name'],
                        'lender_accepted_timestamp': loan_details['lender_accepted_timestamp'],
                        'loan_updated_status': loan_details['loan_updated_status'],
                        'foreclose_fee': foreclosure['foreclose_fee'],
                        'foreclose_amount': foreclosure['foreclose_amount'],
                        'outstanding_amount': foreclosure['outstanding_amount'],
                        'reason': foreclosure['reason'],
                        'total_due_amount': foreclosure['total_due_amount'],
                        'borrower_name': foreclosure['borrower_name'],
                        'paid_amount': foreclosure['paid_amount'],
                        'penalty_amount': foreclosure['penalty_amount'],
                        # Include other relevant details from the foreclosure request
                    })
        return profiles_with_foreclosure

  
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor.dashboard")  

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_2.visible = True
    self.label_3.visible = False   
    self.new.visible = False
    self.label_1.visible = False
    self.repeating_panel_6.visible = False
    self.repeating_panel_5.visible = False  
    self.repeating_panel_7.visible = True
    self.repeating_panel_8.visible = False 
    self.repeating_panel_9.visible = False

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_3.visible = True 
    self.new.visible = False
    self.label_1.visible = False
    self.label_2.visible = False
    self.repeating_panel_6.visible = False
    self.repeating_panel_5.visible = False  
    self.repeating_panel_7.visible = False
    self.repeating_panel_8.visible = True 
    self.repeating_panel_9.visible = False


  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    #self.data_grid_4.visible = not self.data_grid_4.visible
    self.new.visible = True    
    self.label_2.visible = False
    self.label_3.visible = False
    self.label_1.visible = False
    self.repeating_panel_6.visible = False
    self.repeating_panel_5.visible = True
    self.repeating_panel_7.visible = False
    self.repeating_panel_8.visible = False 
    self.repeating_panel_9.visible = False
    

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_1.visible = True 
    self.label_3.visible = False
    self.new.visible = False
    self.label_2.visible = False
    self.repeating_panel_6.visible = True
    self.repeating_panel_5.visible = False
    self.repeating_panel_7.visible = False
    self.repeating_panel_8.visible = False 
    self.repeating_panel_9.visible = False
    
    





   
