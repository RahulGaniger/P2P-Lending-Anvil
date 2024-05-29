from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...bank_users.main_form import main_form_module
from ...bank_users.user_form import user_module

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.email = main_form_module.email
    self.user_id = main_form_module.userId
    self.email = self.email
    self.user_id = self.user_id
    self.components_visible = False  # Flag to keep track of component visibility
    self.load_data(None)

    existing_loans = app_tables.fin_loan_details.search(loan_updated_status=q.any_of(
                          q.like('under process%'),
                          q.like('Under Process%'),
                          q.like('under process')))
    self.label_9.text = str(len(existing_loans) or 0)

    investment = app_tables.fin_lender.get(customer_id=self.user_id)
    self.label_3.text = str(investment['investment'] or 0)

    opening_bal = app_tables.fin_wallet.get(customer_id=self.user_id)
    self.label_5.text = str(opening_bal['wallet_amount'] or 0)

    my_returns = app_tables.fin_lender.get(customer_id=self.user_id)
    self.label_7.text = str(my_returns['return_on_investment'] or 0)

    disbursed_loan = app_tables.fin_loan_details.search(loan_updated_status=q.like('disbursed loan%'), lender_customer_id=self.user_id)
    lost_opportunities = app_tables.fin_loan_details.search(loan_updated_status=q.like('lost opportunities%'), lender_customer_id=self.user_id)
    closed = app_tables.fin_loan_details.search(loan_updated_status=q.like('close%'), lender_customer_id=self.user_id)
    extended = app_tables.fin_loan_details.search(loan_updated_status=q.like('extension%'), lender_customer_id=self.user_id)
    
    self.button_1_copy.text = f"New Loan Requests ({len(existing_loans)})"
    self.button_2_copy.text = f"Loan Disbursed ({len(disbursed_loan)})"
    self.button_3_copy.text = f"Lost Opportunities ({len(lost_opportunities)})"
    self.button_4_copy.text = f"Closed ({len(closed)})"
    self.button_5_copy.text = f"Extended ({len(extended)})"
    # self.column_panel_8.width = '100%'

    # Any code you write here will run before the form opens.
  def load_data(self,status):
        if status == 'close':
            closed_loans = app_tables.fin_loan_details.search(loan_updated_status=q.like('close%'), lender_customer_id=self.user_id)
            self.new_loan =len(closed_loans)
            self.repeating_panel_1.items = self.process_data(closed_loans)
        elif status == 'disbursed loan':
            disbursed_loans = app_tables.fin_loan_details.search(loan_updated_status=q.like('disbursed loan%'), lender_customer_id=self.user_id)
            self.repeating_panel_1.items = self.process_data(disbursed_loans)

        elif status == 'under process':
            underprocess_loans = app_tables.fin_loan_details.search(loan_updated_status=q.any_of(q.like('under process%'),q.like('under process')))
            self.repeating_panel_2.items = self.process_data(underprocess_loans)
            

        elif status == 'lost opportunities':
            lost_opportunities = app_tables.fin_loan_details.search(loan_updated_status=q.like('lost opportunities%'), lender_customer_id=self.user_id)
            self.repeating_panel_1.items = self.process_data(lost_opportunities)

        elif status == 'extension':
            extension_loans = app_tables.fin_loan_details.search(loan_updated_status=q.like('extension%'), lender_customer_id=self.user_id)
            self.repeating_panel_1.items = self.process_data(extension_loans)

  def process_data(self, data):
        profiles_with_loans = []
        for loan in data:
            user_profile = app_tables.fin_user_profile.get(customer_id=loan['borrower_customer_id'])
            
            if user_profile is not None:
                profiles_with_loans.append({
                    'loan_amount': loan['loan_amount'],
                    'tenure': loan['tenure'],
                    'borrower_full_name': loan['borrower_full_name'],
                    'loan_id': loan['loan_id'],
                    'bessem_value': user_profile['bessem_value'],
                    'loan_updated_status': loan['loan_updated_status'],
                    'interest_rate': loan['interest_rate'],
                    'borrower_loan_created_timestamp': loan['borrower_loan_created_timestamp'],
                    'borrower_customer_id': loan['borrower_customer_id'],
                    'beseem_score': user_profile['bessem_value'],
                    'credit_limit': loan['credit_limit'],
                    'product_name': loan['product_name']})
        return profiles_with_loans

  
  def home_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('lendor.dashboard')

  def contact_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.dasboard_contact")

  def about_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('lendor.dashboard.dasboard_about')

  def link_11_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('lendor.dashboard.dashboard_report_a_problem')

  def link_9_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.lender_profile")
    

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.view_borrower_loan_request")

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.view_loan_extension_requests")

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.view_loan_foreclosure_Requests")

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.today_dues")

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.lender_view_loans")

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.view_lost_oppurtunities")

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.change_password")

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.view_transaction_history")

  def link_13_click(self, **event_args):
    """This method is called when the link is clicked"""
    customer_id = self.user_id
    email = self.email
    anvil.server.call('fetch_profile_data_and_insert', email, customer_id)
    open_form("wallet.wallet")

  def link_10_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor.dashboard.view_or_send_notifications")
