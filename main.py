import openpyxl
import requests
from datetime import datetime

def download_file(url: str, output_path: str):
    response=requests.get(url)
    response.raise_for_status()
    with open(output_path,"wb") as f:
        f.write(response.content)
    print(f"File downloaded successfully to {output_path}.")



def convert_txt_to_excel(input_file: str, output_file: str) -> None:
    wb = openpyxl.Workbook()
    ws = wb.active

    header_written = False

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = [col.strip() if col.strip() != "-" else "" for col in line.split(";")]


            if not header_written and "Scheme" in line:
                ws.append(parts)
                header_written = True
                continue
            if not line[0].isdigit():
                continue

            ws.append(parts)

    wb.save(output_file)
    print(f"Excel file '{output_file}' created successfully.")


if __name__ == "__main__":
    url="https://portal.amfiindia.com/spages/NAVAll.txt"
    input_file = "navaii_sample.txt"
    output_file = "data3.xlsx"
    download_file(url, input_file)
    convert_txt_to_excel(input_file, output_file)
