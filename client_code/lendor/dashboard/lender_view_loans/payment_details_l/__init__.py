import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta
import anvil.server
import anvil.tables as tables
from anvil import DataGrid, alert, open_form
from ._anvil_designer import payment_details_lTemplate
class payment_details_l(payment_details_lTemplate):
    def __init__(self, selected_row=None, entered_values=None, **properties):
        self.selected_row = selected_row
        self.init_components(**properties)

        if selected_row:
            self.load_payment_details(selected_row, entered_values)

    def load_payment_details(self, selected_row, entered_values):
        self.load_entered_values(entered_values)
        payment_details = []
        monthly_interest_rate = (self.selected_row['interest_rate'] / 100) / 12
        extra_payment = 0
        emi = (self.selected_row['loan_amount'] * monthly_interest_rate * ((1 + monthly_interest_rate) ** self.selected_row['tenure'])) / (
                ((1 + monthly_interest_rate) ** self.selected_row['tenure']) - 1)
        beginning_balance = self.selected_row['loan_amount']
        for month in range(1, self.selected_row['tenure'] + 1):
            payment_date = self.calculate_payment_date(selected_row, month)
        
            # Print debug information
            #print(f"Debug: Processing month {month}, payment_date={payment_date}")
        
            # Fetch emi_date and account_number from fin_emi_table based on loan_id and emi_number
            loan_id = selected_row['loan_id']
            emi_number = month  # Assuming emi_number starts from 1 and increments
        
            # Print debug information
            #print(f"Debug: loan_id={loan_id}, emi_number={emi_number}")
        
            emi_row = app_tables.fin_emi_table.get(loan_id=loan_id, emi_number=emi_number)
        
            # Print debug information
            #print(f"Debug: emi_row={emi_row}")
        
            # Access emi_date and account_number
            if emi_row is not None:
                scheduled_payment_made = emi_row['scheduled_payment_made']
                account_number = emi_row['account_number']
            else:
                scheduled_payment_made = None
                account_number = None
        
            # Print debug information
            #print(f"Debug: emi_date={emi_date}, account_number={account_number}")
        
            # Handle the case when payment_date is None
            formatted_payment_date = f"{payment_date:%Y-%m-%d}" if payment_date else "Awaiting Update"
            if payment_date is None:
                self.label_1.enabled = True
                self.label_1.text = "Payment Date will be updated after loan disbursed"
            else:
                self.label_1.enabled = False
                self.label_1.text = ""
        
            # Calculate other payment details
            interest_amount = beginning_balance * monthly_interest_rate
            principal_amount = emi - interest_amount
            ending_balance = beginning_balance - principal_amount
        
            # Determine display values for EMIDate and AccountNumber
            scheduled_payment_made_display = f"{scheduled_payment_made:%Y-%m-%d}" if scheduled_payment_made else "N/A"
            emi_time_display = f"{scheduled_payment_made:%I:%M %p}" if scheduled_payment_made else "N/A"
            account_number_display = account_number if account_number else "N/A"
                
            # Add payment details to the list
            payment_details.append({
                'PaymentNumber': month,
                'PaymentDate': formatted_payment_date,
                'EMIDate': scheduled_payment_made_display,
                'EMITime': emi_time_display,
                'AccountNumber': account_number_display,
                'ScheduledPayment': f"₹ {emi:.2f}",
                'Principal': f"₹ {principal_amount:.2f}",
                'Interest': f"₹ {interest_amount:.2f}",
                'BeginningBalance': f"₹ {beginning_balance:.2f}",
                'ExtraPayment': f"₹ {extra_payment:.2f}",
                'TotalPayment': f"₹ {emi + extra_payment:.2f}",
                'EndingBalance': f"₹ {ending_balance:.2f}"
            })

            beginning_balance = ending_balance

        self.repeating_panel_1.items = payment_details

    def load_entered_values(self, entered_values):
        if entered_values:
            # Load previously entered values into the form fields
            self.entered_loan_amount = entered_values.get('loan_amount', None)
            self.entered_tenure = entered_values.get('tenure', None)
            self.entered_payment_type = entered_values.get('payment_type', None)

    def calculate_payment_date(self, selected_row, current_month):
        loan_updated_status = selected_row['loan_updated_status'].lower()
    
        if loan_updated_status in ['close', 'closed loans', 'disbursed loan', 'foreclosure']:
            try:
                loan_disbursed_timestamp = selected_row['loan_disbursed_timestamp']
    
                if loan_disbursed_timestamp:
                    fin_product_details_row = app_tables.fin_product_details.get(
                        product_id=selected_row['product_id']
                    )
                    first_emi_payment = fin_product_details_row['first_emi_payment']
    
                    # Calculate payment date based on loan_disbursed_timestamp and first_emi_payment
                    if current_month == 1:
                        payment_date = loan_disbursed_timestamp + timedelta(
                            days=int(first_emi_payment * 30.44)
                        )
                    else:
                        payment_date = loan_disbursed_timestamp + timedelta(
                            days=int(first_emi_payment * 30.44) + (current_month - 1) * 30  # Assuming an average of 30 days in a month
                        )
    
                    return payment_date
                else:
                    return None
            except Exception as e:
                print(f"Error in calculate_payment_date: {e}")
                return None
        else:
            return None

    def button_1_click(self, **event_args):
        open_form('lendor_registration_form.dashboard')

    def button_2_click(self, **event_args):
        # Pass the selected_row to view_details_1 form
        open_form('lendor.dashboard.lender_view_loans.view_details_1', selected_row=self.selected_row)