from ._anvil_designer import view_loan_extension_requestsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class view_loan_extension_requests(view_loan_extension_requestsTemplate):
  def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.load_data()

  def load_data(self):
        # Retrieve and display all loan extension requests
        all_loan_extensions = app_tables.fin_extends_loan.search()
        self.repeating_panel_6.items = self.process_data(all_loan_extensions)
        self.all.text = str(len(self.repeating_panel_6.items))

        # Retrieve and display approved loan extension requests
        approved_loan_extensions = app_tables.fin_extends_loan.search(status=q.like('approved%'))
        self.repeating_panel_7.items = self.process_data(approved_loan_extensions)
        self.label_5.text = str(len(self.repeating_panel_7.items))

        # Retrieve and display rejected loan extension requests
        rejected_loan_extensions = app_tables.fin_extends_loan.search(status=q.like('rejected%'))
        self.repeating_panel_8.items = self.process_data(rejected_loan_extensions)
        self.label_6.text = str(len(self.repeating_panel_8.items))

        # Retrieve and display loan extension requests under process
        under_process_loan_extensions = app_tables.fin_extends_loan.search(status=q.like('under process%'))
        self.repeating_panel_9.items = self.process_data(under_process_loan_extensions)
        self.label_5_copy.text = str(len(self.repeating_panel_9.items))

        # Retrieve and display new loan extension requests
        new_loan_extensions = app_tables.fin_extends_loan.search(status=q.like('under process%'))
        self.repeating_panel_5.items = self.process_data(new_loan_extensions)
        self.new_request.text = str(len(self.repeating_panel_5.items))

  def process_data(self, data):
        profiles_with_extensions = []
        for loan in data:
            user_profile = app_tables.fin_user_profile.get(customer_id=loan['borrower_customer_id'])
            loan_details = app_tables.fin_loan_details.get(loan_id=loan['loan_id'])
            if user_profile is not None and loan_details is not None:
                profiles_with_extensions.append({
                'mobile': user_profile['mobile'],
                'interest_rate': loan_details['interest_rate'],
                'loan_amount': loan['loan_amount'],
                'tenure': loan_details['tenure'],
                'loan_disbursed_timestamp': loan_details['loan_disbursed_timestamp'],
                'product_name': loan_details['product_name'],
                'product_description': loan_details['product_description'],
                'borrower_full_name': loan_details['borrower_full_name'],
                'loan_id': loan['loan_id'],
                'borrower_loan_created_timestamp': loan_details['borrower_loan_created_timestamp'],
                'loan_updated_status': loan_details['loan_updated_status'],
                  'extend_fee': loan['extend_fee'],
                'extension_amount': loan['extension_amount'],
                'total_extension_months': loan['total_extension_months'],
                'reason': loan['reason'],
                'new_emi': loan['new_emi'],
                'final_repayment_amount': loan['final_repayment_amount'],
                  'status': loan['status'],
                'extension_request_date': loan['extension_request_date'],
                'final_repayment_date': loan['final_repayment_date']
                })
        return profiles_with_extensions
    
  
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor.dashboard")

  
  


  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_2.visible = True
    self.label_3.visible = False
    self.label_4.visible = False    
    self.new.visible = False    
    self.label_1.visible = False    
    self.repeating_panel_5.visible = True
    self.repeating_panel_6.visible = False
    self.repeating_panel_7.visible =True
    self.repeating_panel_8.visible = False
    self.repeating_panel_9.visible = False


  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_3.visible = True
   # self._copy.visible = True
    self.label_4.visible = False    
    self.label_2.visible = False    
    self.new.visible = False    
    self.label_1.visible = False    
    self.repeating_panel_5.visible = False
    self.repeating_panel_6.visible = False
    self.repeating_panel_7.visible =False
    self.repeating_panel_8.visible = True
    self.repeating_panel_9.visible = False

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_4.visible = True
   # self.data_grid_3.visible = True
    self.label_2.visible = False    
    self.label_3.visible = False
    self.new.visible = False    
    self.label_1.visible = False   
    self.repeating_panel_5.visible = False
    self.repeating_panel_6.visible = False
    self.repeating_panel_7.visible =False
    self.repeating_panel_8.visible = False
    self.repeating_panel_9.visible = True

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    # self.data_grid_1.visible = not self.data_grid_1.visible
    self.new.visible = True
    #self.data_grid_4.visible = True
    self.label_4.visible = False   
    self.label_2.visible = False    
    self.label_3.visible = False
    self.label_1.visible = False    
    self.repeating_panel_5.visible = True
    self.repeating_panel_6.visible = False
    self.repeating_panel_7.visible =False
    self.repeating_panel_8.visible = False
    self.repeating_panel_9.visible = False

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    #self.data_grid_4_copy.visible = True
    self.label_1.visible = True
    self.label_4.visible = False    
    self.label_2.visible = False   
    self.label_3.visible = False
    self.new.visible = False    
    self.repeating_panel_5.visible = False
    self.repeating_panel_6.visible = True
    self.repeating_panel_7.visible =False
    self.repeating_panel_8.visible = False
    self.repeating_panel_9.visible = False
