from ._anvil_designer import signup_pageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...user_form import user_module
from .. import main_form_module
import re


class signup_page(signup_pageTemplate):
  def __init__(self, user_type = None,  **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.role = "no-scroll"
    self.user_type = user_type
    self.eye_icon_1.source = '_/theme/eye_closed.png'
    self.eye_icon_2.source = '_/theme/eye_closed.png'

    # Any code you write here will run before the form opens.
  def eye_icon_1_click(self, **event_args):
    """This method is called when the eye icon next to text_box_2 is clicked"""
    if self.text_box_2.hide_text:
      self.text_box_2.hide_text = False  # Show the password
      self.eye_icon_1.source = '_/theme/eye_open.png'  # Change to open eye icon
    else:
      self.text_box_2.hide_text = True  # Hide the password
      self.eye_icon_1.source = '_/theme/eye_closed.png'  # Change to closed eye icon

  def eye_icon_2_click(self, **event_args):
    """This method is called when the eye icon next to text_box_2 is clicked"""
    if self.text_box_3.hide_text:
      self.text_box_3.hide_text = False  # Show the password
      self.eye_icon_2.source = '_/theme/eye_open.png'  # Change to open eye icon
    else:
      self.text_box_3.hide_text = True  # Hide the password
      self.eye_icon_2.source = '_/theme/eye_closed.png'  # Change to closed eye icon



  
  def button_1_click(self, **event_args):
    email = self.text_box_1.text.strip()
        # Get the password
    password = self.text_box_2.text.strip()
    retype_password = self.text_box_3.text.strip()
    if not email or not password:
            self.retype_password_error_label.text = 'Please enter email and password'
            self.retype_password_error_label.visible = True
            return


    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.retype_password_error_label.text = ' Please enter a valid email address.'
            self.retype_password_error_label.visible = True
            return
      
    if password != retype_password:
            self.retype_password_error_label.text = 'Passwords do not match. Please re-enter.'
            self.retype_password_error_label.visible = True
            return

    # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    if email:
      print(email)
      check_user_already_exist = user_module.check_user_profile(email)
      if check_user_already_exist is None:
                print("main if statement was executed")
                user_module.add_email_and_user_id(email ,password, self.user_type)
                main_form_module.email = email
                main_form_module.flag = True
                open_form('bank_users.main_form.signin_page')
      else:
        self.retype_password_error_label.text = 'Email is already exists'
        self.retype_password_error_label.visible = True

  # def check_box_1_change(self, **event_args):
  #   """This method is called when this checkbox is checked or unchecked"""
  #   self.password_visible = self.check_box_1.checked
  #   if self.password_visible:
  #        self.text_box_3.hide_text = False  # Show decrypted password
  #        self.text_box_2.hide_text = False
  #   else:
  #       self.text_box_3.hide_text = True
  #       self.text_box_2.hide_text = True

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('bank_users.main_form.signin_page')

  def home_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('bank_users.main_form')

  def about_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('bank_users.main_form.about_main_form')

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('bank_users.main_form.products_main_form')

  def contact_main_form_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('bank_users.main_form.contact_main_form')

  def login_signup_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('bank_users.main_form.signin_page')

  def send_otp_click(self, **event_args):
    email = self.text_box_1.text.strip()
    if not email:
        alert("Please fill the email")
        return

    check_user_already_exist = anvil.server.call('check_user_profile', email)
    if check_user_already_exist is None:
      self.otp = anvil.server.call('send_email_otp', email)
      if self.otp:
        alert(f"OTP has been sent to {email}")
        self.show_otp_input()
      else:
        self.retype_password_error_label.text = 'Failed to send OTP. Please try again later.'
        self.retype_password_error_label.visible = True
    else:
      self.retype_password_error_label.text = 'Email already exists'
      self.retype_password_error_label.visible = True

  def show_otp_input(self):
    self.text_box_otp.visible = True
    self.verify_otp_button.visible = True
    self.send_otp.text = "Resend"  # Change text of send_otp link
    self.send_otp.visible = True

  def verify_otp_button_click(self, **event_args):
    entered_otp = self.text_box_otp.text.strip()
    if str(self.otp) == entered_otp:
        self.retype_password_error_label.text = 'OTP verified successfully'
        
        self.retype_password_error_label.visible = True
        # Update email verified status in user table
        email = self.text_box_1.text.strip()
        # open_form('bank_users.main_form.forgot_password',email)
        anvil.server.call('update_user_status', email, email_verified=True)
    else:
        self.retype_password_error_label.text = 'Invalid OTP. Please try again.'
        self.retype_password_error_label.visible = True
        self.send_otp.visible = True

  def text_box_otp_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

