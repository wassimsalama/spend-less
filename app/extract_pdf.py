import fitz  # PyMuPDF
import pandas as pd
import re
from datetime import datetime

def parse_td_pdf(pdf_path, output_csv):
    doc = fitz.open(pdf_path)
    full_text = ""

    # Collect all pages' text
    for page in doc:
        full_text += page.get_text() + "\n"

    # Regex to match transactions like:
    # MAY 9   MAY 12   $13.27   CENTURION COFFEE-GUELPH
    transaction_pattern = re.findall(
        r"(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+(\d{1,2})\s+"
        r"(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+(\d{1,2})\s+"
        r"(-?\$[\d,]+\.\d{2})\s+(.*?)(?=\n[A-Z]{3}|$)",  # Lookahead for end of line or next transaction
        full_text,
        re.IGNORECASE | re.DOTALL
    )

    transactions = []

    for match in transaction_pattern:
        try:
            trans_month, trans_day, _, _, amount_str, description = match
            date_obj = datetime.strptime(f"{trans_month} {trans_day} 2025", "%b %d %Y")
            date = date_obj.strftime("%Y-%m-%d")
            if "-" in amount_str:
                continue  # Skip payments/refunds

            amount = float(amount_str.replace("$", "").replace(",", ""))
            amount = -amount  # Make it negative to reflect spend

            description = re.sub(r"\s+", " ", description.strip())  # collapse multi-spaces/newlines

            transactions.append((date, description, amount))
        except Exception as e:
            print(f"❌ Error parsing: {match} — {e}")

    df = pd.DataFrame(transactions, columns=["Date", "Description", "Amount"])
    df.to_csv(output_csv, index=False)
    print(f"✅ Parsed {len(df)} transactions and saved to {output_csv}")

# Run it
parse_td_pdf("content.pdf", "parse_5.csv")
