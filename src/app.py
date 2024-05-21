### MAIN APPLICATION ENTRY POINT
### DONT START UNTIL WAY LATER
# look into dash
import dash
from src.utils.analysis.testing import create_plots

# Initialize the dashboard
app = dash.Dash(__name__)

# Create the plots
create_plots()

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)