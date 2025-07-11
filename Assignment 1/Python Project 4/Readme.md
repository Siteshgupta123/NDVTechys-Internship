
![NDV LOGO](https://github.com/user-attachments/assets/27b20622-fbe9-46ec-8872-a246e73597c6)

# LifeFlow – Intelligent Scenario-Based Calculator
<img width="500" height="500" alt="ChatGPT Image Jul 12, 2025, 01_48_14 AM" src="https://github.com/user-attachments/assets/59e149c3-b11b-4aa4-998c-6d0c8c497c78" />

Welcome to **LifeFlow**, a Python-based desktop application that helps users simulate real-world financial scenarios through smart calculation panels, intuitive recommendations, and historical comparison tools. Designed and developed by **Sitesh Gupta**, TYBCA student at Reena Mehta College, Mumbai, as part of an internship at **NDVTechsys**, guided by **Srinu Sir**.

---
# Project View:
https://github.com/user-attachments/assets/1b22b0e7-5ef0-4da5-9ff9-16a036c5bfd1

<img width="600" height="500" alt="Screenshot 2025-07-12 011038" src="https://github.com/user-attachments/assets/9569848a-afd0-4c4a-95bc-62f1e643f67c" />
<img width="600" height="500" alt="Screenshot 2025-07-12 011236" src="https://github.com/user-attachments/assets/d5a7572a-3147-4771-8b32-7084bc66b286" />
<img width="600" height="500" alt="Screenshot 2025-07-12 011431" src="https://github.com/user-attachments/assets/7b0bfc0c-6da4-47f1-af73-eed1294161fb" />
<img width="600" height="500" alt="Screenshot 2025-07-12 011945" src="https://github.com/user-attachments/assets/bca0f24b-6b7a-489a-9d52-e1b647bbae4b" />


## Project Highlights

- **Modular Scenarios**: Supports Home Loan, Freelancer Forecast, and Education Budget Planning
- **Smart Recommendations**: Analyzes user inputs and gives contextual financial suggestions
- **Session Saving**: Automatically logs calculations to CSV for historical review
- **Compare Panel**: Lets users view and compare previously saved calculations across scenarios
- **Responsive UI**: Clean layout built with Tkinter, styled using `ttk` and custom themes

---

## Scenarios Covered

### Home Loan Planner
- Calculates EMI, total interest & repayment schedule
- Warns if EMI exceeds 40% of income

### Freelancer Forecaster
- Estimates monthly earnings, expenses & net income
- Offers a 3-month financial outlook

### Education Budget Explorer
- Projects a 4-year academic expense timeline
- Adjusts for inflation and breaks down semester-wise costs

---

## Technologies Used

| Tech      | Purpose                              |
|-----------|--------------------------------------|
| `Python`  | Core language                        |
| `Tkinter` | GUI interface                        |
| `ttk`     | Styled widgets for tabbed navigation |
| `Pandas`  | Data handling and CSV I/O            |
| `Decimal` | Precision arithmetic for calculations |
| `ttk.Notebook` | Tabbed scenario layout           |
| `ttk.Treeview` | History comparison display       |

---

##  Project Structure
```
LifeFlow/ ├── Calculator.py               
Main application ├── home_loan_history.csv
Auto-generated session log ├── freelancer_history.csv
Auto-generated session log ├── education_history.csv       
Auto-generated session log ├── NDVTechsys_logo.ico         # Window icon
```
--------------
## Future Enhancements
- Add visual dashboards using matplotlib or seaborn
- Include scenario badges and gamified achievements
- Introduce profile-based saving with encryption



