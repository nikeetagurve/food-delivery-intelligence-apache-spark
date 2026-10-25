# FoodPulse — Food Delivery Intelligence & Operations Analytics

FoodPulse is an academic Big Data Analytics project that analyzes food-delivery operations using Apache Spark and presents interactive insights through a Streamlit dashboard.

## Project Overview

The project uses a publicly distributed Zomato food-delivery dataset containing 45,584 records and 20 raw attributes. It explores delivery duration, traffic, weather, vehicle characteristics, order patterns, and city categories.

**Important:** The dataset's `City` field contains categories such as `Metropolitian`, `Urban`, and `Semi-Urban`, not individual city names such as Nagpur. The dataset is not an official internal Zomato production database.

## Main Features

- Data cleaning and preprocessing
- Feature engineering, including estimated straight-line delivery distance
- Delivery performance categorization
- Apache Spark DataFrame and RDD analysis
- Spark SQL aggregations
- Interactive Streamlit dashboard with eight analytical pages
- Filters for available dataset categories
- Data exploration and CSV export features

Delivery performance categories are project-defined:
- Fast: under 25 minutes
- Standard: 25–35 minutes
- Delayed: over 35 minutes

These thresholds are for this academic project and are not official Zomato service-level targets.

## Technology Stack

- Python
- Apache Spark / PySpark
- Pandas and NumPy
- Streamlit
- Plotly
- Jupyter Notebook / Google Colab

## Repository Structure

```text
food-delivery-intelligence-apache-spark/
├── app/
│   ├── app.py
│   ├── pages/
│   ├── utils/
│   └── .streamlit/
├── data/
│   └── README.md
├── notebooks/
│   └── FoodPulse_Authentic_Zomato_Spark_Colab.ipynb
├── requirements.txt
├── .gitignore
└── README.md
```

## Run the Streamlit Dashboard Locally

Use Python 3.11 or 3.12 for a compatible environment, then run:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app/app.py
```

Open the local URL printed in your terminal.

The app retrieves the dataset from its configured public source, so internet access is required.

## Run the Spark Notebook

Open `notebooks/FoodPulse_Authentic_Zomato_Spark_Colab.ipynb` in Google Colab and run the cells in order. The notebook is designed for a Colab environment and uses Colab-specific paths for its temporary data and outputs.

## Dataset Provenance

The dataset is publicly distributed through:

https://github.com/Varunnagar/Zomato-Food-Delivery-Analysis

The raw CSV is not included in this repository. Dataset availability and the upstream source may change.

## Limitations

- The dataset does not identify individual named cities in its `City` column.
- Estimated distance is a straight-line geographic estimate, not actual road distance.
- The analysis identifies patterns and associations; it does not establish causation.
- The project-defined delivery categories are not official business targets.
- The dataset does not provide verified internal revenue or customer-satisfaction measurements.

## Academic Context

**Project:** Food Delivery Intelligence & Operations Analytics using Apache Spark  
**Product:** FoodPulse  
**Course:** Big Data Analytics Lab  
**Course Code:** 24CS02PR0503  
**Institution:** Ramdeobaba University, Nagpur  
**Academic Year:** 2026–27

## License and Dataset Notice

No license is asserted here for the upstream dataset. Check the source repository's terms before redistributing its data.
