# Process Swimlane Descriptions (BPMN)

## 1. Procurement (As-Is — Manual)
```
[Dept Head] → Raise PR in Excel → Email to Manager
[Manager]   → Review PR → Approve/Reject via email reply
[Purchase]  → Vendor selection from Excel master list → Create PO manually
[Vendor]    → Deliver goods
[Warehouse] → GRN entry in separate Excel file
[Finance]   → Manual 3-way match (PO + GRN + Invoice) ← BOTTLENECK (6-day avg delay)
[Finance]   → Payment processing
```
**Inefficiencies:** 7 manual handoffs, no automated approval routing, 3-way match done manually, 12% error rate.

---

## 2. Invoicing (As-Is — Manual)
```
[Vendor]    → Send invoice (email / physical)
[AP Clerk]  → Manual data entry into Excel ← BOTTLENECK (18% error rate)
[AP Clerk]  → Cross-check with PO (separate file)
[Manager]   → Email approval chain (2–3 levels)
[Finance]   → Payment processing
```
**Inefficiencies:** Manual entry = 18% error rate, re-entry loops add 4–5 days per invoice.

---

## 3. Inventory (As-Is — Manual)
```
[Warehouse] → Weekly manual stock count
[Warehouse] → Update Excel master file
[Purchase]  → Weekly review of stock levels ← BOTTLENECK (reactive, not real-time)
[Purchase]  → Raise PO if below reorder point
[Warehouse] → Receive stock → Manual GRN
[Finance]   → Monthly reconciliation
```
**Inefficiencies:** No real-time visibility, stockouts discovered post-facto, ₹40L revenue leakage.

---

## 4. HR & Payroll (As-Is — Manual)
```
[HR]        → Collect attendance sheets from team leads
[HR]        → Manual leave calculation in Excel
[Finance]   → Payroll computation ← BOTTLENECK (attendance mismatches cause rework)
[Finance]   → Tax deduction calculation
[Finance]   → Bank disbursement
```
**Inefficiencies:** Attendance data mismatch = 8% payroll rework rate.

---

## 5. Sales (As-Is — Manual)
```
[Sales Rep] → Manual lead entry (CRM = separate Excel)
[Sales Rep] → Quotation via Word/email
[Sales]     → Order confirmation email
[Finance]   → Invoice generated manually ← BOTTLENECK (duplicate data entry)
[Warehouse] → Delivery note (separate file)
[Finance]   → Collection tracking
```
**Inefficiencies:** CRM and billing disconnected, 10% duplicate entry error rate.

---

## 6. Reporting & MIS (As-Is — Manual)
```
[Finance]   → Pull data from 14 Excel files (6 departments)
[Finance]   → Manual consolidation + VLOOKUP cross-referencing ← BOTTLENECK
[Finance]   → Manual checks and error correction
[Finance]   → Build report in PowerPoint / Excel
[Finance]   → Email distribution (D+4 from month-end)
```
**Inefficiencies:** 4-day delay, 20% error rate in consolidated data, decisions on stale numbers.

---

## To-Be State (Post ERP — MS Dynamics 365)
- All 6 processes on single unified platform
- Automated approval workflows with mobile notifications
- Real-time inventory visibility with auto-reorder triggers
- 3-way match automated — invoice processing in <1 day
- Live Power BI dashboards replacing manual MIS reports
- Projected: 35% cycle-time reduction, 75% error reduction in Year 1
