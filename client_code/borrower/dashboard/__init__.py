# from ._anvil_designer import dashboardTemplate
# from anvil import *
# import anvil.server
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables
# from ...bank_users.main_form import main_form_module

# SUPERSCRIPT_DIGITS = {
#     '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
#     '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
# }

# def to_superscript(number):
#     return ''.join(SUPERSCRIPT_DIGITS.get(digit, '') for digit in str(number))

# class dashboard(dashboardTemplate):
#     def __init__(self, **properties):
#         self.init_components(**properties)
#         self.email = main_form_module.email
#         self.user_Id = main_form_module.userId
#         self.notifications.text = "0"
#         self.populate_loan_history()
#         self.update_wallet_info()
#         self.update_user_profile()
#         self.load_notifications()
#         self.update_platform_fees()

#     def update_platform_fees(self, **event_args):
#         result = anvil.server.call('update_fin_platform_fees')
#         # if result is not None:
#         #     alert(result)

#     def populate_loan_history(self):
#         try:
#             customer_loans = app_tables.fin_loan_details.search(borrower_customer_id=self.user_Id)
#             if customer_loans:
#                 self.data = [{'product_name': loan['product_name'], 'loan_amount': loan['loan_amount'],
#                               'tenure': loan['tenure'], 'interest_rate': loan['interest_rate'],
#                               'total_repayment_amount': round(loan['total_repayment_amount'], 2),
#                               'loan_updated_status': loan['loan_updated_status']} for loan in customer_loans]
#                 self.repeating_panel_1.items = self.data
#             else:
#                 Notification("No Data Available Here!").show()
#         except anvil.tables.TableError:
#             alert("No data found")

#     def update_wallet_info(self):
#         wallet = app_tables.fin_wallet.get(customer_id=self.user_Id)
#         if wallet:
#             self.label_9.text = "{:.2f}".format((wallet['wallet_amount'] or 0))
#             self.label_2_copy_copy.text = "{:.2f}".format((wallet['wallet_amount'] or 0))

#     def update_user_profile(self):
#         user_profile = app_tables.fin_user_profile.get(customer_id=self.user_Id)
#         if user_profile:
#             self.label_3.text = user_profile['mobile']
#             self.image_1_copy_copy.source = user_profile['user_photo']
#             self.label_2_copy.text = "Welcome " + user_profile['full_name']

#     def update_notification_count(self, count):
#         self.notifications.text = str(count)

#     def load_notifications(self):
#         notifications = anvil.server.call('get_notifications', self.user_Id)
#         unread_count = len([n for n in notifications if not n['read']])
#         self.update_notification_count(unread_count)

#     def notifications_click(self, **event_args):
#         open_form('borrower.dashboard.borrower_notifications', user_Id=self.user_Id)

#     # All other link click methods...

#     def link_1_click(self, **event_args):
#         try:
#             existing_loans = app_tables.fin_loan_details.search(
#                 borrower_customer_id=self.user_Id,
#                 loan_updated_status=q.any_of(
#                     q.like('accepted%'),
#                     q.like('Approved%'),
#                     q.like('approved%'),
#                     q.like('under process%'),
#                     q.like('foreclosure%'),
#                     q.like('extension'),
#                     q.like('disbursed%'),
#                     q.like('Disbursed%'),
#                     q.like('Under Process%'),
#                     q.like('rejected')
#                 )
#             )
#             num_existing_loans = len(existing_loans)
#             if num_existing_loans >= 5:
#                 alert("You already have 5 loans. Cannot open a new loan request.")
#             else:
#                 wallet_row = app_tables.fin_wallet.get(customer_id=self.user_Id)
#                 if wallet_row and wallet_row['wallet_id'] is not None:
#                     open_form('borrower.dashboard.new_loan_request')
#                 else:
#                     alert("Wallet not found. Please create a wallet.")
#         except anvil.tables.TableError as e:
#             alert("Error fetching existing loans.")

#     def link_2_click(self, **event_args):
#         open_form('borrower.dashboard.today_dues')

#     def link_3_click(self, **event_args):
#         open_form('borrower.dashboard.view_loans')

#     def link_4_click(self, **event_args):
#         open_form('borrower.dashboard.foreclosure_request')

#     def link_5_click(self, **event_args):
#         open_form('borrower.dashboard.application_tracker')

#     def link_6_click(self, **event_args):
#         open_form('borrower.dashboard.extension_loan_request')

#     def link_7_click(self, **event_args):
#         open_form('borrower.dashboard.view_transaction_history')

#     def link_8_click(self, **event_args):
#         open_form('borrower.dashboard.discount_coupons')

#     def link_10_click(self, **event_args):
#         open_form('lendor.dashboard.lender_portfolio_first_page')

#     def button_12_click(self, **event_args):
#         open_form('borrower.dashboard.borrower_view_profile')

#     def image_1_copy_copy_mouse_up(self, x, y, button, **event_args):
#         open_form('borrower.dashboard.borrower_view_profile')

#     def link_9_click(self, **event_args):
#         customer_id = self.user_Id
#         email = self.email
#         anvil.server.call('fetch_profile_data_and_insert', email, customer_id)
#         open_form("wallet.wallet")

#     def home_main_form_link_click(self, **event_args):
#         open_form('borrower.dashboard')

#     def about_main_form_link_click(self, **event_args):
#         open_form("borrower.dashboard.dashboard_about")

#     def contact_main_form_link_click(self, **event_args):
#         open_form("borrower.dashboard.dashboard_contact")

#     def link_11_click(self, **event_args):
#         open_form('borrower.dashboard.dashboard_report_a_problem')

#     def link_12_click(self, **event_args):
#         pass

#     def button_1_click(self, **event_args):
#         customer_id = self.user_Id
#         email = self.email
#         anvil.server.call('fetch_profile_data_and_insert', email, customer_id)
#         open_form("wallet.wallet")




from ._anvil_designer import dashboardTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...bank_users.main_form import main_form_module
from datetime import datetime, timezone, timedelta


SUPERSCRIPT_DIGITS = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
}

def to_superscript(number):
    return ''.join(SUPERSCRIPT_DIGITS.get(digit, '') for digit in str(number))

class dashboard(dashboardTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.email = main_form_module.email
        self.user_Id = main_form_module.userId
        self.notifications.text = "0"
        self.populate_loan_history()
        self.update_wallet_info()
        self.update_user_profile()
        self.load_notifications()
        self.update_platform_fees()
        self.image_1_copy_copy.role = 'circular-image'
         # Search for loans taken by the current user
        self.data= app_tables.fin_loan_details.search(borrower_customer_id=self.user_Id)
        loan_count = len(self.data)

        # Update the UI with the count of loans
        self.label_9.text = str(loan_count)

        # today_date = datetime.now(timezone.utc).date()
        # loan_details = []
    
        # all_loans_disbursed = app_tables.fin_loan_details.search(
        #         loan_updated_status=q.any_of("disbursed", "extension", "foreclosure"),
        #         first_emi_payment_due_date=q.less_than_or_equal_to(today_date),
        #         borrower_customer_id=self.user_Id
        #     )
        
        # for loan in all_loans_disbursed:
        #         loan_id = loan['loan_id']
        #         borrower_customer_id = loan['borrower_customer_id']
    
        #         payment_done = list(app_tables.fin_emi_table.search(
        #             loan_id=loan_id,
        #             next_payment=q.greater_than(today_date),
        #             payment_type ='pay now',
        #             borrower_customer_id=borrower_customer_id
        #         ))
        #         if payment_done:
        #           payment_done.sort(key=lambda x: x['next_payment'], reverse=True)
        #           latest_payment_done = payment_done[0]
        #           if latest_payment_done:
        #             continue
                  
        #         all_loans = list(app_tables.fin_emi_table.search(
        #             loan_id=loan_id,
        #             next_payment=q.less_than_or_equal_to(today_date),
        #             borrower_customer_id=borrower_customer_id
        #         ))
                
        #         if all_loans:
        #             all_loans.sort(key=lambda x: x['next_payment'], reverse=True)
        #             latest_loan = all_loans[0]
        #             loan_detail = app_tables.fin_loan_details.get(loan_id=latest_loan['loan_id'])
        #             user_profile = app_tables.fin_user_profile.get(customer_id=loan_detail['lender_customer_id'])
        #             if loan_detail is not None and user_profile is not None  and (loan_detail['remaining_amount'] is  None or loan_detail['remaining_amount'] > 0):        
        #                 loan_amount = loan_detail['loan_amount']
        #                 scheduled_payment = latest_loan['scheduled_payment']
        #                 next_payment = latest_loan['next_payment']
        #                 days_left = (today_date - next_payment).days
                  
        #                 emi_number = latest_loan['emi_number']
        #                 account_number = latest_loan['account_number']
        #                 tenure = loan_detail['tenure']
        #                 interest_rate = loan_detail['interest_rate']
        #                 borrower_loan_created_timestamp = loan_detail['borrower_loan_created_timestamp']
        #                 loan_updated_status = loan_detail['loan_updated_status']
        #                 loan_disbursed_timestamp = loan_detail['loan_disbursed_timestamp']
        #                 emi_payment_type = loan_detail['emi_payment_type']
        #                 lender_customer_id = loan_detail['lender_customer_id']
        #                 borrower_customer_id = loan_detail['borrower_customer_id']
        #                 first_emi_payment_due_date = loan_detail['first_emi_payment_due_date']
        #                 total_repayment_amount = loan_detail['total_repayment_amount']
        #                 total_processing_fee_amount = loan_detail['total_processing_fee_amount']
        #                 mobile = user_profile['mobile']
        #                 user_photo = user_profile['user_photo']
        #                 product_name = loan_detail['product_name']
        #                 product_description = loan_detail['product_description']
        #                 lender_full_name = loan_detail['lender_full_name']
        #                 loan_state_status = loan_detail['loan_state_status']
        #                 product_id = loan_detail['product_id']
        #                 total_interest_amount = loan_detail['total_interest_amount']
        #                 Scheduled_date = latest_loan['next_payment']
        #                 lender_email_id = loan_detail['lender_email_id']
        #                 borrower_email_id = loan_detail['borrower_email_id']
        #                 total_amount_paid = loan_detail['total_amount_paid']
        #                 remaining_amount = loan_detail['remaining_amount']
        #                 payment_type = latest_loan['payment_type']
        #                 part_payment_date = latest_loan['part_payment_date']
        #                 remaining_tenure = latest_loan['remaining_tenure']
                      
        #                 loan_details.append({
        #                     'loan_id': loan_id,
        #                     'loan_amount': loan_amount,
        #                     'scheduled_payment': scheduled_payment,
        #                     'days_left': days_left,
        #                     'tenure': tenure,
        #                     'interest_rate': interest_rate,
        #                     'borrower_loan_created_timestamp': borrower_loan_created_timestamp,
        #                     'emi_number': emi_number,
        #                     'account_number': account_number,
        #                     'loan_updated_status': loan_updated_status,
        #                     'loan_disbursed_timestamp': loan_disbursed_timestamp,
        #                     'next_payment': next_payment,
        #                     'emi_payment_type': emi_payment_type,
        #                     'lender_customer_id': lender_customer_id,
        #                     'first_emi_payment_due_date': first_emi_payment_due_date,
        #                     'total_repayment_amount': total_repayment_amount,
        #                     'total_processing_fee_amount': total_processing_fee_amount,
        #                     'mobile': mobile,
        #                     'product_description': product_description,
        #                     'product_name': product_name,
        #                     'lender_full_name': lender_full_name,
        #                     'borrower_customer_id': borrower_customer_id,
        #                     'loan_state_status': loan_state_status,
        #                     'product_id':product_id,
        #                     'total_interest_amount':total_interest_amount,
        #                     'Scheduled_date':Scheduled_date,
        #                     'user_photo':user_photo,
        #                     'lender_email_id':lender_email_id,
        #                     'borrower_email_id':borrower_email_id,
        #                     'total_amount_paid':total_amount_paid,
        #                     'remaining_amount':remaining_amount,
        #                     'payment_type': payment_type,
        #                     'part_payment_date':part_payment_date,
        #                     'remaining_tenure':remaining_tenure,
        #                 })
        #         else:
        #             pay_now_loan = app_tables.fin_emi_table.search(
        #                 loan_id=loan_id,
        #                 payment_type="pay now"
        #             )
        #             if any(pay_now_loan):
        #                 continue
    
        #             loan_detail = app_tables.fin_loan_details.get(loan_id=loan_id)
    
                      
        #             user_profile = app_tables.fin_user_profile.get(customer_id=loan_detail['lender_customer_id'])
    
        #             if loan_detail is not None and user_profile is not None and (loan_detail['remaining_amount'] is  None or loan_detail['remaining_amount'] > 0):
        #               user_photo = user_profile['user_photo']
        #               loan_amount = loan_detail['loan_amount']
        #               first_emi_payment_due_date = loan_detail['first_emi_payment_due_date']
        #               days_left = (today_date - first_emi_payment_due_date).days
        #               # Fetch account number from user profile table based on customer_id
        #               user_profile_1 = app_tables.fin_user_profile.get(customer_id=loan_detail['borrower_customer_id'])
        #               if user_profile_1 is not None:
        #                   account_number = user_profile['account_number']
        #               else:
        #                   account_number = "N/A"
                      
        #               # Set emi_number to 0
                    
                        
                      
        #               emi_number = 0
        #               remaining_tenure = 0
        #               tenure = loan_detail['tenure']
        #               interest_rate = loan_detail['interest_rate']
        #               borrower_loan_created_timestamp = loan_detail['borrower_loan_created_timestamp']
        #               loan_updated_status = loan_detail['loan_updated_status']
        #               loan_disbursed_timestamp = loan_detail['loan_disbursed_timestamp']
        #               emi_payment_type = loan_detail['emi_payment_type']
        #               lender_customer_id = loan_detail['lender_customer_id']
        #               total_repayment_amount = loan_detail['total_repayment_amount']
        #               total_processing_fee_amount = loan_detail['total_processing_fee_amount']
        #               mobile = user_profile['mobile']
        #               product_name = loan_detail['product_name']
        #               product_description = loan_detail['product_description']
        #               borrower_customer_id = loan_detail['borrower_customer_id']
        #               lender_full_name = loan_detail['lender_full_name']
        #               scheduled_payment = loan_disbursed_timestamp.date()
        #               loan_state_status = loan_detail['loan_state_status']
        #               product_id =loan_detail['product_id']
        #               total_interest_amount  = loan_detail['total_interest_amount']
        #               Scheduled_date = loan_detail['first_emi_payment_due_date']
        #               lender_email_id = loan_detail['lender_email_id']
        #               borrower_email_id = loan_detail['borrower_email_id']
        #               total_amount_paid = loan_detail['total_amount_paid']
        #               remaining_amount = loan_detail['remaining_amount']
    
                      
        #               # Calculate next_payment based on first_payment_due_date
        #               if emi_payment_type == 'One Time':
        #                   if tenure:
        #                       next_payment = loan_disbursed_timestamp.date() + timedelta(days=30 * tenure)
        #               elif emi_payment_type == 'Monthly':
        #                   # For monthly payment, set next_payment to a month after first_payment_due_date
        #                   next_payment = loan_disbursed_timestamp.date() + timedelta(days=30)
        #               elif emi_payment_type == 'Three Months':
        #                   # For three-month payment, set next_payment to three months after first_payment_due_date
        #                   next_payment = loan_disbursed_timestamp.date() + timedelta(days=90)
        #               elif emi_payment_type == 'Six Months':
        #                   # For six-month payment, set next_payment  six months after first_payment_due_date
        #                   next_payment = loan_disbursed_timestamp.date() + timedelta(days=180)
        #               else:
        #                   # Default to monthly calculation if emi_payment_type is not recognized
        #                   next_payment = loan_disbursed_timestamp.date() + timedelta(days=30)
                      
        #               loan_details.append({
        #                   'loan_id': loan_id,
        #                   'loan_amount': loan_amount,
        #                   'scheduled_payment': scheduled_payment,   # Set scheduled_payment to first_payment_due_date first_emi_payment_due_date
        #                   'next_payment': next_payment,
        #                   'days_left': days_left,
        #                   'tenure': tenure,
        #                   'interest_rate': interest_rate,
        #                   'borrower_loan_created_timestamp': borrower_loan_created_timestamp,
        #                   'loan_updated_status': loan_updated_status,
        #                   'loan_disbursed_timestamp': loan_disbursed_timestamp,
        #                   'emi_number': emi_number,
        #                   'account_number': account_number,
        #                   'emi_payment_type': emi_payment_type,
        #                   'lender_customer_id': lender_customer_id,
        #                   'total_repayment_amount': total_repayment_amount,
        #                   # 'first_payment_due_date': first_payment_due_date
        #                   'total_processing_fee_amount': total_processing_fee_amount,
        #                   'mobile': mobile,
        #                   'product_description': product_description,
        #                   'product_name': product_name,
        #                   'lender_full_name': lender_full_name,  
        #                   'borrower_customer_id': borrower_customer_id,
        #                   'loan_state_status':loan_state_status,
        #                   'product_id':product_id,
        #                   'total_interest_amount':total_interest_amount,
        #                   'Scheduled_date':Scheduled_date,
        #                   'user_photo' : user_photo,
        #                   'lender_email_id':lender_email_id,
        #                   'borrower_email_id':borrower_email_id,
        #                   'total_amount_paid':total_amount_paid,
        #                   'remaining_amount':remaining_amount,
        #                   'remaining_tenure':remaining_tenure
                          
        #               })
        #         self.repeating_panel_2.items = loan_details

    def update_platform_fees(self, **event_args):
        result = anvil.server.call('update_fin_platform_fees')

    def populate_loan_history(self):
        try:
            customer_loans = app_tables.fin_loan_details.search(borrower_customer_id=self.user_Id)
            if customer_loans:
                self.data = [{'product_name': loan['product_name'], 'loan_amount': loan['loan_amount'],
                              'tenure': loan['tenure'], 'interest_rate': loan['interest_rate'],
                              'total_repayment_amount': round(loan['total_repayment_amount'], 2),
                              'loan_updated_status': loan['loan_updated_status']} for loan in customer_loans]
                self.repeating_panel_1.items = self.data
            else:
                Notification("No Data Available Here!").show()
        except anvil.tables.TableError:
            alert("No data found")

    def update_wallet_info(self):
        wallet = app_tables.fin_wallet.get(customer_id=self.user_Id)
        if wallet:
            # self.label_9.text = "{:.2f}".format((wallet['wallet_amount'] or 0))
            self.label_2_copy_copy.text = "{:.2f}".format((wallet['wallet_amount'] or 0))

    def update_user_profile(self):
        user_profile = app_tables.fin_user_profile.get(customer_id=self.user_Id)
        if user_profile:
            self.label_3.text = user_profile['mobile']
            self.image_1_copy_copy.source = user_profile['user_photo']
            self.label_2_copy.text = "Welcome " + user_profile['full_name']

    def update_notification_count(self, count):
        self.notifications.text = str(count)

    def load_notifications(self):
        notifications = anvil.server.call('get_notifications', self.user_Id)
        unread_count = len([n for n in notifications if not n['read']])
        self.update_notification_count(unread_count)

    def notifications_click(self, **event_args):
        open_form('borrower.dashboard.borrower_notifications', user_Id=self.user_Id)

    def link_1_click(self, **event_args):
        try:
            existing_loans = app_tables.fin_loan_details.search(
                borrower_customer_id=self.user_Id,
                loan_updated_status=q.any_of(
                    q.like('accepted%'),
                    q.like('Approved%'),
                    q.like('approved%'),
                    q.like('under process%'),
                    q.like('foreclosure%'),
                    q.like('extension'),
                    q.like('disbursed%'),
                    q.like('Disbursed%'),
                    q.like('Under Process%'),
                    q.like('rejected')
                )
            )
            num_existing_loans = len(existing_loans)
            if num_existing_loans >= 5:
                alert("You already have 5 loans. Cannot open a new loan request.")
            else:
                wallet_row = app_tables.fin_wallet.get(customer_id=self.user_Id)
                if wallet_row and wallet_row['wallet_id'] is not None:
                    open_form('borrower.dashboard.new_loan_request')
                else:
                    alert("Wallet not found. Please create a wallet.")
        except anvil.tables.TableError as e:
            alert("Error fetching existing loans.")

    def link_2_click(self, **event_args):
        open_form('borrower.dashboard.today_dues')

    def link_3_click(self, **event_args):
        open_form('borrower.dashboard.view_loans')

    def link_4_click(self, **event_args):
        open_form('borrower.dashboard.foreclosure_request')

    def link_5_click(self, **event_args):
        open_form('borrower.dashboard.application_tracker')

    def link_6_click(self, **event_args):
        open_form('borrower.dashboard.extension_loan_request')

    def link_7_click(self, **event_args):
        open_form('borrower.dashboard.view_transaction_history')

    def link_8_click(self, **event_args):
        open_form('borrower.dashboard.discount_coupons')

    def link_10_click(self, **event_args):
        open_form('lendor.dashboard.lender_portfolio_first_page')

    def button_12_click(self, **event_args):
        open_form('borrower.dashboard.borrower_view_profile')

    def image_1_copy_copy_mouse_up(self, x, y, button, **event_args):
        open_form('borrower.dashboard.borrower_view_profile')

    def link_9_click(self, **event_args):
        customer_id = self.user_Id
        email = self.email
        anvil.server.call('fetch_profile_data_and_insert', email, customer_id)
        open_form("wallet.wallet")

    def home_main_form_link_click(self, **event_args):
        open_form('borrower.dashboard')

    def about_main_form_link_click(self, **event_args):
        open_form("borrower.dashboard.dashboard_about")

    def contact_main_form_link_click(self, **event_args):
        open_form("borrower.dashboard.dashboard_contact")

    def link_11_click(self, **event_args):
        open_form('borrower.dashboard.dashboard_report_a_problem')

    def link_12_click(self, **event_args):
        pass

    def button_1_click(self, **event_args):
        customer_id = self.user_Id
        email = self.email
        anvil.server.call('fetch_profile_data_and_insert', email, customer_id)
        open_form("wallet.wallet")
