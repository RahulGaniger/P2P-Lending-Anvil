from ._anvil_designer import dashboardTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class dashboard(dashboardTemplate):
  def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

  def button_2_click(self, **event_args):
   
    open_form('admin.dashboard.admin_management')

  def button_3_click(self, **event_args):
   
    open_form('admin.dashboard.borrowers')

  def button_4_click(self, **event_args):
   
    open_form('admin.dashboard.lenders')

  def button_5_click(self, **event_args):
    
    open_form('admin.dashboard.loan_management')

  def button_6_click(self, **event_args):
    
    open_form('admin.dashboard.manage_products')

  def button_7_click(self, **event_args):
    
    open_form('admin.dashboard.manage_settings')

  def button_8_click(self, **event_args):
    open_form('admin.dashboard.revenue_share')

  def button_9_click(self, **event_args):
    open_form('admin.dashboard.risk_pool')

  def button_10_click(self, **event_args):
    open_form('admin.dashboard.manage_cms')

  def button_11_click(self, **event_args):
    open_form('admin.dashboard.manage_issues')

  def button_13_click(self, **event_args):
    open_form('admin.dashboard.performance_tracker')

  def button_1_copy_click(self, **event_args):
    open_form('admin.dashboard.manage_dropdown')

  def manage_lender_click(self, **event_args):
    open_form('admin.dashboard.lenders')

  def manage_ascend_click(self, **event_args):
    open_form('admin.dashboard.manage_ascend')

  def logout__click(self, **event_args):
    anvil.users.logout()
    open_form('bank_users.main_form')

  def button_14_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.admin_management')

  def button_12_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.borrowers')

  def button_15_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_loan_details')

  def button_16_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_products')

  def button_18_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_settings')

  def button_20_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.revenue_share')

  def button_19_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.reporting_and_analytical_modules')

  def button_17_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_cms')

  def button_21_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_issues')

  def button_22_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.performance_tracker')

  def button_23_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.manage_ascend')

  def image_9_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.manage_cms')

  def image_1_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.admin_management')

  def image_2_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.borrowers')

  def image_3_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.lenders')

  def image_4_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.manage_loan_details')

  def image_5_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.manage_products')

  def image_6_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.manage_settings')

  def image_7_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.revenue_share')

  def image_8_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.risk_pool')

  def image_10_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.manage_issues')

  def image_11_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.performance_tracker')

  def image_12_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    open_form('admin.dashboard.manage_ascend')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.Accounting')

 

  

    





