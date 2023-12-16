import streamlit as st

st.title("Handwashing Discovery Analysis")

st.subheader('Introduction')
st.text('''In the past people thought of illness as caused by "bad air" or evil spirits.
But in the 1800s Doctors started looking more at anatomy,
doing autopsies and started making arguments based on data.''')

# Import Statements
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

pd.options.display.float_format = '{:,.2f}'.format

# Create locators for ticks on the time axis


from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

st.subheader('Read the Data')

st.text('''df_yearly = pd.read_csv('annual_deaths_by_clinic.csv')
# parse_dates avoids DateTime conversion later
df_monthly = pd.read_csv('monthly_deaths.csv',
                         parse_dates=['date'])''')

df_yearly = pd.read_csv('annual_deaths_by_clinic.csv')
# parse_dates avoids DateTime conversion later
df_monthly = pd.read_csv('monthly_deaths.csv',
                         parse_dates=['date'])

st.subheader('Preliminary Data Exploration')

st.write(df_yearly.head())

st.write(df_monthly.head())

st.write(df_monthly.shape)

st.subheader('Checking for Nan Values and Duplicates')


st.text('df_yearly null values')
st.code(df_yearly.isna().any())

st.text('df_yearly duplicate values')
st.code(df_yearly.duplicated().values.any())

st.text('df_monthly null values')
st.code(df_monthly.isna().any())

st.text('df_monthly duplicate values')
st.code(df_monthly.duplicated().values.any())

st.subheader('Descriptive Statistics')

st.text('df_monthly.describe()')
st.code(df_monthly.describe())

st.text('df_yearly.describe()')
st.code(df_yearly.describe())

st.text('We see that on average there were about 267 births and 22.47 deaths per month.')

st.subheader('Percentage of Women Dying in Childbirth')

st.text('''In comparison, the United States recorded 18.5 maternal deaths per 100,000 or 0.018% in 2013 [(source).](
https://en.wikipedia.org/wiki/Maternal_death#:~:text=The%20US%20has%20the%20%22highest,17.8%20per%20100%2C000%20in%202009)''')

st.text('df_yearly.head()')
st.code(df_yearly.head())

st.text('df_monthly.head()')
st.code(df_monthly.head())

prob = df_yearly.deaths.sum() / df_yearly.births.sum() * 100
st.text('prob = df_yearly.deaths.sum() / df_yearly.births.sum() * 100')
st.code(f'Chances of dying in the 1840s in Vienna: {prob:.3}%')

st.subheader('Visualise the Total Number of Births 🤱 and Deaths 💀 over Time')

plt.figure(figsize=(14, 8), dpi=200)
plt.title('Total Number of Monthly Births and Deaths', fontsize=18)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.grid(color='grey', linestyle='--')

ax1.plot(df_monthly.date,
         df_monthly.births,
         color='skyblue',
         linewidth=3)

ax2.plot(df_monthly.date,
         df_monthly.deaths,
         color='crimson',
         linewidth=2,
         linestyle='--')

st.pyplot(plt)

st.subheader('The Yearly Data Split by Clinic')
line = px.line(df_yearly,
               x='year',
               y='births',
               color='clinic',
               title='Total Yearly Births by Clinic')

st.plotly_chart(line)

line = px.line(df_yearly,
               x='year',
               y='deaths',
               color='clinic',
               title='Total Yearly Deaths by Clinic')



st.plotly_chart(line)


st.subheader('Calculate the Proportion of Deaths at Each Clinic')

df_yearly['pct_deaths'] = df_yearly.deaths / df_yearly.births
clinic_1 = df_yearly[df_yearly.clinic == 'clinic 1']
avg_c1 = clinic_1.deaths.sum() / clinic_1.births.sum() * 100
st.text('''df_yearly['pct_deaths'] = df_yearly.deaths / df_yearly.births
clinic_1 = df_yearly[df_yearly.clinic == 'clinic 1']
avg_c1 = clinic_1.deaths.sum() / clinic_1.births.sum() * 100''')
st.code(f'Average death rate in clinic 1 is {avg_c1:.3}%.')

st.text('9.92%. In comparison, clinic 2 which was staffed by midwives had a much lower death rate of 3.88% over the course of the entire period.')




clinic_2 = df_yearly[df_yearly.clinic == 'clinic 2']
avg_c2 = clinic_2.deaths.sum() / clinic_2.births.sum() * 100
st.text('''clinic_2 = df_yearly[df_yearly.clinic == 'clinic 2']
avg_c2 = clinic_2.deaths.sum() / clinic_2.births.sum() * 100''')
st.code(f'Average death rate in clinic 2 is {avg_c2:.3}%.')


st.subheader('Plotting the Proportion of Yearly Deaths by Clinic')
line = px.line(df_yearly,
               x='year',
               y='pct_deaths',
               color='clinic',
               title='Proportion of Yearly Deaths by Clinic')

st.plotly_chart(line)

st.text("1842 was a rough year. About 16% of women died in clinic 1 and about 7.6% of women died in clinic 2.")

st.header('The Effect of Handwashing')

st.text('Date when handwashing was made mandatory 1847-06-01')

handwashing_start = pd.to_datetime('1847-06-01')
df_monthly['pct_deaths'] = df_monthly.deaths/df_monthly.births
before_washing = df_monthly[df_monthly.date < handwashing_start]
after_washing = df_monthly[df_monthly.date >= handwashing_start]

avg_prob_before = before_washing.pct_deaths.mean() * 100
st.code(f'Chance of death during childbirth before handwashing: {avg_prob_before:.3}%.')

avg_prob_after = after_washing.pct_deaths.mean() * 100
st.code(f'Chance of death during childbirth AFTER handwashing: {avg_prob_after:.3}%.')

mean_diff = avg_prob_before - avg_prob_after
st.code(f'Handwashing reduced the monthly proportion of deaths by {mean_diff:.3}%!')

times = avg_prob_before / avg_prob_after
st.code(f'This is a {times:.2}x improvement!')

df_monthly['washing_hands'] = np.where(df_monthly.date < handwashing_start, 'No', 'Yes')

box = px.box(df_monthly,
             x='washing_hands',
             y='pct_deaths',
             color='washing_hands',
             title='How Have the Stats Changed with Handwashing?')

box.update_layout(xaxis_title='Washing Hands?',
                  yaxis_title='Percentage of Monthly Deaths', )

st.plotly_chart(box)

st.subheader('Using a T-Test to Show Statistical Significance')
st.text('If the p-value is less than 1% then we can be 99% certain that handwashing has made a difference to the average monthly death rate. ')
import scipy.stats as stats

t_stat, p_value = stats.ttest_ind(a=before_washing.pct_deaths,
                                  b=after_washing.pct_deaths)

st.text('''t_stat, p_value = stats.ttest_ind(a=before_washing.pct_deaths, 
                                  b=after_washing.pct_deaths)''')

st.code(f'p-palue is {p_value:.10f}')
st.code(f't-statstic is {t_stat:.4}')



