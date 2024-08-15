import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")


# CSS for styling the container and metrics
container_style = """
<style>
.custom-container {
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 20px;
    background-color: #f9f9f9;
    box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    text-align: center;
}
.metric-box {
    border-radius: 10px;
    padding: 20px;
    color: white;
    font-size: 1.2rem;
    font-weight: bold;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 340px;  /* Fixed width to ensure boxes are square */
    height: 150px; /* Fixed height to ensure boxes are square */
    text-align: center;
    margin: 30px 40px;     /* No margin between boxes */
}

.metric-box1 {
    border-radius: 10px;
    padding: 20px;
    color: white;
    font-size: 1.2rem;
    font-weight: bold;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 320px;  /* Fixed width to ensure boxes are square */
    height: 200px; /* Fixed height to ensure boxes are square */
    text-align: center;
    margin: 0;     /* No margin between boxes */
}

.metric-box .metric-heading {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    margin-bottom: 10px;
}
.metric-box .metric-heading i {
    margin-right: 8px; /* Space between icon and text */
    font-size: 1.2rem; /* Adjust icon size */
}
.metric-box .metric-value {
    font-size: 1.5rem;
    font-weight: bold;
}
.metric-box.total-employees {
    background-color: #4CAF50; /* Green */
}

.metric-box1.total-employees {
    background-color: #7c82d7; /* Green */
}

.metric-box.daily-attendance {
    background-color: #7c82d7; /* Green */
}
.metric-box.avg-daily-absenteeism {
    background-color: #FFC107; /* Amber */
}
.metric-box.absenteeism-rate {
    background-color: #F44336; /* Red */
}
.metric-container {
    display: flex;
    justify-content: center; /* Center boxes horizontally */
    gap: 10px; /* Small gap between boxes */
}
</style>
"""




def home_page():
    with st.sidebar:
        st.sidebar.header("Navigation")
        selected_option = option_menu(
            menu_title=None,  # required
            options=["Upload File", "View Dashboard","Employees"],  # required
            icons=["upload", "bar-chart","people"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="vertical"  # optional
        )
        
    if selected_option == "Upload File":
        upload_file_section()
    elif selected_option == "View Dashboard":
        dashboard_page()
    elif selected_option == "Employees":
        employees_page()
    
def upload_file_section():
    st.subheader("Upload Attendance File")
    uploaded_file = st.file_uploader("Choose an attendance file", type=['csv'])
    
    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        # Ensure the Date column is in datetime format
        df['Date/Time'] = pd.to_datetime(df['Date/Time'])
        df["Day"] = df['Date/Time'].dt.day
        df["Year"] = df["Date/Time"].dt.year
        df['Month'] = df['Date/Time'].dt.strftime('%B')
        df['Weekday'] = df['Date/Time'].dt.weekday 
        df['week'] = df['Date/Time'].apply(lambda x: x.isocalendar()[1])
        #df['Month Week Number'] = df.groupby('Month')['ISO Week Number'].transform(lambda x: x - x.min() + 1)
        st.subheader("Raw Data")
        st.write(df)
        
        # Save the dataframe in the session state for later use
        st.session_state['df'] = df
        st.success("File uploaded successfully. You can now view the dashboard.")
    else:
        st.warning("Please upload a CSV file to proceed.")
import plotly.graph_objs as go

def create_custom_gauge(absenteeism_rate):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=absenteeism_rate,
        #title={'text': "Absenteeism Rate", 'font': {'size': 24}},
        #delta={'reference': 50, 'increasing': {'color': "red"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 20], 'color': 'green'},
                {'range': [20, 40], 'color': 'yellow'},
                {'range': [40, 60], 'color': 'orange'},
                {'range': [60, 80], 'color': 'red'},
                {'range': [80, 100], 'color': 'darkred'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': absenteeism_rate}}))

    fig.update_layout(
        font={'color': "gray", 'family': "Arial"},
        margin=dict(l=40, r=60, t=40, b=50),
        height=300,
        title={
                        'text': f'Absenteeism Rate by Day',
                        'x': 0.5,  # Center alignment
                        'xanchor': 'center'
                                        }
        
    )

    return fig

def dashboard_page():
    st.markdown("<h1 style='text-align: center;'>EASTC EMPLOYEES ATTENDANCE SUMMARY</h1>", unsafe_allow_html=True)
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">', unsafe_allow_html=True)
    
    if 'df' in st.session_state:
        df = st.session_state['df']
        
        col1, col2,col3= st.columns(3)
        
        with col1:
            selected_year = st.selectbox("Select Year", df['Year'].unique())
        
        # Filter data based on the selected year first
        year_filtered_df = df[df['Year'] == selected_year]
        
        import calendar

        # Correctly map the month names or numbers
        if year_filtered_df['Month'].dtype == 'O':  # If 'Month' column is a string
            month_to_num = {month: index for index, month in enumerate(calendar.month_name) if month}
            year_filtered_df['Month_Number'] = year_filtered_df['Month'].map(month_to_num)
        else:  # If 'Month' column is numeric
            year_filtered_df['Month_Number'] = year_filtered_df['Month'].astype(int)

        year_filtered_df['Month_Name'] = year_filtered_df['Month_Number'].apply(lambda x: calendar.month_name[x])

        with col2:
            selected_month = st.selectbox("Select Month", year_filtered_df['Month_Name'].unique())
           # Filter data based on the selected month name and year
        filtered_df = year_filtered_df[year_filtered_df['Month_Name'] == selected_month]
            
        with col3:
             # Add a date picker for selecting a specific day
            selected_date = st.date_input("Select Date", value=pd.to_datetime(filtered_df['Date/Time'].min()).date(),
                                        min_value=pd.to_datetime(filtered_df['Date/Time'].min()).date(),
                                        max_value=pd.to_datetime(filtered_df['Date/Time'].max()).date())
            
            # Filter data based on the selected date
            date_filtered_df = filtered_df[filtered_df['Date/Time'].dt.date == pd.to_datetime(selected_date).date()]
    

     
        

        
        # Identify working days
        working_days = filtered_df['Day'].unique()
        
        daily_absent = []
        total_employees = filtered_df['No.'].nunique()
        
        for day in working_days:
            daily_check_ins = filtered_df[(filtered_df['Day'] == day) & (filtered_df['Status'] == 'C/In')]['No.'].nunique()
            daily_absent.append(total_employees - daily_check_ins)
        
        # Calculate average monthly absenteeism
        average_monthly_absent = sum(daily_absent) / len(working_days)
        
        # Calculate median daily absenteeism
        median_daily_absent = pd.Series(daily_absent).median()
        
        # Calculate absenteeism rate
        absenteeism_rate = sum(daily_absent) / (total_employees * len(working_days)) * 100
        total_check_ins_on_date = date_filtered_df[date_filtered_df['Status'] == 'C/In']['No.'].nunique()
        daily_absent_on_date = total_employees - total_check_ins_on_date
        daily_absenteeism_rate = (daily_absent_on_date / total_employees) * 100
    
        
        # Inject the CSS styles for the container
        st.markdown(container_style, unsafe_allow_html=True)
        
        # Display metrics in styled containers with icons
        st.markdown('<div class="custom-container">', unsafe_allow_html=True)
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'''
            <div class="metric-box total-employees">
                <div class="metric-heading"><i class="fas fa-users"></i>Total Employees </div>
                <div class="metric-value">{total_employees}</div>
            </div>''', unsafe_allow_html=True)
            
        with col2:
            check_ins_day =  date_filtered_df[ date_filtered_df['Status'] == 'C/In']
            st.markdown(f'''
            <div class="metric-box daily-attendance">
                <div class="metric-heading"><i class="fas fa-users"></i>Daily Attendance</div>
                <div class="metric-value">{check_ins_day['Status'].count()}</div>
            </div>''', unsafe_allow_html=True)
            
        with col3:
            st.markdown(f'''
            <div class="metric-box absenteeism-rate">
                <div class="metric-heading"><i class="fas fa-chart-line"></i>Absenteeism Rate by Month</div>
                <div class="metric-value">{absenteeism_rate:.2f}%</div>
            </div>''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Filter for check-ins (attendance)
        check_ins_df = filtered_df[filtered_df['Status'] == 'C/In']
        check_out_df = filtered_df[filtered_df['Status'] == 'C/Out']

        # Calculate the total number of unique employees (if needed for other calculations)
        total_employees = filtered_df['No.'].nunique()

        # Group by week and calculate the average attendance (number of check-ins per day in that week)
        weekly_attendance = check_ins_df.groupby('week').size().reset_index(name='total_check_ins')

        # Calculate the number of unique days within each week
        days_per_week = check_ins_df.groupby('week')['Day'].nunique().reset_index(name='unique_days')

        # Merge the two DataFrames to calculate average attendance per day per week
        weekly_attendance = pd.merge(weekly_attendance, days_per_week, on='week')

        # Calculate the average attendance per week
        weekly_attendance['average_attendance'] = weekly_attendance['total_check_ins'] / weekly_attendance['unique_days']

        # Adjust week numbers to start from 1
        min_week = weekly_attendance['week'].min()
        weekly_attendance['week'] = weekly_attendance['week'] - min_week + 1
        
        # Create a new column for labeling weeks as "Week 1", "Week 2", etc.
        weekly_attendance['week_label'] = 'Week ' + weekly_attendance['week'].astype(str)
        
        col1, col2, col3= st.columns(3)
        
        with col1:
            #st.markdown(f"<h6 style='text-align: center;'>Average Weekly Attendance Trend for {selected_month}</h6>",unsafe_allow_html=True)
            # Plot the average weekly attendance
            fig = px.line(weekly_attendance, x='week_label', y='average_attendance', 
                        #title=f'Average Weekly Attendance Trend for {selected_month}',
                        labels={'week': 'Week Number', 'average_attendance': 'Average Attendance per Day'},
                        markers=True)

             # Update layout to adjust size
            fig.update_layout(
                width=400,  # Width in pixels
                height=300,  # Height in pixels
                margin=dict(l=50, r=70, t=50, b=50),  # Adjust margins as needed
                title={
                        'text': f'Average Weekly Attendance Trend for {selected_month}',
                        'x': 0.5,  # Center alignment
                        'xanchor': 'center'
                                        }
            )

            # Display the plot in Streamlit
            
            st.plotly_chart(fig, use_container_width=False)  # Use container width to fit the column

        

        # Inside the dashboard_page function
        with col3:
            
            # Create the custom gauge chart
            fig_custom_gauge = create_custom_gauge(daily_absenteeism_rate)
            
            # Display the gauge chart in Streamlit
            st.plotly_chart(fig_custom_gauge, use_container_width=True)


        with col2:
            absenteeism_per_week = weekly_attendance[['week', 'average_attendance']]
            absenteeism_per_week['absenteeism_rate'] = (1 - absenteeism_per_week['average_attendance'] / total_employees) * 100
            absenteeism_per_week['week'] = absenteeism_per_week['week'] - absenteeism_per_week['week'].min() + 1
        
        # Create a new column for labeling weeks as "Week 1", "Week 2", etc.
            absenteeism_per_week['week_label'] = 'Week ' + absenteeism_per_week['week'].astype(str)
            #st.markdown(f"<h6 style='text-align: center;'>Weekly Absenteeism Rate Trend for {selected_month}</h6>", unsafe_allow_html=True)

            fig_trend = px.line(
                absenteeism_per_week,
                x='week_label',
                y='absenteeism_rate',
                labels={'week_label': 'Week', 'absenteeism_rate': 'Absenteeism Rate (%)'},
                markers=True
            )
            
            fig_trend.update_layout(
                width= 300,
                height=300,
                margin=dict(l=30, r=30, t=50, b=50),
                xaxis_title='Week',
                yaxis_title='Absenteeism Rate (%)',
                #title=f'Weekly Absenteeism Rate Trend for {selected_month}' 
                title={
                        'text': f'Weekly Absenteeism Rate Trend for {selected_month}',
                        'x': 0.5,  # Center alignment
                        'xanchor': 'center'
                                        }
            )

            st.plotly_chart(fig_trend, use_container_width=True)
            
                   
    else:
        st.warning("No data available. Please upload a file first.")



def employees_page():
    
    st.markdown("<h1 style='text-align: center;'>EMPLOYEES SUMMARY</h1>", unsafe_allow_html=True)

    if 'df' in st.session_state:
        df = st.session_state['df']
        
        col1, col2,col3= st.columns(3)
        
        with col1:
            selected_year = st.selectbox("Select Year", df['Year'].unique())
        
        # Filter data based on the selected year first
        year_filtered_df = df[df['Year'] == selected_year]
        
        import calendar

        # Correctly map the month names or numbers
        if year_filtered_df['Month'].dtype == 'O':  # If 'Month' column is a string
            month_to_num = {month: index for index, month in enumerate(calendar.month_name) if month}
            year_filtered_df['Month_Number'] = year_filtered_df['Month'].map(month_to_num)
        else:  # If 'Month' column is numeric
            year_filtered_df['Month_Number'] = year_filtered_df['Month'].astype(int)

        year_filtered_df['Month_Name'] = year_filtered_df['Month_Number'].apply(lambda x: calendar.month_name[x])

        with col2:
            selected_month = st.selectbox("Select Month", year_filtered_df['Month_Name'].unique())
           # Filter data based on the selected month name and year
        filtered_df = year_filtered_df[year_filtered_df['Month_Name'] == selected_month]
            
        with col3:
             # Add a date picker for selecting a specific day
            selected_date = st.date_input("Select Date", value=pd.to_datetime(filtered_df['Date/Time'].min()).date(),
                                        min_value=pd.to_datetime(filtered_df['Date/Time'].min()).date(),
                                        max_value=pd.to_datetime(filtered_df['Date/Time'].max()).date())
            
            # Filter data based on the selected date
            date_filtered_df = filtered_df[filtered_df['Date/Time'].dt.date == pd.to_datetime(selected_date).date()]
        
        # Filter rows with 'C/In' status
        check_in_df = filtered_df[filtered_df['Status'] == 'C/In']
        
        
        
        # Count unique attendance days for each employee
        attendance_counts = check_in_df.groupby('Name')['Day'].nunique().reset_index()
        attendance_counts.columns = ['Name', 'Attendance Days']
        
        # Calculate total working days in the dataset (assuming the data spans a known range)
        total_working_days = check_in_df['Day'].nunique()
        
        attendance_counts['Attendance Percentage'] = (attendance_counts['Attendance Days'] / total_working_days) * 100
        # Select top 5 employees by attendance percentage
        top_5_attendance = attendance_counts.sort_values(by='Attendance Percentage', ascending=False).head(10)
        top_5_absentees = attendance_counts.sort_values(by='Attendance Percentage', ascending=False).tail(10)
        
        fig = px.bar(
    top_5_attendance,
    x='Attendance Percentage',
    y='Name',
    orientation='h',
    text='Attendance Percentage',
    color_discrete_sequence=['#ff6f61'],  # Custom color
    title='Top 5 Employees by Attendance'
)

    # Update the layout
    fig.update_layout(
        xaxis=dict(ticksuffix="%"),  # Ensure the x-axis covers 0% to 100%
        yaxis=dict(autorange="reversed",range=[0, 100]),  # Reverse the y-axis to have the highest value at the top
        template='simple_white',
        title_x=0.3,  # Center the title
        margin=dict(l=10, r=0, t=60, b=50),
        title={
            'text': f'Top 10 Employees Attendees In {selected_month}',
            'x': 0.5,  # Center alignment
            'xanchor': 'center'
        }
    )

    col1, col2 = st.columns(2)
    with col1:
        # Show percentages on bars
        fig.update_traces(texttemplate='%{x:.2f}%', textposition='outside')
        #fig.update_layout(xaxis=dict(range=[0, 100]))

        # Display the plot
        st.plotly_chart(fig, use_container_width=True)
    
    intervals = [
    (pd.Timestamp('07:00:00'), pd.Timestamp('08:30:00'), 'Before 8:30 AM'),
    (pd.Timestamp('08:30:00'), pd.Timestamp('09:30:00'), '8:30-9:30 AM'),
    (pd.Timestamp('09:30:00'), pd.Timestamp('10:30:00'), '9:30-10:30 AM'),
    (pd.Timestamp('10:30:00'), pd.Timestamp('12:00:00'), '10:30 AM-12:00 PM'),
    (pd.Timestamp('12:00:00'), pd.Timestamp('23:59:59'), 'After 12:00 PM')
]
    
    def categorize_time(check_in_time):
        check_in_time_only = check_in_time.time()  # Extract the time part of the Timestamp
        for start, end, label in intervals:
            if start.time() <= check_in_time_only < end.time():
                return label
    
    
    check_in_dy = date_filtered_df[date_filtered_df["Status"] == "C/In"]
    
    
    
    check_in_dy['Check-In Interval'] = check_in_dy['Date/Time'].apply(categorize_time)
    
    # Calculate the distribution of check-ins across the intervals
    check_in_distribution = check_in_dy['Check-In Interval'].value_counts(normalize=True) * 100
    check_in_distribution = check_in_distribution.reset_index()
    check_in_distribution.columns = ['Interval', 'Percentage']
    
    fig = px.pie(
    check_in_distribution,
    values='Percentage',
    names='Interval',
    title='Distribution of Employee Check-In Times by Day',
    color_discrete_sequence=px.colors.sequential.RdBu,  # Custom color sequence
    hole=0.6
)
    
    fig.update_layout(
        margin=dict(l=100, r=0, t=50, b=50),
        width =600,
        title={
            #'text': f'Top 5 Employees by Attendance for {selected_month}',
            'x': 0.45,  # Center alignment
            'xanchor': 'center'
            
        }
    )
    with col2:
        # Update layout for better appearance
        fig.update_traces(textposition='outside', textinfo='percent', hoverinfo='percent+label')
        
        # Display the pie chart in Streamlit
        st.plotly_chart(fig, use_container_width=False)
        
    col1,col2 = st.columns(2)
    
    fig = px.bar(
    top_5_absentees,
    x='Attendance Percentage',
    y='Name',
    orientation='h',
    text='Attendance Percentage',
    color_discrete_sequence=['#5b4413   '],  # Custom color
    title='Top 5 Employees by Attendance'
)

    # Update the layout
    fig.update_layout(
        xaxis=dict(ticksuffix="%"),  # Ensure the x-axis covers 0% to 100%
        yaxis=dict(autorange="reversed",range=[0, 100]),  # Reverse the y-axis to have the highest value at the top
        template='simple_white',
        title_x=0.3,  # Center the title
        margin=dict(l=10, r=0, t=60, b=50),
        title={
            'text': f'Top 10 Employees Absentees In {selected_month}',
            'x': 0.5,  # Center alignment
            'xanchor': 'center'
        }
    )

    col1, col2 = st.columns(2)
    with col1:
        # Show percentages on bars
        fig.update_traces(texttemplate='%{x:.2f}%', textposition='outside')
        #fig.update_layout(xaxis=dict(range=[0, 100]))

        # Display the plot
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("""
            <style>
                .container {
                    display: flex;
                    flex-direction: row;
                    justify-content: space-between;
                }
                .metric-box {
                    padding: 20px;
                    margin: 10px 0;
                    border-radius: 10px;
                    text-align: center;
                }
                .late {
                    background-color: #FF6F61;  /* Light red */
                    color: white;
                }
                .early {
                    background-color: #9e7723;  /* Light blue */
                    color: white;
                }
            </style>
        """, unsafe_allow_html=True)

    # Create a container for the late coming and early going sections
        container = st.container()
        with container:
            
            st.markdown("<h3 style='text-align: center;'>Check-In and Check-Out Thresholds</h3>", unsafe_allow_html=True)
            # Create two columns
            col1, col2 = st.columns(2)

            # Late Coming Section
            with col1:
                # Slider for late coming threshold
                late_check_in_threshold = st.slider(
                    "Select the threshold time for Late Coming:",
                    value=(pd.to_datetime("09:00").time()),
                    format="HH:mm"
                )
                
                # Filter for late check-ins (after 9:00 AM)
                late_check_in = date_filtered_df[(date_filtered_df['Status'] == 'C/In') & (date_filtered_df['Date/Time'].dt.time > late_check_in_threshold)]
                late_check_in_count = late_check_in.shape[0]

                # Late Coming Box
                st.markdown(f"""
                    <div class="metric-box late">
                        <h3>Late Coming</h3>
                        <h1>{late_check_in_count}</h1>
                    </div>
                    """, unsafe_allow_html=True)

            # Early Going Section
            with col2:
                # Slider for early going threshold
                early_check_out_threshold = st.slider(
                    "Select the threshold time for Early Going:",
                    value=(pd.to_datetime("16:00").time()),
                    format="HH:mm"
                )
                
                # Filter for early check-outs (before 4:00 PM)
                early_check_out = date_filtered_df[(date_filtered_df['Status'] == 'C/Out') & (date_filtered_df['Date/Time'].dt.time < early_check_out_threshold)]
                early_check_out_count = early_check_out.shape[0]

                # Early Going Box
                st.markdown(f"""
                    <div class="metric-box early">
                        <h3>Early Going</h3>
                        <h1>{early_check_out_count}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                
    check_ins_df = filtered_df[filtered_df['Status'] == 'C/In']
    check_out_df = filtered_df[filtered_df['Status'] == 'C/Out']
    # Convert the 'Date/Time' column to datetime format
    check_ins_df['Date/Time'] = pd.to_datetime(check_ins_df['Date/Time'])
    check_out_df['Date/Time'] = pd.to_datetime(check_out_df['Date/Time'])

    # Extract hour from 'Date/Time' for both check-ins and check-outs
    check_ins_df['hour'] = check_ins_df['Date/Time'].dt.hour + check_ins_df['Date/Time'].dt.minute / 60
    check_out_df['hour'] = check_out_df['Date/Time'].dt.hour + check_out_df['Date/Time'].dt.minute / 60

    # Group by week and calculate average check-in and check-out times
    check_ins_df['week'] = check_ins_df['Date/Time'].dt.isocalendar().week
    check_out_df['week'] = check_out_df['Date/Time'].dt.isocalendar().week

    weekly_avg_check_in = check_ins_df.groupby('week')['hour'].mean().reset_index(name='weekly_avg_check_in_hour')
    weekly_avg_check_out = check_out_df.groupby('week')['hour'].mean().reset_index(name='weekly_avg_check_out_hour')

    # Merge the weekly averages of check-in and check-out times
    weekly_avg_times = pd.merge(weekly_avg_check_in, weekly_avg_check_out, on='week')

    # Adjust week numbers to start from 1
    min_week = weekly_avg_times['week'].min()
    weekly_avg_times['week'] = weekly_avg_times['week'] - min_week + 1

    # Create a new column for labeling weeks as "Week 1", "Week 2", etc.
    weekly_avg_times['week_label'] = 'Week ' + weekly_avg_times['week'].astype(str)

    # Convert the 'weekly_avg_check_in_hour' and 'weekly_avg_check_out_hour' columns to float
    weekly_avg_times['weekly_avg_check_in_hour'] = weekly_avg_times['weekly_avg_check_in_hour'].astype(float)
    weekly_avg_times['weekly_avg_check_out_hour'] = weekly_avg_times['weekly_avg_check_out_hour'].astype(float)

    def format_time(hours):
        hours, minutes = divmod(int(hours * 60), 60)
        return f"{hours:02d}:{minutes:02d}"

    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h2 style='text-align: center;'>Weekly Average Check-In Time</h2>", unsafe_allow_html=True)
        overall_avg_check_in = weekly_avg_times['weekly_avg_check_in_hour'].mean()
        #st.metric("Overall Average Check-In Time", format_time(overall_avg_check_in))
        with st.expander("Weekly Breakdown"):
            for index, row in weekly_avg_times.iterrows():
                st.metric(f"Week {row['week']}", format_time(row['weekly_avg_check_in_hour']))

    with col2:
        st.markdown("<h2 style='text-align: center;'>Weekly Average Check-Out Time</h2>", unsafe_allow_html=True)
        overall_avg_check_out = weekly_avg_times['weekly_avg_check_out_hour'].mean()
        #st.metric("Overall Average Check-Out Time", format_time(overall_avg_check_out))
        with st.expander("Weekly Breakdown"):
            for index, row in weekly_avg_times.iterrows():
                st.metric(f"Week {row['week']}", format_time(row['weekly_avg_check_out_hour']))

# Call home_page function to render the Streamlit app
if __name__ == "__main__":
    home_page()
