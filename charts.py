import streamlit as st


PRIMARY_COLOR = "#a63737"
# Charts
def throttle_chart_2(telemetry_concat):
    
    throttle_telemetry = telemetry_concat[["Distance", "Driver 1 Throttle", "Driver 2 Throttle"]]
    throttle_telemetry["Distance"] = throttle_telemetry["Distance"].squeeze()
    throttle_telemetry.set_index("Distance", inplace=True)
        
    st.line_chart(data=throttle_telemetry)

    speed_telemetry = telemetry_concat[["Distance", "Driver 1 Speed", "Driver 2 Speed"]]
    speed_telemetry["Distance"] = speed_telemetry["Distance"].squeeze()
    speed_telemetry.set_index("Distance", inplace=True)
    
    st.line_chart(data=speed_telemetry)
    
def throttle_chart_3(telemetry_concat):
    
    throttle_telemetry = telemetry_concat[["Distance", "Driver 1 Throttle", "Driver 2 Throttle", "Driver 3 Throttle"]]
    throttle_telemetry["Distance"] = throttle_telemetry["Distance"].squeeze()
    throttle_telemetry.set_index("Distance", inplace=True)
        
    st.line_chart(data=throttle_telemetry)
    
    speed_telemetry = telemetry_concat[["Distance", "Driver 1 Speed", "Driver 2 Speed", "Driver 3 Speed"]]
    speed_telemetry["Distance"] = speed_telemetry["Distance"].squeeze()
    speed_telemetry.set_index("Distance", inplace=True)
    
    st.line_chart(data=speed_telemetry)

def create_speed_chart(telemetry):
    st.subheader("Speed")
    st.line_chart(
        data=telemetry,
        x="Distance",
        y="Speed",
        width=1500,
        height=600,
        color=PRIMARY_COLOR
    )

def create_lap_time_chart(data):
    st.line_chart(
        data=data, 
        x='LapNumber', 
        y='LapTime',
        x_label='Lap Number',
        y_label='Lap Time',
        width=2000,
        height=600,
        color=PRIMARY_COLOR
    )