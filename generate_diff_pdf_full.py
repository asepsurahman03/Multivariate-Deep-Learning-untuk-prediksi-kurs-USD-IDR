import os
try:
    from fpdf import FPDF
except ImportError:
    import sys
    sys.exit(1)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Detail Perubahan Paragraf - Paper Rupiah', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

changes = [
    {
        "title": "1. Abstrak",
        "before": "over 2015-2024. A 42-feature engineering suite is constructed with strict train-only normalization to prevent data leakage.",
        "after": "over 2016-2026. A 42-feature engineering suite is constructed with strict train-only normalization to prevent data leakage."
    },
    {
        "title": "2. Paragraf Deskripsi Kontribusi",
        "before": "(1) a reproducible multivariate dataset comprising nine daily financial and macroeconomic time series (2015-2024); (2) a 42-feature engineering pipeline...",
        "after": "(1) a reproducible multivariate dataset comprising nine daily financial and macroeconomic time series (2016-2026); (2) a 42-feature engineering pipeline..."
    },
    {
        "title": "3. Paragraf Penjelasan Dataset (yfinance)",
        "before": "Nine financial time series are retrieved via the yfinance Python library from Yahoo Finance for the period January 1, 2015 through December 31, 2024. The dataset end date is fixed, ensuring a clearly defined and reproducible experimental boundary. The chronological partition is as follows: Training (80%): January 2015-December 2022; Validation: 10% of training, shuffle=False; Test (20%, held-out): April 2023-December 2024 (432 trading days). No hyperparameter tuning was conducted by examining test-set metrics.",
        "after": "Nine financial time series are retrieved via the yfinance Python library from Yahoo Finance for the period June 1, 2016 through June 1, 2026. The dataset end date is fixed, ensuring a clearly defined and reproducible experimental boundary. The chronological partition is as follows: Training (80%): June 2016-March 2024; Validation: 10% of training, shuffle=False; Test (20%, held-out): April 2024-June 2026 (543 trading days). No hyperparameter tuning was conducted by examining test-set metrics."
    },
    {
        "title": "4. Tabel 1 (Dataset Variables)",
        "before": "TABLE I. Dataset Variables - Yahoo Finance Daily Data, Jan 2015-Dec 2024",
        "after": "TABLE I. Dataset Variables - Yahoo Finance Daily Data, Jun 2016-Jun 2026"
    },
    {
        "title": "5. Paragraf Normalisasi Data",
        "before": "Min-Max normalization is fitted exclusively on the training set (January 2015-December 2022), preventing information from validation or test periods from influencing scaling parameters.",
        "after": "Min-Max normalization is fitted exclusively on the training set (June 2016-March 2024), preventing information from validation or test periods from influencing scaling parameters."
    },
    {
        "title": "6. Paragraf Analisis Visual (Fig 2)",
        "before": "Fig. 2 visualizes the daily USD/IDR exchange rate from January 2015 through December 2024, overlaid with its 30-day moving average... a period of gradual depreciation from 2015 to 2019...",
        "after": "Fig. 2 visualizes the daily USD/IDR exchange rate from June 2016 through June 2026, overlaid with its 30-day moving average... a period of gradual depreciation from 2016 to 2019..."
    },
    {
        "title": "7. Caption Fig 2",
        "before": "Fig. 2. USD/IDR exchange rate historical trend (January 2015-December 2024) with 30-day moving average. Gray shading: COVID-19 shock (2020). Orange shading: Fed tightening cycle (2022-2023). The test period (April 2023-December 2024) is delineated by the right boundary.",
        "after": "Fig. 2. USD/IDR exchange rate historical trend (June 2016-June 2026) with 30-day moving average. Gray shading: COVID-19 shock (2020). Orange shading: Fed tightening cycle (2022-2023). The test period (April 2024-June 2026) is delineated by the right boundary."
    },
    {
        "title": "8. Caption Fig 3 (Correlation Heatmap)",
        "before": "computed exclusively on the training set (January 2015-December 2022).",
        "after": "computed exclusively on the training set (June 2016-March 2024)."
    },
    {
        "title": "9. Tabel 3 (Performance Comparison)",
        "before": "TABLE III. Forecasting Performance Comparison - All Models on Held-Out Test Set (April 2023-December 2024)",
        "after": "TABLE III. Forecasting Performance Comparison - All Models on Held-Out Test Set (April 2024-June 2026)"
    },
    {
        "title": "10. Caption Fig 5 (Actual vs Predicted)",
        "before": "Fig. 5. Actual vs. predicted USD/IDR on the held-out test period (April 2023-December 2024).",
        "after": "Fig. 5. Actual vs. predicted USD/IDR on the held-out test period (April 2024-June 2026)."
    },
    {
        "title": "11. Kesimpulan / Conclusion",
        "before": "This study presents a multivariate deep learning framework for USD/IDR Rupiah exchange rate prediction, integrating nine macroeconomic and financial market indicators over 2015-2024. Methodological safeguards include a fixed December 2024 data cutoff...",
        "after": "This study presents a multivariate deep learning framework for USD/IDR Rupiah exchange rate prediction, integrating nine macroeconomic and financial market indicators over 2016-2026. Methodological safeguards include a fixed June 2026 data cutoff..."
    },
    {
        "title": "12. Data Availability Statement",
        "before": "All raw data are publicly available through Yahoo Finance and retrieved via yfinance (January 2015-December 2024).",
        "after": "All raw data are publicly available through Yahoo Finance and retrieved via yfinance (June 2016-June 2026)."
    }
]

pdf = PDF()
pdf.add_page()

for change in changes:
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, change['title'], 0, 1)
        
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(200, 0, 0)
    pdf.cell(0, 8, 'Teks Sebelumnya:', 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, change['before'])
    pdf.ln(2)
    
    pdf.set_text_color(0, 128, 0)
    pdf.cell(0, 8, 'Teks Setelah Di-update:', 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, change['after'])
    
    pdf.ln(5)

pdf.output('Perubahan_Paper_Rupiah_LENGKAP.pdf', 'F')
print("PDF Lengkap created successfully.")
