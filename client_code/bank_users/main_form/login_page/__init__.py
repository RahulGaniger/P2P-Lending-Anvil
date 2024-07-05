from ._anvil_designer import login_pageTemplate
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
from datetime import datetime


class login_page(login_pageTemplate):
  def __init__(self,  **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.role = "no-scroll"
    # login_date = datetime.now()

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    email = self.text_box_1.text.strip()
        # Get the password
    password = self.text_box_2.text.strip()
    if not email or not password:
            self.error_label.text = 'Please enter email and password'
            self.error_label.visible = True
            return
        # Get the user based on login input
    user = anvil.server.call('get_user_for_login',email)
    if user is None:
            self.error_label.text = 'Invalid email or password'
            self.error_label.visible = True
            return
    password_hash = user['password_hash']
    hashed_password = anvil.server.call('hash_password_1', password ,password_hash)
    print(hashed_password)
    print(password_hash)
    print(password)
        # Check if user exists and password matches
    if user is not None and  hashed_password is True:
            user_row = app_tables.users.get(email=email)
            # Update the login date for the user
            user_row['last_login'] = datetime.now()
            # Save changes to the users table
            user_row.update()
            
            print(email)
            if email:
                user_email = email
                print(user_email)
                check_user_already_exist = user_module.check_user_profile(user_email)
                print(check_user_already_exist)
                if check_user_already_exist is None:
                    print("main if statement was executed")
                    user_module.add_email_and_user_id(user_email)
                    main_form_module.email = user_email
                    main_form_module.flag = True
                    open_form('bank_users.main_form.basic_registration_form')
                else:
                    check_user_registration = user_module.check_user_registration_form_done_or_not_engine(user_email)
                    print("main else statement was executed")
                    user_profile_e = app_tables.fin_user_profile.get(email_user=user_email)
                    main_form_module.email = user_email
                    main_form_module.userId = user_module.find_user_id(user_email)
                    self.user_id =  user_module.find_user_id(user_email)
                    userid = self.user_id
                    if user_profile_e is not None:
                        user_type = user_profile_e['usertype']
                        last_confirm = user_profile_e['last_confirm']
                        marital_status = user_profile_e['marital_status']
                        actual_count=user_profile_e['form_count']
                        print(actual_count)
                        print("")
                        if user_type == 'admin' or user_type == 'super admin':
                            open_form('admin.dashboard')
                        elif user_type == 'lender' and last_confirm:
                            open_form('lendor.dashboard')
                        elif user_type == 'borrower' and last_confirm:
                            if user_profile_e['one_time_settlement'] != True:
                                open_form('borrower.dashboard')
                            elif user_profile_e['one_time_settlement'] == True:
                                open_form('borrower.ots_dashboard')

                        elif actual_count is not None and actual_count == 0:
                          open_form('bank_users.user_form')
                        # For Borrower Registration Form  
                        elif user_type == 'borrower' and actual_count==1:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_1_education',user_id=userid)
                        elif user_type == 'borrower' and actual_count==1.1:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_10th_class',user_id=userid) 
                        elif user_type == 'borrower' and actual_count==1.2:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_intermediate',user_id=userid) 
                        elif user_type == 'borrower' and actual_count==1.3:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_btech',user_id=userid)   
                        elif user_type == 'borrower' and actual_count==1.4:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_mtech',user_id=userid)
                        elif user_type == 'borrower' and actual_count==1.5:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_phd',user_id=userid)
                        elif user_type == 'borrower' and actual_count==2:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment',user_id=userid)
                        elif user_type == 'borrower' and actual_count==2.1:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_student',user_id=userid)
                        elif user_type == 'borrower' and actual_count==2.2:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_self_employment',user_id=userid)
                        elif user_type == 'borrower' and actual_count==2.21:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_business_1',user_id=userid)
                        elif user_type == 'borrower' and actual_count==2.22:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_business_2',user_id=userid)
                        elif user_type == 'borrower' and actual_count==2.23:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_business_3',user_id=userid)
                        elif user_type == 'borrower' and actual_count==2.31:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_1',user_id=userid)
                        elif user_type == 'borrower' and actual_count==2.32:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_2',user_id=userid)
                        elif user_type == 'borrower' and actual_count==2.33:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_3',user_id=userid)
                        elif user_type == 'borrower' and actual_count==2.4:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_farmer',user_id=userid)
                        elif user_type == 'borrower' and actual_count==3:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_3_marital',user_id=userid)
                        # elif user_type == 'borrower' and actual_count==3.1:
                        #   open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_3_marital.star_1_borrower_registration_form_3_marital_married',user_id=userid, marital_status = marital_status)
                        elif user_type == 'borrower' and actual_count==4:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_4_loan',user_id=userid)
                        elif user_type == 'borrower' and actual_count==5:
                          open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_5_bank_1',user_id=userid)
                        # elif user_type == 'borrower' and actual_count==6:
                        #   open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_5_bank_2',user_id=userid)
                        # For Lender Registration Form  
                        elif user_type == 'lender' and actual_count==1:
                          open_form('lendor.lendor_registration_forms.lender_registration_form_1_education_form',user_id=userid)
                        elif user_type == 'lender' and actual_count==1.1:
                          open_form('lendor.lendor_registration_forms.lender_registration_form_1_education_form.lender_registration_education_10th_class',user_id=userid) 
                        elif user_type == 'lender' and actual_count==1.2:
                          open_form('lendor.lendor_registration_forms.lender_registration_form_1_education_form.lender_registration_education_Intermediate',user_id=userid) 
                        elif user_type == 'lender' and actual_count==1.3:
                          open_form('lendor.lendor_registration_forms.lender_registration_form_1_education_form.lender_registration_education_Btech',user_id=userid)   
                        elif user_type == 'lender' and actual_count==1.4:
                          open_form('lendor.lendor_registration_forms.lender_registration_form_1_education_form.lender_registration_education_Mtech',user_id=userid)
                        elif user_type == 'lender' and actual_count==1.5:
                          open_form('lendor.lendor_registration_forms.lender_registration_form_1_education_form.lender_registration_education_Phd',user_id=userid)
                        elif user_type == 'lender' and actual_count==2:
                          open_form('lendor.lendor_registration_forms.lender_registration_form_2',user_id=userid)
                        elif user_type == 'lender' and actual_count==2.21:
                          open_form('lendor.lendor_registration_forms.lender_registration_form_2.lender_registration_Institutional_form_1',user_id=userid)
                        elif user_type == 'lender' and actual_count==2.22:
                          open_form('lendor.lendor_registration_forms.lender_registration_form_2.lender_registration_Institutional_form_2',user_id=userid)
                        elif user_type == 'lender' and actual_count==2.23:
                          open_form('lendor.lendor_registration_forms.lender_registration_form_2.lender_registration_Institutional_form_3',user_id=userid)
                        elif user_type == 'lender' and actual_count==2.31:
                          open_form('lendor.lendor_registration_forms.lender_registration_form_2.lender_registration_individual_form_1',user_id=userid)
                        elif user_type == 'lender' and actual_count==2.32:
                          open_form('lendor.lendor_registration_forms.lender_registration_form_2.lender_registration_individual_form_2',user_id=userid)
                        elif user_type == 'lender' and actual_count==2.33:
                          open_form('lendor.lendor_registration_forms.lender_registration_form_2.lender_registration_individual_form_3',user_id=userid)
                        elif user_type == 'lender' and actual_count==3:
                          open_form('lendor.lendor_registration_forms.lender_registration_form_3_marital_details',user_id=userid)
                        # elif user_type == 'lender' and actual_count==3.1:
                        #   open_form('lendor.lendor_registration_forms.lender_registration_form_3_marital_details.lender_registration_form_3_marital_married',user_id=userid,marital_status = marital_status)
                        elif actual_count==4:
                          open_form('lendor.lendor_registration_forms.lender_registration_form_4_bank_form_1',user_id=userid)
                        # elif actual_count==5:
                        #   open_form('lendor.lendor_registration_forms.lender_registration_form_4_bank_form_2',user_id=userid)
        
                        else:
                            open_form('bank_users.main_form.basic_registration_form')

                    else:
                        # Handle the case when user_profile_e is None
                        open_form('bank_users.user_form')
            else:
                # Handle the case when current_user is None
                open_form('bank_users.user_form')


    else:
      self.error_label.text = 'Invalid email or password'
      self.error_label.visible = True


  def check_box_1_change(self, **event_args):
   #  """This method is called when this checkbox is checked or unchecked"""
        self.password_visible = self.check_box_1.checked
        if self.password_visible:
            self.text_box_2.hide_text = False  # Show decrypted password
        else:
            self.text_box_2.hide_text = True

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('bank_users.main_form.signup_page')

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

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.user_issue.user_bugreports')

  def button_10_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('bank_users.main_form.investNow_applyForLoan')

  def send_otp_click(self, **event_args):
    self.label_5.visible = False
    self.text_box_2.visible = False
    self.check_box_1.visible = False
    self.label_2.visible = False
    self.check_box_1.visible = False
    self.button_1.visible = False
    self.label_8.visible = False
    self.send_otp.text = "Send otp"
    email = self.text_box_1.text.strip()
    if not email:
        alert("Please fill the email")
        return
    if email is not None:  # This check seems redundant
      self.otp = anvil.server.call('send_email_otp', email)
      if self.otp:
        alert(f"OTP has been sent to {email}")
        self.show_otp_input()
      else:
        self.retype_password_error_label.text = 'Failed to send OTP. Please try again later.'
        self.retype_password_error_label.visible = True

  def show_otp_input(self):
    self.text_box_otp.visible = True
    self.verify_otp_button.visible = True
    self.send_otp.visible = True
    self.label_5.visible = False
    self.text_box_2.visible = False
    self.send_otp.text = "Resend"  # Change text of send_otp link
    self.label_2.visible = False
    self.check_box_1.visible = False
    self.button_1.visible = False
    self.label_8.visible = False

  def verify_otp_button_click(self, **event_args):
    entered_otp = self.text_box_otp.text.strip()
    email = self.text_box_1.text.strip()  
    if not email:
        alert("Please fill the email")
        return
    if str(self.otp) == entered_otp:
        self.error_label.text = 'OTP verified successfully'
        self.error_label.visible = True
        user_row = app_tables.users.get(email=email)
        # Update the login date for the user
        user_row['last_login'] = datetime.now()
        # Save changes to the users table
        user_row.update()
        
        print(email)
        if email:
            user_email = email
            print(user_email)
            check_user_already_exist = user_module.check_user_profile(user_email)
            print(check_user_already_exist)
            if check_user_already_exist is None:
                print("main if statement was executed")
                user_module.add_email_and_user_id(user_email)
                main_form_module.email = user_email
                main_form_module.flag = True
                open_form('bank_users.main_form.basic_registration_form')
            else:
                check_user_registration = user_module.check_user_registration_form_done_or_not_engine(user_email)
                print("main else statement was executed")
                user_profile_e = app_tables.fin_user_profile.get(email_user=user_email)
                main_form_module.email = user_email
                main_form_module.userId = user_module.find_user_id(user_email)
                self.user_id =  user_module.find_user_id(user_email)
                userid = self.user_id
                if user_profile_e is not None:
                    user_type = user_profile_e['usertype']
                    last_confirm = user_profile_e['last_confirm']
                    marital_status = user_profile_e['marital_status']
                    actual_count=user_profile_e['form_count']
                    print(actual_count)
                    print("")
                    if user_type == 'admin' or user_type == 'super admin':
                        open_form('admin.dashboard')
                    elif user_type == 'lender' and last_confirm:
                        open_form('lendor.dashboard')
                    elif user_type == 'borrower' and last_confirm:
                        if user_profile_e['one_time_settlement'] != True:
                            open_form('borrower.dashboard')
                        elif user_profile_e['one_time_settlement'] == True:
                            open_form('borrower.ots_dashboard')

                    elif actual_count is not None and actual_count == 0:
                      open_form('bank_users.user_form')
                    # For Borrower Registration Form  
                    elif user_type == 'borrower' and actual_count==1:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_1_education',user_id=userid)
                    elif user_type == 'borrower' and actual_count==1.1:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_10th_class',user_id=userid) 
                    elif user_type == 'borrower' and actual_count==1.2:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_intermediate',user_id=userid) 
                    elif user_type == 'borrower' and actual_count==1.3:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_btech',user_id=userid)   
                    elif user_type == 'borrower' and actual_count==1.4:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_mtech',user_id=userid)
                    elif user_type == 'borrower' and actual_count==1.5:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_1_education.star_1_borrower_registration_form_education_phd',user_id=userid)
                    elif user_type == 'borrower' and actual_count==2:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment',user_id=userid)
                    elif user_type == 'borrower' and actual_count==2.1:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_student',user_id=userid)
                    elif user_type == 'borrower' and actual_count==2.2:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_self_employment',user_id=userid)
                    elif user_type == 'borrower' and actual_count==2.21:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_business_1',user_id=userid)
                    elif user_type == 'borrower' and actual_count==2.22:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_business_2',user_id=userid)
                    elif user_type == 'borrower' and actual_count==2.23:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_business_3',user_id=userid)
                    elif user_type == 'borrower' and actual_count==2.31:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_1',user_id=userid)
                    elif user_type == 'borrower' and actual_count==2.32:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_2',user_id=userid)
                    elif user_type == 'borrower' and actual_count==2.33:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_3',user_id=userid)
                    elif user_type == 'borrower' and actual_count==2.4:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_farmer',user_id=userid)
                    elif user_type == 'borrower' and actual_count==3:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_3_marital',user_id=userid)
                    elif user_type == 'borrower' and actual_count==3.1:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_3_marital.star_1_borrower_registration_form_3_marital_married',user_id=userid, marital_status = marital_status)
                    elif user_type == 'borrower' and actual_count==4:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_4_loan',user_id=userid)
                    elif user_type == 'borrower' and actual_count==5:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_5_bank_1',user_id=userid)
                    elif user_type == 'borrower' and actual_count==6:
                      open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_5_bank_2',user_id=userid)
                    # For Lender Registration Form  
                    elif user_type == 'lender' and actual_count==1:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_1_education_form',user_id=userid)
                    elif user_type == 'lender' and actual_count==1.1:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_1_education_form.lender_registration_education_10th_class',user_id=userid) 
                    elif user_type == 'lender' and actual_count==1.2:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_1_education_form.lender_registration_education_Intermediate',user_id=userid) 
                    elif user_type == 'lender' and actual_count==1.3:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_1_education_form.lender_registration_education_Btech',user_id=userid)   
                    elif user_type == 'lender' and actual_count==1.4:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_1_education_form.lender_registration_education_Mtech',user_id=userid)
                    elif user_type == 'lender' and actual_count==1.5:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_1_education_form.lender_registration_education_Phd',user_id=userid)
                    elif user_type == 'lender' and actual_count==2:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_2',user_id=userid)
                    elif user_type == 'lender' and actual_count==2.21:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_2.lender_registration_Institutional_form_1',user_id=userid)
                    elif user_type == 'lender' and actual_count==2.22:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_2.lender_registration_Institutional_form_2',user_id=userid)
                    elif user_type == 'lender' and actual_count==2.23:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_2.lender_registration_Institutional_form_3',user_id=userid)
                    elif user_type == 'lender' and actual_count==2.31:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_2.lender_registration_individual_form_1',user_id=userid)
                    elif user_type == 'lender' and actual_count==2.32:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_2.lender_registration_individual_form_2',user_id=userid)
                    elif user_type == 'lender' and actual_count==2.33:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_2.lender_registration_individual_form_3',user_id=userid)
                    elif user_type == 'lender' and actual_count==3:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_3_marital_details',user_id=userid)
                    elif user_type == 'lender' and actual_count==3.1:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_3_marital_details.lender_registration_form_3_marital_married',user_id=userid,marital_status = marital_status)
                    elif actual_count==4:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_4_bank_form_1',user_id=userid)
                    elif actual_count==5:
                      open_form('lendor.lendor_registration_forms.lender_registration_form_4_bank_form_2',user_id=userid)
    
                    else:
                        open_form('bank_users.main_form.basic_registration_form')

                else:
                    # Handle the case when user_profile_e is None
                    open_form('bank_users.user_form')
        else:
            # Handle the case when current_user is None
            open_form('bank_users.user_form')

        
    else:
        self.error_label.text = 'Invalid OTP. Please try again.'
        self.error_label.text = True
        self.send_otp.visible = True

  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass


