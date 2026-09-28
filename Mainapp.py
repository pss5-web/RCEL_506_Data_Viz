import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
df=pd.read_csv('https://raw.githubusercontent.com/pss5-web/RCEL_506_Data_Viz/refs/heads/main/Grid%20view.csv')
df
df.columns
cols2remove=['Author','Secondary Author(s)', 'Illustrator(s)', 'Translator(s)', 'Series Name', 'Initiating Action']
df.drop(columns=cols2remove, inplace=True)
banned_df = df[df['Ban Status'] == 'Banned']
banned_df
state_counts = banned_df.groupby(banned_df.iloc[:, 1])['Title'].count().reset_index(name='Title_Count')
print(state_counts)
unique_states = banned_df.iloc[:, 1].unique().tolist()
print(unique_states)
plt.figure(figsize=(10, 5))
state_counts.plot(kind='bar')
plt.title('Count of Banned Titles by State')
plt.xlabel('State')
plt.ylabel('Number of Titles')
plt.tight_layout()
plt.show()
sns.scatterplot(data=state_counts, x='State', y='Title_Count')
plt.show()
bins = [-1, 10, 100, 500, 1000, 3000, 6000]
labels = [
    '0-10',
    '11-100',
    '101-500',
    '501-1000',
    '1001-3000',
    '3001-6000',
]
state_counts['Interval'] = pd.cut(
    state_counts['Title_Count'], bins=bins, labels=labels
)

plt.figure(figsize=(12, 6))
sns.scatterplot(data=state_counts, x='State', y='Interval')
plt.xticks(rotation=90)
plt.ylabel('Title Count Range')
plt.show()
plt.boxplot(state_counts['Title_Count'])
bins = [-1, 10, 100, 500, 1000, 3000, 6000]
labels = [
    '0-10',
    '11-100',
    '101-500',
    '501-1000',
    '1001-3000',
    '3001-6000',
]
state_counts['Interval'] = pd.cut(
    state_counts['Title_Count'], bins=bins, labels=labels
)
interval_codes = state_counts['Interval'].cat.codes

plt.figure(figsize=(8, 5))
plt.boxplot(interval_codes)
plt.yticks(ticks=range(len(labels)), labels=labels)
plt.ylabel('Title Count Range')
plt.show()
state_counts=state_counts[state_counts['Title_Count']<1000]
fig, ax = plt.subplots(figsize=(30, 8))
sns.scatterplot(data=state_counts, x='State', y='Title_Count',ax=ax)
ax.tick_params(axis='x', labelrotation=90, labelsize=10)
ax.set_xlabel("State")
ax.set_ylabel("Title Count")

fig.subplots_adjust(bottom=0.1)
plt.show()
state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}
st.set_page_config(layout="wide")

st.title("US Banned Books Dashboard")
state_counts['State_Code'] = state_counts['State'].map(state_abbrev)
state_counts
color_discrete_map = {
    '0-10': '#e0ecf4',
    '11-100': '#9ebcda',
    '101-500': '#8856a7',
    '501-1000': '#810f7c',
    '1001-3000': '#4d004b',
    '3001-6000': '#2d002b'
}

df_map = px.choropleth(
    state_counts,
    locations="State_Code",       # 2-letter state code column
    locationmode='USA-states',
    color='Interval',             # Categorical column forces separate legend boxes
    color_discrete_map=color_discrete_map,
    scope='usa',
    hover_name="State",
    hover_data={'Title_Count': True},
    labels={'Interval': 'Title Range'},
    title="<b>Banned Books by State</b><br><sup>Data from July 2023 to June 2024</sup>"
)

# Center the titles and set layout
df_map.update_layout(
    title={
        'x': 0.5,
        'xanchor': 'center'
    },
    legend_title_text='Books Count',
    margin={"r":0, "t":60, "l":0, "b":0}
)

st.plotly_chart(df_map, use_container_width=True)
