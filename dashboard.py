import streamlit as st
import pandas as pd

# Assuming idc is already defined and available in session state
idc = st.session_state.idc

st.title('Dashboard')

st.header('Road iRating')

# Fetching the graph data
irgraph_data = idc.member_chart_data(category_id=2, chart_type=1)

#fetchingGeneralACCDAta

accountDetails = idc.member_info()

if accountDetails and 'account' in accountDetails:
    balanceData = accountDetails['account']
    print(balanceData)
if accountDetails and 'licenses' in accountDetails:
    licensesData = accountDetails['licenses']
    sportsCarData = licensesData['sports_car']
    formulaCarData = licensesData['formula_car']

ir_dollars = balanceData['ir_dollars']
ir_credits = balanceData['ir_credits']
roadIrating = sportsCarData['irating']
roadSafetyRating = sportsCarData['safety_rating']
roadClassName = sportsCarData['group_name']

# Extracting only the 'when' and 'value' fields from the raw data
import datetime

date = datetime.datetime.now()

if irgraph_data and 'data' in irgraph_data:
    cleaned_data = [{'when': entry['when'], 'value': entry['value']} for entry in irgraph_data['data']]
    cleaned_data.append({'when': date, 'value': roadIrating})
    df = pd.DataFrame(cleaned_data)

    df['when'] = pd.to_datetime(df['when'])



    df.set_index('when', inplace=True)

    st.line_chart(df['value'])
else:
    st.warning("No data available to display.")



career_stats = idc.stats_member_career()
yearly_stats = idc.stats_member_yearly()


# Przekształcenie danych do DataFrame
if yearly_stats and 'stats' in yearly_stats and career_stats and 'stats' in career_stats:
    yearly_df = pd.DataFrame(yearly_stats['stats'])
    yearly_df['year'] = yearly_df['year'].astype(str)  # upewniamy się, że rok to string

    carreer_df = pd.DataFrame(career_stats['stats'])
    carreer_df['year'] = 'ALL TIME'  # dodajemy kolumnę "year" z wartością "ALL TIME"

    combined_df = pd.concat([yearly_df, carreer_df], ignore_index=True)

    combined_df['year_sort'] = combined_df['year'].apply(lambda x: 9999 if x == 'ALL TIME' else int(x))
    combined_df.sort_values(by=['year_sort', 'category'], ascending=[False, True], inplace=True)
    combined_df.drop(columns='year_sort', inplace=True)

    display_columns = [
        'year', 'category', 'starts', 'wins', 'top5', 'poles',
        'avg_start_position', 'avg_finish_position', 'laps', 'laps_led',
        'avg_incidents', 'avg_points', 'win_percentage', 'top5_percentage',
        'laps_led_percentage', 'poles_percentage'
    ]

    combined_df = combined_df[display_columns]
    combined_df.rename(columns={
        'year': 'Year',
        'category': 'Category',
        'starts': 'Starts',
        'wins': 'Wins',
        'top5': 'Top 5s',
        'poles': 'Poles',
        'avg_start_position': 'Avg Start',
        'avg_finish_position': 'Avg Finish',
        'laps': 'Laps',
        'laps_led': 'Laps Led',
        'avg_incidents': 'Avg Inc',
        'avg_points': 'Avg Points',
        'win_percentage': 'Win %',
        'top5_percentage': 'Top5 %',
        'laps_led_percentage': 'Laps Led %',
        'poles_percentage': 'Poles %'
    }, inplace=True)

    st.header("Combined Yearly & Career Stats")
    st.dataframe(combined_df, use_container_width=True)

else:
    st.warning("No stats data available.")

recent_races = idc.stats_member_recent_races()

if recent_races and 'races' in recent_races:
    # Create DataFrame from the races data
    races_df = pd.DataFrame(recent_races['races'])


    # Convert session_start_time to datetime
    races_df['session_start_time'] = pd.to_datetime(races_df['session_start_time'])

    # Extract track name from the nested dictionary
    races_df['track_name'] = races_df['track'].apply(lambda x: x['track_name'])

    # Select and rename columns for display
    display_columns = [
        'session_start_time', 'series_name', 'track_name',
        'start_position', 'finish_position', 'laps', 'laps_led',
        'incidents', 'points', 'strength_of_field',
        'oldi_rating', 'newi_rating', 'drop_race'
    ]

    races_df = races_df[display_columns]

    races_df.rename(columns={
        'session_start_time': 'Date/Time',
        'series_name': 'Series',
        'track_name': 'Track',
        'start_position': 'Start Pos',
        'finish_position': 'Finish Pos',
        'laps': 'Laps',
        'laps_led': 'Laps Led',
        'incidents': 'Incidents',
        'points': 'Points',
        'strength_of_field': 'SOF',
        'oldi_rating': 'Old iRating',
        'newi_rating': 'New iRating',
        'drop_race': 'Drop Race'
    }, inplace=True)

    # Format datetime for better display
    races_df['Date/Time'] = races_df['Date/Time'].dt.strftime('%Y-%m-%d %H:%M')

    st.title("Recent Races")
    st.dataframe(races_df, use_container_width=True)
else:
    st.warning("No recent races data available.")

recentEvents = recent_races['races']
newiratings = []
oldiratings = []
sofs = []
incidents = []
finishPositions = []

recentEvents = recent_races['races']
for event in recentEvents:
    iRatingChange = 0
    newiratings.append(event['newi_rating'])
    oldiratings.append(event['oldi_rating'])
    sofs.append(event['strength_of_field'])
    incidents.append(event['incidents'])
    finishPositions.append(event['finish_position'])

recentIratingGain = newiratings[0] - oldiratings[-1]

avgSOF = sum(sofs) / len(sofs)

recentINC = sum(incidents) / len(incidents)

avgFinishPos = sum(finishPositions) / len(finishPositions)

st.header('Miscellaneous')
st.write('Recent iRating Change:', recentIratingGain)
st.write('Recent average SOF', avgSOF)
st.write('Recent incidents', recentINC)
st.write('Average finish positions:', avgFinishPos)

st.write('IR dollars:', ir_dollars)
st.write('IR credits:', ir_credits)

st.subheader('Sports Car')

st.write('iRating:', roadIrating)
st.write('Safety Rating:', roadSafetyRating, roadClassName)

st.subheader('Formula Cars')

formulaIrating = formulaCarData['irating']
formulaSafetyRating = formulaCarData['safety_rating']
formulaClassName = formulaCarData['group_name']

st.write('iRating:', formulaIrating)
st.write('Safety Rating:', formulaSafetyRating, formulaClassName)

