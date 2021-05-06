import pandas as pd                               # to organize data in Dataframes
import numpy as np                                # to store data in arrays
import datetime                                   # to work with time series
import plotly.graph_objects as go                 # to generate interactive plots
from plotly.subplots import make_subplots         # to make interactive subplots
import plotly.offline                             # to display the interactive plot
from sklearn.linear_model import LinearRegression # to predict linear forecasts


## Prepare the dataframe for analysis

def clean_df(df_owid_orig):
    
    # Work with a copy, not the original dataset
    df_owid = df_owid_orig.copy()
    
    # Store the location and date as indices for the dataframe
    df_owid.sort_values(by=['location', 'date'])
    df_owid.loc[:, 'datetime'] = pd.to_datetime(df_owid.loc[:, 'date'])
    df_owid = df_owid.set_index(['location', 'datetime'], drop=False)
    df_owid.rename_axis(['location_index', 'datetime_index'], axis='index', inplace=True)
    
    # Count the number of days since beginning of recording - helps with regression model
    df_owid['days_since'] = (df_owid['datetime'] - df_owid['datetime'].iloc[0]).dt.days
    
    # Using forward fill method to fill missing values (fill missing values with previous available day's value)
    # Lets us avoid errors with the linear regression and is acceptable for small stretches of missing data
    df_owid.fillna(method='ffill', inplace=True)
    
    # Examine these columns in the forecast
    ListofCols = ['share_doses_used', 'people_vaccinated_per_hundred']
    
    return df_owid, ListofCols
    

## Get user input of US states to examine
    
def getStateInput(df_owid):
    
    ListofStates = []
    state_input = ''
    AllStates_lower = [ df_owid.index.levels[0][state_idx].lower() for state_idx, state in enumerate(df_owid.index.levels[0]) ]
    
    while state_input != 'done':
        if len(ListofStates) < 1:
            state_input = input('\nPlease enter a state: ')
        else:
            state_input = input('Please enter another state or "done": ')
        if state_input.lower() in AllStates_lower:
            state = df_owid.index.levels[0][AllStates_lower.index(state_input.lower())]
            ListofStates.append(state)
        elif state_input == 'done':
            if len(ListofStates) < 1:
                print('You have not selected a state yet.')
            else:
                print('\nDone. List of States:', ', '.join(ListofStates))
                break
        else:
            print('"{}" is not a valid state. Please enter a valid state.'.format(state_input))
            
    return ListofStates
    

## Plot actual data only

# def plotStateActual(df_owid, ListofStates, ListofCols):
    
#     ## For trial, test with these lists:
#     # ListofStates = ['Alabama', 'Texas', 'New York State']
#     # ListofCols = ['share_doses_used', 'people_vaccinated_per_hundred']
    
#     print('\nGenerating plot of \ndata: {} \nfor \nstates: {}'.format(
#         '"'+'" and "'.join(ListofCols)+'"', ', '.join(ListofStates)))
    
#     fig = []
    
#     fig = make_subplots(rows=len(ListofCols)+1,
#                         cols=1,
#                         shared_xaxes=True,
#                         subplot_titles=['Efficiency of Vaccine Administration',
#                                        'Path to Herd Immunity (Goal: 70-90%)'])
    
#     for col_idx, col in enumerate(ListofCols):
        
#         col_pred = ListofCols_pred[col_idx]
        
#         for state in ListofStates:
#             data = go.Scatter(x=df_owid.loc[state]['datetime'], y=df_owid.loc[state][col], name=state+' '+col)
#             fig.add_trace(data, row=col_idx+1, col=1)
            
#     fig.update_layout(hovermode='x')
#     fig.update_layout(
#         # autosize=True,
#         # width=1000,
#         height=3000,
#         margin=dict(
#         #     l=50,
#         #     r=50,
#             b=5,
#             t=5,
#             pad=100
#         ))
#     # fig.update_xaxes(title_text="Date", row=1, col=1)
#     # fig.update_xaxes(title_text="Date", row=2, col=1)
#     fig.update_yaxes(title_text="(Doses used)/(doses shipped)", row=1, col=1)
#     fig.update_yaxes(title_text="% of state population\nvaccinated at least once", row=2, col=1)
#     # fig.show()
    
#     fig_actual = fig
    
#     plotly.offline.plot(fig_actual)
    
#     return fig_actual

## Plot actual state data, with option to also plot stat projected values

def plotStates(df_owid, ListofStates, ListofCols, **kwargs):
    
    ## For trial, test with these lists:
    # ListofStates = ['Alabama', 'Texas', 'New York State']
    # ListofCols = ['share_doses_used', 'people_vaccinated_per_hundred']
    
    print('\nGenerating plot of \ndata: {} \nfor \nstates: {}'.format(
        '"'+'" and "'.join(ListofCols)+'"', ', '.join(ListofStates)))
    
    fig = []
    
    fig = make_subplots(rows=len(ListofCols)+1,
                        cols=1,
                        shared_xaxes=True,
                        subplot_titles=['Efficiency of Vaccine Administration',
                                       'Path to Herd Immunity (Goal: 70-90%)'])
    
    ListofCols_pred = [ 'PREDICTED'+' '+col for col in ListofCols ]
    
    for col_idx, col in enumerate(ListofCols):
        
        col_pred = ListofCols_pred[col_idx]
        
        for state in ListofStates:
            data = go.Scatter(x=df_owid.loc[state]['datetime'], y=df_owid.loc[state][col], name=state+' '+col)
            fig.add_trace(data, row=col_idx+1, col=1)
            
            if 'Y_pred' in kwargs:
                Y_pred = kwargs['Y_pred']
                data_pred = go.Scatter(x=Y_pred.loc[state].index, y=Y_pred.loc[state][col_pred], name=state+' '+col_pred)
                fig.add_trace(data_pred, row=col_idx+1, col=1)
            
    fig.update_layout(hovermode='x')
    fig.update_layout(
        # autosize=True,
        # width=1000,
        height=3000,
        margin=dict(
        #     l=50,
        #     r=50,
            b=5,
            t=5,
            pad=100
        ))
    # fig.update_xaxes(title_text="Date", row=1, col=1)
    # fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="(Doses used)/(doses shipped)", row=1, col=1)
    fig.update_yaxes(title_text="% of state population\nvaccinated at least once", row=2, col=1)
    # fig.show()
    
    plotly.offline.plot(fig)
    
    return fig
    

## Select Dates for Forecast - End date for training and end date for forecast

def getForecastDates():
    
    ## Select End Date for Forecast Training
    
    # Limit the dates that the user can input
    train_date_earliest = datetime.datetime.strptime('2021-01-12', '%Y-%m-%d')
    train_date_latest = datetime.datetime.today() - datetime.timedelta(5)
    
    earliest_str = datetime.datetime.strftime(train_date_earliest, '%B %d, %Y')
    latest_str = datetime.datetime.strftime(train_date_latest, '%B %d, %Y')
    
    train_date_range = pd.date_range(train_date_earliest, train_date_latest)
    
    # Take user input for training end date
    print('\n\nSelect an end date to train the model.')
    print('e.g. "Based on trends up to date March 15, 2021, we can forecast the following trajectory."')
    
    train_date_end = ''
    train_date_end_input = ''
    while train_date_end not in train_date_range:
        try:
            train_date_end_input = input(('Please provide a date from {} to {} in the format "Month Day, Year": ').format(earliest_str, latest_str))
            train_date_end = datetime.datetime.strptime(train_date_end_input, '%B %d, %Y')
        except ValueError:
            print(train_date_end_input, 'is not in a valid format\nPlease provide a valid date in the format "Month Day, Year".')
        else:
            print('Done. Using', train_date_end_input, 'as end date for forecast training.')
            break
    
    
    ## Select Optional Start Date for Forecast Training
    
    print('\n\nWould you like to select a start date for the training?')
    print('e.g. "We only want to base our prediction on trends from "March 1, 2021" to March 15, 2021."')
    print('If yes, then select a date. If no, then type "no", which will examine all data before the end date.')
    
    too_late = []
    train_date_start = ''
    train_date_start_input = ''
    
    # Take user input for optional forecasting start date
    while train_date_start_input != 'no':
        try:
            train_date_start_input = input(('Please provide a date from {} to {} in the format "Month Day, Year": ').format(earliest_str, train_date_end_input))
            train_date_start = datetime.datetime.strptime(train_date_start_input, '%B %d, %Y')
            while train_date_start >= train_date_end:
                too_late = 1
                print('\nError: Date is too late. Please choose a date before the train end date of {}.'.format(train_date_end_input))
                train_date_end = datetime.datetime.strptime('', '%B %d, %Y')
        except ValueError:
            if train_date_start_input == 'no':
                train_date_start = train_date_earliest
                print('Selected "no". Using {} as start date for training.'.format(earliest_str))
                break
            else:
                try:
                    int(too_late)
                    too_late = []
                    continue
                except ValueError:
                    print(train_date_start_input, 'is not in a valid format. Please provide a valid date in the format "Month Day, Year".')
        else:
            print('Done. Using', train_date_start_input, 'as start date for forecast training.')
            break
    
    
    ## Select Furthest Future Date to Forecast
    
    forecast_date_end = ''
    forecast_date_end_input = ''
    
    print('\nSelect an end date for forecast.')
    print('e.g. "We will predict the trends up to June 4, 2021.')
    
    too_early = []
    while True:
        try:
            forecast_date_end_input = input('Please enter a date to end the forecast ("Month Day, Year"): ')
            forecast_date_end = datetime.datetime.strptime(forecast_date_end_input, '%B %d, %Y')
            while forecast_date_end <= train_date_end:
                too_early = 1
                print('Please choose a date after the train end date of {}.'.format(train_date_end_input))
                forecast_date_end = datetime.datetime.strptime('', '%B %d, %Y')
                break
        except ValueError: 
            try:
                int(too_early)
                too_early = []
                continue
            except ValueError:
                print(forecast_date_end_input, 'is not a valid date.')
                print('Please choose a valid date in the format "Month Day, Year".')
        else:
            print('Done. Selected', forecast_date_end_input,'as end date for forecast.')
            break

    return train_date_start, train_date_end, forecast_date_end


## Perform linear regression on training data

def getLinreg(X_trn, y_trn):
    mdl = LinearRegression()
    mdl.fit(X_trn, y_trn)
    
    return mdl

    
## Forecast the selected columns' data using the train date limit and forecast span

def forecaster(df_owid, train_date_start, train_date_end, forecast_date_end, ListofStates, ListofCols):
    
    forecast_dates = pd.date_range(train_date_end, forecast_date_end)
    days_ahead = len(forecast_dates)
    ListofCols_pred = [ 'PREDICTED'+' '+col for col in ListofCols ]
    
    Y_pred_state = []
    for state in ListofStates:
        indices = [[ state for day in range(days_ahead) ], forecast_dates]
        Y_pred_state.append( pd.DataFrame(columns=ListofCols, index=indices) )
    Y_pred = pd.concat(Y_pred_state)
    
    y_pred_list = []
    y_p_state_list = []
    
    for state in ListofStates:
        
        TrainData = df_owid.loc[state][train_date_start:train_date_end]
        X_train = TrainData['days_since']
        Y_train = TrainData[ListofCols]
        
        for idx, col in enumerate(Y_train.columns):
            slope = getLinreg(np.array(X_train).reshape(-1, 1), Y_train[col]).coef_[0]
            train_end_point = (Y_train.index[-1], Y_train[col][-1])
            y_linreg = [ train_end_point[1] + slope*day for day in range(days_ahead) ]
            y_forecast = pd.DataFrame(data=y_linreg, columns=[col], index=forecast_dates)
            y_pred_list.append(y_forecast)
        y_p_state_list.append(y_pred_list[-1].join(y_pred_list[-2]))
    
    Y_pred = pd.concat(y_p_state_list, keys=ListofStates)
    for col_idx, col in enumerate(ListofCols):
        Y_pred.rename(columns={col: ListofCols_pred[col_idx]}, inplace=True)

    return Y_pred, ListofCols_pred


# Plot the data for each state, comparing actual and forecasted values
# This uses the plotly package for interactive graphs 

# def plotStatePred(df_owid, ListofStates, ListofCols, Y_pred, ListofCols_pred):
    
#     ## For trial, test with these lists:
#     # ListofStates = ['Alabama', 'Texas', 'New York State']
#     # ListofCols = ['share_doses_used', 'people_vaccinated_per_hundred']
    
#     print('\nGenerating plot of \ndata: {} \nfor \nstates: {}'.format(
#         '"'+'" and "'.join(ListofCols)+'"', ', '.join(ListofStates)))
    
#     fig = []
    
#     fig = make_subplots(rows=len(ListofCols)+1,
#                         cols=1,
#                         shared_xaxes=True,
#                         subplot_titles=['Efficiency of Vaccine Administration',
#                                        'Path to Herd Immunity (Goal: 70-90%)'])
    
#     for col_idx, col in enumerate(ListofCols):
        
#         col_pred = ListofCols_pred[col_idx]
        
#         for state in ListofStates:
#             data = go.Scatter(x=df_owid.loc[state]['datetime'], y=df_owid.loc[state][col], name=state+' '+col)
#             fig.add_trace(data, row=col_idx+1, col=1)
            
#             data_pred = go.Scatter(x=Y_pred.loc[state].index, y=Y_pred.loc[state][col_pred], name=state+' '+col_pred)
#             fig.add_trace(data_pred, row=col_idx+1, col=1)
            
#     fig.update_layout(hovermode='x')
#     fig.update_layout(
#         # autosize=True,
#         # width=1000,
#         height=3000,
#         margin=dict(
#         #     l=50,
#         #     r=50,
#             b=5,
#             t=5,
#             pad=100
#         ))
#     # fig.update_xaxes(title_text="Date", row=1, col=1)
#     # fig.update_xaxes(title_text="Date", row=2, col=1)
#     fig.update_yaxes(title_text="(Doses used)/(doses shipped)", row=1, col=1)
#     fig.update_yaxes(title_text="% of state population\nvaccinated at least once", row=2, col=1)
#     # fig.show()
    
#     fig_pred = fig
    
#     plotly.offline.plot(fig_pred)
    
#     return fig_pred
    
if __name__ == '__main__':
    df_owid_orig = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/us_state_vaccinations.csv')
    df_owid, ListofCols = clean_df(df_owid_orig)
    ListofStates = getStateInput(df_owid)
    fig_actual = plotStates(df_owid, ListofStates, ListofCols)
 
    train_date_start, train_date_end, forecast_date_end = getForecastDates()
    ListofCols = ['share_doses_used', 'people_vaccinated_per_hundred']
    Y_pred, ListofCols_pred = forecaster(df_owid, train_date_start, train_date_end, forecast_date_end, ListofStates, ListofCols)
    
    kwargs = {'Y_pred': Y_pred}
    fig_pred = plotStates(df_owid, ListofStates, ListofCols, **kwargs)
    
