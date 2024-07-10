import anvil.secrets
import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
# from . import bessem as bessemfunctions
from . import wallet
import anvil.pdf
# import datetime

@anvil.server.callable()
def create_pdf1(name, image_source, selected_row):
    # A4 size in points (width, height) is (595, 842), for landscape swap to (842, 595)
    # landscape_a4 = (842, 595)   
    # Create the PDF in landscape mode by specifying the size
    pdf = anvil.pdf.PDFRenderer(landscape=True).render_form("borrower.dashboard.borrower_portfolio", selected_row=selected_row)   
    return pdf

@anvil.server.callable
def add_borrower_step1(qualification,user_id):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['qualification'] = qualification
    row[0]['form_count']=1
    
@anvil.server.callable
def add_borrower_step2(status_of_user,user_id):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['profession'] = status_of_user
    row[0]['form_count']=2

@anvil.server.callable
def add_borrower_student(college_name,college_id,college_proof,college_address,user_id):
  row=app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['college_name']=college_name
    row[0]['college_id']=college_id
    row[0]['college_address']=college_address
    row[0]['college_proof']=college_proof
    row[0]['form_count']=2

@anvil.server.callable
def add_borrwer_self_employment(status_of_user,user_id):
  row=app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['self_employment']=status_of_user
    row[0]['form_count']=2.2

@anvil.server.callable
def add_borrower_farmer(land_type,total_acres,crop_name,farmer_earnings,user_id):
  total_acres_numeric = float(total_acres)
  row = app_tables.fin_user_profile.search(customer_id = user_id)
  if row:
    row[0]['land_type'] = land_type
    row[0]['total_acres'] = total_acres_numeric
    row[0]['crop_name'] = crop_name
    row[0]['farmer_earnings'] = farmer_earnings 
    row[0]['form_count'] = 2

@anvil.server.callable
def add_borrower_step3(marital_status,user_id):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['marital_status']=marital_status
    row[0]['form_count']=3



@anvil.server.callable
def add_borrower_step4(home_loan,other_loan,user_id,credit_card,vehicle):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['home_loan'] = home_loan
    row[0]['other_loan']=other_loan
    row[0]['credit_card_loans']=credit_card
    row[0]['vehicle_loan']=vehicle
    row[0]['form_count']=4
    
@anvil.server.callable
def add_borrower_step5(account_name, account_type,account_number,bank_name, user_id):
  row = app_tables.fin_user_profile.search(customer_id=user_id)
  if row:
    row[0]['account_name'] = account_name
    row[0]['account_type'] = account_type
    row[0]['account_number'] = account_number
    row[0]['bank_name'] = bank_name  
    row[0]['form_count']=5

@anvil.server.callable
def add_borrower_step6(bank_id, bank_branch, user_id):
    print('inside add_borrower_step6')
    row = app_tables.fin_user_profile.search(customer_id=user_id)
    _user_type = "borrower"
    if row:
        row[0]['bank_id'] = bank_id
        row[0]['account_bank_branch'] = bank_branch
        ascend_value = final_points_update_ascend_table(user_id)
        if ascend_value is not None:
           row[0]['ascend_value'] = float(ascend_value)
        else:
           row[0]['ascend_value'] = 0.0
           print("Warning: Ascend Value is None for user_id:", user_id)

        row[0]['usertype'] = 'borrower'
        row[0]['last_confirm'] = True
        row[0]['form_count'] = 6
        wallet.find_user_update_type(user_id,row[0]['full_name'],_user_type)
        # user_exists = app_tables.fin_wallet.search(customer_id=user_id)
        # if user_exists:
        #     wallet.find_user_update_type(user_id, row[0]['full_name'],_user_type)      

        # Search for an existing row with the same email_id in fin_borrower table
        manage_credit_limit_row = app_tables.fin_manage_credit_limit.get()
        print("manage credit limit")
        print(app_tables.fin_manage_credit_limit.get())
        
        
        # if manage_credit_limit_row:
        
        credit_limit_value = manage_credit_limit_row['credit_limit']
        existing_borrower_row = app_tables.fin_borrower.get(email_id=row[0]['email_user'])
        print("existing borrower row")
        print(existing_borrower_row)
        
        if existing_borrower_row:
            # If a row exists, update the existing row
            existing_borrower_row['user_name'] = row[0]['full_name']
            existing_borrower_row['bank_acc_details'] = row[0]['account_number']
            existing_borrower_row['ascend_score'] = row[0]['ascend_value']
            existing_borrower_row['credit_limit'] =  credit_limit_value

            if row[0]['last_confirm']:
                existing_borrower_row['borrower_since'] = datetime.now().date()

            existing_borrower_row.update()
        else:
            # If no row exists, create a new row in fin_borrower table
            fin_borrower_row = app_tables.fin_borrower.add_row(
                customer_id=row[0]['customer_id'],
                email_id=row[0]['email_user'],
                user_name=row[0]['full_name'],
                bank_acc_details=row[0]['account_number'],
                ascend_score=row[0]['ascend_value'],
                credit_limit= credit_limit_value
            )

            if row[0]['last_confirm']:
                fin_borrower_row['borrower_since'] = datetime.now().date()

            fin_borrower_row.update()
    else:
        # If user not found in fin_user_profile table
        raise ValueError("User not found in fin_user_profile table")



@anvil.server.callable
def update_loan_details(loan_id, emi, total_repayment_amount, interest_rate):
    rows = app_tables.fin_loan_details.search(loan_id=loan_id)

    if rows:
        row = rows[0]
        row['emi'] = emi
        row['total_repayment_amount'] = total_repayment_amount
        row['interest_rate'] = interest_rate
        row.update()
    else:
        raise ValueError(f"Row not found for loan_id {loan_id}")

@anvil.server.callable
def add_loan_details(loan_amount, tenure,user_id,interest_rate, total_repayment_amount,product_id,membership_type,credit_limit,product_name,emi_payment_type,processing_fee_amount,total_interest,product_description,emi):
                                    
    
    # Generate a unique loan ID and get the updated counter
    loan_id = generate_loan_id()
    loan_created_timestamp = datetime.now().date()

    # Search for the user profile
    user_profiles = app_tables.fin_user_profile.search(customer_id=user_id)
    
    if user_profiles and len(user_profiles) > 0:
        # If there is a user profile, get the first one
        user_profile = user_profiles[0]

        # Extract the full name from the user profile
        borrower_full_name = user_profile['full_name']
        borrower_email_id = user_profile['email_user']

 
        app_tables.fin_loan_details.add_row(
          loan_amount=loan_amount,
          tenure=tenure,
          borrower_customer_id=user_id,
          interest_rate = interest_rate,
          total_repayment_amount = total_repayment_amount,
          loan_id = loan_id,
          membership_type = membership_type,
          credit_limit=int(credit_limit),
          borrower_full_name = borrower_full_name,
          borrower_email_id = borrower_email_id,
          loan_updated_status = "under process",
          borrower_loan_created_timestamp=loan_created_timestamp,
          product_id = product_id,
          product_name = product_name,
          emi_payment_type = emi_payment_type,
          total_processing_fee_amount = processing_fee_amount,
          total_interest_amount = total_interest,
          product_description = product_description,
          monthly_emi = emi,
          remaining_amount=total_repayment_amount
         )

        # Return the generated loan ID to the client
        return loan_id
    else:
        # Handle the case where no user profile is found
        return "User profile not found"


def generate_loan_id():
    # Query the latest loan ID from the data table
    latest_loan = app_tables.fin_loan_details.search(tables.order_by("loan_id", ascending=False))

    if latest_loan and len(latest_loan) > 0:
        # If there are existing loans, increment the last loan ID
        last_loan_id = latest_loan[0]['loan_id']
        counter = int(last_loan_id[2:]) + 1
    else:
        # If there are no existing loans, start the counter at 100001
        counter = 1000001

    # Return the new loan ID
    return f"LA{counter}"


@anvil.server.callable
def add_fin_emi_details(borrower_customer_id, borrower_email, scheduled_payment,
                     payment_number, payment_date, loan_id, emi_status):
    # Generate a unique loan ID and get the updated counter
    emi_id = generate_emi_id()
    loan_details = app_tables.fin_loan_details.search(borrower_customer_id = borrower_customer_id)
                       
    if loan_details and len(loan_details) > 0:
        loan_details = loan_details[0]
        loan_id = loan_details['loan_id']
    
        # Add details to fin_emi_table
        app_tables.fin_emi_table.add_row(
            emi_id=emi_id,
            borrower_customer_id=borrower_customer_id,  # Fix: use borrower_customer_id instead of user_id
            borrower_email=borrower_email,
            scheduled_payment=scheduled_payment,
            payment_number=payment_number,
            payment_date=payment_date,
            loan_id=loan_id,
            emi_status=emi_status
        )
        return emi_id
    else:
      return 'loan details not found'
      

def generate_emi_id():
    # Query the latest EMI ID from the data table
    latest_emi = app_tables.fin_emi_table.search(tables.order_by("emi_id", ascending=False))

    if latest_emi and len(latest_emi) > 0:
        # If there are existing EMIs, increment the last EMI ID
        last_emi_id = latest_emi[0]['emi_id']
        counter = int(last_emi_id[3:]) + 1
    else:
        # If there are no existing EMIs, start the counter at 1000
        counter = 1000

    # Return the new EMI ID
    return f"EMI{counter}"




# Ascend Score code
@anvil.server.callable
def final_points_update_ascend_table(user_id):
    user_points = get_user_points(user_id)
    group_points = get_group_points(user_id)

    print(f"Debug: user_points={user_points}, group_points={group_points}")

    if user_points is not None and group_points is not None and group_points != 0:
        points = (user_points / group_points) * 100

        final_points = '{:.2f}'.format(points)

        return final_points
    return None

def get_user_points(id):
    users = app_tables.fin_user_profile.search(customer_id=id)

    if users:
        user = users[0]
        user_points = 0
        email = user['email_user']
        gender = user['gender'].lower() if user['gender'] else None
        qualification = user['qualification'].lower() if user['qualification'] else None
        marital_status = user['marital_status'].lower() if user['marital_status'] else None
        profession = user['profession'].lower() if user['profession'] else None
        user_age = user['user_age']
        organization_type = user['organization_type'].lower() if user['organization_type'] else None
        present_address = user['present_address'].lower() if user['present_address'] else None
        duration_at_address = str(user['duration_at_address']).lower() if user['duration_at_address'] else None
        self_employment = user['self_employment']
        if self_employment is not None:
            self_employment = self_employment.lower()
        occupation_type = user['occupation_type']
        age_of_business = user['business_age']
        salary_type = user['salary_type'].lower() if user['salary_type'] else None
        home_loan = user['home_loan'].lower() if user['home_loan'] else None
        other_loan = user['other_loan'].lower() if user['other_loan'] else None
        credit_card_loan = user['credit_card_loans'].lower() if user['credit_card_loans'] else None
        vehicle_loan = user['vehicle_loan'].lower() if user['vehicle_loan'] else None

        user_age_range = None
        if user_age is not None:
           if 18 <= user_age <= 24:
              user_age_range = '18-24'
           elif 25 <= user_age <= 30:
              user_age_range = '25-30'
           elif 31 <= user_age <= 36:
              user_age_range = '31-36'
           elif 37 <= user_age <= 40:
              user_age_range = '37-40'
           elif 41 <= user_age <= 50:
              user_age_range = '41-50'
           else:
              user_age_range = '51+'

        search_categories = {
            'gender': gender,
            'present_address': present_address,
            'duration_at_address': duration_at_address,
            'qualification': qualification,
            'profession': profession,
            'home_loan': home_loan,
            'other_loan': other_loan,
            'credit_card_loan': credit_card_loan,
            'vehicle_loan': vehicle_loan
        }

        for category, value in search_categories.items():
            category_search = app_tables.fin_admin_ascend_categories.search(group_name=category)
            print(f"Size of {category}_search: {len(category_search)}")
            for row in category_search:
                if row['sub_category'].split(","): 
                    sub_categories = row['sub_category'].split(",")
                    min_points = row['min_points']
                    for sub_cat in sub_categories:
                        if sub_cat.strip().lower() == value:
                            category_points = min_points
                            print(f"{category.capitalize()} Points:", category_points)
                            user_points += category_points
                            break
                elif row['sub_category'].lower() == value:
                    category_points = row['min_points']
                    print(f"{category.capitalize()} Points:", category_points)
                    user_points += category_points
                    break

        if profession.lower() == 'self employment' or profession.lower() == 'employee':
           self_employment_search = app_tables.fin_admin_ascend_categories.search(group_name='profession')
           print(f"Size of self_employment_search: {len(self_employment_search)}")
           for row in self_employment_search:
             if row['sub_category']: 
               sub_categories = row['sub_category'].split(",")
               min_points = row['min_points']
               for sub_cat in sub_categories:
                 if profession and sub_cat.strip().lower() == profession.lower() or occupation_type and sub_cat.strip().lower() == occupation_type.lower():
                    user_points += min_points
                    print("Self Employment Points:", min_points)
                    break
             else: 
                if profession and row['sub_category'].lower() == profession.lower() or occupation_type and row['sub_category'].lower() == occupation_type.lower():
                   user_points += row['min_points']
                   print("Self Employment Points:", row['min_points'])
                   break

        elif profession == 'employee':
           for category in ['organization_type', 'salary_type']:
              category_search = app_tables.fin_admin_ascend_categories.search(group_name=category)
              print(f"Size of {category}_search: {len(category_search)}")
              for row in category_search:
                 if row['sub_category'].split(","):
                    sub_categories = row['sub_category'].split(",")
                    min_points = row['min_points']
                    for sub_cat in sub_categories:
                       if sub_cat.strip().lower() == locals()[category]:
                          category_points = min_points
                          print(f"{category.capitalize()} Points:", category_points)
                          user_points += category_points
                          break
                 elif row['sub_category'].lower() == locals()[category]:
                    category_points = row['min_points']
                    print(f"{category.capitalize()} Points:", category_points)
                    user_points += category_points
                    break

        elif profession == 'business':
           business_age_search = app_tables.fin_admin_ascend_categories.search(group_name='age_of_business')
           print(f"Size of business_age_search: {len(business_age_search)}")
           for row in business_age_search:
              if row['sub_category'].split(","): 
                sub_categories = row['sub_category'].split(",")
                min_points = row['min_points']
                for sub_cat in sub_categories:
                  if sub_cat.strip().lower() == age_of_business.lower():
                      user_points += min_points
                      print("Business Age Points:", min_points)
                      break
              elif row['sub_category'].lower() == age_of_business.lower():
                min_points = row['min_points']
                print("Business Age Points:", min_points)
                user_points += min_points
                break

        marital_status_search = app_tables.fin_admin_ascend_categories.search(group_name='marital_status')
        print(f"Size of marital_status_search: {len(marital_status_search)}")
        for row in marital_status_search:
           if row['sub_category'].split(","):
             sub_categories = row['sub_category'].split(",")
             min_points = row['min_points']
             for sub_cat in sub_categories:
               if sub_cat.strip().lower() == marital_status.lower() and any(age.strip().lower() == user_age_range.lower() for age in row['age'].split(",")):
                   marital_status_points = min_points
                   print("Marital Status Points:", marital_status_points)
                   user_points += marital_status_points
                   break
           elif row['sub_category'].lower() == marital_status.lower() and any(age.strip().lower() == user_age_range.lower() for age in row['age'].split(",")):
               marital_status_points = row['min_points']
               print("Marital Status Points:", marital_status_points)
               user_points += marital_status_points
               break

        data = app_tables.fin_guarantor_details.search(customer_id=id)
        for item in data:
           another_person = item['another_person'].lower()
           spouse_profession = item['guarantor_profession'].lower()

           if marital_status == 'married' and another_person == 'spouse':
               spouse_profession_search = app_tables.fin_admin_ascend_categories.search(group_name='spouse_profession')
               print(f"Size of spouse_profession_search: {len(spouse_profession_search)}")

               for row in spouse_profession_search:
                   if row['sub_category'].split(","): 
                       sub_categories = row['sub_category'].split(",")
                       min_points = row['min_points']

                       for sub_cat in sub_categories:
                           if sub_cat.strip().lower() == spouse_profession.lower():
                               user_points += min_points
                               print("Spouse profession Points:", min_points)
                               break

                       break  

                   elif row['sub_category'].lower() == spouse_profession.lower():
                       min_points = row['min_points']
                       print("Spouse profession Points:", min_points)
                       user_points += min_points
                       break  
                     
               break 
        return user_points

    else:
        return None


def get_group_points(customer_id):
    # Fetch user details
    user = app_tables.fin_user_profile.get(customer_id=customer_id)
    if user:
        profession = user['profession'].lower() if user['profession'] else None
        marital_status = user['marital_status'].lower() if user['marital_status'] else None
        
        loans_data = app_tables.fin_guarantor_details.search(customer_id=customer_id)
        another_person = ''
        spouse_profession = ''
        if loans_data:
            for item in loans_data:
                another_person = item['another_person'].lower()
                spouse_profession = item['guarantor_profession'].lower()

        groups = app_tables.fin_admin_ascend_groups.search()
        if groups:
            group_points = 0
            for group_row in groups:
                group_name = group_row['group_name'].lower()
                max_points = group_row['max_points']
                
                if group_name == 'gender':
                    group_points += max_points
                    print("GroupPoints Gender:", group_points)
                elif group_name == 'present_address':
                    group_points += max_points
                    print("GroupPoints present_address:", group_points)
                elif group_name == 'duration_at_address':
                    group_points += max_points
                    print("GroupPoints duration_at_address:", group_points)
                elif group_name == 'qualification':
                    group_points += max_points
                    print("GroupPoints qualification:", group_points)
                elif group_name == 'home_loan':
                    group_points += max_points
                    print("GroupPoints home_loan:", group_points)
                elif group_name == 'other_loan':
                    group_points += max_points
                    print("GroupPoints other_loan:", group_points)
                elif group_name == 'credit_card_loan':
                    group_points += max_points
                    print("GroupPoints credit_card_loan:", group_points)
                elif group_name == 'vehicle_loan':
                    group_points += max_points
                    print("GroupPoints vehicle_loan:", group_points)
                elif group_name == 'profession':
                    group_points += max_points
                    print("GroupPoints profession:", group_points)
                elif group_name == 'organization_type' and profession == 'employee':
                    group_points += max_points
                    print("GroupPoints organization_type:", group_points)
                elif group_name == 'salary_type' and profession == 'employee':
                    group_points += max_points
                    print("GroupPoints salary_type:", group_points)
                elif group_name == 'age_of_business' and profession == 'business':
                    group_points += max_points
                    print("GroupPoints age_of_business:", group_points)
                elif group_name == 'marital_status':
                    group_points += max_points
                    print("GroupPoints marital_status:", group_points)
                elif group_name == 'spouse_profession' and marital_status == 'married' and another_person == 'spouse':
                    group_points += max_points
                    print("GroupPoints spouse_profession:", group_points)

            return group_points

    return None


@anvil.server.callable
def create_zaphod_pdf():
  media_object = anvil.pdf.render_form('borrower.dashboard.borrower_portfolio')
  return media_object









# @anvil.server.callable
# def get_notifications(user_id):
#     notifications = []
#     loans = app_tables.fin_loan_details.search(borrower_customer_id=user_id)
#     for loan in loans:
#         loan_status = loan['loan_updated_status']
#         if loan_status in ['rejected', 'approved', 'disbursed']:
#             if loan_status == 'rejected':
#                 notification_date = loan['lender_rejected_timestamp']
#             elif loan_status == 'approved':
#                 notification_date = loan['lender_accepted_timestamp']
#             elif loan_status == 'disbursed':
#                 notification_date = loan['loan_disbursed_timestamp']
            
#             notifications.append({
#                 'message': f"Your loan for {loan['product_name']} is {loan_status}",
#                 'loan_updated_status': loan_status,
#                 'read': loan['notification_read'] if 'notification_read' in loan else False,
#                 'date': notification_date,
#                 'customer_id': loan['borrower_customer_id'],
#                 'loan_id': loan['loan_id']
#             })
#     return notifications

# @anvil.server.callable
# def mark_notification_as_read(loan_id):
#     loan = app_tables.fin_loan_details.get(loan_id=loan_id)
#     if loan:
#         loan['notification_read'] = True  # Directly update the field

# @anvil.server.callable
# def update_notifications(user_id):
#     loans = app_tables.fin_loan_details.search(borrower_customer_id=user_id)
#     for loan in loans:
#         loan_status = loan['loan_updated_status']
#         if loan_status in ['rejected', 'approved', 'disbursed']:
#             loan['notification_read'] = False
#         else:
#             loan['notification_read'] = True


@anvil.server.callable
def get_notifications(user_id):
    notifications = []
    loans = app_tables.fin_loan_details.search(borrower_customer_id=user_id)
    for loan in loans:
        loan_status = loan['loan_updated_status']
        if loan_status in ['rejected', 'approved', 'disbursed']:
            if loan_status == 'rejected':
                notification_date = loan['lender_rejected_timestamp']
            elif loan_status == 'approved':
                notification_date = loan['lender_accepted_timestamp']
            elif loan_status == 'disbursed':
                notification_date = loan['loan_disbursed_timestamp']
            
            notifications.append({
                'message': f"Your loan for {loan['product_name']} is {loan_status}",
                'loan_updated_status': loan_status,
                'read': loan['notification_read'] if 'notification_read' in loan else False,
                'date': notification_date,
                'customer_id': loan['borrower_customer_id'],
                'loan_id': loan['loan_id']
            })
    return notifications

@anvil.server.callable
def mark_notification_as_read(loan_id):
    loan = app_tables.fin_loan_details.get(loan_id=loan_id)
    if loan:
        loan['notification_read'] = True  # Directly update the field
        loan.update()

@anvil.server.callable
def update_notifications(user_id):
    loans = app_tables.fin_loan_details.search(borrower_customer_id=user_id)
    for loan in loans:
        loan_status = loan['loan_updated_status']
        if loan_status in ['rejected', 'approved', 'disbursed']:
            loan['notification_read'] = False
        else:
            loan['notification_read'] = True
        loan.update()













# second
# def get_user_points(id):
#     users = app_tables.fin_user_profile.search(customer_id=id)
#     if users:
#         user = users[0]
#         email = user['email_user']
#         gender = user['gender'].lower() 
#         qualification = user['qualification'].lower()  
#         marital_status = user['marital_status'].lower()  
#         profession = user['profession'].lower()
#         user_age = user['user_age']
#         organization_type = user['organization_type'].lower()
#         present_address = user['present_address'].lower()
#         duration_at_address = str(user['duration_at_address']).lower()
#         self_employment = user['self_employment']
#         if self_employment is not None:
#           self_employment = self_employment.lower()
#         age_of_business = user['business_age']
#         salary_type = user['salary_type'].lower()
#         home_loan = user['home_loan'].lower()
#         other_loan = user['other_loan'].lower()
#         credit_card_loan = user['credit_card_loans'].lower()
#         vehicle_loan = user['vehicle_loan'].lower()
        
#         user_points = 0

#         # Find the age range for the user_age
#         user_age_range = None
#         if 18 <= user_age <= 24:
#             user_age_range = '18-24'
#         elif 25 <= user_age <= 30:
#             user_age_range = '25-30'
#         elif 31 <= user_age <= 36:
#             user_age_range = '31-36'
#         elif 37 <= user_age <= 40:
#             user_age_range = '37-40'
#         elif 41 <= user_age <= 50:
#             user_age_range = '41-50'
#         else:
#             user_age_range = '51'      
      
#         gender_search = app_tables.fin_admin_beseem_categories.search(group_name='gender', sub_category=gender.lower())
#         if gender_search:
#             gender_points = gender_search[0]['min_points']
#             print("Gender Points:", gender_points)
#             user_points += gender_points

#         present_address_search = app_tables.fin_admin_beseem_categories.search(group_name='present_address', sub_category=present_address.lower())
#         if present_address_search:
#             present_address_points = present_address_search[0]['min_points']
#             print("Present address Points:", present_address_points)
#             user_points += present_address_points

#         duration_at_address_search = app_tables.fin_admin_beseem_categories.search(group_name='duration_at_address', sub_category=duration_at_address.lower())
#         if duration_at_address_search:
#             duration_at_address_points = duration_at_address_search[0]['min_points']
#             print("Duration at address Points:", duration_at_address_points)
#             user_points += duration_at_address_points

#         qualification_search = app_tables.fin_admin_beseem_categories.search(group_name='qualification', sub_category=qualification.lower())
#         if qualification_search:
#            qualification_points = qualification_search[0]['min_points']
#            print("Qualification Points:", qualification_points)
#            user_points += qualification_points
#         else:
#            print("Qualification not found in categories.")

        # profession_search = app_tables.fin_admin_beseem_categories.search(group_name='profession', sub_category=profession.lower())
        # if profession_search:
        #     profession_points = profession_search[0]['min_points']
        #     print("Profession Points:", profession_points)
        #     user_points += profession_points

        #     if profession == 'self employment':
        #         self_employment_search = app_tables.fin_admin_beseem_categories.search(group_name='profession', sub_category=self_employment.lower())
        #         if self_employment_search:
        #             self_employment_points = self_employment_search[0]['min_points']
        #             print("self employment Points:", self_employment_points)
        #             user_points += self_employment_points
                
        #     elif profession == 'employee':
        #         organization_type_search = app_tables.fin_admin_beseem_categories.search(group_name='organization_type', sub_category=organization_type.lower())
        #         if organization_type_search:
        #             organization_type_points = organization_type_search[0]['min_points']
        #             print("Organization type Points:", organization_type_points)
        #             user_points += organization_type_points
        #         salary_type_search = app_tables.fin_admin_beseem_categories.search(group_name='salary_type', sub_category=salary_type.lower())
        #         if salary_type_search:
        #             salary_type_points = salary_type_search[0]['min_points']
        #             print("Salary type Points:", salary_type_points)

        #     elif profession == 'business':
        #         business_age_search = app_tables.fin_admin_beseem_categories.search(group_name='age_of_business', sub_category=age_of_business.lower())
        #         if business_age_search:
        #             business_age_points = business_age_search[0]['min_points']
        #             print("Business Age Points:", business_age_points)
        #             user_points += business_age_points
                  
        # marital_status_search = app_tables.fin_admin_beseem_categories.search(group_name='marital_status', sub_category=marital_status.lower(), age=user_age_range)
        # if marital_status_search:
        #     marital_status_points = marital_status_search[0]['min_points']
        #     print("Marital status Points:", marital_status_points)
        #     user_points += marital_status_points
    
        #     data = app_tables.fin_guarantor_details.search(customer_id=id)
        #     if data:
        #         for item in data:
        #             another_person = item['another_person'].lower()
        #             spouse_profession = item['guarantor_profession'].lower()

        #             if marital_status == 'married' and another_person == 'spouse':
        #                 spouse_profession_search = app_tables.fin_admin_beseem_categories.search(group_name='spouse_profession', sub_category=spouse_profession.lower())
        #                 if spouse_profession_search:
        #                     spouse_profession_points = spouse_profession_search[0]['min_points']
        #                     print("Spouse profession:", spouse_profession_points)
        #                     user_points += spouse_profession_points        

#         home_loan_search = app_tables.fin_admin_beseem_categories.search(group_name='home_loan', sub_category=home_loan.lower())
#         if home_loan_search:
#             home_loan_points = home_loan_search[0]['min_points']
#             print("Home loan Points:", home_loan_points)
#             user_points += home_loan_points

#         other_loan_search = app_tables.fin_admin_beseem_categories.search(group_name='other_loan', sub_category=other_loan.lower())
#         if other_loan_search:
#             other_loan_points = other_loan_search[0]['min_points']
#             print("Other loan Points:", other_loan_points)
#             user_points += other_loan_points
          
#         credit_card_loan_search = app_tables.fin_admin_beseem_categories.search(group_name='credit_card_loan', sub_category=credit_card_loan.lower())
#         if credit_card_loan_search:
#             credit_card_loan_points = credit_card_loan_search[0]['min_points']
#             print("Credit card loan Points:", credit_card_loan_points)
#             user_points += credit_card_loan_points

#         vehicle_loan_search = app_tables.fin_admin_beseem_categories.search(group_name='vehicle_loan', sub_category=vehicle_loan.lower())
#         if vehicle_loan_search:
#             vehicle_loan_points = vehicle_loan_search[0]['min_points']
#             print("Vehicle Points:", vehicle_loan_points)
#             user_points += vehicle_loan_points                     

#         return user_points
#     else:
#         return None

# third
# @anvil.server.callable
# def get_user_points(id):
#     users = app_tables.fin_user_profile.search(customer_id=id)

#     if users:
#         user = users[0]
#         user_points = 0
#         email = user['email_user']
#         gender = user['gender'].lower()
#         qualification = user['qualification'].lower()
#         marital_status = user['marital_status'].lower()
#         profession = user['profession'].lower()
#         user_age = user['user_age']
#         organization_type = user['organization_type'].lower()
#         present_address = user['present_address'].lower()
#         duration_at_address = str(user['duration_at_address']).lower()
#         self_employment = user['self_employment']
#         if self_employment is not None:
#             self_employment = self_employment.lower()
#         age_of_business = user['business_age']
#         salary_type = user['salary_type'].lower()
#         home_loan = user['home_loan'].lower()
#         other_loan = user['other_loan'].lower()
#         credit_card_loan = user['credit_card_loans'].lower()
#         vehicle_loan = user['vehicle_loan'].lower()

#         if 18 <= user_age <= 24:
#             user_age_range = '18-24'
#         elif 25 <= user_age <= 30:
#             user_age_range = '25-30'
#         elif 31 <= user_age <= 36:
#             user_age_range = '31-36'
#         elif 37 <= user_age <= 40:
#             user_age_range = '37-40'
#         elif 41 <= user_age <= 50:
#             user_age_range = '41-50'
#         else:
#             user_age_range = '51+'

#         # categories_to_check = ['gender', 'present_address', 'duration_at_address']
#         # for category in categories_to_check:
#         #     category_search = app_tables.fin_admin_beseem_categories.search(group_name=category, sub_category=locals()[category])
#         #     print("Category_Search" ,category_search)
#         #     for row in category_search:
#         #         basic_points = row['min_points']
#         #         print("Basic Points:", basic_points)
#         #         user_points += basic_points

#         gender_search = app_tables.fin_admin_beseem_categories.search(group_name='gender', sub_category=gender.lower())
#         for row in gender_search:
#             print("Size of gender_search_search:", gender_search)
#             gender_points = row['min_points']
#             print("Gender Points:", gender_points)
#             user_points += gender_points

#         present_address_search = app_tables.fin_admin_beseem_categories.search(group_name='present_address', sub_category=present_address.lower())
#         for row in present_address_search:
#             print("Size of present_address_search:", len(present_address_search))
#             present_address_points = row['min_points']
#             print("Present address Points:", present_address_points)
#             user_points += present_address_points

#         duration_at_address_search = app_tables.fin_admin_beseem_categories.search(group_name='duration_at_address', sub_category=duration_at_address.lower())
#         for row in duration_at_address_search:
#             duration_at_address_points = row['min_points']
#             print("Duration_at_address Points:", duration_at_address_points)
#             user_points += duration_at_address_points
      
#         qualification_search = app_tables.fin_admin_beseem_categories.search(group_name='qualification', sub_category=qualification)
#         for row in qualification_search:
#             qualification_points = row['min_points']
#             print("Qualification Points:", qualification_points)
#             user_points += qualification_points
                 
#         profession_search = app_tables.fin_admin_beseem_categories.search(group_name='profession', sub_category=profession)
#         for row in profession_search:
#             profession_points = row['min_points']
#             print("Profession Points:", profession_points)
#             user_points += profession_points

#             if profession == 'self employment':
#                 self_employment_search = app_tables.fin_admin_beseem_categories.search(group_name='profession', sub_category=self_employment)
#                 for row in self_employment_search:
#                     self_employment_points = row['min_points']
#                     print("Self employment Points:", self_employment_points)
#                     user_points += self_employment_points
#             elif profession == 'employee':
#                 categories_to_check = ['organization_type', 'salary_type']
#                 for category in categories_to_check:
#                     category_search = app_tables.fin_admin_beseem_categories.search(group_name=category, sub_category=locals()[category])
#                     for row in category_search:
#                         employee_points = row['min_points']
#                         print("Employee Points:", employee_points)
#                         user_points += employee_points
#             elif profession == 'business':
#                 business_age_search = app_tables.fin_admin_beseem_categories.search(group_name='age_of_business', sub_category=age_of_business)
#                 for row in business_age_search:
#                     business_age_points = row['min_points']
#                     print("Business age Points:", business_age_points)
#                     user_points += business_age_points

#         marital_status_search = app_tables.fin_admin_beseem_categories.search(group_name='marital_status', sub_category=marital_status, age=user_age_range)
#         for row in marital_status_search:
#             marital_status_points = row['min_points']
#             print("Marital Status Points:", marital_status_points)
#             user_points += marital_status_points

#             data = app_tables.fin_guarantor_details.search(customer_id=id)
#             for item in data:
#                 another_person = item['another_person'].lower()
#                 spouse_profession = item['guarantor_profession'].lower()

#                 if marital_status == 'married' and another_person == 'spouse':
#                     spouse_profession_search = app_tables.fin_admin_beseem_categories.search(group_name='spouse_profession', sub_category=spouse_profession.lower())
#                     for row in spouse_profession_search:
#                         spouse_profession_points = row['min_points']
#                         print("Spouse profession Points:", spouse_profession_points)
#                         user_points += spouse_profession_points

#         loans_to_check = ['home_loan', 'other_loan', 'credit_card_loan', 'vehicle_loan']
#         for loan_category in loans_to_check:
#             loan_search = app_tables.fin_admin_beseem_categories.search(group_name=loan_category, sub_category=locals()[loan_category])
#             for row in loan_search:
#                 loan_points = row['min_points']
#                 print("Loan Points:", loan_points)
#                 user_points += loan_points

#         return user_points

#     else:
#         return None


# def get_group_points():
#     groups = app_tables.fin_admin_beseem_groups.search()

#     if groups:
#         group_points = 0

#         for group_row in groups:
#             group_points += group_row['max_points']

#         return group_points
#     return None








