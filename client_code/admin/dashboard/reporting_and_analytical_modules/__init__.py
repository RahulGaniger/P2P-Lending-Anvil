from ._anvil_designer import reporting_and_analytical_modulesTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class reporting_and_analytical_modules(reporting_and_analytical_modulesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def risk_poolh_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.reporting_and_analytical_modules.risk_pool')

  def port_polio_risk_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.reporting_and_analytical_modules.port_folio_risk')

  def kay_metrics_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.dashboard.reporting_and_analytical_modules.key_metrice')
