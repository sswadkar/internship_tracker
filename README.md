# Internship Tracker – Historical and Predictive Internship Listings

This Streamlit app allows you to:
- Search and filter historical internship postings (via [SimplifyJobs Summer 2026 GitHub repo](https://github.com/SimplifyJobs/Summer2026-Internships))
- View detailed listing metadata (post dates, sponsorship, activity)
- Predict future internship release dates based on historical patterns
- Explore a global forecast of listings expected to drop soon

## Features

### Search Listings
- Filter by company and job title
- View:
  - Posting and update dates
  - Job posting link
  - Active/inactive status

### Release Prediction
- Predicts upcoming posting date using the average historical posting window
- Adjusts forecast depending on past trends (e.g., Jan–May = likely next year)

### Global Prediction Explorer
- Shows all internships expected to post in the next 2 weeks, 1 month, or any custom range
- Aggregates listings across all companies/titles
- Ignores listings only present for Summer 2026 to avoid bias

### Filters
- Filter by:
  - Term (e.g., Summer 2024, 2025, 2026)
  - Sponsorship status (Offers, Does Not Offer, or Any)

## Installation

```bash
git clone https://github.com/yourusername/internship-tracker.git
cd internship-tracker
pip install -r requirements.txt
streamlit run app.py
```

## File Structure

```
.
├── app.py              # Streamlit app code
├── requirements.txt    # Python dependencies
├── .gitignore          # git file
└── README.md           # Project documentation
```

## Requirements

Create a `requirements.txt` with:

```
streamlit
pandas
```

## Data Source

This app uses internship data from:
[SimplifyJobs Summer2026-Internships](https://github.com/SimplifyJobs/Summer2026-Internships)

The live JSON source is:  
`https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/refs/heads/dev/.github/scripts/listings.json`