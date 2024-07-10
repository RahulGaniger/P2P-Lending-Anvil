# from ._anvil_designer import lender_registration_individual_form_1Template
# from anvil import *
# import anvil.server
# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables
# import re

# class lender_registration_individual_form_1(lender_registration_individual_form_1Template):
#   def __init__(self,user_id, **properties):
#     self.userId = user_id
#     user_id = int(user_id)
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)
#     user_data=app_tables.fin_user_profile.get(customer_id=user_id)
#     if user_data:
#       self.text_box_1_copy.text=user_data['company_name']
#       self.drop_down_3_copy.selected_value=user_data['organization_type']
#       self.drop_down_1_copy.selected_value=user_data['employment_type']
#       self.drop_down_2_copy.selected_value = user_data['occupation_type']
#       self.text_box_1_copy_2.text=user_data['company_address']
#       self.text_box_3_copy.text=user_data['company_landmark']
#       self.text_box_2_copy.text=user_data['business_no']
#       self.text_box_1_copy_3.text=user_data['annual_salary']
#       self.text_box_2_copy_2.text=user_data['designation']
#       self.drop_down_1_copy_2.selected_value = user_data['salary_type']
#       user_data.update()

#     def validate_file(self, file):
#         """Validate file type and size."""
#         if file is None:
#           return False, "No file uploaded."
    
#         file_type = file.content_type
#         file_size = len(file.get_bytes())  # Use len to get size in bytes
    
#         if file_type not in ['image/jpeg','image/png','image/jpg', 'application/pdf']:
#           return False, "Only JPG images and PDF files are allowed."
    
#         if file_size > 2 * 1024 * 1024:  # 2MB limit
#           return False, "File size must be less than 2MB."
    
#         return True, ""
    
    
#     options = app_tables.fin_lendor_employee_type.search()
#     options_string = [str(option['lendor_employee_type']) for option in options]
#     self.drop_down_1_copy.items = options_string

#     options = app_tables.fin_lendor_organization_type.search()
#     options_string = [str(option['lendor_organization_type']) for option in options]
#     self.drop_down_3_copy.items = options_string

#     options = app_tables.fin_occupation_type.search()
#     option_strings = [str(option['occupation_type']) for option in options]
#     self.drop_down_2_copy.items = option_strings
#     # Any code you write here will run before the form opens.

#     options_5 = app_tables.fin_lendor_salary_type.search()
#     option_strings = [str(option['lendor_salary_type']) for option in options_5]
#     self.drop_down_1_copy_2.items = option_strings

#   def button_2_click(self, **event_args):      
#       company_name = self.text_box_1_copy.text    
#       org_type = self.drop_down_3.selected_value
#       emp_type = self.drop_down_1_copy.selected_value
#       occupation_type = self.drop_down_2_copy.selected_value
#       comp_address = self.text_box_1_copy_2.text
#       landmark = self.text_box_3_copy.text
#       business_phone_number = self.text_box_2_copy.text

#       annual_salary = self.text_box_1_copy_3.text
#       designation = self.text_box_2_copy_2.text
#       emp_id_proof = self.file_loader_1.file
#       last_six_month = self.file_loader_2.file
#       salary_type = self.drop_down_1_copy_2.selected_value
    
#       if not re.match(r'^[A-Za-z\s]+$', company_name):
#               alert('Enter valid business name')
#       elif not company_name or not org_type or not emp_type or not occupation_type:
#               Notification("please fill the required fields ").show()                     
#       elif not business_phone_number.isdigit():
#               Notification("Business number should be valid").show()
#       elif not comp_address or not landmark or not business_phone_number:
#             Notification("please fill the required fields").show()              
#       elif not (annual_salary and designation and emp_id_proof and last_six_month and salary_type):
#             Notification("Please fill in all required fields.").show()
#       else:
#             anvil.server.call('add_lendor_individual_form_1', company_name,org_type,emp_type,occupation_type,user_id)
#             # open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_2',user_id=self.userId)
#             anvil.server.call('add_lendor_individual_form_2',comp_address,landmark,business_phone_number,user_id)
#             # open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_3',user_id=user_id)
            
#             anvil.server.call('add_lendor_individual_form_3', annual_salary, designation, emp_id_proof, last_six_month, user_id,salary_type )
#             open_form('lendor.lendor_registration_forms.lender_registration_form_3_marital_details', user_id=self.userId)
    
#   def button_1_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     user_id = self.userId
#     open_form('lendor.lendor_registration_forms.lender_registration_form_2',user_id = user_id)

  
#   def button_3_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     open_form("bank_users.user_form")

#   def file_loader_1_change(self, file, **event_args):
#         """This method is called when a new file is loaded into this FileLoader"""
#         valid, message = self.validate_file(file)
#         if valid:
#             self.image_1_copy_3.source = file
#         else:
#             Notification(message).show()
#             self.file_loader_1_copy_2.clear()

#   def file_loader_2_change(self, file, **event_args):
#         """This method is called when a new file is loaded into this FileLoader"""
#         valid, message = self.validate_file(file)
#         if valid:
#             self.image_2.source = file
#         else:
#             Notification(message).show()
#             self.file_loader_2.clear()


  
from ._anvil_designer import lender_registration_individual_form_1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re

# class lender_registration_individual_form_1(lender_registration_individual_form_1Template):
#     def __init__(self, user_id, **properties):
#         self.userId = user_id
#         user_id = int(user_id)
#         # Set Form properties and Data Bindings.
#         self.init_components(**properties)
#         user_data = app_tables.fin_user_profile.get(customer_id=user_id)
#         if user_data:
#             self.text_box_1_copy.text = user_data['company_name']
#             self.drop_down_3_copy.selected_value = user_data['organization_type']
#             self.drop_down_1_copy.selected_value = user_data['employment_type']
#             self.drop_down_2_copy.selected_value = user_data['occupation_type']
#             self.text_box_1_copy_2.text = user_data['company_address']
#             self.text_box_3_copy.text = user_data['company_landmark']
#             self.text_box_2_copy.text = user_data['business_no']
#             self.text_box_1_copy_3.text = user_data['annual_salary']
#             self.text_box_2_copy_2.text = user_data['designation']
#             self.drop_down_1_copy_2.selected_value = user_data['salary_type']
#             user_data.update()

#         options = app_tables.fin_lendor_employee_type.search()
#         options_string = [str(option['lendor_employee_type']) for option in options]
#         self.drop_down_1_copy.items = options_string

#         options = app_tables.fin_lendor_organization_type.search()
#         options_string = [str(option['lendor_organization_type']) for option in options]
#         self.drop_down_3_copy.items = options_string

#         options = app_tables.fin_occupation_type.search()
#         option_strings = [str(option['occupation_type']) for option in options]
#         self.drop_down_2_copy.items = option_strings

#         options_5 = app_tables.fin_lendor_salary_type.search()
#         option_strings = [str(option['lendor_salary_type']) for option in options_5]
#         self.drop_down_1_copy_2.items = option_strings

#     def validate_file(self, file):
#         """Validate file type and size."""
#         if file is None:
#             return False, "No file uploaded."
    
#         file_type = file.content_type
#         file_size = len(file.get_bytes())  # Use len to get size in bytes
    
#         if file_type not in ['image/jpeg','image/png','image/jpg', 'application/pdf']:
#             return False, "Only JPG images and PDF files are allowed."
    
#         if file_size > 2 * 1024 * 1024:  # 2MB limit
#             return False, "File size must be less than 2MB."
    
#         return True, ""

#     def button_2_click(self, **event_args):      
#         company_name = self.text_box_1_copy.text    
#         org_type = self.drop_down_3_copy.selected_value
#         emp_type = self.drop_down_1_copy.selected_value
#         occupation_type = self.drop_down_2_copy.selected_value
#         comp_address = self.text_box_1_copy_2.text
#         landmark = self.text_box_3_copy.text
#         business_phone_number = self.text_box_2_copy.text

#         annual_salary = self.text_box_1_copy_3.text
#         designation = self.text_box_2_copy_2.text
#         emp_id_proof = self.file_loader_1.file
#         last_six_month = self.file_loader_2.file
#         salary_type = self.drop_down_1_copy_2.selected_value
    
#         if not re.match(r'^[A-Za-z\s]+$', company_name):
#             alert('Enter valid business name')
#         elif not company_name or not org_type or not emp_type or not occupation_type:
#             Notification("please fill the required fields ").show()                     
#         elif not business_phone_number.isdigit():
#             Notification("Business number should be valid").show()
#         elif not comp_address or not landmark or not business_phone_number:
#             Notification("please fill the required fields").show()              
#         elif not (annual_salary and designation and emp_id_proof and last_six_month and salary_type):
#             Notification("Please fill in all required fields.").show()
#         else:
#             anvil.server.call('add_lendor_individual_form_1', company_name, org_type, emp_type, occupation_type, user_id)
#             anvil.server.call('add_lendor_individual_form_2', comp_address, landmark, business_phone_number, user_id)
#             anvil.server.call('add_lendor_individual_form_3', annual_salary, designation, emp_id_proof, last_six_month, user_id, salary_type)
#             open_form('lendor.lendor_registration_forms.lender_registration_form_3_marital_details', user_id=self.userId)
    
#     def button_1_click(self, **event_args):
#         """This method is called when the button is clicked"""
#         user_id = self.userId
#         open_form('lendor.lendor_registration_forms.lender_registration_form_2', user_id=user_id)

#     def button_3_click(self, **event_args):
#         """This method is called when the button is clicked"""
#         open_form("bank_users.user_form")

#     def file_loader_1_change(self, file, **event_args):
#         """This method is called when a new file is loaded into this FileLoader"""
#         valid, message = self.validate_file(file)
#         if valid:
#             self.image_1_copy_3.source = file
#         else:
#             Notification(message).show()
#             self.file_loader_1_copy_2.clear()

#     def file_loader_2_change(self, file, **event_args):
#         """This method is called when a new file is loaded into this FileLoader"""
#         valid, message = self.validate_file(file)
#         if valid:
#             self.image_2.source = file
#         else:
#             Notification(message).show()
#             self.file_loader_2.clear()

class lender_registration_individual_form_1(lender_registration_individual_form_1Template):
    def __init__(self, user_id, **properties):
        self.userId = user_id
        user_id = int(user_id)
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        user_data = app_tables.fin_user_profile.get(customer_id=user_id)
        if user_data:
            self.text_box_1_copy.text = user_data['company_name']
            self.drop_down_3_copy.selected_value = user_data['organization_type']
            self.drop_down_1_copy.selected_value = user_data['employment_type']
            self.drop_down_2_copy.selected_value = user_data['occupation_type']
            self.text_box_1_copy_2.text = user_data['company_address']
            self.text_box_3_copy.text = user_data['company_landmark']
            self.text_box_2_copy.text = user_data['business_no']
            self.text_box_1_copy_3.text = user_data['annual_salary']
            self.text_box_2_copy_2.text = user_data['designation']
            self.drop_down_1_copy_2.selected_value = user_data['salary_type']
            # Note: Removed unnecessary user_data.update() here

        options = app_tables.fin_lendor_employee_type.search()
        options_string = [str(option['lendor_employee_type']) for option in options]
        self.drop_down_1_copy.items = options_string

        options = app_tables.fin_lendor_organization_type.search()
        options_string = [str(option['lendor_organization_type']) for option in options]
        self.drop_down_3_copy.items = options_string

        options = app_tables.fin_occupation_type.search()
        option_strings = [str(option['occupation_type']) for option in options]
        self.drop_down_2_copy.items = option_strings

        options_5 = app_tables.fin_lendor_salary_type.search()
        option_strings = [str(option['lendor_salary_type']) for option in options_5]
        self.drop_down_1_copy_2.items = option_strings

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
        company_name = self.text_box_1_copy.text    
        org_type = self.drop_down_3_copy.selected_value
        emp_type = self.drop_down_1_copy.selected_value
        occupation_type = self.drop_down_2_copy.selected_value
        comp_address = self.text_box_1_copy_2.text
        landmark = self.text_box_3_copy.text
        business_phone_number = self.text_box_2_copy.text

        annual_salary = self.text_box_1_copy_3.text
        designation = self.text_box_2_copy_2.text
        emp_id_proof = self.file_loader_1.file
        last_six_month = self.file_loader_2.file
        salary_type = self.drop_down_1_copy_2.selected_value
    
        if not re.match(r'^[A-Za-z\s]+$', company_name):
            alert('Enter valid business name')
        elif not company_name or not org_type or not emp_type or not occupation_type:
            Notification("please fill the required fields ").show()                     
        elif not business_phone_number.isdigit():
            Notification("Business number should be valid").show()
        elif not comp_address or not landmark or not business_phone_number:
            Notification("please fill the required fields").show()              
        elif not (annual_salary and designation and emp_id_proof and last_six_month and salary_type):
            Notification("Please fill in all required fields.").show()
        else:
            anvil.server.call('add_lendor_individual_form_1', company_name, org_type, emp_type, occupation_type, self.userId)
            anvil.server.call('add_lendor_individual_form_2', comp_address, landmark, business_phone_number, self.userId)
            anvil.server.call('add_lendor_individual_form_3', annual_salary, designation, emp_id_proof, last_six_month, self.userId, salary_type)
            open_form('lendor.lendor_registration_forms.lender_registration_form_3_marital_details', user_id=self.userId)
    
    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('lendor.lendor_registration_forms.lender_registration_form_2', user_id=self.userId)

    def button_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form("bank_users.user_form")

    def file_loader_1_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        valid, message = self.validate_file(file)
        if valid:
            self.image_1.source = file
        else:
            Notification(message).show()
            self.file_loader_1.clear()

    def file_loader_2_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        valid, message = self.validate_file(file)
        if valid:
            self.image_2.source = file
        else:
            Notification(message).show()
            self.file_loader_2.clear()






 
    

