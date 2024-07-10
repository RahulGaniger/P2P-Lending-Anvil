from ._anvil_designer import lender_registration_individual_form_3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class lender_registration_individual_form_3(lender_registration_individual_form_3Template):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.text_box_1.text=user_data['annual_salary']
      self.text_box_2.text=user_data['designation']
      self.drop_down_1.selected_value = user_data['salary_type']
      
      user_data.update()
    # user_data = anvil.server.call('get_user_data', user_id)
        
    # if user_data:
    #         self.annual_salary = user_data.get('annual_salary', '')
    #         self.salary_type = user_data.get('salary_type', '')
    #         self.designation = user_data.get('designation', '')
     
    # else:
    #     self.annual_salary = ''
    #     self.salary_type = ''
    #     self.designation = ''

    #    #Restore previously entered data if available
    # if self.annual_salary:
    #    self.text_box_1.text= self.annual_salary
    # if self.salary_type:
    #    self.drop_down_1.selected_value = self.salary_type
    # if self.designation:
    #    self.text_box_2.text= self.designation

    options = app_tables.fin_lendor_salary_type.search()
    option_strings = [str(option['lendor_salary_type']) for option in options]
    self.drop_down_1.items = option_strings


  def button_2_click(self, **event_args):
    #self.userId = user_id
    open_form('lendor.lendor_registration_forms.lender_registration_form_2.lender_registration_individual_form_2',user_id=self.userId)
    

  def button_1_click(self, **event_args):
      annual_salary = self.text_box_1.text
      designation = self.text_box_2.text
      emp_id_proof = self.file_loader_1.file
      last_six_month = self.file_loader_2.file
      user_id = self.userId
      salary_type = self.drop_down_1.selected_value
      
      # Validation: Check if any of the required fields is empty
      if not annual_salary or not designation or not emp_id_proof or not last_six_month or not salary_type:
        Notification("Please fill all the required fields").show()
      elif ' ' in annual_salary:
        Notification("Annual Salary should not contain spaces").show()  
      else:
        # Validation: Check if the uploaded files are not empty
        if not emp_id_proof or not last_six_month:
          Notification("Please upload all required documents").show()
        else:
          anvil.server.call('add_lendor_individual_form_3', annual_salary, designation, emp_id_proof, last_six_month, user_id, salary_type)
          open_form('lendor.lendor_registration_forms.lender_registration_form_3_marital_details', user_id=self.userId)
  
  def button_3_click(self, **event_args):
    open_form("bank_users.user_form")
