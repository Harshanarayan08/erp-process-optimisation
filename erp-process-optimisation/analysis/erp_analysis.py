"""
ERP Process Optimisation & Cost-Benefit Analysis
=================================================
Author  : Harsha Narayan
Project : Consulting Resume — Project 1
Frame   : Issue Tree → Root Cause Analysis → Options → NPV/IRR → Recommendation

Business Context
----------------
A mid-size retail enterprise (800 employees, ₹350Cr revenue) operates on
fragmented manual workflows across 6 core departments. This analysis:

1. Maps 6 end-to-end business processes and identifies inefficiencies
2. Applies 5-Whys and Fishbone root-cause analysis to surface bottlenecks
3. Builds a cost-benefit model comparing 3 ERP vendors (SAP, Oracle, MS Dynamics)
4. Computes NPV, IRR, and Payback Period for each option over 5 years
5. Delivers a structured executive recommendation in consulting output format

Consulting Framework Applied
-----------------------------
Issue Tree  →  Hypothesis  →  Data  →  Insight  →  Recommendation
"""

import json
import math
import os
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

warnings.filterwarnings("ignore")
os.makedirs("output", exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 1. FIRM PROFILE
# ═══════════════════════════════════════════════════════════════════════════════
FIRM = {
    "name"              : "RetailCo India (Simulated)",
    "employees"         : 800,
    "annual_revenue_cr" : 350,
    "departments"       : ["Procurement", "Invoicing", "Inventory",
                           "HR & Payroll", "Sales", "Reporting & MIS"],
    "current_erp"       : "None (fully manual / MS Excel)",
}

# ═══════════════════════════════════════════════════════════════════════════════
# 2. PROCESS MAPPING — 6 DEPARTMENTS
#    Each process: steps, avg cycle time, error rate, FTE hours/month
# ═══════════════════════════════════════════════════════════════════════════════
PROCESSES = {
    "Procurement": {
        "steps"           : ["Raise PR", "Manager Approval", "Vendor Selection",
                             "PO Creation", "GRN", "3-Way Match", "Payment"],
        "cycle_days"      : 18,
        "error_rate_pct"  : 12,
        "fte_hours_month" : 320,
        "bottleneck"      : "Manual 3-way match causes 6-day average delay",
        "annual_cost_lakh": 28,
    },
    "Invoicing": {
        "steps"           : ["Receive Invoice", "Manual Data Entry", "Verification",
                             "Approval Chain", "Payment Processing"],
        "cycle_days"      : 14,
        "error_rate_pct"  : 18,
        "fte_hours_month" : 210,
        "bottleneck"      : "Manual data entry error rate 18% — triggers rework loops",
        "annual_cost_lakh": 19,
    },
    "Inventory": {
        "steps"           : ["Stock Count", "Excel Update", "Reorder Check",
                             "PO Trigger", "Receive Stock", "Reconcile"],
        "cycle_days"      : 7,
        "error_rate_pct"  : 15,
        "fte_hours_month" : 280,
        "bottleneck"      : "No real-time visibility — stockouts discovered post-facto",
        "annual_cost_lakh": 42,
    },
    "HR & Payroll": {
        "steps"           : ["Attendance Capture", "Leave Calculation",
                             "Payroll Computation", "Tax Deduction", "Disbursement"],
        "cycle_days"      : 5,
        "error_rate_pct"  : 8,
        "fte_hours_month" : 160,
        "bottleneck"      : "Payroll rework due to attendance data mismatches",
        "annual_cost_lakh": 14,
    },
    "Sales": {
        "steps"           : ["Lead Entry", "Quotation", "Order Confirmation",
                             "Invoice Generation", "Delivery", "Collection"],
        "cycle_days"      : 10,
        "error_rate_pct"  : 10,
        "fte_hours_month" : 240,
        "bottleneck"      : "Disconnected CRM and billing — duplicate data entry",
        "annual_cost_lakh": 22,
    },
    "Reporting & MIS": {
        "steps"           : ["Data Pull (multiple Excel files)", "Consolidation",
                             "Manual Checks", "Report Build", "Distribution"],
        "cycle_days"      : 4,
        "error_rate_pct"  : 20,
        "fte_hours_month" : 190,
        "bottleneck"      : "MIS reports take 4 days — decisions made on stale data",
        "annual_cost_lakh": 16,
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# 3. ROOT CAUSE ANALYSIS — 5-WHYS
# ═══════════════════════════════════════════════════════════════════════════════
ROOT_CAUSES = {
    "Revenue Leakage (₹40L/yr)": {
        "why1": "Stockouts occurring 3–4 times/month across top-20 SKUs",
        "why2": "Reorder triggers are manual — depend on weekly Excel reviews",
        "why3": "No real-time inventory data — stock counts done weekly",
        "why4": "Inventory, procurement, and sales systems not integrated",
        "why5": "Root cause: No unified ERP — data lives in 6 disconnected Excel files",
        "impact_lakh": 40,
    },
    "Process Inefficiency (₹28L/yr)": {
        "why1": "1,400 FTE hours/month spent on manual data entry and rework",
        "why2": "Each department maintains its own spreadsheet — no single source of truth",
        "why3": "Cross-department handoffs require manual re-entry (avg 3x per transaction)",
        "why4": "No workflow automation or approval routing in place",
        "why5": "Root cause: Absence of integrated workflow management system",
        "impact_lakh": 28,
    },
    "Reporting Delays (₹12L/yr)": {
        "why1": "MIS reports delayed by 3–4 days every month",
        "why2": "Finance team manually consolidates 14 Excel files from 6 departments",
        "why3": "No automated data aggregation or BI pipeline exists",
        "why4": "Decisions made on D-4 data — missed sales opportunities and overstock",
        "why5": "Root cause: No centralised data warehouse or real-time reporting layer",
        "impact_lakh": 12,
    },
}

TOTAL_ANNUAL_LOSS_LAKH = sum(v["impact_lakh"] for v in ROOT_CAUSES.values())

# ═══════════════════════════════════════════════════════════════════════════════
# 4. ERP VENDOR OPTIONS & COST-BENEFIT MODEL
# ═══════════════════════════════════════════════════════════════════════════════
ERP_OPTIONS = {
    "Option A: Microsoft Dynamics 365": {
        "capex_lakh"                : 45,
        "opex_per_year_lakh"        : 12,
        "implementation_weeks"      : 16,
        "process_efficiency_gain_pct": 68,
        "error_reduction_pct"       : 75,
        "risk"                      : "Medium — change management for 800 employees",
        "fit_score"                 : 8.2,   # out of 10
        "modules"                   : ["Finance", "SCM", "HR", "Sales", "BI"],
    },
    "Option B: SAP S/4HANA (SME Edition)": {
        "capex_lakh"                : 90,
        "opex_per_year_lakh"        : 22,
        "implementation_weeks"      : 28,
        "process_efficiency_gain_pct": 85,
        "error_reduction_pct"       : 90,
        "risk"                      : "High — long implementation, high licence cost",
        "fit_score"                 : 7.4,
        "modules"                   : ["Finance", "SCM", "HR", "Sales", "Analytics", "AI"],
    },
    "Option C: Oracle NetSuite": {
        "capex_lakh"                : 62,
        "opex_per_year_lakh"        : 16,
        "implementation_weeks"      : 20,
        "process_efficiency_gain_pct": 74,
        "error_reduction_pct"       : 80,
        "risk"                      : "Medium — cloud-first, faster go-live",
        "fit_score"                 : 7.9,
        "modules"                   : ["Finance", "Inventory", "CRM", "Ecommerce", "BI"],
    },
}

DISCOUNT_RATE = 0.10   # 10% WACC

def compute_financials(option: dict, years: int = 5) -> dict:
    """NPV, IRR (Newton-Raphson), and payback period computation."""
    eff_gain  = option["process_efficiency_gain_pct"] / 100
    err_red   = option["error_reduction_pct"] / 100
    annual_saving = TOTAL_ANNUAL_LOSS_LAKH * (eff_gain * 0.6 + err_red * 0.4)
    annual_net    = annual_saving - option["opex_per_year_lakh"]
    capex         = option["capex_lakh"]

    cashflows = [-capex] + [annual_net] * years

    # NPV
    npv = sum(cf / (1 + DISCOUNT_RATE) ** t for t, cf in enumerate(cashflows))

    # Payback
    cum, payback = -capex, None
    for yr in range(1, years + 1):
        cum += annual_net
        if cum >= 0 and payback is None:
            prev_cum = cum - annual_net
            payback = round(yr - 1 + (-prev_cum) / annual_net, 1)

    # IRR via Newton-Raphson
    def npv_fn(r):
        return sum(cf / (1 + r) ** t for t, cf in enumerate(cashflows))
    def dnpv_fn(r):
        return sum(-t * cf / (1 + r) ** (t + 1) for t, cf in enumerate(cashflows))
    r = 0.2
    for _ in range(100):
        fn_val = npv_fn(r)
        if abs(fn_val) < 1e-6:
            break
        r -= fn_val / (dnpv_fn(r) + 1e-10)
    irr = round(r * 100, 1)

    # 5yr ROI
    roi = round((npv / capex) * 100, 0)

    return {
        "annual_saving_lakh" : round(annual_saving, 1),
        "annual_net_lakh"    : round(annual_net, 1),
        "5yr_npv_lakh"       : round(npv, 1),
        "irr_pct"            : irr,
        "payback_years"      : payback,
        "5yr_roi_pct"        : roi,
    }

# ═══════════════════════════════════════════════════════════════════════════════
# 5. PRINT EXECUTIVE BUSINESS CASE
# ═══════════════════════════════════════════════════════════════════════════════
def print_business_case():
    print("\n" + "═"*68)
    print("  ERP PROCESS OPTIMISATION — EXECUTIVE BUSINESS CASE")
    print(f"  Client : {FIRM['name']}  |  Revenue: ₹{FIRM['annual_revenue_cr']}Cr  |  Employees: {FIRM['employees']}")
    print("═"*68)

    print("\n📌 PROBLEM STATEMENT")
    total_fte = sum(p["fte_hours_month"] for p in PROCESSES.values())
    total_cost = sum(p["annual_cost_lakh"] for p in PROCESSES.values())
    print(f"   {len(PROCESSES)} core processes run on disconnected Excel files.")
    print(f"   {total_fte:,} FTE hours/month lost to manual work.")
    print(f"   ₹{total_cost}L annual process cost — ₹{TOTAL_ANNUAL_LOSS_LAKH}L directly recoverable.")

    print("\n🔍 PROCESS INEFFICIENCY MAP")
    print(f"  {'Process':<22} {'Cycle (days)':>12} {'Error Rate':>11} {'FTE hrs/mo':>11} {'Cost/yr':>10}  Bottleneck")
    print("  " + "-"*90)
    for proc, d in PROCESSES.items():
        print(f"  {proc:<22} {d['cycle_days']:>12} {d['error_rate_pct']:>10}%"
              f" {d['fte_hours_month']:>11} ₹{d['annual_cost_lakh']:>7}L  {d['bottleneck'][:50]}")

    print("\n🌳 ROOT CAUSE ANALYSIS (5-Whys)")
    for issue, rc in ROOT_CAUSES.items():
        print(f"\n  Issue: {issue}")
        for i in range(1, 6):
            print(f"    Why {i}: {rc[f'why{i}']}")

    print(f"\n  Total Recoverable Loss: ₹{TOTAL_ANNUAL_LOSS_LAKH}L/yr")

    print("\n🏗  ERP OPTIONS — FINANCIAL COMPARISON")
    header = f"  {'Option':<42} {'CapEx':>7} {'OpEx/yr':>8} {'Eff Gain':>9} {'Payback':>9} {'5yr NPV':>10} {'IRR':>7} {'Fit':>5}"
    print(header)
    print("  " + "-"*100)

    fin_data = {}
    for name, opt in ERP_OPTIONS.items():
        fin = compute_financials(opt)
        fin_data[name] = fin
        short = name.split(":")[1].strip()
        pb = f"{fin['payback_years']}yr" if fin["payback_years"] else "5yr+"
        print(f"  {short:<42} ₹{opt['capex_lakh']:>4}L  ₹{opt['opex_per_year_lakh']:>4}L/yr"
              f"  {opt['process_efficiency_gain_pct']:>6}%  {pb:>9}  ₹{fin['5yr_npv_lakh']:>6}L"
              f"  {fin['irr_pct']:>5}%  {opt['fit_score']:>5}/10")

    best = max(fin_data, key=lambda n: fin_data[n]["5yr_npv_lakh"])
    best_fin = fin_data[best]
    print(f"\n✅ RECOMMENDATION: {best.split(':')[1].strip()}")
    print(f"   → Highest 5-yr NPV at ₹{best_fin['5yr_npv_lakh']}L | IRR {best_fin['irr_pct']}% | Payback {best_fin['payback_years']}yr")
    print(f"   → Phased rollout: Finance + Inventory (Month 1–4) → HR + Sales (Month 5–8) → Full BI (Month 9+)")
    print(f"   → Projected cycle-time reduction: 35% across all 6 processes in Year 1")
    print("═"*68)

    return fin_data

# ═══════════════════════════════════════════════════════════════════════════════
# 6. VISUALISATIONS
# ═══════════════════════════════════════════════════════════════════════════════
def generate_charts(fin_data: dict):
    NAVY   = "#1B3A6B"
    COLORS = ["#2E86C1", "#E67E22", "#27AE60"]
    BG     = "#F7F9FC"

    fig = plt.figure(figsize=(18, 11), facecolor=BG)
    gs  = GridSpec(2, 3, figure=fig, hspace=0.50, wspace=0.38)

    names_short  = ["MS Dynamics 365", "SAP S/4HANA", "Oracle NetSuite"]
    names_full   = list(ERP_OPTIONS.keys())
    capex        = [ERP_OPTIONS[n]["capex_lakh"] for n in names_full]
    eff_gain     = [ERP_OPTIONS[n]["process_efficiency_gain_pct"] for n in names_full]
    npvs         = [fin_data[n]["5yr_npv_lakh"] for n in names_full]
    irrs         = [fin_data[n]["irr_pct"] for n in names_full]
    paybacks     = [fin_data[n]["payback_years"] or 5 for n in names_full]

    # Chart 1: CapEx comparison
    ax1 = fig.add_subplot(gs[0, 0])
    bars = ax1.bar(names_short, capex, color=COLORS, edgecolor="white", linewidth=1.2)
    ax1.set_title("Implementation CapEx (₹ Lakh)", fontweight="bold", color=NAVY, fontsize=11)
    ax1.set_ylabel("₹ Lakh", color=NAVY, fontsize=9)
    for b, v in zip(bars, capex):
        ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 1, f"₹{v}L",
                 ha="center", fontsize=9, fontweight="bold")
    ax1.set_facecolor(BG)

    # Chart 2: 5yr NPV
    ax2 = fig.add_subplot(gs[0, 1])
    bars2 = ax2.bar(names_short, npvs, color=COLORS, edgecolor="white", linewidth=1.2)
    ax2.axhline(0, color="black", linewidth=0.7)
    ax2.set_title("5-Year NPV (₹ Lakh, 10% discount)", fontweight="bold", color=NAVY, fontsize=11)
    ax2.set_ylabel("₹ Lakh", color=NAVY, fontsize=9)
    for b, v in zip(bars2, npvs):
        ax2.text(b.get_x() + b.get_width()/2, v + 2, f"₹{v}L",
                 ha="center", fontsize=9, fontweight="bold", color="green" if v > 0 else "red")
    ax2.set_facecolor(BG)

    # Chart 3: IRR %
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.barh(names_short, irrs, color=COLORS, edgecolor="white", linewidth=1.2)
    ax3.set_title("Internal Rate of Return (%)", fontweight="bold", color=NAVY, fontsize=11)
    ax3.set_xlabel("IRR %", color=NAVY, fontsize=9)
    ax3.axvline(10, color="red", linestyle="--", linewidth=1, alpha=0.7, label="WACC 10%")
    ax3.legend(fontsize=8)
    for i, v in enumerate(irrs):
        ax3.text(v + 0.5, i, f"{v}%", va="center", fontsize=9, fontweight="bold")
    ax3.set_facecolor(BG)

    # Chart 4: Cumulative cashflow
    ax4 = fig.add_subplot(gs[1, :2])
    years = list(range(6))
    for i, (name, opt) in enumerate(ERP_OPTIONS.items()):
        fin    = fin_data[name]
        capex_ = opt["capex_lakh"]
        anb    = fin["annual_net_lakh"]
        cum    = [-capex_] + [round(-capex_ + anb * y, 1) for y in range(1, 6)]
        label  = names_short[i]
        ax4.plot(years, cum, marker="o", markersize=5, label=label,
                 color=COLORS[i], linewidth=2.2)
    ax4.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
    ax4.set_title("Cumulative Net Benefit Over 5 Years (₹ Lakh)", fontweight="bold", color=NAVY, fontsize=11)
    ax4.set_xlabel("Year", color=NAVY, fontsize=9)
    ax4.set_ylabel("₹ Lakh", color=NAVY, fontsize=9)
    ax4.legend(fontsize=9)
    ax4.set_xticks(years)
    ax4.set_facecolor(BG)

    # Chart 5: Process inefficiency costs
    ax5 = fig.add_subplot(gs[1, 2])
    procs  = list(PROCESSES.keys())
    costs  = [PROCESSES[p]["annual_cost_lakh"] for p in procs]
    short_procs = [p.split("&")[0].strip()[:12] for p in procs]
    ax5.barh(short_procs, costs, color=NAVY, alpha=0.8, edgecolor="white")
    ax5.set_title("Annual Process Cost (₹ Lakh)", fontweight="bold", color=NAVY, fontsize=11)
    ax5.set_xlabel("₹ Lakh", color=NAVY, fontsize=9)
    for i, v in enumerate(costs):
        ax5.text(v + 0.3, i, f"₹{v}L", va="center", fontsize=8, fontweight="bold")
    ax5.set_facecolor(BG)

    fig.suptitle(
        f"ERP Cost-Benefit Analysis — {FIRM['name']} | ₹{FIRM['annual_revenue_cr']}Cr Revenue",
        fontsize=14, fontweight="bold", color=NAVY, y=1.01
    )
    plt.savefig("output/erp_roi_analysis.png", dpi=150, bbox_inches="tight", facecolor=BG)
    print("[Chart] Saved → output/erp_roi_analysis.png")
    plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# 7. EXPORT — JSON for Power BI / Tableau
# ═══════════════════════════════════════════════════════════════════════════════
def export_data(fin_data: dict):
    # Process map
    proc_df = pd.DataFrame([
        {"process": k, **{x: v[x] for x in ["cycle_days","error_rate_pct","fte_hours_month","annual_cost_lakh","bottleneck"]}}
        for k, v in PROCESSES.items()
    ])
    proc_df.to_csv("output/process_map.csv", index=False)

    # Financial comparison
    rows = []
    for name, opt in ERP_OPTIONS.items():
        fin = fin_data[name]
        rows.append({"vendor": name.split(":")[1].strip(), **opt, **fin})
    fin_df = pd.DataFrame(rows)
    fin_df.to_csv("output/erp_financial_comparison.csv", index=False)

    # Root causes
    rc_df = pd.DataFrame([
        {"issue": k, "impact_lakh": v["impact_lakh"],
         "root_cause": v["why5"]}
        for k, v in ROOT_CAUSES.items()
    ])
    rc_df.to_csv("output/root_cause_analysis.csv", index=False)

    print("[Export] CSVs saved to output/ — connect Power BI / Tableau for dashboarding.")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    fin_data = print_business_case()
    generate_charts(fin_data)
    export_data(fin_data)
    print("\n[Done] All outputs in /output/")
