
from ._anvil_designer import my_returnsTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go
from anvil.tables import app_tables
import anvil.tables.query as q
from .. import main_form_module as main_form_module


class my_returns(my_returnsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user_id = main_form_module.userId

        # Check if user_id is correctly set
        print(f"User ID: {self.user_id}")

    def create_bar_chart(self):
        # Fetch investment data for the specific user
        investments = app_tables.fin_loan_details.search(loan_updated_status=q.like('closed%'), lender_customer_id=self.user_id)
        
        # Debugging: Print fetched investments
        print(f"Fetched investments for user {self.user_id}: {list(investments)}")
        
        # Initialize lists to store data for the bar chart
        products = []
        total_investments = []
        total_returns = []
        tenures = []
        percentages = []
        
        for index, investment in enumerate(investments):
            product = f"{investment['product_name']} ({index + 1})"
            products.append(product)
            total_investments.append(investment['loan_amount'] if investment['loan_amount'] is not None else 0)
            total_returns.append(investment['lender_returns'] if investment['lender_returns'] is not None else 0)
            tenures.append(investment['tenure'])
            
            # Calculate percentages only if both values are not None
            if investment['lender_returns'] is not None and investment['loan_amount'] is not None:
                percentages.append((investment['lender_returns'] / investment['loan_amount']) * 100)
            else:
                percentages.append(0)

        # Create bar chart traces
        investment_trace = go.Bar(x=products, y=total_investments, name='Investment', marker_color='blue')
        returns_trace = go.Bar(x=products, y=total_returns, name='Returns', marker_color='green')

        # Create annotations for tenure and percentage returns with bold text
        annotations = []
        for i, product in enumerate(products):
            max_value = max(total_investments[i], total_returns[i])
            annotation_text = f"Tenure: {tenures[i]} months"
            annotations.append(dict(
                x=product,
                y=max_value + (max(total_investments + total_returns) * 0.02),  # Position above the highest bar
                text=annotation_text,
                showarrow=False,
                font=dict(color='black', size=8, weight='bold')  # Set the color of the text to dark black and bold
            ))
            # Position the percentage above the returns bar
            annotations.append(dict(
                x=product,
                y=total_returns[i] + (max(total_investments + total_returns) * 0.01),  # Position above the returns bar
                text=f"{percentages[i]:.2f}%",
                showarrow=False,
                font=dict(color='black', size=8, weight='bold'),  # Set the color of the text to dark black and bold
                xanchor="left"
            ))

        # Create a layout with annotations
        layout = go.Layout(
            title=dict(text='Investment and Returns by Product', font=dict(size=16, weight='bold')),
            xaxis=dict(title='Product Details', tickfont=dict(size=10, weight='bold')),
            yaxis=dict(title='Amount (0.1M=100000)'),
            barmode='group',  # Use group mode to display bars side by side
            annotations=annotations
        )

        # Create a figure
        fig = go.Figure(data=[investment_trace, returns_trace], layout=layout)

        # Debugging: Print the figure to ensure it's created
        print(f"Created figure: {fig}")

        # Set the plot in the Plot component
        self.plot_1.data = fig['data']
        self.plot_1.layout = fig['layout']

        # Debugging: Check if the plot is assigned correctly
        print(f"Assigned figure to plot_1: {self.plot_1.data}")
    
    def create_user_bar_chart(self):
      # Fetch investment data
      investments = app_tables.fin_lender.search()
      
      # Debugging: Print fetched investments
      print(f"Fetched investments: {list(investments)}")
      
      # Initialize a dictionary to store total return_on_investment for each customer_id
      customer_returns = {}
      
      for investment in investments:
          customer_id = investment['customer_id']
          if customer_id not in customer_returns:
              customer_returns[customer_id] = 0
          # Add only if return_on_investment is not None
          if investment['return_on_investment'] is not None:
              customer_returns[customer_id] += investment['return_on_investment']
      
      # Convert the dictionary to a list of tuples and sort by return_on_investment in descending order
      sorted_returns = sorted(customer_returns.items(), key=lambda x: x[1], reverse=True)
      
      # Prepare data for the bar chart
      categories = [item[0] for item in sorted_returns]  # customer_ids
      values = [item[1] for item in sorted_returns]  # return_on_investments
      
      # Create bar chart trace
      trace = go.Bar(x=categories, y=values, marker_color='green')
      
      # Create a layout
      layout = go.Layout(
          title=dict(text='Return on Investment by Customer', font=dict(size=16, weight='bold')),
          xaxis=dict(title='Customer ID', tickfont=dict(size=10, weight='bold')),
          yaxis=dict(title='Return on Investment'),
          barmode='group'
      )
      
      # Create a figure
      fig = go.Figure(data=[trace], layout=layout)
      
      # Debugging: Print the figure to ensure it's created
      print(f"Created figure: {fig}")
      
      # Set the plot in the Plot component
      self.plot_2.figure = fig
      
      # Debugging: Check if the plot is assigned correctly
      print(f"Assigned figure to plot_3: {self.plot_2.figure}")

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('lendor.dashboard')
      
    def button_2_click(self, **event_args):
        self.plot_2.visible = True
        self.plot_1.visible = False
        self.create_user_bar_chart()
      
    def button_3_click(self, **event_args):
        self.plot_1.visible = True
        self.plot_2.visible = False
        self.create_bar_chart()






# from ._anvil_designer import my_returnsTemplate
# from anvil import *
# import plotly.graph_objects as go
# from anvil.tables import app_tables
# import anvil.tables.query as q
# from .. import main_form_module as main_form_module


# class my_returns(my_returnsTemplate):
#     def __init__(self, **properties):
#         # Set Form properties and Data Bindings.
#         self.init_components(**properties)
#         self.user_id = main_form_module.userId

#         # Check if user_id is correctly set
#         print(f"User ID: {self.user_id}")

#     def create_bar_chart(self):
#         # Fetch investment data for the specific user
#         investments = app_tables.fin_loan_details.search(loan_updated_status=q.like('close%'), lender_customer_id=self.user_id)
        
#         # Debugging: Print fetched investments
#         print(f"Fetched investments for user {self.user_id}: {list(investments)}")
        
#         # Initialize lists to store data for the bar chart
#         products = []
#         total_investments = []
#         total_returns = []
#         tenures = []
#         percentages = []
        
#         for index, investment in enumerate(investments):
#             product = f"{investment['product_name']} ({index + 1})"
#             products.append(product)
#             total_investments.append(investment['loan_amount'])
#             total_returns.append(investment['lender_returns'])
#             tenures.append(investment['tenure'])
#             percentages.append((investment['lender_returns'] / investment['loan_amount']) * 100)

#         # Create bar chart traces
#         investment_trace = go.Bar(x=products, y=total_investments, name='Investment', marker_color='blue')
#         returns_trace = go.Bar(x=products, y=total_returns, name='Returns', marker_color='green')

#         # Create annotations for tenure and percentage returns with bold text
#         annotations = []
#         for i, product in enumerate(products):
#             max_value = max(total_investments[i], total_returns[i])
#             annotation_text = f"Tenure: {tenures[i]} months"
#             annotations.append(dict(
#                 x=product,
#                 y=max_value + (max(total_investments + total_returns) * 0.05),  # Position above the highest bar
#                 text=annotation_text,
#                 showarrow=False,
#                 font=dict(color='black', size=8, weight='bold')  # Set the color of the text to dark black and bold
#             ))
#             # Position the percentage above the returns bar
#             annotations.append(dict(
#                 x=product,
#                 y=total_returns[i] + (max(total_investments + total_returns) * 0.05),  # Position above the returns bar
#                 text=f"{percentages[i]:.2f}%",
#                 showarrow=False,
#                 font=dict(color='black', size=8, weight='bold')  # Set the color of the text to dark black and bold
#             ))

#         # Create a layout with annotations
#         layout = go.Layout(
#             title=dict(text='Investment and Returns by Product', font=dict(size=16, weight='bold')),
#             xaxis=dict(title='Product Details', tickfont=dict(size=10, weight='bold')),
#             yaxis=dict(title='Amount (0.1M=100000)'),
#             barmode='group',  # Use group mode to display bars side by side
#             annotations=annotations
#         )

#         # Create a figure
#         fig = go.Figure(data=[investment_trace, returns_trace], layout=layout)

#         # Debugging: Print the figure to ensure it's created
#         print(f"Created figure: {fig}")

#         # Set the plot in the Plot component
#         self.plot_1.data = fig['data']
#         self.plot_1.layout = fig['layout']

#         # Debugging: Check if the plot is assigned correctly
#         print(f"Assigned figure to plot_1: {self.plot_1.data}")

#     def create_user_bar_chart(self):
#         # Fetch investment data for the specific user
#         investments = app_tables.fin_lender.search(customer_id=self.user_id)
        
#         # Debugging: Print fetched investments
#         print(f"Fetched investments for user {self.user_id}: {list(investments)}")
        
#         # Initialize variables to store total investments and returns
#         total_investment = 0
#         total_returns = 0
        
#         for investment in investments:
#             total_investment += investment['investment']
#             total_returns += investment['return_on_investment']
  
#         # Calculate the percentage return
#         percentage_return = (total_returns / total_investment) * 100 if total_investment != 0 else 0

#         # Debugging: Print aggregated values
#         print(f"Total Investment: {total_investment}, Total Returns: {total_returns}, Percentage Return: {percentage_return:.2f}%")
  
#         # Prepare data for bar chart
#         categories = ['Investment', 'Returns']
#         values = [total_investment, total_returns]
  
#         # Create bar chart trace
#         trace = go.Bar(x=categories, y=values, marker_color=['blue', 'green'])
  
#         # Create annotations
#         annotations = []
#         annotations.append(dict(
#             x='Returns',
#             y=total_returns + (max(values) * 0.05),  # Position above the returns bar
#             text=f"{percentage_return:.2f}%",
#             showarrow=False,
#             font=dict(color='black', size=8, weight='bold')  # Set the color of the text to dark black and bold
#         ))
  
#         # Create a layout with annotations
#         layout = go.Layout(
#             title=dict(text='Investment and Returns for User', font=dict(size=16, weight='bold')),
#             xaxis=dict(title='Category', tickfont=dict(size=10, weight='bold')),
#             yaxis=dict(title='Amount (0.1M=100000)'),
#             barmode='group',  # Use group mode to display bars side by side
#             annotations=annotations
#         )
  
#         # Create a figure
#         fig = go.Figure(data=[trace], layout=layout)
  
#         # Debugging: Print the figure to ensure it's created
#         print(f"Created figure: {fig}")
  
#         # Set the plot in the Plot component
#         self.plot_2.data = fig['data']
#         self.plot_2.layout = fig['layout']
  
#         # Debugging: Check if the plot is assigned correctly
#         print(f"Assigned figure to plot_2: {self.plot_2.data}")

#     def button_1_click(self, **event_args):
#         """This method is called when the button is clicked"""
#         open_form('lendor.dashboard')
      
#     def button_2_click(self, **event_args):
#         self.plot_2.visible = True
#         self.plot_1.visible = False
#         self.create_user_bar_chart()
      
#     def button_3_click(self, **event_args):
#         self.plot_1.visible = True
#         self.plot_2.visible = False
#         self.create_bar_chart()
