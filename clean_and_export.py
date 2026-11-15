import openpyxl
import shutil
import json
import os
from datetime import datetime

# ══════════════════════════════════════════════════════════════
#  CONFIGURATION — Update SRC when you get a new Excel file
# ══════════════════════════════════════════════════════════════
SRC  = r"c:\Users\I758345\Downloads\C user dashboard as on 15th Nov (2).xlsx"
# ══════════════════════════════════════════════════════════════

DST      = r"c:\Users\I758345\Documents\GitHub\contract-worker-dashboard\C user dashboard cleaned.xlsx"
JSON_OUT = r"c:\Users\I758345\Documents\GitHub\contract-worker-dashboard\dashboard_data.json"


shutil.copy2(SRC, DST)
wb = openpyxl.load_workbook(DST)

ws_val = wb["Validation"]
val_lookup = {}
for r in range(2, ws_val.max_row + 1):
    sow_id   = ws_val.cell(r, 2).value
    pricing  = ws_val.cell(r, 6).value
    contract = ws_val.cell(r, 7).value
    if sow_id:
        val_lookup[sow_id] = (pricing, contract)
print("Validation lookup: {} unique SOW IDs".format(len(val_lookup)))


def process_sheet(ws, sow_col, buyer_col, start_col, wo_col,
                  pricing_col, contract_col, data_start_row, sheet_name):
    print("\n=== Processing: {} ===".format(sheet_name))
    filled = 0
    for r in range(data_start_row, ws.max_row + 1):
        sow_id = ws.cell(r, sow_col).value
        if sow_id and sow_id in val_lookup:
            pricing, contract = val_lookup[sow_id]
            ws.cell(r, pricing_col).value  = pricing
            ws.cell(r, contract_col).value = contract
            filled += 1
    print("  Filled {} rows with Pricing + Contract".format(filled))

    data_rows = {}
    for r in range(data_start_row, ws.max_row + 1):
        br = ws.cell(r, buyer_col).value
        if not br:
            continue
        data_rows.setdefault(br, []).append(r)

    rows_to_delete = set()
    for br, row_list in data_rows.items():
        if len(row_list) > 1:
            dated = []
            for r in row_list:
                sd = ws.cell(r, start_col).value or ""
                wo = ws.cell(r, wo_col).value   or ""
                dated.append((sd, wo, r))
            dated.sort(key=lambda x: (x[0], x[1]), reverse=True)
            for _, _, r in dated[1:]:
                rows_to_delete.add(r)

    print("  Duplicate rows removed: {}".format(len(rows_to_delete)))
    for r in sorted(rows_to_delete, reverse=True):
        ws.delete_rows(r)
    print("  Rows remaining: {}".format(ws.max_row - data_start_row + 1))


process_sheet(wb["Tejaswini C"], 2, 5, 10, 7, 20, 21, 3, "Tejaswini C")
process_sheet(wb["Radhisha R"],  2, 5, 10, 7, 16, 17, 3, "Radhisha R")

wb.save(DST)
print("\nCleaned Excel saved to: {}".format(DST))


def dt_str(val):
    if val is None:
        return ""
    if isinstance(val, datetime):
        return val.strftime("%Y-%m-%d")
    return str(val)

records = []

ws = wb["Tejaswini C"]
for r in range(3, ws.max_row + 1):
    row = [ws.cell(r, c).value for c in range(1, 22)]
    if not any(row):
        continue
    records.append({
        "owner": "Tejaswini C",
        "supplier": row[0] or "",
        "sow_id": row[1] or "",
        "sow_name": row[2] or "",
        "sow_status": row[3] or "",
        "buyer_ref": row[4] or "",
        "worker_name": row[5] or "",
        "work_order_id": row[6] or "",
        "worker_id": row[7] or "",
        "cost_center": row[8] or "",
        "worker_start": dt_str(row[9]),
        "worker_end": dt_str(row[10]),
        "sow_start": dt_str(row[11]),
        "sow_end": dt_str(row[12]),
        "role": row[13] or "",
        "sow_owner": row[14] or "",
        "personnel_area": row[15] or "",
        "tax_location": row[16] or "",
        "pricing_type": row[19] or "",
        "contract_name": row[20] or "",
    })

ws2 = wb["Radhisha R"]
for r in range(3, ws2.max_row + 1):
    row = [ws2.cell(r, c).value for c in range(1, 18)]
    if not any(row):
        continue
    records.append({
        "owner": "Radhisha R",
        "supplier": row[0] or "",
        "sow_id": row[1] or "",
        "sow_name": row[2] or "",
        "sow_status": row[3] or "",
        "buyer_ref": row[4] or "",
        "worker_name": row[5] or "",
        "work_order_id": row[6] or "",
        "worker_id": row[7] or "",
        "cost_center": row[8] or "",
        "worker_start": dt_str(row[9]),
        "worker_end": dt_str(row[10]),
        "sow_start": dt_str(row[11]),
        "sow_end": dt_str(row[12]),
        "role": "",
        "sow_owner": row[13] or "",
        "personnel_area": "",
        "tax_location": "",
        "pricing_type": row[15] or "",
        "contract_name": row[16] or "",
    })

with open(JSON_OUT, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print("JSON exported: {} records".format(len(records)))
