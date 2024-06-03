from ._anvil_designer import dashboardTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...bank_users.main_form import main_form_module
from ...bank_users.user_form import user_form
from ...bank_users.user_form import user_module


class dashboard(dashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.email = main_form_module.email
    self.user_Id = main_form_module.userId
    self.email = self.email
    user_id = self.user_Id
    self.populate_loan_history()

    wallet = app_tables.fin_wallet.get(customer_id=self.user_Id)
    if wallet:
      self.label_9.text = wallet['wallet_amount']

    user_profile = app_tables.fin_user_profile.get(customer_id=self.user_Id)
    if user_profile:
      self.label_3.text = user_profile['mobile']
      self.image_1_copy_copy.source = user_profile['user_photo']
      self.label_2_copy.text = "Welcome " + user_profile['full_name']

    borrower = app_tables.fin_borrower.get(customer_id=user_id)
    if borrower:
      self.label_7.text = borrower['borrower_since']
      self.label_5.text = borrower['credit_limit']

  def populate_loan_history(self):
    try:
      customer_loans = app_tables.fin_loan_details.search(borrower_customer_id=self.user_Id)
      if customer_loans:
        self.data = [{'product_name': loan['product_name'], 'loan_amount': loan['loan_amount'],
                      'tenure': loan['tenure'], 'interest_rate': loan['interest_rate'],
                      'total_repayment_amount': round(loan['total_repayment_amount'], 2),
                      'loan_updated_status': loan['loan_updated_status']} for loan in customer_loans]
        self.repeating_panel_1.items = self.data
      else:
        Notification("No Data Available Here!").show()
    except anvil.tables.TableError:
      alert("No data found")

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    try:
      existing_loans = app_tables.fin_loan_details.search(
        borrower_customer_id=self.user_Id,
        loan_updated_status=q.any_of(
          q.like('accept%'),
          q.like('Approved%'),
          q.like('approved%'),
          q.like('under process%'),
          q.like('foreclosure%'),
          q.like('disbursed loan%'),
          q.like('Disbursed loan%'),
          q.like('Under Process%')
        )
      )
      num_existing_loans = len(existing_loans)
      if num_existing_loans >= 5:
        alert("You already have 5 loans. Cannot open a new loan request.")
      else:
        wallet_row = app_tables.fin_wallet.get(customer_id=self.user_Id)
        if wallet_row and wallet_row['wallet_id'] is not None:
          open_form('borrower.dashboard.new_loan_request')
        else:
          alert("Wallet not found. Please create a wallet.")
    except anvil.tables.TableError as e:
      alert("Error fetching existing loans.")

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('borrower.dashboard.today_dues')

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('borrower.dashboard.view_loans')

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('borrower.dashboard.foreclosure_request')

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('borrower.dashboard.application_tracker')

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('borrower.dashboard.extension_loan_request')

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('borrower.dashboard.view_transaction_history')

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('borrower.dashboard.discount_coupons')

  def link_10_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('borrower.dashboard.borrower_portfolio')

  def button_12_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('borrower.dashboard.borrower_view_profile')

  def image_1_copy_copy_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('borrower.dashboard.borrower_profile')

  def link_9_click(self, **event_args):
    """This method is called when the link is clicked"""
    customer_id = self.user_Id
    email = self.email
    anvil.server.call('fetch_profile_data_and_insert', email, customer_id)
    open_form("wallet.wallet")

  def home_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('borrower.dashboard')

  def about_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("borrower.dashboard.dashboard_about")

  def contact_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("borrower.dashboard.dashboard_contact")

  def link_11_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('borrower.dashboard.dashboard_report_a_problem')

  def link_12_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass
