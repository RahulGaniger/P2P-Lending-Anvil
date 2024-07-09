from ._anvil_designer import basic_registration_formTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta
from .. import main_form
from .. import main_form_module
from ...user_form import user_module
import re


class basic_registration_form(basic_registration_formTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.email = main_form_module.email
        email = self.email
        self.user_id = user_module.find_user_id(email)
        print(self.user_id)
        self.load_form_state()

        user_id = self.user_id
        user_data = app_tables.fin_user_profile.get(customer_id=user_id)
        if user_data:
            self.full_name_text_box.text = user_data['full_name']
            self.gender_dd.selected_value = user_data['gender']
            self.date_picker_1.date = datetime.strptime(user_data['date_of_birth'], '%Y-%m-%d').date() if user_data['date_of_birth'] else None
            self.mobile_number_box.text = user_data['mobile']
            self.alternate_email_text_box.text = user_data['another_email']
            self.govt_id1_text_box.text = user_data['aadhaar_no']
            self.govt_id2_text_box.text = user_data['pan_number']
            self.text_box_1.text = user_data['street_adress_1']
            self.text_box_2.text = user_data['street_address_2']
            self.text_box_3.text = user_data['city']
            self.text_box_4.text = user_data['pincode']
            self.text_box_5.text = user_data['state']
            self.text_box_6.text = user_data['country']
            self.drop_down_1.selected_value = user_data['present_address']
            self.drop_down_2.selected_value = user_data['duration_at_address']
            user_data.update()

        options = app_tables.fin_gender.search()
        option_strings = [str(option['gender']) for option in options]
        self.gender_dd.items = option_strings

        options = app_tables.fin_present_address.search()
        option_strings = [str(option['present_address']) for option in options]
        self.drop_down_1.items = option_strings

        options = app_tables.fin_duration_at_address.search()
        option_strings = [str(option['duration_at_address']) for option in options]
        self.drop_down_2.items = option_strings

        # Add event handlers for real-time validation
        self.full_name_text_box.add_event_handler('change', self.validate_full_name)
        self.date_picker_1.add_event_handler('change', self.validate_dob)
        self.mobile_number_box.add_event_handler('change', self.validate_mobile_no)
        self.alternate_email_text_box.add_event_handler('change', self.validate_alternate_email)
        self.text_box_3.add_event_handler('change', self.validate_city)
        self.text_box_5.add_event_handler('change', self.validate_state)
        self.text_box_6.add_event_handler('change', self.validate_country)
        self.text_box_4.add_event_handler('change', self.validate_zip)
        self.govt_id1_text_box.add_event_handler('change', self.toggle_upload_buttons)
        self.govt_id2_text_box.add_event_handler('change', self.toggle_upload_buttons1)
        # Add event handlers for file upload validation
        self.registration_img_file_loader.add_event_handler('change', self.validate_file_upload)
        self.registration_img_aadhar_file_loader.add_event_handler('change', self.validate_file_upload)
        self.registration_img_pan_file_loader.add_event_handler('change', self.validate_file_upload)

    def validate_full_name(self, **event_args):
        full_name = self.full_name_text_box.text
        if re.match(r'^[A-Za-z\s]+$', full_name):
            self.full_name_text_box.background = None
        else:
            self.full_name_text_box.background = '#FF0000'  # Red background for invalid input
            
    def validate_zip(self, **event_args):
        zip = self.text_box_4.text
        if re.match(r'^\d+$', zip):
            self.text_box_4.background = None
        else:
            self.text_box_4.background = '#FF0000'
        
    def validate_dob(self, **event_args):
        dob = self.date_picker_1.date.strftime('%Y-%m-%d') if self.date_picker_1.date else None
        if dob and datetime.strptime(dob, '%Y-%m-%d').date() <= datetime.now().date():
            self.date_picker_1.background = None
        else:
            self.date_picker_1.background = '#FF0000'  # Red background for invalid input

    def validate_mobile_no(self, **event_args):
        mobile_no = self.mobile_number_box.text
        if re.match(r'^\d{10}$', mobile_no):
            self.mobile_number_box.background = None
        else:
            self.mobile_number_box.background = '#FF0000'  # Red background for invalid input

    def validate_alternate_email(self, **event_args):
        alternate_email = self.alternate_email_text_box.text
        if alternate_email:  # Check if the field is not empty
            if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', alternate_email):
                self.alternate_email_text_box.background = None  # Reset background for valid input
            else:
                self.alternate_email_text_box.background = '#FF0000'  # Red background for invalid input
        else:
            self.alternate_email_text_box.background = None  # Reset background if the field is empty


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

    def validate_city(self, **event_args):
        city = self.text_box_3.text
        if re.match(r'^[A-Za-z]+$', city):
            self.text_box_3.background = None
        else:
            self.text_box_3.background = '#FF0000'  # Red background for invalid input

    def validate_state(self, **event_args):
        state = self.text_box_5.text
        if re.match(r'^[A-Za-z]+$', state):
            self.text_box_5.background = None
        else:
            self.text_box_5.background = '#FF0000'  # Red background for invalid input

    def validate_country(self, **event_args):
        country = self.text_box_6.text
        if re.match(r'^[A-Za-z]+$', country):
            self.text_box_6.background = None
        else:
            self.text_box_6.background = '#FF0000 ' # Red background for invalid 

    def toggle_upload_buttons(self, **event_args):
        # Show the upload buttons if govt_id1_text_box is not empty
        self.label_3_copy_1_copy_2.visible = bool(self.govt_id1_text_box.text)
        self.registration_img_aadhar_file_loader.visible = bool(self.govt_id1_text_box.text)
        self.image_aadhar.visible = bool(self.govt_id1_text_box.text)
        
    def toggle_upload_buttons1(self, **event_args):
        # Show the upload buttons if govt_id2_text_box is not empty
        self.label_3_copy_1_copy_4.visible = bool(self.govt_id1_text_box.text)
        self.registration_img_pan_file_loader.visible = bool(self.govt_id1_text_box.text)
        self.image_pan.visible = bool(self.govt_id1_text_box.text)
        
    def save_form_state(self):
        form_state = {
            'full_name': self.full_name_text_box.text,
            'gender': self.gender_dd.selected_value,
            'dob': self.date_picker_1.date,
            'mobile_no': self.mobile_number_box.text,
            'alternate_email': self.alternate_email_text_box.text,
            'aadhar': self.govt_id1_text_box.text,
            'pan': self.govt_id2_text_box.text,
            'street_adress_1': self.text_box_1.text,
            'street_address_2': self.text_box_2.text,
            'city': self.text_box_3.text,
            'pincode': self.text_box_4.text,
            'state': self.text_box_5.text,
            'country': self.text_box_6.text,
            'present_address': self.drop_down_1.selected_value,
            'duration_at_address': self.drop_down_2.selected_value,
        }
        anvil.server.session['basic_registration_form_state'] = form_state

    def load_form_state(self):
        form_state = anvil.server.session.get('basic_registration_form_state', {})
        self.full_name_text_box.text = form_state.get('full_name', '')
        self.gender_dd.selected_value = form_state.get('gender', '')
        self.date_picker_1.date = form_state.get('dob', None)
        self.mobile_number_box.text = form_state.get('mobile_no', '')
        self.alternate_email_text_box.text = form_state.get('alternate_email', '')
        self.govt_id1_text_box.text = form_state.get('aadhar', '')
        self.govt_id2_text_box.text = form_state.get('pan', '')
        self.text_box_1.text = form_state.get('street_adress_1', '')
        self.text_box_2.text = form_state.get('street_address_2', '')
        self.text_box_3.text = form_state.get('city', '')
        self.text_box_4.text = form_state.get('pincode', '')
        self.text_box_5.text = form_state.get('state', '')
        self.text_box_6.text = form_state.get('country', '')
        self.drop_down_1.selected_value = form_state.get('present_address', '')
        self.drop_down_2.selected_value = form_state.get('duration_at_address', '')

    def submit_button_click(self, **event_args):
        # Save the form state before submitting
        self.save_form_state()

        full_name = self.full_name_text_box.text
        gender = self.gender_dd.selected_value
        dob = self.date_picker_1.date.strftime('%Y-%m-%d') if self.date_picker_1.date else None
        mobile_no = self.mobile_number_box.text
        alternate_email = self.alternate_email_text_box.text
        aadhar = self.govt_id1_text_box.text
        pan = self.govt_id2_text_box.text
        street_address1 = self.text_box_1.text
        street_address2 = self.text_box_2.text
        city = self.text_box_3.text
        pincode = self.text_box_4.text
        state = self.text_box_5.text
        country = self.text_box_6.text
        present_address = self.drop_down_1.selected_value
        duration_at_address = self.drop_down_2.selected_value
        
        # Create a dictionary to store the data
        form_data = {
            'full_name': full_name,
            'gender': gender,
            'date_of_birth': dob,
            'mobile': mobile_no,
            'another_email': alternate_email,
            'aadhaar_no': aadhar,
            'pan_number': pan,
            'street_adress_1': street_address1,
            'street_address_2': street_address2,
            'city': city,
            'pincode': pincode,
            'state': state,
            'country': country,
            'present_address': present_address,
            'duration_at_address': duration_at_address,
        }
        
        # Call the server function with the dictionary
        anvil.server.call('create_or_update_profile', form_data)
        
        # Optionally, provide feedback to the user
        alert("Profile updated successfully!")

        # Navigate to the user form or any other form as needed
        open_form('user_form')

        # Code to execute the button click event
        full_name = self.full_name_text_box.text
        gender = self.gender_dd.selected_value
        dob = self.date_picker_1.date.strftime('%Y-%m-%d') if self.date_picker_1.date else None
        mobile_no = self.mobile_number_box.text
        alternate_email = self.alternate_email_text_box.text
        aadhar = self.govt_id1_text_box.text
        pan = self.govt_id2_text_box.text
        street_address1 = self.text_box_1.text
        street_address2 = self.text_box_2.text
        city = self.text_box_3.text
        pincode = self.text_box_4.text
        state = self.text_box_5.text
        country = self.text_box_6.text
        present_address = self.drop_down_1.selected_value
        duration_at_address = self.drop_down_2.selected_value

        # Insert or update the data in the Anvil Data Table
        user_id = self.user_id
        user_data = app_tables.fin_user_profile.get(customer_id=user_id)
        if user_data:
            user_data.update(
                full_name=full_name,
                gender=gender,
                date_of_birth=dob,
                mobile=mobile_no,
                another_email=alternate_email,
                aadhaar_no=aadhar,
                pan_number=pan,
                street_adress_1=street_address1,
                street_address_2=street_address2,
                city=city,
                pincode=pincode,
                state=state,
                country=country,
                present_address=present_address,
                duration_at_address=duration_at_address
            )
        else:
            app_tables.fin_user_profile.add_row(
                customer_id=user_id,
                full_name=full_name,
                gender=gender,
                date_of_birth=dob,
                mobile=mobile_no,
                another_email=alternate_email,
                aadhaar_no=aadhar,
                pan_number=pan,
                street_adress_1=street_address1,
                street_address_2=street_address2,
                city=city,
                pincode=pincode,
                state=state,
                country=country,
                present_address=present_address,
                duration_at_address=duration_at_address
            )

        # Save profile photo
        photo = self.registration_img_file_loader.file
        if photo:
            anvil.server.call('upload_profile_photo', self.user_id, photo)
        # Save aadhar document
        aadhar_doc = self.registration_img_aadhar_file_loader.file
        if aadhar_doc:
            anvil.server.call('upload_aadhar_doc', self.user_id, aadhar_doc)
        # Save pan document
        pan_doc = self.registration_img_pan_file_loader.file
        if pan_doc:
            anvil.server.call('upload_pan_doc', self.user_id, pan_doc)

        open_form('user_form')




    def registration_img_aadhar_file_loader_change(self, file, **event_args):
        if file:
            self.govt_id1_file_name.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_aadhar.source = self.registration_img_aadhar_file_loader.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_aadhar.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.registration_img_aadhar_file_loader.clear()



    def registration_img_pan_file_loader_change(self, file, **event_args):
        if file:
            self.govt_id2_file_name.text = file.name if file else ''
            content_type = file.content_type
            
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                # Display the image directly
                self.image_pan.source = self.registration_img_pan_file_loader.file
            elif content_type == 'application/pdf':
                # Display a default PDF image temporarily
                self.image_pan.source = '_/theme/bank_users/default%20pdf.png'
            else:
                alert('Invalid file type. Only JPEG, PNG, and PDF are allowed')
                self.registration_img_pan_file_loader.clear()


    def registration_img_file_loader_change(self, file, **event_args):
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


    def gender_dd_change(self, **event_args):
        """This method is called when an item is selected"""
        pass

    def logout_click(self, **event_args):
        """This method is called when the button is clicked"""
        alert("Logged out successfully")
        anvil.users.logout()
        open_form('bank_users.main_form') 

   






