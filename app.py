import streamlit as st
import pandas as pd
import requests
import datetime

st.set_page_config(page_title="Internship Tracker", layout="wide")
st.title("🔍 Internship Tracker – Historical and Predictive Listings")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/refs/heads/dev/.github/scripts/listings.json"
    raw = requests.get(url).json()
    df = pd.DataFrame(raw)
    df['date_posted'] = pd.to_datetime(df['date_posted'], unit='s')
    df['date_updated'] = pd.to_datetime(df['date_updated'], unit='s')
    return df

df = load_data()

st.subheader("🔎 Search Listings")
col1, col2 = st.columns(2)

with col1:
    selected_company = st.selectbox("Company", sorted(df['company_name'].unique()))
    company_df = df[df['company_name'] == selected_company]

with col2:
    job_titles = sorted(company_df['title'].unique())
    selected_title = st.selectbox("Job Title", job_titles)
    selected_df = company_df[company_df['title'] == selected_title]

st.markdown("### 📄 Historical Listing Information")
if selected_df.empty:
    st.warning("No listings found with that combination.")
else:
    for _, row in selected_df.iterrows():
        with st.expander(f"{row['title']} @ {row['company_name']} ({', '.join(row['terms'])})"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Posted:** {row['date_posted'].date()}")
                st.markdown(f"**Updated:** {row['date_updated'].date()}")
                st.markdown(f"**Active:** {'✅' if row['active'] else '❌'}")
            with col2:
                st.markdown(f"**Sponsorship:** {row['sponsorship']}")
                st.markdown(f"[🔗 View Posting]({row['url']})")

st.markdown("---")
st.markdown("### 📅 Expected Release Prediction")

def is_summer_2026_only(terms):
    return "Summer 2026" in terms and len(terms) == 1

non_2026_rows = selected_df[~selected_df['terms'].apply(is_summer_2026_only)]

if not non_2026_rows.empty:
    dayofyears = non_2026_rows['date_posted'].dt.dayofyear
    months = non_2026_rows['date_posted'].dt.month
    mean_day = int(dayofyears.mean())
    expected_year = datetime.datetime.now().year

    # If majority of past postings were in Jan-May, expect release next year
    if (months <= 5).mean() > 0.5:
        expected_year += 1

    expected_date = datetime.datetime(expected_year, 1, 1) + datetime.timedelta(days=mean_day)
    delta_days = (expected_date - datetime.datetime.now()).days

    if delta_days < 0:
        st.info(f"Most recent average posting was around **{expected_date.strftime('%b %d, 20%y')}**. Likely already posted this year.")
    elif delta_days <= 14:
        st.success(f"Expected in the **next 2 weeks**: around **{expected_date.strftime('%b %d, 20%y')}**")
    elif delta_days <= 30:
        st.warning(f"Expected in the **next month**: around **{expected_date.strftime('%b %d, 20%y')}**")
    else:
        st.info(f"Expected later this season: around **{expected_date.strftime('%b %d, 20%y')}**")
else:
    st.warning("Not enough historical data (excluding Summer 2026) to estimate.")

st.markdown("---")
st.markdown("### 🌐 Global Prediction Explorer")
range_days = st.slider("Show jobs expected within (days)...", 7, 90, 7)
today = datetime.datetime.now()
predictions = []

for (comp, tit), group in df.groupby(['company_name', 'title']):
    valid_rows = group[~group['terms'].apply(lambda terms: "Summer 2026" in terms and len(terms) == 1)]
    if valid_rows.empty:
        continue
    mean_doy = int(valid_rows['date_posted'].dt.dayofyear.mean())
    pred_date = datetime.datetime(today.year, 1, 1) + datetime.timedelta(days=mean_doy)
    delta = (pred_date - today).days
    if 0 <= delta <= range_days:
        predictions.append((pred_date.date(), comp, tit))

predictions.sort()

if predictions:
    for date, comp, tit in predictions:
        st.markdown(f"- **{comp}** – *{tit}* – expected around **{date.strftime('%b %d')}**")
else:
    st.info("No expected postings in the selected time window.")
