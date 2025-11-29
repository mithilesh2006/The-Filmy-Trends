# The-Filmy-Trends
“The Filmy Trends” is a dashboard project analyzing budget, genre, and rating trends across Indian and Hollywood movie industries using data-driven insights from multiple Kaggle movie datasets.


Project: The Filmy Trends
- Exploring Budget and Genre Trends in the Global Film Industry
-- Overview

The Filmy Trends project focuses on analyzing budget and genre trends across Indian and Hollywood movie industries.
Our goal is to visualize how different movie genres, production budgets, and ratings vary between industries — and how they have evolved over time.

This project culminates in an interactive dashboard that helps users understand patterns in filmmaking trends globally.

📊 Datasets Used

We combined data from two Kaggle sources:

- Hollywood Movies Dataset

→ Used to extract information for Hollywood movies (hollywood_movies.csv)

- IMDB Indian Movie Dataset

→ Used to obtain data for Indian movies (indian_movies.csv)

After cleaning and preprocessing, the final combined dataset (final_movies_dataset.csv) includes:

Movie Title

Genre

Budget

Revenue

Rating

Year

Industry

⚙️ Data Preparation Steps

Preprocessing

Removed missing or inconsistent entries.

Handled duplicates and standardized column names.

Cleaned currency symbols and converted budgets to USD (where applicable).

Data Integration

Merged Indian and Hollywood movie datasets using movies_merging.ipynb.

Created a unified column structure for analysis.

Feature Engineering

Derived new features like budget range, rating category, and decade.

Simplified genre groups for clear visual comparison.

Visualization

Analyzed average budgets by genre and industry.

Compared ratings and revenues across time periods.

Created dashboard visualizations for insights.
https://data-visuvalization-1.onrender.com


Tools & Libraries Used

Python (Pandas, Matplotlib, Seaborn, Plotly)

Power BI / Streamlit (for dashboard)

Jupyter Notebook

GitHub (for project hosting and collaboration)

 Insights

Hollywood movies generally have higher budgets but similar genre popularity to Indian movies.

Indian cinema shows a greater diversity of genres with moderate budgets.

Certain genres (like Action & Drama) dominate both industries, while Comedy is more common in Indian movies.


Future Work

Add real-time movie data via IMDb or TMDB APIs

Incorporate OTT/Streaming trends

Expand dashboard interactivity

-- Contributors

Project by:
 M. Sai Jagadeesh ,
 
 P.N.V. Navadeep ,
 
 R. Mithilesh 


dashboard : " https://data-visuvalization-1.onrender.com"
