from ._anvil_designer import lender_registration_Institutional_form_1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import re


class lender_registration_Institutional_form_1(lender_registration_Institutional_form_1Template):
  def __init__(self, user_id,**properties):
    self.userId = user_id
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
            self.text_box_1_copy.text = user_data['business_add']
            self.text_box_2_copy.text = user_data['business_name']
            self.drop_down_12.selected_value = user_data['business_type']
            self.date_picker_1.date = user_data['year_estd']
            self.text_box_3.text = user_data['industry_type']
            self.text_box_4.text = user_data['six_month_turnover']      
          
            self.text_box_5.text = user_data['din'].replace(' ', '') if 'din' in user_data else ''
            self.text_box_6.text = user_data['cin'].replace(' ', '') if 'cin' in user_data else ''
            self.text_box_7.text = user_data['registered_off_add'] if 'registered_off_add' in user_data else ''
      
    user_data.update()
    # user_data = anvil.server.call('get_user_data', user_id)
        
    # if user_data:
    #         self.business_type = user_data.get('business_type', '')
    #         self.empolyees_working = user_data.get('employees_working', '')
    #         # self.year = user_data.get('year_estd', '')
    #         self.business_name = user_data.get('business_name', '')
    #         self.business_add = user_data.get('business_add', '')
  
            
    # else:
    #     self.business_type = ''
    #     self.empolyees_working = ''
    #     # self.year = ''
    #     self.business_name = ''
    #     self.business_add = ''
        

    #    #Restore previously entered data if available
    # if self.business_type:
    #         self.drop_down_1.items = self.business_type
    # if self.empolyees_working:
    #        self.drop_down_2.items = self.empolyees_working
    # # if self.year:
    # #        self.date_picker_1.date = self.year

    # if self.business_name:
    #         self.text_box_1.text= self.business_name
    # if self.business_add:
    #         self.text_box_2.text= self.business_add

    options = app_tables.fin_lendor_business_type.search()
    options_string = [str(option['lendor_business_type']) for option in options]
    self.drop_down_12.items = options_string

  def validate_file(self, file):
        """Validate file type and size."""
        if file is None:
          return False, "No file uploaded."
    
        file_type = file.content_type
        file_size = len(file.get_bytes())  # Use len to get size in bytes
    
        if file_type not in ['image/jpeg','image/png','image/jpg', 'application/pdf']:
          return False, "Only JPG images and PDF files are allowed."
    
        if file_size > 2 * 1024 * 1024:  # 2MB limit
          return False, "File size must be less than 2MB."
    
        return True, ""

  def button_2_click(self, **event_args):
    business_name = self.text_box_2_copy.text
    business_add = self.text_box_1_copy.text
    business_type = self.drop_down_12.selected_value        
    empolyees_working = self.drop_down_4.selected_value
    year = self.date_picker_1.date
    industry_type = self.text_box_3.text
    turn_over = self.text_box_4.text
    last_six_statements = self.file_loader_1.file
    din = self.text_box_5.text
    cin = self.text_box_6.text
    reg_off_add = self.text_box_7.text
    proof_verification = self.file_loader_1_copy.file
       
    user_id = self.userId


    
     # Get today's date
    today = datetime.today()
    
    # Validation for Business
    if not re.match(r'^[A-Za-z\s]+$', business_name):
      alert('Enter valid business name')
    elif not business_name or not business_add or not business_type or not empolyees_working:
      Notification("Please fill all the fields").show()

    elif year and year.year > today.year:
      alert("The year cannot be in the future. Please select a valid year.", title="Invalid Year")
      return
    elif year and year.year == today.year and year.month > today.month:
      alert("The month cannot be in the future. Please select a valid month.", title="Invalid Month")
      return
    elif year and year.year == today.year and year.month == today.month and year.day > today.day:
      alert("The date cannot be in the future. Please select a valid date.", title="Invalid Date")
      return              
    elif not year or not industry_type or not turn_over or not last_six_statements:
      alert("Please fill all the fields", title="Missing Information")
    elif ' ' in cin:
      Notification("Spaces are not allowed in the CIN input").show()
      return    
    # DIN Validation
    elif ' ' in din:
      Notification("Spaces are not allowed in the DIN input").show()
      return
    # Other field validations
    elif not din or not cin or not reg_off_add or not proof_verification:
      Notification("Please fill all the fields").show()
    else:
      anvil.server.call('add_lendor_institutional_form_1',business_name,business_add,business_type,empolyees_working,user_id)
      months = (datetime.now().year - year.year) * 12 + (datetime.now().month - year.month)
      anvil.server.call('add_lendor_institutional_form_2', year, months, industry_type, turn_over, last_six_statements, user_id)
      anvil.server.call('add_lendor_institutional_form_3', din, cin, reg_off_add, proof_verification, user_id)
      open_form('lendor.lendor_registration_forms.lender_registration_form_3_marital_details',user_id=user_id)


   

  def button_1_click(self, **event_args):
    user_id = self.userId
    open_form('lendor.lendor_registration_forms.lender_registration_form_2',user_id = user_id)
    """This method is called when the button is clicked"""

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("bank_users.user_form")

  def file_loader_1(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    valid, message = self.validate_file(file)
    if valid:
          self.image_1.source = file
    else:
          Notification(message).show()
          self.file_loader_1.clear()


  def file_loader_1_copy(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    valid, message = self.validate_file(file)
    if valid:
          self.image_1_copy.source = file
    else:
          Notification(message).show()
          self.file_loader_1_copy.clear()
    
