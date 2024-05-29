from ._anvil_designer import lender_profileTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....bank_users.main_form import main_form_module


class lender_profile(lender_profileTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    email=main_form_module.email
    user_profile=app_tables.fin_user_profile.get(email_user=email)
    if user_profile: 
      self.label_1.text=user_profile['full_name']
      self.email.text=user_profile['email_user']
      self.mobile.text=user_profile['mobile']
      self.birh.text=user_profile['date_of_birth']
      self.city.text=user_profile['city']
      # self.pan_text.text=user_profile['pan_number']
      self.gender.text=user_profile['gender']
      # self.language.text=user_profile['mouther_tounge']
      self.image_1.source = user_profile['user_photo']
      self.status.text=user_profile['marital_status']

  def button_1_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('lendor.dashboard.edit_profile')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('lendor.dashboard')
