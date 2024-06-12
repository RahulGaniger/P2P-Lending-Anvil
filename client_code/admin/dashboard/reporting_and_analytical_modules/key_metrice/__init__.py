from ._anvil_designer import key_metriceTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go


class key_metrice(key_metriceTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_panel_1.items = []
    self.all_items = []

    # Aggregate counts for all risk levels and initialize plot
    self.aggregate_counts()
    self.initialize_plot()
    

    # Any code you write here will run before the form opens.


  def aggregate_counts(self):
    """Aggregate the counts of loans for each risk level"""
    self.very_count = len(self.get_filtered_rows("VeryGood"))
    self.good_count = len(self.get_filtered_rows("Good"))
    self.average_count = len(self.get_filtered_rows("Average"))
    self.bad_count = len(self.get_filtered_rows("Bad"))



  def get_filtered_rows(self, risk_level):
    """Fetch and filter rows from EMI table based on risk level"""
    lapsed_settings = app_tables.fin_ascend_score_range.get(ascend_category=risk_level)
    min_days = lapsed_settings['min_ascend_score_range']
    max_days = lapsed_settings['max_ascend_score_range']
    emi_rows = app_tables.fin_borrower.search()
    return [row for row in emi_rows if min_days <= row['ascend_score'] <= max_days]

  def initialize_plot(self):
    """Initialize the plot with aggregated counts"""
    fig = go.Figure(data=[
      go.Bar(name='Very Good', x=['Very Good'], y=[self.very_count], marker_color='green'),
      go.Bar(name='Good', x=['Good'], y=[self.good_count], marker_color='orange'),
      go.Bar(name='Average', x=['Average'], y=[self.average_count], marker_color='#F08080'),
      go.Bar(name='Bad', x=['Bad'], y=[self.bad_count], marker_color='red')
    ])
    
    fig.update_layout(title='Loan Risk Distribution',
                      xaxis={'title': 'Ascend Categories'},
                      yaxis={'title': 'Number of Borrower'},
                      barmode='group')
    
    self.risk_plot.data = fig.data
    self.risk_plot.layout = fig.layout

  def very_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.text_box_search.text = ""
    filtered_rows = self.get_filtered_rows("VeryGood")

    # Set the filtered rows to the repeating panel
    result = []
    for row in filtered_rows:
      user_details = app_tables.fin_user_profile.get(customer_id=row['customer_id'])
      if user_details:
        combined_data = {
          'customer_id': row['customer_id'],
          'borrower_since': row['borrower_since'],
          'user_name': row['user_name'],
          'ascend_score': row['ascend_score'],
          'email_id': row['email_id'],
          'credit_limit': row['credit_limit'],
          'mobile': user_details['mobile'],
          # 'ascend_score': row['ascend_score'],

        }
        result.append(combined_data)
    self.all_items = result
    self.repeating_panel_1.items = result
    self.text_box_search.placeholder = 'Search Verygood ascend score'
    self.label.visible = True
    self.label.text = 'Very good Ascend Score details'
    self.data_grid_1.visible = True
    self.column_panel_1.visible = True
    self.data_grid_2.visible = False

    # Update the plot
    # self.aggregate_counts()
    # self.update_plot()

  def good_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.text_box_search.text = ""
    filtered_rows = self.get_filtered_rows("Good")
  
    # Fetch additional details from the loan details table
    result = []
    for row in filtered_rows:
      user_details = app_tables.fin_user_profile.get(customer_id=row['customer_id'])
      if user_details:
        combined_data = {
          'customer_id': row['customer_id'],
          'borrower_since': row['borrower_since'],
          'user_name': row['user_name'],
          'ascend_score': row['ascend_score'],
          'email_id': row['email_id'],
          'credit_limit': row['credit_limit'],
          'mobile': user_details['mobile'],

        }
        result.append(combined_data)
    self.all_items = result
    self.repeating_panel_1.items = result
    self.text_box_search.placeholder = ' Search good ascend score'
    self.label.visible = True
    self.label.text = 'Good Ascend Score details'
    self.data_grid_1.visible = True
    self.column_panel_1.visible = True
    self.data_grid_2.visible = False
    
    # Update the plot
    # self.aggregate_counts()
    # self.update_plot()

  def average_clik(self, **event_args):
    """This method is called when the button is clicked"""
    self.text_box_search.text = ""
    filtered_rows = self.get_filtered_rows("Average")
  
    # Fetch additional details from the loan details table
    result = []
    for row in filtered_rows:
      user_details = app_tables.fin_user_profile.get(customer_id=row['customer_id'])
      if user_details:
        combined_data = {
          'customer_id': row['customer_id'],
          'borrower_since': row['borrower_since'],
          'user_name': row['user_name'],
          'ascend_score': row['ascend_score'],
          'email_id': row['email_id'],
          'credit_limit': row['credit_limit'],
          'mobile': user_details['mobile'],

        }
        result.append(combined_data)
    self.all_items = result
    self.repeating_panel_1.items = result
    self.text_box_search.placeholder = 'Search average ascend score'
    self.label.visible = True
    self.label.text = 'Average Ascend Score details'
    self.data_grid_1.visible = True
    self.column_panel_1.visible = True
    self.data_grid_2.visible = False
      
    # Update the plot
    # self.aggregate_counts()
    # self.update_plot()

  def search_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    search_text = self.text_box_search.text.strip().lower()
    if search_text:
      # Filter items based on search text
      filtered_items = [
        item for item in self.all_items
        if (search_text in str(item['customer_id']).lower() or
            search_text in str(item['email_id']).lower() or
            search_text in item['user_name'].lower())
            # search_text in item['borrower_full_name'].lower()or
            # search_text in item['borrower_email'].lower())
      ]
      self.suggestions_panel.items = filtered_items
      self.data_grid_2.visible = True
      self.data_grid_1.visible = False
    else:
      self.suggestions_panel.items = []
      self.data_grid_2.visible = False
      self.data_grid_1.visible = True

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.reporting_and_analytical_modules')

  def bad_clidk(self, **event_args):
    """This method is called when the button is clicked"""
    self.text_box_search.text = ""
    filtered_rows = self.get_filtered_rows("Bad")
  
    # Fetch additional details from the loan details table
    result = []
    for row in filtered_rows:
      user_details = app_tables.fin_user_profile.get(customer_id=row['customer_id'])
      if user_details:
        combined_data = {
          'customer_id': row['customer_id'],
          'borrower_since': row['borrower_since'],
          'user_name': row['user_name'],
          'ascend_score': row['ascend_score'],
          'email_id': row['email_id'],
          'credit_limit': row['credit_limit'],
          'mobile': user_details['mobile'],

        }
        result.append(combined_data)
    self.all_items = result
    self.repeating_panel_1.items = result
    self.text_box_search.placeholder = 'Search bad ascend scores'
    self.label.visible = True
    self.label.text = 'Bad Ascend Score details'
    self.data_grid_1.visible = True
    self.column_panel_1.visible = True
    self.data_grid_2.visible = False
