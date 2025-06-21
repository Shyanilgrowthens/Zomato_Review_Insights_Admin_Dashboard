# Zomato Review Insights - Admin Dashboard

This project is focused on extracting, analyzing, and visualizing customer review data for a specific restaurant listed on Zomato. The objective is to help the business gain insights from customer feedback to improve service and operations.

## Phase 1: Restaurant Review Data Collection and Analysis

### Objective

- Automatically fetch reviews of our own restaurant from Zomato using the public API or web scraping.
- Extract relevant data such as ratings, comments, and timestamps.
- Perform basic sentiment and trend analysis on the collected reviews.
- Present the analysis through an internal admin-facing dashboard.

### Features

- Review scraping using API or Selenium-based automation.
- Storage of structured review data (JSON/CSV/DB).
- Sentiment analysis using NLP techniques.
- Admin dashboard to visualize:
  - Review count over time
  - Sentiment distribution
  - Frequent keywords
  - Rating trends

### Tech Stack (Shyanil Planned)

- **Backend:** Python (FastAPI)
- **Frontend:** React 
- **Scraping:** Selenium , json , time and  Requests + BeautifulSoup 
- **NLP:** NLTK
- **Visualization:**  Matplotlib and Seaborn
- **Database (Optional):** MySQL
### Backend Libraries Used

The scraping and data processing in this phase use the following Python libraries:



### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/zomato-review-insights.git
   cd zomato-review-insights
