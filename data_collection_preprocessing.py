import fastf1
import pandas as pd
from datetime import datetime, timedelta
import time
import streamlit as st

class get_data:
    def __init__(self, grand_prix, session, year):
        
        self.grand_prix = grand_prix
        self.session = session
        self.year = year

    def get_session_data(self, drivers):
        session = fastf1.get_session(self.year, self.grand_prix, self.session)
        session.load()
    
        results = session.results[['Position', 'BroadcastName', 'Q1', 'Q2', 'Q3', "Time"]]
        results = results.fillna("N/A")
        
        results["Q1"] = pd.to_timedelta(results["Q1"], errors='coerce')
        results["Q1"] = results["Q1"].dt.total_seconds()
        
        results["Q2"] = pd.to_timedelta(results["Q2"], errors='coerce')
        results["Q2"] = results["Q2"].dt.total_seconds()
        
        results["Q3"] = pd.to_timedelta(results["Q3"], errors='coerce')
        results["Q3"] = results["Q3"].dt.total_seconds()
        
        if len(drivers) == 1:
            
            driver = session.laps.pick_driver(drivers[0])
            
            return driver, results
        elif len(drivers) == 2:
            
            driver = session.laps.pick_driver(drivers[0])
            driver_2 = session.laps.pick_driver(drivers[1])
            
            return driver, driver_2, results
        
        elif len(drivers) == 3:
            
            driver = session.laps.pick_driver(drivers[0])
            driver_2 = session.laps.pick_driver(drivers[1])
            driver_3 = session.laps.pick_driver(drivers[2])
            
            return driver, driver_2, driver_3, results
          

    def get_telemetry(self, lap_number, data, fastest):
        if fastest:
            lap = data.pick_fastest()
        else:
            lap = data.loc[data['LapNumber'] == lap_number]
        telemetry = lap.get_car_data()
        telemetry = telemetry.add_distance()
        
        return telemetry
    
    
    def data_preprocessing(self, data):
        
        data.fillna(method='ffill', inplace=True) # use last avaliable laptime
        data['LapTime'] = data['LapTime'].dt.total_seconds()
        return data
    
    
    def save_data(self, data, filename):
        data.to_csv(filename, index=True)
        print(f"Data saved to {filename}")


def get_drivers(year, gp, session_type):
    st.session_state.loading=True
    
    session = fastf1.get_session(year, gp, session_type)
    session.load()
    laps = session.laps['LapNumber'].max()
    drivers = sorted(session.laps['Driver'].unique().tolist())  
    
    st.session_state.loading=False
    
    return laps, drivers
    
    
def get_valid_events(year):
    st.session_state.loading=True
    
    year = int(year)
    schedule = fastf1.get_event_schedule(year)
    
    schedule = schedule['EventName'].tolist()
        
    st.session_state.loading=False
    
    return schedule



def preprocess_3_drivers_laps(data):
    
    data = data[['LapNumber', 'LapTime_x', 'LapTime_y', 'LapTime']]
    data = data.rename(columns={'LapTime_x':"First Driver",
                                'LapTime_y':"Second Driver",
                                'LapTime' : "Third Driver"})
    
    return data
def preprocess_drivers_laps(data):
    data = data[['LapNumber', 'LapTime_x', 'LapTime_y']]
    data = data.rename(columns={'LapTime_x':"First Driver",
                                'LapTime_y':"Second Driver" })
    return data

def preprocess_driver_lap(data):
    data.to_csv("test.csv")
    data['LapTime'] = data['LapTime'].dt.total_seconds()
    data = data[["LapNumber", "LapTime"]]
    return data
