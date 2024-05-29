from ._anvil_designer import View_DetailsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta
from .. import main_form_module as main_form_module
from datetime import date
from collections import defaultdict
# from ...Module1 import transfer_money_1

class View_Details(View_DetailsTemplate):
    def __init__(self, selected_row, **properties):
        self.selected_row = selected_row
        self.user_id = main_form_module.userId
        self.init_components(**properties)
  
        loan_id = selected_row['loan_id']
        remaining_amount = selected_row['remaining_amount']
        total_paid_amount = selected_row['total_amount_paid']
        extension_months = self.get_extension_details(loan_id, selected_row['emi_number'])
        extension_amount = self.get_extension_details_1(loan_id,selected_row['emi_number'])
        loan_amount = selected_row['loan_amount']
        tenure = selected_row['tenure'] + extension_months
        interest_rate = selected_row['interest_rate']
        emi_payment_type = selected_row['emi_payment_type']
        total_interest_amount = selected_row['total_interest_amount']
        total_processing_fee_amount = selected_row['total_processing_fee_amount']
        processing_fee = total_processing_fee_amount/ tenure
        self.processing_fee.text = "{:.2f}".format(processing_fee)
        monthly_interest_rate = interest_rate / 12 / 100
        total_payments = tenure * 12
        total_repayment_amount = selected_row['total_repayment_amount']
        total_i_a = total_interest_amount / tenure
        if remaining_amount is None:
          self.remainining_amount.text = "{:.2f}".format(total_repayment_amount)
        else:
          self.remainining_amount.text =  "{:.2f}".format(remaining_amount)
      
        if emi_payment_type == 'One Time':
            emi = total_repayment_amount
            interest_amount = total_interest_amount
            #total_emi += emi  # Add extension amount to 12-month EMI total
            total_emi = emi +  extension_amount + total_processing_fee_amount
        elif emi_payment_type == 'Monthly':
            # Calculate monthly EMI amount
            interest_amount = total_i_a
            emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure)) / (((1 + monthly_interest_rate) ** tenure) - 1)
            total_emi = emi + extension_amount + processing_fee  # Add extension amount to monthly EMI
        elif emi_payment_type == 'Three Months':
            # Calculate EMI amount for 3 months
            interest_amount = total_i_a * 3
            processing_fee = processing_fee * 3
            emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** (tenure ))) / (((1 + monthly_interest_rate) ** (tenure)) - 1)
            emi*=3
            total_emi = emi + extension_amount + processing_fee # Add extension amount to 3-month EMI
        elif emi_payment_type == 'Six Months':
            interest_amount = total_i_a * 6
            processing_fee = processing_fee * 6
            # Calculate EMI amount for 6 months
            emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** (tenure ))) / (((1 + monthly_interest_rate) ** (tenure)) - 1)
            emi*=6
            total_emi = emi + extension_amount+ processing_fee  # Add extension amount to 6-month EMI
        else:
            # Default to monthly calculation
            emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
            total_emi = emi + extension_amount + processing_fee # Add extension amount to monthly EMI

        self.i_r.text = "{:.2f}".format(interest_amount)
        self.emi.text = "{:.2f}".format(emi)
      
      
        lapsed_settings = app_tables.fin_loan_settings.get(loans="lapsed fee")
        default_settings = app_tables.fin_loan_settings.get(loans="default fee")
        npa_settings = app_tables.fin_loan_settings.get(loans="NPA fee")
        
        days_left = selected_row['days_left']
        product_id = selected_row['product_id']        
        # Initialize variables for different fees
        total_lapsed_amount = 0
        total_default_fee = 0
        total_npa_fee = 0
        
        if lapsed_settings:
            lapsed_start = lapsed_settings['minimum_days']
            lapsed_end = lapsed_settings['maximum_days']
            if lapsed_start < days_left <= lapsed_end:
                lapsed_fee_percentage = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
                days_difference = days_left - lapsed_start
                total_lapsed_amount = days_difference * (lapsed_fee_percentage * emi / 100)
                total_emi += total_lapsed_amount
                self.lapsed.text = "{:.2f}".format(total_lapsed_amount)
                self.lapsed.visible = True
                self.label_5.visible = True
                self.default.visible = False
                self.label_9.visible = False
        
        if default_settings:
            default_start = int(default_settings['minimum_days'])
            default_end = int(default_settings['maximum_days'])
            if default_start < days_left <= default_end:
                product_details = app_tables.fin_product_details.get(product_id=product_id)
                if product_details['default_fee'] != 0:
                    days_difference = days_left - default_start
                    default_fee_percentage = product_details['default_fee']
                    total_default_fee = days_difference * (default_fee_percentage * emi / 100)
                elif product_details['default_fee_amount'] != 0:
                    days_difference = days_left - default_start
                    total_default_fee = days_difference * product_details['default_fee_amount']
                
                # Include lapsed fee during default period
                if days_left > lapsed_end:
                    lapsed_fee_percentage = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
                    days_in_lapsed = lapsed_end - lapsed_start
                    total_lapsed_amount = days_in_lapsed * (lapsed_fee_percentage * emi / 100)
                    total_default_fee += total_lapsed_amount
                
                total_emi += total_default_fee
                self.default.text = "{:.2f}".format(total_default_fee)
                self.default.visible = True
                self.label_9.visible = True
                self.lapsed.visible = False
                self.label_5.visible = False
        
        if npa_settings:
            npa_start = int(npa_settings['minimum_days'])
            npa_end = int(npa_settings['maximum_days'])
            if npa_start < days_left <= npa_end:
                product_details = app_tables.fin_product_details.get(product_id=product_id)
                if product_details['npa'] != 0:
                    days_difference = days_left - npa_start
                    npa_percentage = product_details['npa']
                    total_npa_fee = days_difference * (npa_percentage * emi / 100)
                elif product_details['npa_amount'] != 0:
                    days_difference = days_left - npa_start
                    total_npa_fee = days_difference * product_details['npa_amount']
                
                # Include lapsed and default fees during NPA period
                if days_left > lapsed_end:
                    lapsed_fee_percentage = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
                    days_in_lapsed = lapsed_end - lapsed_start
                    total_lapsed_amount = days_in_lapsed * (lapsed_fee_percentage * emi / 100)
                    total_npa_fee += total_lapsed_amount
                
                if days_left > default_end:
                    default_fee_amount = 0
                    product_details = app_tables.fin_product_details.get(product_id=product_id)
                    if product_details['default_fee'] != 0:
                        days_in_default = default_end - default_start
                        default_fee_percentage = product_details['default_fee']
                        default_fee_amount = days_in_default * (default_fee_percentage * emi / 100)
                    elif product_details['default_fee_amount'] != 0:
                        days_in_default = days_left - default_start
                        default_fee_amount = days_in_default * product_details['default_fee_amount']
                    total_npa_fee += default_fee_amount
        
                total_emi += total_npa_fee
                self.npa.text = "{:.2f}".format(total_npa_fee)
                self.npa.visible = True
                self.label_12.visible = True
                self.default.visible = False
                self.label_9.visible = False
                self.lapsed.visible = False
                self.label_5.visible = False



        # Display the calculated EMI amount in the EMI amount label
        self.emi_amount_label.text = "{:.2f}".format(emi)  # Show only the EMI amount without extension
        
        self.update_total_emi_amount(total_emi)
        self.total_emi_amount_label.visible = True

        # Update labels based on the presence of extension amount
        if extension_amount > 0:
            self.total_emi_amount_label.text = "{:.2f}".format(total_emi)
            self.extension_amount_label.text = "{:.2f}".format(extension_amount)
            self.total_emi_amount_label.visible = True
            self.extension_amount_label.visible = True
            self.label_6.visible = True
            self.label_3.visible = True
        else:
            self.total_emi_amount_label.visible = True
            self.extension_amount_label.visible = False
            self.label_6.visible = False
            self.label_3.visible = True
  
        # Update other labels
        self.loan_id_label.text = str(selected_row['borrower_full_name'])
        self.loan_amount_label.text = str(loan_amount)
        self.interest_label.text = "{:.2f}".format(total_interest_amount)
        self.tenure_label.text = str(tenure)
        self.account_no_label.text = str(selected_row['account_number'])
      
        # Display total EMI amount including extension amount
        self.update_total_emi_amount(total_emi)
      
        

        emi_row = app_tables.fin_emi_table.get(
            loan_id=loan_id,
            emi_number=selected_row['emi_number'] + 1
        )

        if emi_row is not None and emi_row['payment_type'] == 'part payment':
          amount = emi_row['part_payment_amount']
          self.part_payment_label.text = "{:.2f}".format(amount)
          self.part_payment_amount.visible = True
          self.back.visible = True
          self.part_payment_label.visible = True
          # self.label_3.visible = False
          # self.label_5.visible = False
          # self.label_9.visible = False
          # self.label_12.visible = False
          # self.total_emi_amount_label.visible = False
          # self.lapsed.visible = False
          # self.default.visible = False
          # self.npa.visible = False

        adding_remaining_part_payment = app_tables.fin_emi_table.get(
            loan_id=loan_id,
            emi_number=selected_row['emi_number']
        )
        if adding_remaining_part_payment:
          part_pay = adding_remaining_part_payment['payment_type']
          if part_pay == 'part payment':
            remaining_part_payment = adding_remaining_part_payment['part_payment_amount']
            # total_due_amount += remaining_part_payment
            additional_fees = self.calculate_additional_fees(adding_remaining_part_payment)
            print(additional_fees)
            self.label_14.text = additional_fees + remaining_part_payment
            # total_due_amount +=additional_fees

            total_emi += remaining_part_payment
            total_emi +=additional_fees
            # self.part_payment.visible = False
            # self.back.visible = False
            self.label_14.visible = True
            self.label_15.visible = True
        self.update_total_emi_amount(total_emi)

        foreclosure_details = self.get_foreclosure_details(loan_id, selected_row['emi_number'])
        if foreclosure_details is not None:
          total_due_amount = foreclosure_details['total_due_amount']
          foreclosure_amount = foreclosure_details['foreclose_amount']
          foreclosure_emi_amount = foreclosure_details['total_due_amount']
      
          lapsed_settings = app_tables.fin_loan_settings.get(loans="lapsed fee")
          default_settings = app_tables.fin_loan_settings.get(loans="default fee")
          npa_settings = app_tables.fin_loan_settings.get(loans="NPA fee")
          
          days_left = self.selected_row['days_left']
          product_id = self.selected_row['product_id']
          # emi = self.loan_details['emi']
      
          if lapsed_settings:
              lapsed_start = lapsed_settings['minimum_days']
              lapsed_end = lapsed_settings['maximum_days']
              if lapsed_start < days_left <= lapsed_end:
                  lapsed_fee_percentage = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
                  days_difference = days_left - lapsed_start
                  total_lapsed_amount = days_difference * (lapsed_fee_percentage * emi / 100)
                  total_due_amount += total_lapsed_amount
                  print(f"Lapsed Fee: {total_lapsed_amount}")
                  self.lapsed.visible = True
                  self.label_5.visible = True
      
          if default_settings:
              default_start = default_settings['minimum_days']
              default_end = default_settings['maximum_days']
              if default_start < days_left <= default_end:
                  default_fee_amount = 0
      
                  # Include lapsed end fee if applicable
                  if lapsed_settings and days_left > lapsed_end:
                      days_in_lapsed = lapsed_end - lapsed_start
                      lapsed_fee_percentage = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
                      total_lapsed_amount = days_in_lapsed * (lapsed_fee_percentage * emi / 100)
                      default_fee_amount += total_lapsed_amount
      
                  product_details = app_tables.fin_product_details.get(product_id=product_id)
                  if product_details['default_fee'] != 0:
                      days_in_default = days_left - default_start
                      default_fee_percentage = product_details['default_fee']
                      default_fee_amount += days_in_default * (default_fee_percentage * emi / 100)
                  elif product_details['default_fee_amount'] != 0:
                      days_in_default = days_left - default_start
                      default_fee_amount += days_in_default * product_details['default_fee_amount']
                  
                  total_due_amount += default_fee_amount
                  print(f"Default Fee: {default_fee_amount}")
                  self.default.visible = True
                  self.label_9.visible = True
      
          if npa_settings:
              npa_start = npa_settings['minimum_days']
              npa_end = npa_settings['maximum_days']
              if npa_start < days_left <= npa_end:
                  npa_fee_amount = 0
      
                  # Include lapsed end fee if applicable
                  if lapsed_settings and days_left > lapsed_end:
                      days_in_lapsed = lapsed_end - lapsed_start
                      lapsed_fee_percentage = app_tables.fin_product_details.get(product_id=product_id)['lapsed_fee']
                      total_lapsed_amount = days_in_lapsed * (lapsed_fee_percentage * emi / 100)
                      npa_fee_amount += total_lapsed_amount
      
                  # Include default end fee if applicable
                  if default_settings and days_left > default_end:
                      days_in_default = default_end - default_start
                      product_details = app_tables.fin_product_details.get(product_id=product_id)
                      if product_details['default_fee'] != 0:
                          default_fee_percentage = product_details['default_fee']
                          default_fee_amount = days_in_default * (default_fee_percentage * emi / 100)
                          npa_fee_amount += default_fee_amount
                      elif product_details['default_fee_amount'] != 0:
                          default_fee_amount = product_details['default_fee_amount']
                          days_in_default = days_left - default_start
                          default_fee_amount = days_in_default * default_fee_amount
                          npa_fee_amount += default_fee_amount
      
                  product_details = app_tables.fin_product_details.get(product_id=product_id)
                  if product_details['npa'] != 0:
                      days_difference = days_left - npa_start
                      npa_percentage = product_details['npa']
                      npa_fee_amount += days_difference * (npa_percentage * emi / 100)
                  elif product_details['npa_amount'] != 0:
                      npa_amount = product_details['npa_amount']
                      days_difference = days_left - npa_start
                      npa_fee_amount += days_difference * npa_amount
                  
                  total_due_amount += npa_fee_amount
                  print(f"NPA Fee: {npa_fee_amount}")
                  self.npa.visible = True
                  self.label_12.visible = True
      
          adding_remaining_part_payment = app_tables.fin_emi_table.get(
              loan_id=loan_id,
              emi_number=selected_row['emi_number']
          )
          if adding_remaining_part_payment:
              part_pay = adding_remaining_part_payment['payment_type']
              if part_pay == 'part payment':
                  remaining_part_payment = adding_remaining_part_payment['part_payment_amount']
                  additional_fees = self.calculate_additional_fees(adding_remaining_part_payment)
                  print(additional_fees)
                  self.label_14.text = additional_fees + remaining_part_payment
                  total_due_amount += remaining_part_payment
                  total_due_amount += additional_fees
                  # self.part_payment.enabled = False
                  self.label_14.visible = True
                  self.label_15.visible = True
      
          self.emi_amount_label.text = "{:.2f}".format(foreclosure_emi_amount)
          self.extension_amount_label.text = "{:.2f}".format(foreclosure_amount)
          self.total_emi_amount_label.text = "{:.2f}".format(total_due_amount + foreclosure_amount)
          self.total_emi_amount_label.visible = True
          self.label_3.visible = True

    def calculate_date_difference(self,date_to_subtract, today_date):
      return (today_date - date_to_subtract).days
      print ((today_date - date_to_subtract).days)

    def calculate_additional_fees(self, adding_remaining_part_payment):
        # Retrieve the part_payment_date from emi_row
        part_payment_date = adding_remaining_part_payment['scheduled_payment']
        print(part_payment_date)
    
        # Calculate the difference in days between part_payment_date and today's date
        days_elapsed = self.calculate_date_difference(part_payment_date, datetime.now().date())
        print(days_elapsed)
        product_id = self.selected_row['product_id']
    
        lapsed_settings = app_tables.fin_loan_settings.get(loans="lapsed fee")
        default_settings = app_tables.fin_loan_settings.get(loans="default fee")
        npa_settings = app_tables.fin_loan_settings.get(loans="NPA fee")
        # Fetch necessary fee details based on loan state status and product ID
        product_details = app_tables.fin_product_details.get(product_id=product_id)
    
        # Initialize total additional fees
        total_additional_fees = 0
    
        # Check lapsed settings and calculate fees if applicable
        if lapsed_settings:
            lapsed_start = lapsed_settings['minimum_days']
            lapsed_end = lapsed_settings['maximum_days']
            if lapsed_start < days_elapsed <= lapsed_end:
                days_in_lapsed = days_elapsed - lapsed_start
                lapsed_fee_percentage = product_details['lapsed_fee']
                lapsed_fee_amount = days_in_lapsed * (lapsed_fee_percentage * float(self.emi.text) / 100)
                total_additional_fees += lapsed_fee_amount
                print(f"Lapsed Fee: {lapsed_fee_amount}")
    
        # Check default settings and calculate fees if applicable
        if default_settings:
            default_start = default_settings['minimum_days']
            default_end = default_settings['maximum_days']
            if default_start < days_elapsed <= default_end:
                days_in_default = days_elapsed - default_start
                default_fee_amount = 0
    
                # Include lapsed end fee if applicable
                if lapsed_settings and days_elapsed > lapsed_end:
                    days_in_lapsed = lapsed_end - lapsed_start
                    lapsed_fee_percentage = product_details['lapsed_fee']
                    lapsed_fee_amount = days_in_lapsed * (lapsed_fee_percentage * float(self.emi.text) / 100)
                    default_fee_amount += lapsed_fee_amount
    
                if product_details['default_fee'] != 0:
                    default_fee_percentage = product_details['default_fee']
                    default_fee_amount += days_in_default * (default_fee_percentage * float(self.emi.text) / 100)
                elif product_details['default_fee_amount'] != 0:
                    default_fee_amount += days_in_default * product_details['default_fee_amount']
                
                total_additional_fees += default_fee_amount
                print(f"Default Fee: {default_fee_amount}")
    
        # Check NPA settings and calculate fees if applicable
        if npa_settings:
            npa_start = npa_settings['minimum_days']
            npa_end = npa_settings['maximum_days']
            if npa_start < days_elapsed <= npa_end:
                days_in_npa = days_elapsed - npa_start
                npa_fee_amount = 0
    
                # Include lapsed end fee if applicable
                if lapsed_settings and days_elapsed > lapsed_end:
                    days_in_lapsed = lapsed_end - lapsed_start
                    lapsed_fee_percentage = product_details['lapsed_fee']
                    lapsed_fee_amount = days_in_lapsed * (lapsed_fee_percentage * float(self.emi.text) / 100)
                    npa_fee_amount += lapsed_fee_amount
    
                # Include default end fee if applicable
                if default_settings and days_elapsed > default_end:
                    days_in_default = default_end - default_start
                    if product_details['default_fee'] != 0:
                        default_fee_percentage = product_details['default_fee']
                        default_fee_amount = days_in_default * (default_fee_percentage * float(self.emi.text) / 100)
                        npa_fee_amount += default_fee_amount
                    elif product_details['default_fee_amount'] != 0:
                        default_fee_amount = days_in_default * product_details['default_fee_amount']
                        npa_fee_amount += default_fee_amount
    
                if product_details['npa'] != 0:
                    npa_fee_percentage = product_details['npa']
                    npa_fee_amount += days_in_npa * (npa_fee_percentage * float(self.emi.text) / 100)
                elif product_details['npa_amount'] != 0:
                    npa_fee_amount += days_in_npa * product_details['npa_amount']
                
                total_additional_fees += npa_fee_amount
                print(f"NPA Fee: {npa_fee_amount}")
    
        print(f"Total Additional Fees: {total_additional_fees}")
        return total_additional_fees
          
  
    def get_extension_details(self, loan_id, emi_number):
        extension_row = app_tables.fin_extends_loan.get(
            borrower_customer_id=self.selected_row['borrower_customer_id'],
            loan_id=loan_id,
            emi_number=q.less_than_or_equal_to(emi_number)
        )
        extension_months = 0
        if extension_row is not None and extension_row['status'] == 'approved':
            extension_months = extension_row['total_extension_months']
        return  extension_months

    def get_extension_details_1(self, loan_id, emi_number):
        extension_row = app_tables.fin_extends_loan.get(
            borrower_customer_id=self.selected_row['borrower_customer_id'],
            loan_id=loan_id,
            emi_number=emi_number
        )
        extension_amount = 0
        if extension_row is not None and extension_row['status'] == 'approved':
            extension_amount = extension_row['extension_amount']
        return extension_amount

    def get_foreclosure_details(self, loan_id, emi_number):
      foreclosure_row = app_tables.fin_foreclosure.get(
          loan_id=loan_id,
          foreclosure_emi_num=emi_number,
      )
      
      if foreclosure_row is not None and foreclosure_row['status'] == 'approved':
          return foreclosure_row
      else:
          return None
  
    def update_total_emi_amount(self, total_emi):
        self.total_emi_amount_label.text = "{:.2f}".format(total_emi)

    def get_first_payment_due_date(self, loan_id):
        loan_row = app_tables.fin_loan_details.get(loan_id=loan_id)
        if loan_row is not None:
            return loan_row['first_emi_payment_due_date']
        else:
            return None  # or handle the case where the loan ID is not found

    def back_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('lendor.dashboard.today_dues')



    def update_loan_status(self, loan_id, new_status):
    # Update loan status in the loan details table for the given loan ID
      loan_row = app_tables.fin_loan_details.get(loan_id=loan_id)
      if loan_row is not None:
          loan_row['loan_updated_status'] = new_status
          loan_row.update()


    def foreclosure_condition_satisfied(self, loan_id, emi_number):
    # Check if foreclosure details are returned for the given loan and EMIs
      foreclosure_row = app_tables.fin_foreclosure.get(
          loan_id=loan_id,
          foreclosure_emi_num=emi_number,
        
      )
      if foreclosure_row is not None and foreclosure_row['status'] == 'approved':
          return foreclosure_row
      else:
          return None

    # def update_payment_status(self):
    # # Update payment status in loan details table for the given loan ID, borrower ID, and condition
    #   loan_details = app_tables.fin_loan_details.search(
    #     loan_id=self.selected_row['loan_id'],
    #     borrower_customer_id=self.selected_row['borrower_customer_id'],
    #     first_emi_payment_due_date=q.less_than_or_equal_to(datetime.now().date())
    # )
    #   for loan_detail in loan_details:
    #     loan_detail['payment_status'] = True
    #     loan_detail.update()


    def get_foreclosure_details_for_status_rejection(self, loan_id, emi_number):
      foreclosure_row = app_tables.fin_foreclosure.get(
          loan_id=loan_id,
          foreclosure_emi_num=emi_number - 1,
      )
      
      if foreclosure_row is not None :
          return foreclosure_row
      else:
          return None

    def part_payment_click(self, **event_args):
      """This method is called when the button is clicked"""

      try:
        # Try to convert and get the values, and calculate the extra fee
        lapsed_fee = float(self.lapsed.text)
      except ValueError:
          lapsed_fee = 0.0
          
      try:
          default_fee = float(self.default.text)
      except ValueError:
          default_fee = 0.0
          
      try:
          extension_amount = float(self.extension_amount_label.text)
      except ValueError:
          extension_amount = 0.0
          
      try:
          npa_fee = float(self.npa.text)
      except ValueError:
          npa_fee = 0.0
      
      # Calculate the extra fee
      extra_fee = lapsed_fee + default_fee + extension_amount + npa_fee
      loan_details = {
        'i_r': self.i_r.text,
        'emi': self.emi.text,
        'total_emi_amount': self.total_emi_amount_label.text,
        'emi_amount': self.emi_amount_label.text,
        'loan_id': self.selected_row['loan_id'],
        'loan_amount': self.loan_amount_label.text,
        'tenure': self.tenure_label.text,
        'account_no': self.account_no_label.text,
        'interest_amount': self.interest_label.text,
        'remainining_amount': self.remainining_amount.text,
        'borrower_customer_id': self.selected_row['borrower_customer_id'],
        'lender_customer_id': self.selected_row['lender_customer_id'],
        'lender_email' : self.selected_row['lender_email_id'],
        'borrower_email' : self.selected_row['borrower_email_id'],
        'emi_payment_type' : self.selected_row['emi_payment_type'],
        'current_emi_number' : int(self.selected_row['emi_number']),
        'extra_fee':extra_fee,
        'prev_scheduled_payment' : self.selected_row['scheduled_payment'],
        'prev_next_payment' : self.selected_row['next_payment'],
        'product_id' : self.selected_row['product_id'],
        'loan_state_status' : self.selected_row['loan_state_status'],
        # 'part_payment_date' : self.selected_row['part_payment_date'],
        # 'payment_type' : self.selected_row['payment_type'],
        'tenure':self.tenure_label.text,
        'borrower_full_name':  self.selected_row['borrower_full_name']
    }
    
    # Open the part_payment form and pass loan_details as a parameter
      open_form('lendor.dashboard.today_dues.View_Details.part_payment_copy', loan_details=loan_details , selected_row=self.selected_row)
