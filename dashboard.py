import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
merged_df = pd.read_csv("bike_sharing.csv")

st.title("🚲 Bike Sharing Data Dashboard 📊")

# Sidebar filters
st.sidebar.header("Filter Data 🛠️")

# Season filter
season_options = merged_df['season_day'].unique().tolist()
season_filter = st.sidebar.multiselect("Select Season:", season_options, default=season_options)

# Weather filter
weather_options = merged_df['weathersit_day'].unique().tolist()
weather_filter = st.sidebar.multiselect("Select Weather Condition:", weather_options, default=weather_options)

# Apply filters
filtered_df = merged_df[(merged_df['season_day'].isin(season_filter)) & (merged_df['weathersit_day'].isin(weather_filter))]

# Visualization 1: Dampak Cuaca pada Penyewaan Sepeda
st.subheader("🌦️ Impact of Weather on Bike Rentals")

weather_avg = filtered_df.groupby("weathersit_day")["cnt_day"].mean().reset_index()

st.subheader("📊 Average Bike Rentals per Weather Condition")
st.write(weather_avg)

if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='weathersit_day', y='cnt_day', data=filtered_df, palette='coolwarm', estimator=lambda x: np.mean(x), ax=ax)

    for p in ax.patches:
        ax.annotate(f'{p.get_height():.0f}', 
                    (p.get_x() + p.get_width() / 2, p.get_height()), 
                    ha='center', va='bottom', fontsize=10, color='black')

    ax.set_xlabel('Weather Condition')
    ax.set_ylabel('Average Bike Rentals')
    ax.set_title('Impact of Weather on Bike Rentals')
    st.pyplot(fig)
else:
    st.warning("No data available for the selected filter.")

st.markdown("📌 **Insight:** Poorer weather (e.g. rainy or extreme) tends to lower the number of bike loans. _Cuaca yang lebih buruk (misalnya hujan atau ekstrem) cenderung menurunkan jumlah peminjaman sepeda._")

fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x=filtered_df['weathersit_day'], y=filtered_df['cnt_day'], hue=filtered_df['weathersit_day'], data=merged_df, palette='coolwarm', legend=False, ax=ax)
ax.set_title('Impact of Weather on Bike Rentals')
ax.set_xlabel('Weather Condition')
ax.set_ylabel('Number of Bike Rentals')
st.pyplot(fig)

# Visualization 2: Tren Penyewaan Sepeda Per Jam
st.subheader("⏰ Bike Rentals Trend by Hour")

# Hitung tren peminjaman sepeda per jam
hourly_trend = filtered_df.groupby('hr')['cnt_hour'].mean()

# Cek apakah hourly_trend kosong sebelum mencari max & min
if not hourly_trend.empty:
    max_hour = hourly_trend.idxmax()
    min_hour = hourly_trend.idxmin()
    max_value = hourly_trend.max()
    min_value = hourly_trend.min()
else:
    max_hour, min_hour = None, None
    max_value, min_value = 0, 0  # Supaya tidak error saat menampilkan grafik

st.markdown(f"📈 **Peak Hour:** {max_hour if max_hour is not None else 'N/A'}:00 "
            f"with an average of {max_value:.0f} rentals.")
st.markdown(f"📉 **Lowest Hour:** {min_hour if min_hour is not None else 'N/A'}:00 "
            f"with an average of {min_value:.0f} rentals.")

# Buat visualisasi hanya jika ada data
if not hourly_trend.empty:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=hourly_trend.index, y=hourly_trend.values, marker="o", color="b", ax=ax)

    ax.annotate(f"Peak: {max_hour}:00", xy=(max_hour, max_value), xytext=(max_hour, max_value + 10),
                arrowprops=dict(facecolor='green', shrink=0.05), ha='center', fontsize=10, color='green')

    ax.annotate(f"Lowest: {min_hour}:00", xy=(min_hour, min_value), xytext=(min_hour, min_value - 10),
                arrowprops=dict(facecolor='red', shrink=0.05), ha='center', fontsize=10, color='red')

    ax.set_title('Average Bike Rentals per Hour')
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Number of Rentals')
    ax.set_xticks(range(0, 24))
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning("⚠️ No data available for the selected filters.")

# Visualization 3: Pola Penyewaan Sepeda Musiman
st.subheader("🍂 Seasonal Bike Rentals")

# Hitung jumlah peminjaman sepeda berdasarkan musim
seasonal_trend = filtered_df.groupby("season_day")["cnt_day"].sum().reset_index()

# Cek apakah seasonal_trend kosong
if not seasonal_trend.empty:
    max_season = seasonal_trend.loc[seasonal_trend["cnt_day"].idxmax()]
    min_season = seasonal_trend.loc[seasonal_trend["cnt_day"].idxmin()]

    st.markdown(f"📈 **Highest Rentals in:** {max_season['season_day']} with {max_season['cnt_day']:,} rentals.")
    st.markdown(f"📉 **Lowest Rentals in:** {min_season['season_day']} with {min_season['cnt_day']:,} rentals.")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="season_day", y="cnt_day", data=seasonal_trend, palette="viridis", estimator=sum, ax=ax)

    for p in ax.patches:
        ax.annotate(f'{p.get_height():,.0f}', 
                    (p.get_x() + p.get_width() / 2, p.get_height()), 
                    ha='center', va='bottom', fontsize=10, color='black')

    ax.set_xlabel("Season")
    ax.set_ylabel("Total Bike Rentals")
    ax.set_title("Seasonal Bike Rentals")
    st.pyplot(fig)

    # Hitung total rentals dan persentase
    total_rentals = seasonal_trend["cnt_day"].sum()
    seasonal_trend["percentage"] = (seasonal_trend["cnt_day"] / total_rentals) * 100

    for _, row in seasonal_trend.iterrows():
        st.markdown(f"🟢 **{row['season_day']}:** {row['cnt_day']:,} rentals ({row['percentage']:.2f}%)")

else:
    st.warning("⚠️ No data available for the selected filters.")

# Visualization 4: Tren Penyewaan Sepeda per Jam Berdasarkan Musim
st.subheader("⏳ Hourly Bike Rental Trends Across Seasons")

hourly_trend = filtered_df.groupby(["season_day", "hr"])["cnt_hour"].mean().reset_index()

season_max_min = hourly_trend.groupby("season_day").agg(
    max_hour=("cnt_hour", "idxmax"),
    min_hour=("cnt_hour", "idxmin")
).reset_index()

for _, row in season_max_min.iterrows():
    max_hr = hourly_trend.iloc[row["max_hour"]]
    min_hr = hourly_trend.iloc[row["min_hour"]]
    st.markdown(f"🌟 **{row['season_day']}** - Peak at **{max_hr['hr']}h** ({max_hr['cnt_hour']:.0f} rentals), Lowest at **{min_hr['hr']}h** ({min_hr['cnt_hour']:.0f} rentals)")

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=hourly_trend, x='hr', y='cnt_hour', hue='season_day', palette='Set2', marker="o", ax=ax)
ax.set_xlabel("Hour")
ax.set_ylabel("Average Bike Rentals")
ax.set_title("Hourly Bike Rental Trends Across Seasons")
ax.legend(title="Season")
plt.xticks(range(0, 24))
plt.grid(True)
st.pyplot(fig)

# Visualization 5: Total Penyewaan per Jam Berdasarkan Musim dan Kondisi Cuaca
st.subheader("🌦️ Hourly Bike Rental Trends Across Weather Conditions")

hourly_trend = filtered_df.groupby(["weathersit_day", "hr"])["cnt_hour"].mean().reset_index()

weather_max_min = hourly_trend.groupby("weathersit_day").agg(
    max_hour=("cnt_hour", "idxmax"),
    min_hour=("cnt_hour", "idxmin")
).reset_index()

for _, row in weather_max_min.iterrows():
    max_hr = hourly_trend.iloc[row["max_hour"]]
    min_hr = hourly_trend.iloc[row["min_hour"]]
    st.markdown(f"🌟 **Weather {row['weathersit_day']}** - Peak at **{max_hr['hr']}h** ({max_hr['cnt_hour']:.0f} rentals), Lowest at **{min_hr['hr']}h** ({min_hr['cnt_hour']:.0f} rentals)")

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=hourly_trend, x='hr', y='cnt_hour', hue='weathersit_day', palette='coolwarm', marker="o", ax=ax)
ax.set_xlabel("Hour")
ax.set_ylabel("Average Bike Rentals")
ax.set_title("Hourly Bike Rental Trends Across Weather Conditions")
ax.legend(title="Weather Condition")
plt.xticks(range(0, 24))
plt.grid(True)
st.pyplot(fig)

# Footer
st.write("🚀 Dashboard Created with Streamlit & Matplotlib")
