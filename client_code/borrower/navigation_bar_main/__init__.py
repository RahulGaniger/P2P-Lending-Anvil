from ._anvil_designer import navigation_bar_mainTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class navigation_bar_main(navigation_bar_mainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def home_main_form_link_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('bank_users.main_form')

  def about_main_form_link_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('bank_users.main_form.about_main_form')

  def contact_main_form_link_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('bank_users.main_form.contact_main_form')

  

  
        
