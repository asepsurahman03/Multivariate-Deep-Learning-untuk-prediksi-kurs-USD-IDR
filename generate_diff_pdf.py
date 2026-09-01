import os
try:
    from fpdf import FPDF
except ImportError:
    import sys
    print("fpdf not installed.")
    sys.exit(1)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Perubahan Teks Paper Rupiah Prediction', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

changes = [
    {
        "title": "1. Rentang Tahun Keseluruhan",
        "desc": "Terletak di bagian Abstrak, Judul Tabel I, Penjelasan Gambar 2, dan Kesimpulan",
        "before": "2015-2024 (atau January 2015-December 2024)",
        "after": "2016-2026 (atau June 2016-June 2026)"
    },
    {
        "title": "2. Rentang Tanggal Spesifik (Dataset)",
        "desc": "Tanggal fix yang memastikan dataset terdefinisi secara historis",
        "before": "January 1, 2015 through December 31, 2024",
        "after": "June 1, 2016 through June 1, 2026"
    },
    {
        "title": "3. Data Training (80%)",
        "desc": "Digunakan pada penjelasan partisi training set, heatmap korelasi",
        "before": "January 2015-December 2022",
        "after": "June 2016-March 2024"
    },
    {
        "title": "4. Data Testing (20%)",
        "desc": "Digunakan pada partisi test set, Gambar 2, Gambar 5, Tabel III, Tabel VI",
        "before": "April 2023-December 2024",
        "after": "April 2024-June 2026"
    },
    {
        "title": "5. Jumlah Hari Perdagangan (Test Set)",
        "desc": "Detail perhitungan hari perdagangan",
        "before": "(432 trading days)",
        "after": "(543 trading days)"
    },
    {
        "title": "6. Tren Historis Awal",
        "desc": "Konteks tren pergerakan awal Rupiah",
        "before": "from 2015 to 2019",
        "after": "from 2016 to 2019"
    },
    {
        "title": "7. Batasan Metodologi",
        "desc": "Konteks cutoff data",
        "before": "December 2024 data cutoff",
        "after": "June 2026 data cutoff"
    }
]

pdf = PDF()
pdf.add_page()

for change in changes:
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, change['title'], 0, 1)
    
    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 8, change['desc'])
    
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(200, 0, 0)
    pdf.cell(30, 8, 'Sebelumnya:', 0, 0)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, change['before'], 0, 1)
    
    pdf.set_text_color(0, 128, 0)
    pdf.cell(30, 8, 'Setelahnya:', 0, 0)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, change['after'], 0, 1)
    
    pdf.ln(3)

pdf.output('Perubahan_Paper_Rupiah_2026.pdf', 'F')
print("PDF created successfully.")
