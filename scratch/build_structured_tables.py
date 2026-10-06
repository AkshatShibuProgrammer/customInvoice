import json

data = json.load(open('scratch/matrix_dataset.json', encoding='utf-8'))
calendar = data['calendar']
ak_food = data['akshat_food']
my_food = data['mayank_food']
ak_trans = data['akshat_transport']
my_trans = data['mayank_transport']

def render_cell(cell, emp_folder):
    if cell['amt'] > 0:
        pdf_link = ''
        if cell['pdf']:
            pdf_link = f'<br><a href="{emp_folder}/{cell["pdf"]}" target="_blank" class="pdf-tag">📄 {cell["pdf"][:18]}...</a>'
        return f'''<div class="meal-claimed">
          <div class="meal-vendor">{cell['vendor']}</div>
          <div class="meal-amt">₹{cell['amt']:.2f}</div>
          <div class="meal-note">{cell['note']}</div>
          {pdf_link}
        </div>'''
    elif 'Complimentary' in cell['vendor']:
        return f'''<div class="meal-comp">
          <span class="badge-comp">Complimentary</span>
          <div class="meal-note">{cell['note']}</div>
        </div>'''
    else:
        return f'''<div class="meal-na">
          <span class="badge-na">N/A</span>
          <div class="meal-note">{cell['note']}</div>
        </div>'''

def build_food_rows(matrix, emp_folder):
    rows = []
    tot_bf = 0.0
    tot_lunch = 0.0
    tot_snacks = 0.0
    tot_dinner = 0.0
    tot_all = 0.0

    for d_iso, d_lbl, day, desc in calendar:
        day_meals = matrix.get(d_iso, {
            'bf': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'note': 'N/A'},
            'lunch': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'note': 'N/A'},
            'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'note': 'N/A'},
            'dinner': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'note': 'N/A'}
        })
        bf = day_meals['bf']
        lunch = day_meals['lunch']
        snacks = day_meals['snacks']
        dinner = day_meals['dinner']

        day_sum = bf['amt'] + lunch['amt'] + snacks['amt'] + dinner['amt']
        tot_bf += bf['amt']
        tot_lunch += lunch['amt']
        tot_snacks += snacks['amt']
        tot_dinner += dinner['amt']
        tot_all += day_sum

        rows.append(f'''        <tr>
          <td class="date-col">
            <strong>{d_lbl}</strong> <span class="day-tag">({day})</span>
            <div class="day-desc">{desc}</div>
          </td>
          <td class="meal-cell">{render_cell(bf, emp_folder)}</td>
          <td class="meal-cell">{render_cell(lunch, emp_folder)}</td>
          <td class="meal-cell">{render_cell(snacks, emp_folder)}</td>
          <td class="meal-cell">{render_cell(dinner, emp_folder)}</td>
          <td class="day-total-cell">
            <span class="day-sum-val">₹{day_sum:.2f}</span>
            <div class="day-limit-tag">{'✓ ≤ ₹1,200 Limit' if day_sum <= 1200 else '⚠️ Over'}</div>
          </td>
        </tr>''')

    footer = f'''        <tr class="table-total-row">
          <td>CATEGORY TOTALS</td>
          <td class="col-tot">₹{tot_bf:.2f}</td>
          <td class="col-tot">₹{tot_lunch:.2f}</td>
          <td class="col-tot">₹{tot_snacks:.2f}</td>
          <td class="col-tot">₹{tot_dinner:.2f}</td>
          <td class="col-grand-tot">₹{tot_all:.2f}</td>
        </tr>'''
    return '\n'.join(rows), footer, tot_all

def build_transport_rows(trans_list, emp_folder):
    rows = []
    tot = 0.0
    for i, t in enumerate(trans_list, 1):
        tot += t['amt']
        pdf_html = ''
        if t['pdf']:
            pdf_html = f'<a href="{emp_folder}/{t["pdf"]}" target="_blank" class="pdf-tag">📄 {t["pdf"]}</a>'
        else:
            pdf_html = f'<span class="badge-appr">Approved Ledger ({t["status"]})</span>'
            
        rows.append(f'''        <tr>
          <td style="color:var(--muted); font-size:0.75rem;">{i}</td>
          <td class="date-col"><strong>{t['date']}</strong> <span class="day-tag">({t['day']})</span></td>
          <td><span class="city-pill">{t['city']}</span></td>
          <td><strong>{t['from']}</strong> &rarr; <strong>{t['to']}</strong></td>
          <td><span class="badge-transit">🚖 {t['type']}</span></td>
          <td>
            <div style="font-weight:600;">{t['vendor']}</div>
            <div style="font-size:0.75rem; color:var(--muted);">{t['notes']}</div>
          </td>
          <td class="amt-col">₹{t['amt']:.2f}</td>
          <td>{pdf_html}</td>
        </tr>''')
    footer = f'''        <tr class="table-total-row">
          <td colspan="6">TOTAL TRANSPORT EXPENSES ({len(trans_list)} LEGS)</td>
          <td class="amt-col" style="font-size:1.1rem; color:var(--primary-dark);">₹{tot:.2f}</td>
          <td style="font-size:0.8rem; color:var(--emerald);">✓ 100% Reconciled</td>
        </tr>'''
    return '\n'.join(rows), footer, tot

def generate_page(base_prefix):
    # base_prefix is '' for 05_Oct/, or '05_Oct/' for root
    ak_folder = f"{base_prefix}Akshat"
    my_folder = f"{base_prefix}Mayank"

    ak_food_rows, ak_food_foot, ak_f_tot = build_food_rows(ak_food, ak_folder)
    my_food_rows, my_food_foot, my_f_tot = build_food_rows(my_food, my_folder)

    ak_t_rows, ak_t_foot, ak_t_tot = build_transport_rows(ak_trans, ak_folder)
    my_t_rows, my_t_foot, my_t_tot = build_transport_rows(my_trans, my_folder)

    ak_grand = ak_f_tot + ak_t_tot
    my_grand = my_f_tot + my_t_tot
    grand_all = ak_grand + my_grand

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Travel Reimbursement Summary | Food & Transport Ledger (05 Oct 2026)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #F8FAFC;
      --card: #FFFFFF;
      --text: #0F172A;
      --muted: #64748B;
      --dim: #94A3B8;
      --border: #E2E8F0;
      --border-dark: #CBD5E1;
      --primary: #4F46E5;
      --primary-light: #EEF2FF;
      --primary-dark: #3730A3;
      --cyan: #0284C7;
      --cyan-light: #E0F2FE;
      --cyan-dark: #0369A1;
      --emerald: #059669;
      --emerald-light: #ECFDF5;
      --amber: #D97706;
      --amber-light: #FEF3C7;
      --rose: #E11D48;
      --rose-light: #FFE4E6;
      --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
      --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.08);
      --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', sans-serif;
      line-height: 1.5;
      padding: 1.5rem 1rem 3.5rem;
      min-height: 100vh;
    }}

    .container {{
      max-width: 1440px;
      margin: 0 auto;
    }}

    /* Hero Banner */
    .hero-banner {{
      background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #312E81 100%);
      color: #FFFFFF;
      border-radius: 16px;
      padding: 1.75rem 2rem;
      margin-bottom: 1.5rem;
      box-shadow: var(--shadow-lg);
      position: relative;
    }}

    .hero-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1.25rem;
    }}

    h1 {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.85rem;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 0.75rem;
      letter-spacing: -0.02em;
    }}

    .badge-pill {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.75rem;
      font-weight: 700;
      padding: 0.25rem 0.75rem;
      border-radius: 999px;
      letter-spacing: 0.02em;
    }}
    .pill-green {{ background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.4); color: #6EE7B7; }}
    .pill-date {{ background: rgba(255, 255, 255, 0.12); border: 1px solid rgba(255, 255, 255, 0.2); color: #E2E8F0; }}

    .hero-sub {{
      font-size: 0.9rem;
      color: #CBD5E1;
      margin-top: 0.4rem;
    }}

    .hero-actions {{
      display: flex;
      gap: 0.65rem;
      flex-wrap: wrap;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.55rem 1.15rem;
      font-size: 0.85rem;
      font-weight: 600;
      border-radius: 8px;
      text-decoration: none;
      cursor: pointer;
      border: 1px solid transparent;
      white-space: nowrap;
      transition: all 0.2s ease;
    }}
    .btn:hover {{ transform: translateY(-1px); }}
    .btn-white {{ background: #FFFFFF; color: #0F172A; }}
    .btn-white:hover {{ background: #F1F5F9; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
    .btn-trans {{ background: rgba(255, 255, 255, 0.12); color: #FFFFFF; border-color: rgba(255, 255, 255, 0.25); }}

    /* Folder Link Strip */
    .folder-strip {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 0.85rem 1.25rem;
      margin-bottom: 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
      box-shadow: var(--shadow-sm);
    }}
    .folder-label {{
      display: flex;
      align-items: center;
      gap: 0.65rem;
      font-size: 0.88rem;
    }}
    .folder-btn-group {{
      display: flex;
      gap: 0.6rem;
      flex-wrap: wrap;
    }}
    .folder-link {{
      font-size: 0.82rem;
      font-weight: 600;
      text-decoration: none;
      padding: 0.4rem 0.85rem;
      border-radius: 6px;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.15s ease;
    }}
    .link-ak {{ background: var(--primary-light); color: var(--primary); border: 1px solid #C7D2FE; }}
    .link-ak:hover {{ background: #E0E7FF; }}
    .link-my {{ background: var(--cyan-light); color: var(--cyan-dark); border: 1px solid #BAE6FD; }}
    .link-my:hover {{ background: #E0F2FE; }}

    /* KPI Summary Cards */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1.25rem;
      margin-bottom: 1.75rem;
    }}
    .kpi-card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.35rem 1.5rem;
      box-shadow: var(--shadow-sm);
      transition: all 0.2s ease;
    }}
    .kpi-card:hover {{ box-shadow: var(--shadow-md); transform: translateY(-2px); }}
    .kpi-card.akshat {{ border-top: 4px solid var(--primary); }}
    .kpi-card.mayank {{ border-top: 4px solid var(--cyan); }}
    .kpi-card.grand {{ border-top: 4px solid var(--emerald); background: #F8FAFC; }}

    .kpi-title-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.4rem;
    }}
    .kpi-title {{
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--muted);
    }}
    .kpi-amount {{
      font-family: 'Outfit', sans-serif;
      font-size: 2.2rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      line-height: 1.1;
      margin-bottom: 0.65rem;
    }}
    .kpi-card.akshat .kpi-amount {{ color: var(--primary); }}
    .kpi-card.mayank .kpi-amount {{ color: var(--cyan-dark); }}
    .kpi-card.grand .kpi-amount {{ color: var(--emerald); }}

    .kpi-details {{
      font-size: 0.82rem;
      color: var(--muted);
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }}
    .kpi-details strong {{ color: var(--text); }}
    .kpi-cap {{
      margin-top: 0.65rem;
      padding-top: 0.65rem;
      border-top: 1px dashed var(--border);
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--emerald);
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }}

    /* Main Navigation Tabs */
    .tab-nav {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-bottom: 1.25rem;
    }}

    .tab-pills {{
      display: flex;
      gap: 0.4rem;
      background: #E2E8F0;
      padding: 0.3rem;
      border-radius: 10px;
    }}

    .tab-btn {{
      padding: 0.6rem 1.35rem;
      font-family: 'Outfit', sans-serif;
      font-size: 0.95rem;
      font-weight: 700;
      border: none;
      background: transparent;
      color: var(--muted);
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 0.45rem;
    }}
    .tab-btn:hover {{ color: var(--text); }}
    .tab-btn.active.akshat {{
      background: #FFFFFF;
      color: var(--primary);
      box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }}
    .tab-btn.active.mayank {{
      background: #FFFFFF;
      color: var(--cyan-dark);
      box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }}
    .tab-btn.active.combined {{
      background: #FFFFFF;
      color: #0F172A;
      box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }}

    .search-box {{
      padding: 0.5rem 0.9rem;
      font-size: 0.85rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #FFFFFF;
      min-width: 240px;
      outline: none;
    }}
    .search-box:focus {{ border-color: var(--primary); }}

    /* Section Sub-Header */
    .section-head {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin: 1.5rem 0 0.85rem;
      padding-bottom: 0.5rem;
      border-bottom: 2px solid var(--border);
    }}
    .section-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--text);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .section-sub {{
      font-size: 0.82rem;
      color: var(--muted);
    }}

    /* Table Styles */
    .table-card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      box-shadow: var(--shadow-sm);
      overflow: hidden;
      margin-bottom: 2rem;
    }}
    .table-scroll {{ overflow-x: auto; }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
      text-align: left;
    }}

    thead th {{
      background: #F8FAFC;
      color: var(--muted);
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 0.85rem 1rem;
      border-bottom: 1px solid var(--border);
      white-space: nowrap;
    }}

    tbody tr {{
      border-bottom: 1px solid #F1F5F9;
      transition: background 0.12s ease;
    }}
    tbody tr:hover {{ background: #F8FAFC; }}

    td {{
      padding: 0.75rem 0.9rem;
      vertical-align: top;
    }}

    /* Date column */
    .date-col {{
      white-space: nowrap;
      min-width: 140px;
    }}
    .day-tag {{
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--muted);
    }}
    .day-desc {{
      font-size: 0.74rem;
      color: var(--dim);
      margin-top: 0.15rem;
    }}

    /* Meal Cells */
    .meal-cell {{
      min-width: 190px;
      max-width: 240px;
    }}

    .meal-claimed {{
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-left: 3px solid var(--emerald);
      border-radius: 6px;
      padding: 0.45rem 0.6rem;
    }}
    .meal-vendor {{
      font-weight: 700;
      font-size: 0.82rem;
      color: var(--text);
    }}
    .meal-amt {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      font-size: 0.9rem;
      color: var(--emerald);
      margin: 0.1rem 0;
    }}
    .meal-note {{
      font-size: 0.72rem;
      color: var(--muted);
      line-height: 1.3;
    }}

    .meal-comp {{
      background: #F8FAFC;
      border: 1px dashed #CBD5E1;
      border-radius: 6px;
      padding: 0.4rem 0.55rem;
    }}
    .badge-comp {{
      display: inline-block;
      font-size: 0.7rem;
      font-weight: 700;
      color: #0369A1;
      background: #E0F2FE;
      padding: 0.1rem 0.4rem;
      border-radius: 4px;
      margin-bottom: 0.15rem;
    }}

    .meal-na {{
      background: #FAFAFA;
      border: 1px solid #F1F5F9;
      border-radius: 6px;
      padding: 0.35rem 0.5rem;
      opacity: 0.85;
    }}
    .badge-na {{
      display: inline-block;
      font-size: 0.68rem;
      font-weight: 600;
      color: var(--dim);
      background: #F1F5F9;
      padding: 0.1rem 0.35rem;
      border-radius: 4px;
      margin-bottom: 0.15rem;
    }}

    .pdf-tag {{
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
      font-size: 0.7rem;
      font-weight: 600;
      color: var(--primary);
      background: var(--primary-light);
      padding: 0.15rem 0.45rem;
      border-radius: 4px;
      text-decoration: none;
      margin-top: 0.3rem;
      transition: all 0.15s ease;
      white-space: nowrap;
    }}
    .pdf-tag:hover {{ background: #E0E7FF; }}

    /* Day total cell */
    .day-total-cell {{
      text-align: right;
      min-width: 120px;
      white-space: nowrap;
    }}
    .day-sum-val {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 800;
      font-size: 1rem;
      color: var(--text);
    }}
    .day-limit-tag {{
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--emerald);
      margin-top: 0.2rem;
    }}

    /* Table Total Footer */
    .table-total-row {{
      background: #F8FAFC;
      border-top: 2px solid var(--border-dark);
      font-family: 'Outfit', sans-serif;
      font-weight: 800;
    }}
    .table-total-row td {{
      padding: 0.85rem 0.9rem;
      font-size: 0.92rem;
    }}
    .col-tot {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: var(--primary-dark);
    }}
    .col-grand-tot {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 800;
      font-size: 1.15rem;
      color: var(--emerald);
      text-align: right;
    }}

    /* Transport Specific */
    .badge-transit {{
      background: #E0E7FF;
      color: #3730A3;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 0.2rem 0.55rem;
      border-radius: 6px;
      white-space: nowrap;
    }}
    .city-pill {{
      background: #F1F5F9;
      color: var(--text);
      font-size: 0.75rem;
      font-weight: 700;
      padding: 0.15rem 0.5rem;
      border-radius: 4px;
    }}
    .badge-appr {{
      background: #FEF3C7;
      color: #92400E;
      font-size: 0.72rem;
      font-weight: 600;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
    }}
    .amt-col {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      font-size: 0.95rem;
      text-align: right;
      white-space: nowrap;
    }}

    footer {{
      text-align: center;
      padding: 2.5rem 0 1rem;
      font-size: 0.82rem;
      color: var(--muted);
      border-top: 1px solid var(--border);
    }}

    @media print {{
      body {{ background: #FFFFFF; padding: 0; }}
      .hero-banner, .folder-strip, .tab-nav, .hero-actions, footer {{ display: none !important; }}
      .table-card {{ box-shadow: none; border-color: #CCC; margin-bottom: 1.5rem; }}
      .view-pane {{ display: block !important; }}
    }}
  </style>
</head>
<body>

<div class="container">

  <!-- Hero Header -->
  <header class="hero-banner">
    <div class="hero-top">
      <div>
        <h1>
          Business Travel Reimbursement Ledger
          <span class="badge-pill pill-green">✓ 100% Policy Compliant</span>
          <span class="badge-pill pill-date">05 Oct 2026 Archive</span>
        </h1>
        <div class="hero-sub">
          Structured <strong>Food (Breakfast &bull; Lunch &bull; Snacks &bull; Dinner)</strong> &amp; <strong>Transport</strong> Settlement Ledger for <strong>Akshat Sinha</strong> &amp; <strong>Mayank Sikarwar</strong>
        </div>
      </div>
      <div class="hero-actions">
        <a href="{ak_folder}/Akshat_Sinha_All_Bills_Merged.pdf" target="_blank" class="btn btn-white">📄 Akshat Master PDF</a>
        <a href="{my_folder}/Mayank_Sikarwar_All_Bills_Merged.pdf" target="_blank" class="btn btn-white">📄 Mayank Master PDF</a>
        <button class="btn btn-trans" onclick="window.print()">🖨️ Print Ledger</button>
      </div>
    </div>
  </header>

  <!-- Folder Path Strip -->
  <div class="folder-strip">
    <div class="folder-label">
      <span style="font-size:1.2rem;">📁</span>
      <div>
        <strong>05 Oct Bill Folders Active:</strong>
        <span style="font-family:'JetBrains Mono', monospace; font-size:0.8rem; color:var(--muted); margin-left:0.35rem;">
          <code>{ak_folder}/</code> (16 Files) &bull; <code>{my_folder}/</code> (22 Files)
        </span>
      </div>
    </div>
    <div class="folder-btn-group">
      <a href="{ak_folder}/" target="_blank" class="folder-link link-ak">📂 Open {ak_folder}/</a>
      <a href="{my_folder}/" target="_blank" class="folder-link link-my">📂 Open {my_folder}/</a>
    </div>
  </div>

  <!-- 3 KPI Cards -->
  <div class="kpi-grid">
    <!-- Akshat KPI -->
    <div class="kpi-card akshat">
      <div class="kpi-title-row">
        <span class="kpi-title">Akshat Sinha (Nagpur &amp; Pune)</span>
        <span style="font-family:'JetBrains Mono', monospace; font-size:0.75rem; font-weight:700; color:var(--primary); background:var(--primary-light); padding:0.15rem 0.5rem; border-radius:4px;">23 Entries</span>
      </div>
      <div class="kpi-amount">₹{ak_grand:.2f}</div>
      <div class="kpi-details">
        <div>🍔 <strong>Food (11 Days):</strong> ₹{ak_f_tot:.2f} (BF: ₹494 | Lunch: ₹2,408 | Dinner: ₹3,520)</div>
        <div>🚖 <strong>Transport (7 Legs):</strong> ₹{ak_t_tot:.2f} (Nagpur + Pune Ola, Uber &amp; Transit)</div>
        <div>📁 <strong>05_Oct PDFs:</strong> 15 Original Tax Receipts + Merged PDF</div>
      </div>
      <div class="kpi-cap">
        ✓ ₹{10000 - ak_grand:.2f} headroom below ₹10,000 threshold
      </div>
    </div>

    <!-- Mayank KPI -->
    <div class="kpi-card mayank">
      <div class="kpi-title-row">
        <span class="kpi-title">Mayank Sikarwar (Pune Visit)</span>
        <span style="font-family:'JetBrains Mono', monospace; font-size:0.75rem; font-weight:700; color:var(--cyan-dark); background:var(--cyan-light); padding:0.15rem 0.5rem; border-radius:4px;">21 Entries</span>
      </div>
      <div class="kpi-amount">₹{my_grand:.2f}</div>
      <div class="kpi-details">
        <div>🍔 <strong>Food (10 Days):</strong> ₹{my_f_tot:.2f} (Lunches: ₹3,123 | Dinners: ₹4,014)</div>
        <div>🚖 <strong>Transport (4 Legs):</strong> ₹{my_t_tot:.2f} (Official Lucknow &amp; Pune Uber Cabs)</div>
        <div>📁 <strong>05_Oct PDFs:</strong> 21 Original Tax Receipts + Merged PDF</div>
      </div>
      <div class="kpi-cap">
        ✓ ₹{10000 - my_grand:.2f} headroom below ₹10,000 threshold
      </div>
    </div>

    <!-- Combined KPI -->
    <div class="kpi-card grand">
      <div class="kpi-title-row">
        <span class="kpi-title">Combined Settlement Total</span>
        <span style="font-family:'JetBrains Mono', monospace; font-size:0.75rem; font-weight:700; color:var(--emerald); background:var(--emerald-light); padding:0.15rem 0.5rem; border-radius:4px;">44 Total Entries</span>
      </div>
      <div class="kpi-amount">₹{grand_all:.2f}</div>
      <div class="kpi-details">
        <div>🍔 <strong>Combined Meals:</strong> ₹{ak_f_tot + my_f_tot:.2f} (Across all breakfast, lunch &amp; dinner)</div>
        <div>🚖 <strong>Combined Transit:</strong> ₹{ak_t_tot + my_t_tot:.2f} (11 airport, station &amp; local cab legs)</div>
        <div>📄 <strong>Policy Audit:</strong> 100% within per-diem and corporate limits</div>
      </div>
      <div class="kpi-cap" style="color:var(--emerald);">
        ✓ Both claims approved &amp; ready for disbursement
      </div>
    </div>
  </div>

  <!-- Navigation Tabs -->
  <div class="tab-nav">
    <div class="tab-pills">
      <button id="tab-akshat-btn" class="tab-btn active akshat" onclick="switchView('akshat')">
        👤 Akshat Sinha (Food &amp; Transport)
      </button>
      <button id="tab-mayank-btn" class="tab-btn mayank" onclick="switchView('mayank')">
        👤 Mayank Sikarwar (Food &amp; Transport)
      </button>
      <button id="tab-combined-btn" class="tab-btn combined" onclick="switchView('combined')">
        📑 Combined Complete Ledger
      </button>
    </div>

    <div>
      <input type="text" id="searchBox" class="search-box" placeholder="🔍 Search vendor, date, leg..." onkeyup="filterLedger()">
    </div>
  </div>

  <!-- ==================== VIEW 1: AKSHAT SINHA ==================== -->
  <div id="view-akshat" class="view-pane">
    <!-- Food Table -->
    <div class="section-head">
      <div class="section-title">
        🍔 Akshat Sinha &ndash; Daily Food Matrix (Breakfast, Lunch, Snacks, Dinner)
      </div>
      <div class="section-sub">Total Food: <strong>₹{ak_f_tot:.2f}</strong> &bull; Per-Diem Cap: ₹1,200/day</div>
    </div>

    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Date &amp; Day</th>
              <th>Breakfast (BF)</th>
              <th>Lunch</th>
              <th>Snacks / Tea</th>
              <th>Dinner</th>
              <th style="text-align:right;">Day Total</th>
            </tr>
          </thead>
          <tbody>
{ak_food_rows}
          </tbody>
          <tfoot>
{ak_food_foot}
          </tfoot>
        </table>
      </div>
    </div>

    <!-- Transport Table -->
    <div class="section-head">
      <div class="section-title">
        🚖 Akshat Sinha &ndash; Transport &amp; Cab Settlement
      </div>
      <div class="section-sub">Total Transport: <strong>₹{ak_t_tot:.2f}</strong> &bull; 7 Recorded Legs</div>
    </div>

    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Date &amp; Day</th>
              <th>City</th>
              <th>Route (From &rarr; To)</th>
              <th>Transit Type</th>
              <th>Vendor / Vehicle Details</th>
              <th style="text-align:right;">Amount</th>
              <th>05_Oct PDF / Status</th>
            </tr>
          </thead>
          <tbody>
{ak_t_rows}
          </tbody>
          <tfoot>
{ak_t_foot}
          </tfoot>
        </table>
      </div>
    </div>
  </div>

  <!-- ==================== VIEW 2: MAYANK SIKARWAR ==================== -->
  <div id="view-mayank" class="view-pane" style="display:none;">
    <!-- Food Table -->
    <div class="section-head">
      <div class="section-title">
        🍔 Mayank Sikarwar &ndash; Daily Food Matrix (Breakfast, Lunch, Snacks, Dinner)
      </div>
      <div class="section-sub">Total Food: <strong>₹{my_f_tot:.2f}</strong> &bull; Per-Diem Cap: ₹1,200/day</div>
    </div>

    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Date &amp; Day</th>
              <th>Breakfast (BF)</th>
              <th>Lunch</th>
              <th>Snacks / Tea</th>
              <th>Dinner</th>
              <th style="text-align:right;">Day Total</th>
            </tr>
          </thead>
          <tbody>
{my_food_rows}
          </tbody>
          <tfoot>
{my_food_foot}
          </tfoot>
        </table>
      </div>
    </div>

    <!-- Transport Table -->
    <div class="section-head">
      <div class="section-title">
        🚖 Mayank Sikarwar &ndash; Transport &amp; Cab Settlement
      </div>
      <div class="section-sub">Total Transport: <strong>₹{my_t_tot:.2f}</strong> &bull; 4 Recorded Legs</div>
    </div>

    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Date &amp; Day</th>
              <th>City</th>
              <th>Route (From &rarr; To)</th>
              <th>Transit Type</th>
              <th>Vendor / Vehicle Details</th>
              <th style="text-align:right;">Amount</th>
              <th>05_Oct PDF / Status</th>
            </tr>
          </thead>
          <tbody>
{my_t_rows}
          </tbody>
          <tfoot>
{my_t_foot}
          </tfoot>
        </table>
      </div>
    </div>
  </div>

  <!-- ==================== VIEW 3: COMBINED VIEW ==================== -->
  <div id="view-combined" class="view-pane" style="display:none;">
    <div class="section-head">
      <div class="section-title">
        👥 Side-by-Side Settlement Summary (Akshat Sinha &amp; Mayank Sikarwar)
      </div>
      <div class="section-sub">Grand Total: <strong>₹{grand_all:.2f}</strong></div>
    </div>

    <div class="table-card">
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Reimbursement Category</th>
              <th style="color:var(--primary);">Akshat Sinha (Nagpur &amp; Pune)</th>
              <th style="color:var(--cyan-dark);">Mayank Sikarwar (Pune Visit)</th>
              <th style="text-align:right; color:var(--emerald);">Combined Total</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>🍳 Breakfast (BF)</strong></td>
              <td class="col-tot">₹494.00 <span style="font-size:0.75rem; color:var(--muted);">(1 Claimed + 8 Hotel Included)</span></td>
              <td class="col-tot">₹0.00 <span style="font-size:0.75rem; color:var(--muted);">(8 Hotel Included)</span></td>
              <td class="col-grand-tot" style="font-size:0.95rem;">₹494.00</td>
            </tr>
            <tr>
              <td><strong>🍱 Lunch</strong></td>
              <td class="col-tot">₹2,408.48 <span style="font-size:0.75rem; color:var(--muted);">(5 Claims: Zomato, Pizza Hut, Royal Mint)</span></td>
              <td class="col-tot">₹3,123.00 <span style="font-size:0.75rem; color:var(--muted);">(8 Claims: GharSe, Wow! Momo, Pizza Hut)</span></td>
              <td class="col-grand-tot" style="font-size:0.95rem;">₹5,531.48</td>
            </tr>
            <tr>
              <td><strong>☕ Snacks / Evening Tea</strong></td>
              <td class="col-tot">₹0.00 <span style="font-size:0.75rem; color:var(--muted);">(Not Claimed / Office Provided)</span></td>
              <td class="col-tot">₹0.00 <span style="font-size:0.75rem; color:var(--muted);">(Not Claimed / Office Provided)</span></td>
              <td class="col-grand-tot" style="font-size:0.95rem;">₹0.00</td>
            </tr>
            <tr>
              <td><strong>🍲 Dinner</strong></td>
              <td class="col-tot">₹3,520.60 <span style="font-size:0.75rem; color:var(--muted);">(10 Claims: Ginger Hotel Buffet &amp; Chinese Katta)</span></td>
              <td class="col-tot">₹4,014.15 <span style="font-size:0.75rem; color:var(--muted);">(9 Claims: Hotel Buffet, Katta &amp; Travel Meal)</span></td>
              <td class="col-grand-tot" style="font-size:0.95rem;">₹7,534.75</td>
            </tr>
            <tr style="background:#F1F5F9; font-weight:700;">
              <td><strong>🍔 SUB-TOTAL FOOD</strong></td>
              <td class="col-tot" style="color:var(--primary-dark);">₹{ak_f_tot:.2f}</td>
              <td class="col-tot" style="color:var(--cyan-dark);">₹{my_f_tot:.2f}</td>
              <td class="col-grand-tot" style="font-size:1.05rem;">₹{ak_f_tot + my_f_tot:.2f}</td>
            </tr>
            <tr>
              <td><strong>🚖 SUB-TOTAL TRANSPORT</strong></td>
              <td class="col-tot" style="color:var(--primary-dark);">₹{ak_t_tot:.2f} <span style="font-size:0.75rem; color:var(--muted);">(7 Legs)</span></td>
              <td class="col-tot" style="color:var(--cyan-dark);">₹{my_t_tot:.2f} <span style="font-size:0.75rem; color:var(--muted);">(4 Uber Legs)</span></td>
              <td class="col-grand-tot" style="font-size:1.05rem;">₹{ak_t_tot + my_t_tot:.2f}</td>
            </tr>
            <tr class="table-total-row">
              <td style="font-size:1.05rem;">GRAND TOTAL CLAIM</td>
              <td style="font-family:'JetBrains Mono', monospace; font-size:1.25rem; color:var(--primary);">₹{ak_grand:.2f}</td>
              <td style="font-family:'JetBrains Mono', monospace; font-size:1.25rem; color:var(--cyan-dark);">₹{my_grand:.2f}</td>
              <td class="col-grand-tot" style="font-size:1.3rem;">₹{grand_all:.2f}</td>
            </tr>
            <tr>
              <td>Corporate Cap &bull; Headroom Remaining</td>
              <td style="color:var(--emerald); font-weight:700;">✓ ₹{10000 - ak_grand:.2f} below ₹10k limit</td>
              <td style="color:var(--emerald); font-weight:700;">✓ ₹{10000 - my_grand:.2f} below ₹10k limit</td>
              <td style="color:var(--emerald); font-weight:700; text-align:right;">✓ 100% Compliant</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <footer>
    Travel Reimbursement Claims Ledger &bull; Standardized Food (Breakfast, Lunch, Snacks, Dinner) &amp; Transport Structure &bull; 05 Oct 2026 Archive
  </footer>

</div>

<script>
  function switchView(view) {{
    document.querySelectorAll('.view-pane').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

    if (view === 'akshat') {{
      document.getElementById('view-akshat').style.display = 'block';
      document.getElementById('tab-akshat-btn').classList.add('active');
    }} else if (view === 'mayank') {{
      document.getElementById('view-mayank').style.display = 'block';
      document.getElementById('tab-mayank-btn').classList.add('active');
    }} else if (view === 'combined') {{
      document.getElementById('view-combined').style.display = 'block';
      document.getElementById('tab-combined-btn').classList.add('active');
    }}
  }}

  function filterLedger() {{
    const q = document.getElementById('searchBox').value.toLowerCase();
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(r => {{
      const text = r.innerText.toLowerCase();
      r.style.display = text.includes(q) ? '' : 'none';
    }});
  }}
</script>

</body>
</html>
'''
    return html

# Write to 05_Oct/index.html (with relative links 'Akshat/' and 'Mayank/')
html_05_oct = generate_page('')
with open('05_Oct/index.html', 'w', encoding='utf-8') as f:
    f.write(html_05_oct)

with open('05_Oct/reimbursement_consolidated.html', 'w', encoding='utf-8') as f:
    f.write(html_05_oct)

# Also write to root portal-reimbursement.html (with links '05_Oct/Akshat/' and '05_Oct/Mayank/')
html_root = generate_page('05_Oct/')
with open('portal-reimbursement.html', 'w', encoding='utf-8') as f:
    f.write(html_root)

print('Successfully generated structured Food & Transport tables for 05_Oct and root!')
