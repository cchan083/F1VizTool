import streamlit as st
from data_collection_preprocessing import get_drivers, get_valid_events, get_data, preprocess_drivers_laps, preprocess_3_drivers_laps, preprocess_driver_lap
from animation import load_lottiefile
from streamlit_lottie import st_lottie
import pandas as pd
from charts import throttle_chart_2, throttle_chart_3



if "loading" not in st.session_state:
    st.session_state.loading = False

# Constants
LOADING_ANIMATION = "loading.json"
YEAR_RANGE = range(2018, 2026)
SESSION_OPTIONS = ['R', 'Q', 'FP1', 'FP2', 'FP3']
COMPARISON_TYPES = ['1 Driver', '2 Drivers', '3 Drivers']
PRIMARY_COLOR = "#a63737"


def layout():
    st.title('F1 Visualisation Tool - Hybrid Era')
    st.caption('Note - Visualisations can take a while to load due to data collection and processing')
    st.sidebar.title("Options for visualisations")

def loading_animation():
    lottie_coding = load_lottiefile(LOADING_ANIMATION)
    loading_placeholder = st.sidebar.empty()
    with loading_placeholder.container():
        st_lottie(lottie_coding, height=200)
    return loading_placeholder


def user_input():
    year = st.sidebar.selectbox("Select Year", options=YEAR_RANGE)
    valid_events = get_valid_events(year)
    
    grand_prix = st.sidebar.selectbox("Select Grand Prix", options=valid_events)
    session_type = st.sidebar.selectbox("Select Session", options=SESSION_OPTIONS)
    
    
    try:
        laps, drivers_unique = get_drivers(year, grand_prix, session_type)
        comparisons = st.sidebar.selectbox("Types of Comparisons", options=COMPARISON_TYPES)
        driver = st.sidebar.selectbox("Select Driver", options=drivers_unique)
    except Exception as e:
        st.write("Invalid Inputs - Check that Grand Prix has finished and that the driver has driven it")
    
    
    
    second_driver, third_driver = None, None
    if comparisons == "2 Drivers":
        second_driver = st.sidebar.selectbox("Select Second Driver", options=drivers_unique)
    elif comparisons == "3 Drivers":
        second_driver = st.sidebar.selectbox("Select Second Driver", options=drivers_unique)
        third_driver = st.sidebar.selectbox("Select Third Driver", options=drivers_unique)
    
    lap_number = st.sidebar.slider(
        "Lap Number",
        min_value=1,
        max_value=int(laps),  
        value=5  
    )
    fastest_lap = st.sidebar.checkbox("Fastest Lap")
    
    return {
        'year': year,
        'grand_prix': grand_prix,
        'session_type': session_type,
        'driver': driver,
        'comparisons': comparisons,
        'second_driver': second_driver,
        'third_driver': third_driver,
        'lap_number': lap_number,
        'fastest_lap': fastest_lap
    }


def configure_tab_styles():
    st.markdown(f"""
    <style>
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: #white;
            padding: 10px 15px;
            border-radius: 5px 5px 0px 0px;
            color: white;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {PRIMARY_COLOR};
            color: white;
        }}
    </style>
    """, unsafe_allow_html=True)



def main():
    layout()
    loading_placeholder = loading_animation()
    configure_tab_styles()

    inputs = user_input()
    

    telemetry_tab, lap_time_tab, results_tab= st.tabs([
        "📊 Telemetry", 
        "🏎️ Lap Time Comparison", 
        "Session Results", 
        
    ])
    

    session = get_data(
        year=inputs['year'],
        grand_prix=inputs['grand_prix'],
        session=inputs['session_type']
    )
    
    
    all_drivers = [inputs['driver'], inputs['second_driver'], inputs['third_driver']]
    all_drivers = [x for x in all_drivers if x not in [None, '', [], {}, ()]]
    
    preprocessed_data = None
    telemetry_concat = None
    
    if len(all_drivers) == 1:
        
        
        dataframe, results  = session.get_session_data(drivers=all_drivers)
        preprocessed_data = pd.DataFrame(dataframe)
        preprocessed_data = preprocess_driver_lap(preprocessed_data)
        
        telemetry_data = session.data_preprocessing(dataframe)
        telemetry_data = session.get_telemetry(lap_number=inputs['lap_number'],
                                               data=telemetry_data,
                                               fastest=inputs['fastest_lap'])
        
        telemetry_concat = telemetry_data
        
    elif len(all_drivers) == 2:
        
        dataframe, dataframe_2, results = session.get_session_data(drivers=all_drivers)

        telemetry_data = session.data_preprocessing(dataframe)
        telemetry_data = pd.DataFrame(session.get_telemetry(lap_number=inputs['lap_number'],
                                               data=telemetry_data,
                                               fastest=inputs['fastest_lap']))  
        telemetry_data_2 = session.data_preprocessing(dataframe_2)
        telemetry_data_2 = pd.DataFrame(session.get_telemetry(lap_number=inputs['lap_number'],
                                               data=telemetry_data_2,
                                               fastest=inputs['fastest_lap']))
        telemetry_data_2 = telemetry_data_2.rename(columns={"Throttle":"Driver 2 Throttle", "Speed":"Driver 2 Speed", "Distance":"Driver 2 Distance"})
        telemetry_data = telemetry_data.rename(columns={"Throttle":"Driver 1 Throttle", "Speed":"Driver 1 Speed"})
        telemetry_concat = pd.concat([telemetry_data, telemetry_data_2], axis=1)
        
        dataframe=pd.DataFrame(dataframe)
        dataframe_2=pd.DataFrame(dataframe_2)
        dataframe_laps = pd.merge(dataframe, dataframe_2, on='LapNumber')
        
        preprocessed_data = preprocess_drivers_laps(dataframe_laps)
        
        
    elif len(all_drivers) == 3:
        
        dataframe, dataframe_2, dataframe_3, results = session.get_session_data(drivers=all_drivers)

        telemetry_data = session.data_preprocessing(dataframe)
        telemetry_data = session.get_telemetry(lap_number=inputs['lap_number'],
                                               data=telemetry_data,
                                               fastest=inputs['fastest_lap'])  
        telemetry_data_2 = session.data_preprocessing(dataframe_2)
        telemetry_data_2 = session.get_telemetry(lap_number=inputs['lap_number'],
                                               data=telemetry_data_2,
                                               fastest=inputs['fastest_lap'])
        telemetry_data_3 = session.data_preprocessing(dataframe_3)
        telemetry_data_3 = session.get_telemetry(lap_number=inputs['lap_number'],
                                               data=telemetry_data_3,
                                               fastest=inputs['fastest_lap'])
          
        telemetry_data_3 = telemetry_data_3.rename(columns={"Throttle":"Driver 3 Throttle", "Speed":"Driver 3 Speed", "Distance":"Driver 3 Distance"})
        telemetry_data_2 = telemetry_data_2.rename(columns={"Throttle":"Driver 2 Throttle", "Speed":"Driver 2 Speed", "Distance":"Driver 2 Distance"})
        telemetry_data = telemetry_data.rename(columns={"Throttle":"Driver 1 Throttle", "Speed":"Driver 1 Speed"})
        
        telemetry_concat = pd.concat([telemetry_data, telemetry_data_2, telemetry_data_3], axis=1)
        
        
        dataframe=pd.DataFrame(dataframe)
        dataframe_2=pd.DataFrame(dataframe_2)
        dataframe_3=pd.DataFrame(dataframe_3)
        
        dataframe = pd.merge(dataframe, dataframe_2, on='LapNumber', suffixes=("_x", "_y"))
        dataframe_laps=pd.merge(dataframe, dataframe_3, on='LapNumber', suffixes=("_x", "_y", "_z"))

        preprocessed_data = preprocess_3_drivers_laps(dataframe_laps)
    

    
    
    with lap_time_tab:
        try:
            st.subheader("Lap Times Comparison")
            st.line_chart(preprocessed_data,
                        x="LapNumber")
        except Exception as e:
            st.write("Invalid Inputs - Check that Grand Prix has finished and that the driver has driven it")
            
        
        
    with telemetry_tab:
        try:
                
            st.subheader("Throttle Application")
            
            if len(all_drivers) == 1:
                st.line_chart(
            data=telemetry_concat,
            x="Distance",
            y="Throttle",
            x_label="Distance (m)",
            y_label="Throttle Application (%)",
            width=1500,
            height=400,
            color=PRIMARY_COLOR
            )
                st.subheader("Speed")
                st.line_chart(
                    data=telemetry_concat,
                    x="Distance",
                    y="Speed",
                    width=1500,
                    height=600,
                    color=PRIMARY_COLOR
                )
            
            elif len(all_drivers) == 2:
                throttle_chart_2(telemetry_concat=telemetry_concat)
            
            elif len(all_drivers) ==3:
                throttle_chart_3(telemetry_concat=telemetry_concat)
        except Exception as e:
            st.write("Invalid Inputs - Check that Grand Prix has finished and that the driver has driven it")
        
        
        
            
        
    with results_tab:
        try:
            st.dataframe(
                results,
                width=3000,
                use_container_width=True
            )
        except Exception as e:
            st.write("Invalid Inputs - Check that Grand Prix has finished and that the driver has driven it")
    
            
    
    
    loading_placeholder.empty()



if __name__ == "__main__":
    main()