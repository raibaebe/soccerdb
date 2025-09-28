# Soccer Data Visualization & Analysis

This project analyzes and visualizes soccer data from **soccer.db** using Python, SQLite, and various data science libraries.  
It includes charts, interactive plots, and Excel exports with formatting.  

## Features
- 📊 Visualizations (Pie, Bar, Line, Histogram, Scatter)
- 🎥 Interactive Plotly scatter with year slider
- 📑 Export to Excel with:
  - Frozen headers
  - Auto filters
  - Gradient formatting for numeric columns
- ✅ All data pulled directly from `soccer.db`

## Project Structure
```
├── analytics.py        # Main script with charts
├── export_excel.py     # Excel export with formatting
├── requirements.txt    # List of dependencies
└── README.md           # Documentation
```

## Setup
1. Clone this repo or download the files.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place `soccer.db` in the project root folder.

## Usage
Run analytics (charts):
```bash
python analytics.py
```

Run Excel export:
```bash
python export_excel.py
```

## Outputs
- Charts are saved in `/charts/`
- Excel reports are saved in `/exports/`

## Requirements
- Python 3.9+
- Libraries listed in `requirements.txt`
