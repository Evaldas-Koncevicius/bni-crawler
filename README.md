# BNI Member Scraper  

This script scrapes member information from **BNI country websites** using **Selenium** and **BeautifulSoup**.  
It collects details such as **Name, Company, Description, Phone number, and Email link**, saving results to a CSV file.  

---

## ✨ Features  
- Uses **Selenium WebDriver** for navigation and waits.  
- Supports **resuming from last progress** with `BNI_Pending_*.csv`.  
- Exports:  
  - Main results → `filename.csv`  
  - Remaining links (if interrupted) → `BNI_Pending_filename.csv`  
  - Failed links → `BNI_Failed_Links_filename.csv`  

---

## ⚙️ Requirements  
- Python **3.8+**  
- **Google Chrome**  
- [ChromeDriver](https://chromedriver.chromium.org/) (matching your Chrome version)  
- Python packages:  

```bash
pip install selenium beautifulsoup4
```

## 📖 Usage  

Run the script in a terminal:  

```bash
python bni_scraper.py
```

## 📝 Provide the required inputs when prompted:

- BNI website extension (example: lt → for https://bni.lt)

- Output filename (example: membersLt, **do not add .csv**)

- Delay in seconds for page loading (default = 3 if left empty)


## 📂 Progress is saved automatically:

- Main results → membersLt.csv

- Remaining work → BNI_Pending_membersLt.csv

- Errors → BNI_Failed_Links_membersLt.csv
