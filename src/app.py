# look into dash
import dash
# import sys
# sys.path.append('src/utils/analysis')
# from testing import create_plots

app = dash.Dash(__name__)

# app.layout = create_plots()

# run the application
if __name__ == '__main__':
    app.run_server(debug=True)