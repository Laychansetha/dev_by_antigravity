# Ibis Rice Farm Data — Field Data Dashboard

This repository contains the interactive client-side operations dashboard for the **Ibis Rice Program**. The dashboard visualizes agricultural metrics such as farmer participation, production volumes, crop quality, market pricing, and organic compliance rates across multiple field sites in Cambodia.

---

## 📂 Folder Structure

```
farm_data_dashboard/
├── .git/                      # Git repository files
├── .gitignore                 # Specifies intentionally untracked files to ignore
├── README.md                  # Developer documentation (this file)
├── index.html                 # Main dashboard HTML shell (entry point)
├── data/
│   └── dashboard_data.js      # Compiled JSON database wrapped in a window object
├── data_sources/              # Source CSV databases (dimensions and facts)
│   ├── dim_crop_variety.csv
│   ├── dim_farmer.csv
│   ├── dim_irpg.csv
│   ├── dim_site.csv
│   ├── dim_village.csv
│   ├── fact_afl_inspection.csv
│   ├── fact_ppr_purchase.csv
│   ├── fact_ppr_spec_record.csv
│   └── fact_thr_threshing.csv
├── preprocess/
│   └── build_data.py          # Python preprocessor script
└── src/
    ├── css/
    │   └── dashboard.css      # Core styles (glassmorphism UI, custom scrollbars, layout)
    ├── js/
    │   ├── data.js            # Frontend data filtering, aggregation, and formatting layer
    │   ├── charts.js          # Chart.js initialization and configuration layer
    │   ├── views.js           # Dynamic view loaders, KPI cards, and sub-tab components
    │   └── app.js             # Main controller, router, Map handler, and records pagination
    └── lib/                   # Third-party local dependencies
        ├── chart.umd.min.js   # Chart.js library (local)
        ├── leaflet.js         # Leaflet Map library (local)
        └── leaflet.css        # Leaflet Map styles (local)
```

---

## 🛠️ Installation & Setup

1. **Prerequisites**:
   - A modern web browser.
   - Python 3.7+ (only required if recompiling or updating raw data). No external pip packages are needed (only standard libraries like `csv`, `json`, and `os` are used).

2. **Running Locally**:
   - Because Leaflet and AJAX components can trigger browser security sandboxing when loading local files directly via `file://`, start a local HTTP development server in the repository directory:

     ```bash
     python -m http.server 8000
     ```

   - Open your browser and go to:
     👉 `http://localhost:8000`

---

## 💾 Data Sources

The dashboard preprocessor ingests two classes of raw CSV databases from the `data_sources/` folder:

### Dimension Tables

- `dim_site.csv`: Contains the program site details (e.g., Mondolkiri, Preah Vihear, Prey Lang, Ratanakiri, Siem Pang).
- `dim_village.csv`: Relates village IDs to village names.
- `dim_irpg.csv`: Defines local farmer producer groups.
- `dim_crop_variety.csv`: Mapping of rice varieties.
- `dim_farmer.csv`: Registrations details for each unique farmer (e.g., gender, site, village, registration date).

### Fact Tables

- `fact_afl_inspection.csv`: Field inspection logs containing certification status (`status_harvest`), compliance (`compliant`), land situation, ownership, and surface area (`surface_area_ha`).
- `fact_thr_threshing.csv`: Threshing logs containing production records (`actual_total_rice_production_kg`) and threshing methods.
- `fact_ppr_purchase.csv`: Transaction logs containing quantities bought (`quantity_kg`), grade (`grade`), and payment sums (`total_payment_riel`).
- `fact_ppr_spec_record.csv`: Quality measurements containing moisture level, color purity, good grain vs. broken grain ratios, and impurities.

---

## ⚙️ Data Preprocessor

The preprocessor ([preprocess/build_data.py](file:///c:/Users/DoF_1/Documents/Agv_dev_dashboard/preprocess/build_data.py)) parses and aggregates all raw CSV files into a single optimized JavaScript file ([data/dashboard_data.js](file:///c:/Users/DoF_1/Documents/Agv_dev_dashboard/data/dashboard_data.js)). This output defines a global database object `window.DASHBOARD_DATA` containing pre-aggregated summaries, cohort retentions, and quality stats.

### Running the Preprocessor

Run the script from the root directory whenever raw CSV files in `data_sources/` are modified:

```bash
python preprocess/build_data.py
```

---

## 📐 Calculations, Formulas, and Assumptions

### 1. Weight Units

- Weights are calculated in **Kilograms (Kg)** internally.
- Values under `1,000 Kg` are displayed with `Kg` suffix.
- Values `>= 1,000 Kg` are automatically converted to **Metric Tons (MT)** for cleaner displays on cards and charts.
  $$\text{Weight in MT} = \frac{\text{Weight in Kg}}{1000}$$
- **Average Yield**:
  $$\text{Yield (Kg/Ha)} = \frac{\text{Total Production (Kg)}}{\text{Farmland Area (Ha)}}$$

### 2. Currency Conversions

- Transactions are recorded in **Cambodian Riel (KHR)**.
- Exchange rate assumption: **`1 USD = 4,000 KHR`**.
- Prices under `4,000 KHR` (such as unit prices per Kg of paddy) are formatted in **KHR** (e.g., `1,750 KHR`).
- Large values (e.g., total revenues, income cards, and program totals) are converted and formatted in **US Dollars ($)**.
  $$\text{USD ($)} = \frac{\text{Value in KHR}}{4000}$$
- Values in the millions are represented with the `$M` suffix (e.g., `$5.51M`).

### 3. Active Farmer Status Breakdown

- The preprocessor counts each farmer only once per status per year (and site).
- This is calculated by tracking unique combinations of `(data_year, farmer_uid, farmer_status)` in `fact_afl_inspection.csv` to avoid double-counting farmers who had multiple plots inspected in the same year.

### 4. Site Comparison Calculations

- **True Unique Farmers**: In the Site Comparison, the unique active farmers count is computed in [data.js](file:///c:/Users/DoF_1/Documents/Agv_dev_dashboard/src/js/data.js) by querying all records in `_raw.farmer_records` that match the site and were active in at least one of the selected years (`state.years`). This resolves double-counting across multi-year selections.
- **Mathematically Sound Compliance**: The preprocessor outputs `compliant_count` and `inspection_count` in `site_year`. The frontend sums these raw counts for the selected years to calculate the true compliance rate:
  $$\text{Compliance Rate (\%)} = \left( \frac{\sum \text{Compliant Inspections}}{\sum \text{Total Inspections}} \right) \times 100$$

### 5. Geography Map Views

- The Leaflet map popups, site stats, and village lists displayed under the **Geography** tab represent only the **latest year (`2025`)** to highlight the current active participation in the project.

### 6. Cohort Retention Analysis

- Farmers are grouped into registration cohorts based on the year they registered (`first_year`).
- The retention rate for cohort $C$ in year $N$ (where $N = 1, 2, ...$) represents the percentage of those cohort farmers inspected in year $N$ of their registration.

---

## 📈 UI and Chart Configurations

The dashboard uses **Chart.js v4 (UMD)** for all graphs and **Leaflet.js** for the map. They are configured in `src/js/charts.js`:

1. **Farmer Growth (Stacked Bar)**: Renders the active farmer count by status (`New`, `Rejoin`, `Existing`) over time.
2. **Production Trend (Line)**: Renders the total production in Metric Tons (`MT`).
3. **Purchase Trend (Bar)**: Graphs program purchase totals in Millions of USD (`$M`).
4. **Site Comparison (Grouped Bar/Line)**: Compares sites by unique farmer counts (left axis, `Farmers`) and compliance rates (right axis, `Compliance Rate %`).
5. **Quality Trends (Line)**: Renders moisture levels, Good Grain %, Broken Grain %, and impurity ratios.
6. **Interactive Leaflet Map**: Generates interactive coordinate circles for sites. Clicking a circle populates local statistics and filters the sidebar list of **Villages in this Site**.

---

## 🧩 Customization & Extensibility

### Adding a New Site Coordinate

To add a new site on the map, edit `SITE_COORDS` in [preprocess/build_data.py](file:///c:/Users/DoF_1/Documents/Agv_dev_dashboard/preprocess/build_data.py):

```python
SITE_COORDS = {
    '1': {'name': 'Mondolkiri',   'lat': 12.4535, 'lng': 107.1877},
    ...
    '6': {'name': 'New Site',      'lat': 13.1234, 'lng': 105.1234},
}
```

Run `python preprocess/build_data.py` to regenerate the data.

### Formatting Helper Functions

Formatting changes (e.g., updating currencies or adding unit labels) should be modified in [src/js/data.js](file:///c:/Users/DoF_1/Documents/Agv_dev_dashboard/src/js/data.js):

- `kgFmt(n)`: Dynamic weight formatter (Kg $\to$ MT).
- `rielFmt(n)`: Dynamic money formatter (Riel $\to$ USD / KHR).

---

## 🚀 Deployment to GitHub Pages

1. Rename your repository to `farm_data_dashboard` in the GitHub Repository **Settings** tab.
2. Go to repository **Settings** > **Pages** > **Build and deployment**.
3. Under **Source**, select **Deploy from a branch**.
4. Set the **Branch** to `main` and keep the directory as `/ (root)`.
5. Click **Save**.
6. The site will deploy in 1-2 minutes and be hosted at:
   `https://<username>.github.io/farm_data_dashboard/`
7. Update your local git remote URL:

   ```bash
   git remote set-url origin https://github.com/<username>/farm_data_dashboard.git
   ```
