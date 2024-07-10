# from ._anvil_designer import star_1_borrower_registration_form_2_employmentTemplate
# from anvil import *
# import anvil.server
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables
# import re
# from datetime import date, datetime

# class star_1_borrower_registration_form_2_employment(star_1_borrower_registration_form_2_employmentTemplate):
#     def __init__(self, user_id, **properties):
#         super().__init__(**properties)        
#         self.user_id = user_id
        
#         # Initialize all grid panels as invisible
#         self.column_panel_1.visible = False
#         self.column_panel_22.visible = False
#         self.column_panel_3.visible = False
#         self.column_panel_4.visible = False
#         self.column_panel_5.visible = False
        
#         # Fetch user data from the database
#         user_data = app_tables.fin_user_profile.get(customer_id=user_id)
        
#         if user_data:
#             # Populate form fields if user data exists
            
#             self.text_box_1_copy.text=user_data['company_name']
#             self.drop_down_3.selected_value=user_data['organization_type']
#             self.drop_down_1_copy.selected_value=user_data['employment_type']
#             self.drop_down_2_copy.selected_value = user_data['occupation_type']
#             self.text_box_1_copy_2.text=user_data['company_address']
#             self.text_box_3_copy.text=user_data['company_landmark']
#             self.text_box_2_copy.text=user_data['business_no']
#             self.text_box_1_copy_3.text=user_data['annual_salary']
#             self.text_box_2_copy_2.text=user_data['designation']
#             self.drop_down_1_copy_2.selected_value = user_data['salary_type']
          
#             self.text_box_1.text = user_data['business_add']
#             self.text_box_2.text = user_data['business_name']
#             self.drop_down_12.selected_value = user_data['business_type']
#             self.date_picker_1.date = user_data['year_estd']
#             self.text_box_3.text = user_data['industry_type']
#             self.text_box_4.text = user_data['six_month_turnover']      
          
#             self.text_box_5.text = user_data['din'].replace(' ', '') if 'din' in user_data else ''
#             self.text_box_6.text = user_data['cin'].replace(' ', '') if 'cin' in user_data else ''
#             self.text_box_7.text = user_data['registered_off_add'] if 'registered_off_add' in user_data else ''
          
#             self.borrower_college_name_text.text = user_data['college_name']
#             self.borrower_college_id_text.text=user_data['college_id']
#             self.borrower_college_address_text.text=user_data['college_address']
          
#             self.drop_down_1_copy_3.selected_value = user_data['land_type']
#             self.text_box_1_copy_4.text = str(user_data['total_acres'])  # Convert to string
#             self.text_box_2_copy_3.text = user_data['crop_name']
#             self.text_box_3_copy_2.text = user_data['farmer_earnings']

#             options_2 = app_tables.fin_borrower_land_type.search()
#             option_strings_2 = [str(option['land_type']) for option in options_2]
#             self.drop_down_1_copy_3.items = option_strings_2

#             options_1 = app_tables.fin_borrower_employee_type.search()
#             option_strings_1 = [str(option['borrower_employee_type']) for option in options_1]
#             self.drop_down_1_copy.items = option_strings_1
        
#                 # Populate drop_down_3 with data from 'organization_type' column
#             options_3 = app_tables.fin_borrower_organization_type.search()
#             option_strings_2 = [str(option['borrower_organization_type']) for option in options_3]
#             self.drop_down_3.items = option_strings_2
        
#             options_4 = app_tables.fin_occupation_type.search()
#             option_strings = [str(option['occupation_type']) for option in options_4]
#             self.drop_down_2_copy.items = option_strings

#             options_5 = app_tables.fin_borrower_salary_type.search()
#             option_strings = [str(option['borrower_salary_type']) for option in options_5]
#             self.drop_down_1_copy_2.items = option_strings

#             options_6 = app_tables.fin_borrower_business_type.search()
#             option_strings_1 = [str(option['borrower_business_type']) for option in options_6]
#             self.drop_down_12.items = option_strings_1
            
#             # Handle initial visibility based on user type
#             user_type = user_data['user_type'] if 'user_type' in user_data else ''
#             self.update_visibility(user_type)
#         else:
#             print(f"No user data found for user_id: {user_id}")
#             # Handle case where user_data is None or not found
        
#         # Set up event handler for dropdown change
#         self.drop_down_1.set_event_handler('change', self.drop_down_1_change_handler)
        
#         # Initialize visibility of components inside grid_panel_3
#         self.drop_down_2.visible = True
#         self.column_panel_4.visible = False
#         self.column_panel_5.visible = False
        
#         # Set up event handler for drop_down_2 change
#         self.drop_down_2.set_event_handler('change', self.drop_down_2_change_handler)

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
    
#     def update_visibility(self, user_type):
#         # Reset all grid panel visibilities
#         self.column_panel_1.visible = False
#         self.column_panel_22.visible = False
#         self.column_panel_3.visible = False
#         self.column_panel_4.visible = False
#         self.column_panel_5.visible = False
        
#         # Set visibility based on user_type
#         if user_type == 'Student':
#             self.column_panel_1.visible = True
#         elif user_type == 'Employee':
#             self.column_panel_22.visible = True
#         elif user_type == 'Self Employement':
#             self.column_panel_3.visible = True
#         else:
#             # Handle other user types or default case
#             pass
    
#     def drop_down_1_change_handler(self, **event_args):
#         selected_value = self.drop_down_1.selected_value
#         self.update_visibility(selected_value)
    
#     def drop_down_2_change_handler(self, **event_args):
#         selected_value = self.drop_down_2.selected_value
        
#         if selected_value == 'Business':  # Replace with your actual dropdown values
#             self.column_panel_4.visible = True
#             self.column_panel_5.visible = False
#         elif selected_value == 'Farmer':  # Replace with your actual dropdown values
#             self.column_panel_4.visible = False
#             self.column_panel_5.visible = True
#         else:
#             self.column_panel_4.visible = False
#             self.column_panel_5.visible = False

#         college_name=self.borrower_college_name_text.text
#         college_id=self.borrower_college_id_text.text
#         college_proof=self.borrower_college_proof_img.file
#         college_address=self.borrower_college_address_text.text
      
#         land_type = self.drop_down_1_copy_3.selected_value
#         total_acres = self.text_box_1_copy_4.text
#         crop_name = self.text_box_2_copy_3.text
#         farmer_earnings = self.text_box_3_copy_2.text

#         company_name = self.text_box_1_copy.text    
#         org_type = self.drop_down_3.selected_value
#         emp_type = self.drop_down_1_copy.selected_value
#         occupation_type = self.drop_down_2_copy.selected_value

#         comp_address = self.text_box_1_copy_2.text
#         landmark = self.text_box_3_copy.text
#         business_phone_number = self.text_box_2_copy.text

#         annual_salary = self.text_box_1_copy_3.text
#         designation = self.text_box_2_copy_2.text
#         emp_id_proof = self.file_loader_1_copy_2.file
#         last_six_month = self.file_loader_2.file
#         salary_type = self.drop_down_1_copy_2.selected_value

#         business_name = self.text_box_2.text
#         business_add = self.text_box_1.text
#         business_type = self.drop_down_12.selected_value        
#         empolyees_working = self.drop_down_4.selected_value
#         year = self.date_picker_1.date
#         industry_type = self.text_box_3.text
#         turn_over = self.text_box_4.text
#         last_six_statements = self.file_loader_1.file
#         din = self.text_box_5.text
#         cin = self.text_box_6.text
#         reg_off_add = self.text_box_7.text
#         proof_verification = self.file_loader_1_copy.file
#         # empolyees_working = self.drop_down_2.selected_value 
      
      
#         user_id=self.user_id
      
#         selected_value_drop_down_1 = self.drop_down_1.selected_value
#         selected_value_drop_down_2 = self.drop_down_2.selected_value
#         if selected_value_drop_down_1 == 'Student':
#           if not re.match(r'^[A-Za-z\s]+$', college_name):
#               alert('enter valid college name')
              
#           elif not college_name or not college_id or not college_proof or not college_address:
#               Notification("please fill all requrired fields").show()
#           else:
#               anvil.server.call('add_borrower_student',college_name,college_id,college_proof,college_address,user_id)
#               open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_3_marital',user_id=user_id)

#         elif selected_value_drop_down_1 == 'Employee':
#           if not re.match(r'^[A-Za-z\s]+$', company_name):
#               alert('Enter valid business name')
#           elif not company_name or not org_type or not emp_type or not occupation_type:
#               Notification("please fill the required fields ").show()                     
#           elif not business_phone_number.isdigit():
#               Notification("Business number should be valid").show()
#           elif not comp_address or not landmark or not business_phone_number:
#             Notification("please fill the required fields").show()              
#           elif not (annual_salary and designation and emp_id_proof and last_six_month and salary_type):
#             Notification("Please fill in all required fields.").show()
#           else:
#             anvil.server.call('add_lendor_individual_form_1', company_name,org_type,emp_type,occupation_type,user_id)
#             # open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_2',user_id=self.userId)
#             anvil.server.call('add_lendor_individual_form_2',comp_address,landmark,business_phone_number,user_id)
#             # open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_2_employment.star_1_borrower_registration_form_2_employment_emp_detail_3',user_id=user_id)
            
#             anvil.server.call('add_lendor_individual_form_3', annual_salary, designation, emp_id_proof, last_six_month, user_id,salary_type )
#             open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_3_marital', user_id=user_id)
        
#         elif selected_value_drop_down_1 == 'Self Employement':
#             # Validation for Self Employement
#             # Implement validation logic for Self Employement if needed
#             pass

#         # Get today's date
#         today = date.today()
#         if selected_value_drop_down_2 == 'Business':
#             # Validation for Business
#             if not re.match(r'^[A-Za-z\s]+$', business_name):
#               alert('Enter valid business name')
#             elif not business_name or not business_add or not business_type or not empolyees_working:
#                 Notification("Please fill all the fields").show()

#             elif year and year.year > today.year:
#               alert("The year cannot be in the future. Please select a valid year.", title="Invalid Year")
#               return
#             elif year and year.year == today.year and year.month > today.month:
#               alert("The month cannot be in the future. Please select a valid month.", title="Invalid Month")
#               return
#             elif year and year.year == today.year and year.month == today.month and year.day > today.day:
#               alert("The date cannot be in the future. Please select a valid date.", title="Invalid Date")
#               return              
#             elif not year or not industry_type or not turn_over or not last_six_statements:
#               alert("Please fill all the fields", title="Missing Information")
#             elif ' ' in cin:
#                 Notification("Spaces are not allowed in the CIN input").show()
#                 return    
#             # DIN Validation
#             elif ' ' in din:
#                 Notification("Spaces are not allowed in the DIN input").show()
#                 return
#             # Other field validations
#             elif not din or not cin or not reg_off_add or not proof_verification:
#                 Notification("Please fill all the fields").show()
#             else:
#               anvil.server.call('add_lendor_institutional_form_1',business_name,business_add,business_type,empolyees_working,user_id)
#               months = (datetime.now().year - year.year) * 12 + (datetime.now().month - year.month)
#               anvil.server.call('add_lendor_institutional_form_2', year, months, industry_type, turn_over, last_six_statements, user_id)
#               anvil.server.call('add_lendor_institutional_form_3', din, cin, reg_off_add, proof_verification, user_id)
#               open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_3_marital', user_id=user_id)

              
            
        
#         elif selected_value_drop_down_2 == 'Farmer':
#         # Validation for Farmer
#             if not re.match(r'^[A-Za-z\s]+$', crop_name):
#                 alert('Enter valid crop name')
#             elif not total_acres.isdigit():
#                 Notification("Acres of Land should be valid").show()
#             elif not farmer_earnings.isdigit():
#                 Notification("Yearly Income should be valid").show()
#             elif not crop_name or not total_acres or not farmer_earnings:
#                 Notification("Please fill all the fields").show()
#             else:
#                 anvil.server.call('add_borrower_farmer', land_type, total_acres, crop_name, farmer_earnings, user_id)
  
#     def button_1_click(self, **event_args):
#       """This method is called when the button is clicked"""
#       open_form('borrower.borrower_registration_forms.borrower_registration_form_1_education')

#     def button_1_next_click(self, **event_args):
#       """This method is called when the button is clicked"""
#       open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_3_marital')

  
#     def borrower_college_proof_img_change(self, file, **event_args):
#         """This method is called when a new file is loaded into this FileLoader"""
#         valid, message = self.validate_file(file)
#         if valid:
#           self.image_1_copy_2.source = file
#         else:
#           Notification(message).show()
#           self.borrower_college_proof_img.clear()

#     def file_loader_1_change(self, file, **event_args):
#         """This method is called when a new file is loaded into this FileLoader"""
#         valid, message = self.validate_file(file)
#         if valid:
#           self.image_1_copy_3.source = file
#         else:
#           Notification(message).show()
#           self.file_loader_1_copy_2.clear()

#     def file_loader_2_change(self, file, **event_args):
#         """This method is called when a new file is loaded into this FileLoader"""
#         valid, message = self.validate_file(file)
#         if valid:
#           self.image_2.source = file
#         else:
#           Notification(message).show()
#           self.file_loader_2.clear()

#     def file_loader_1(self, file, **event_args):
#         """This method is called when a new file is loaded into this FileLoader"""
#         valid, message = self.validate_file(file)
#         if valid:
#           self.image_1.source = file
#         else:
#           Notification(message).show()
#           self.file_loader_1.clear()

#     def file_loader_1_copy(self, file, **event_args):
#         """This method is called when a new file is loaded into this FileLoader"""
#         valid, message = self.validate_file(file)
#         if valid:
#           self.image_1_copy.source = file
#         else:
#           Notification(message).show()
#           self.file_loader_1_copy.clear()



from ._anvil_designer import star_1_borrower_registration_form_2_employmentTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re
from datetime import date, datetime

class star_1_borrower_registration_form_2_employment(star_1_borrower_registration_form_2_employmentTemplate):
    def __init__(self, user_id, **properties):
        # super().__init__(**properties)        
        self.user_id = user_id
        
        # Initialize all grid panels as invisible
        self.column_panel_1.visible = False
        self.column_panel_22.visible = False
        self.column_panel_3.visible = False
        self.column_panel_4.visible = False
        self.column_panel_5.visible = False
        
        # Fetch user data from the database
        user_data = app_tables.fin_user_profile.get(customer_id=user_id)
        
        if user_data:
            # Populate form fields if user data exists
            
            self.text_box_1_copy.text=user_data['company_name']
            self.drop_down_3.selected_value=user_data['organization_type']
            self.drop_down_1_copy.selected_value=user_data['employment_type']
            self.drop_down_2_copy.selected_value = user_data['occupation_type']
            self.text_box_1_copy_2.text=user_data['company_address']
            self.text_box_3_copy.text=user_data['company_landmark']
            self.text_box_2_copy.text=user_data['business_no']
            self.text_box_1_copy_3.text=user_data['annual_salary']
            self.text_box_2_copy_2.text=user_data['designation']
            self.drop_down_1_copy_2.selected_value = user_data['salary_type']
          
            self.text_box_1.text = user_data['business_add']
            self.text_box_2.text = user_data['business_name']
            self.drop_down_12.selected_value = user_data['business_type']
            self.date_picker_1.date = user_data['year_estd']
            self.text_box_3.text = user_data['industry_type']
            self.text_box_4.text = user_data['six_month_turnover']      
          
            self.text_box_5.text = user_data['din'].replace(' ', '') if 'din' in user_data else ''
            self.text_box_6.text = user_data['cin'].replace(' ', '') if 'cin' in user_data else ''
            self.text_box_7.text = user_data['registered_off_add'] if 'registered_off_add' in user_data else ''
          
            self.borrower_college_name_text.text = user_data['college_name']
            self.borrower_college_id_text.text=user_data['college_id']
            self.borrower_college_address_text.text=user_data['college_address']
          
            self.drop_down_1_copy_3.selected_value = user_data['land_type']
            self.text_box_1_copy_4.text = str(user_data['total_acres'])  # Convert to string
            self.text_box_2_copy_3.text = user_data['crop_name']
            self.text_box_3_copy_2.text = user_data['farmer_earnings']

            options_2 = app_tables.fin_borrower_land_type.search()
            option_strings_2 = [str(option['land_type']) for option in options_2]
            self.drop_down_1_copy_3.items = option_strings_2

            options_1 = app_tables.fin_borrower_employee_type.search()
            option_strings_1 = [str(option['borrower_employee_type']) for option in options_1]
            self.drop_down_1_copy.items = option_strings_1
        
            # Populate drop_down_3 with data from 'organization_type' column
            options_3 = app_tables.fin_borrower_organization_type.search()
            option_strings_2 = [str(option['borrower_organization_type']) for option in options_3]
            self.drop_down_3.items = option_strings_2
        
            options_4 = app_tables.fin_occupation_type.search()
            option_strings = [str(option['occupation_type']) for option in options_4]
            self.drop_down_2_copy.items = option_strings

            options_5 = app_tables.fin_borrower_salary_type.search()
            option_strings = [str(option['borrower_salary_type']) for option in options_5]
            self.drop_down_1_copy_2.items = option_strings

            options_6 = app_tables.fin_borrower_business_type.search()
            option_strings_1 = [str(option['borrower_business_type']) for option in options_6]
            self.drop_down_12.items = option_strings_1
            
            # Handle initial visibility based on user type
            user_type = user_data['user_type'] if 'user_type' in user_data else ''
            self.update_visibility(user_type)
        else:
            print(f"No user data found for user_id: {user_id}")
            # Handle case where user_data is None or not found
        
        # Set up event handler for dropdown change
        self.drop_down_1.set_event_handler('change', self.drop_down_1_change_handler)
        
        # Initialize visibility of components inside grid_panel_3
        self.drop_down_2.visible = True
        self.column_panel_4.visible = False
        self.column_panel_5.visible = False
        
        # Set up event handler for drop_down_2 change
        self.drop_down_2.set_event_handler('change', self.drop_down_2_change_handler)

    def validate_file_upload(self, **event_args):
        file_loader = event_args['sender']
        file = file_loader.file
        max_size = 2 * 1024 * 1024  # 2MB in bytes
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf']
    
        if file:
            file_size = len(file.get_bytes())
            if file_size > max_size:
                alert('File size should be less than 2MB')
                file_loader.clear()
                return
    
            if file.content_type not in allowed_types:
                alert('Invalid file type. Only JPEG, PNG, jpg and PDF are allowed')
                file_loader.clear()
                return
    
    def update_visibility(self, user_type):
        # Reset all grid panel visibilities
        self.column_panel_1.visible = False
        self.column_panel_22.visible = False
        self.column_panel_3.visible = False
        self.column_panel_4.visible = False
        self.column_panel_5.visible = False
        
        # Set visibility based on user_type
        if user_type == 'Student':
            self.column_panel_1.visible = True
        elif user_type == 'Employee':
            self.column_panel_22.visible = True
        elif user_type == 'Self Employement':
            self.column_panel_3.visible = True
        else:
            # Handle other user types or default case
            pass
    
    def drop_down_1_change_handler(self, **event_args):
        selected_value = self.drop_down_1.selected_value
        self.update_visibility(selected_value)
    
    def drop_down_2_change_handler(self, **event_args):
        selected_value = self.drop_down_2.selected_value
        
        if selected_value == 'Business':  # Replace with your actual dropdown values
            self.column_panel_4.visible = True
            self.column_panel_5.visible = False
        elif selected_value == 'Farmer':  # Replace with your actual dropdown values
            self.column_panel_4.visible = False
            self.column_panel_5.visible = True
        else:
            self.column_panel_4.visible = False
            self.column_panel_5.visible = False

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower.borrower_registration_forms.borrower_registration_form_1_education')

    def button_1_next_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower.borrower_registration_forms.star_1_borrower_registration_form_3_marital')

  
    def borrower_college_proof_img_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        valid, message = self.validate_file(file)
        if valid:
          self.image_1_copy_2.source = file
        else:
          Notification(message).show()
          self.borrower_college_proof_img.clear()

    def file_loader_1_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        valid, message = self.validate_file(file)
        if valid:
          self.image_1_copy_3.source = file
        else:
          Notification(message).show()
          self.file_loader_1_copy_2.clear()

    def file_loader_2_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        valid, message = self.validate_file(file)
        if valid:
          self.image_2.source = file
        else:
          Notification(message).show()
          self.file_loader_2.clear()

    def file_loader_1(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file:
            self.user_photo_file_name.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_profile.source = self.registration_img_file_loader.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_profile.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.registration_img_file_loader.clear()




    

    

    
