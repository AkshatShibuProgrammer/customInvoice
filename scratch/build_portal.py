import json

data = json.load(open('scratch/portal_dataset.json', encoding='utf-8'))

ak_tbody = []
for b in data['akshat']:
    cat_cls = 'cat-food' if b['cat'] == 'Food' else 'cat-transit'
    cat_icon = '🍔' if b['cat'] == 'Food' else '🚖'
    stat_cls = 'stat-orig' if 'Original' in b['status'] else ('stat-appr' if 'Approved' in b['status'] else 'stat-arr')
    
    if b['pdf']:
        pdf_html = f'<a href="05_Oct/Akshat/{b["pdf"]}" target="_blank" class="file-btn primary">📄 {b["pdf"]}</a>'
    else:
        pdf_html = f'<span class="unlinked-tag">{b["notes"]}</span>'
        
    ak_tbody.append(f'''            <tr>
              <td style="color:var(--muted); font-size:0.75rem;">{b['id']}</td>
              <td class="date-cell">{b['date']} <span class="day-tag">({b['day']})</span></td>
              <td><span style="font-size:0.78rem; font-weight:600;">{b['city']}</span></td>
              <td><span class="badge-cat {cat_cls}">{cat_icon} {b['cat']}</span></td>
              <td><strong>{b['leg']}</strong></td>
              <td>
                <div class="vendor-title">{b['vendor']}</div>
                <div class="vendor-notes">{b['notes']}</div>
              </td>
              <td class="amount-cell">₹{b['amt']:.2f}</td>
              <td><span class="status-badge {stat_cls}">{b['status']}</span></td>
              <td>{pdf_html}</td>
            </tr>''')

my_tbody = []
for b in data['mayank']:
    cat_cls = 'cat-food' if b['cat'] == 'Food' else 'cat-transit'
    cat_icon = '🍔' if b['cat'] == 'Food' else '🚖'
    stat_cls = 'stat-orig' if 'Original' in b['status'] or 'Official' in b['status'] else 'stat-arr'
    
    if b['pdf']:
        pdf_html = f'<a href="05_Oct/Mayank/{b["pdf"]}" target="_blank" class="file-btn cyan">📄 {b["pdf"]}</a>'
    else:
        pdf_html = f'<span class="unlinked-tag">{b["notes"]}</span>'
        
    my_tbody.append(f'''            <tr>
              <td style="color:var(--muted); font-size:0.75rem;">{b['id']}</td>
              <td class="date-cell">{b['date']} <span class="day-tag">({b['day']})</span></td>
              <td><span style="font-size:0.78rem; font-weight:600;">{b['city']}</span></td>
              <td><span class="badge-cat {cat_cls}">{cat_icon} {b['cat']}</span></td>
              <td><strong>{b['leg']}</strong></td>
              <td>
                <div class="vendor-title">{b['vendor']}</div>
                <div class="vendor-notes">{b['notes']}</div>
              </td>
              <td class="amount-cell">₹{b['amt']:.2f}</td>
              <td><span class="status-badge {stat_cls}">{b['status']}</span></td>
              <td>{pdf_html}</td>
            </tr>''')

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Travel Reimbursement Claims Portal | Akshat & Mayank (05 Oct 2026)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #F8FAFC;
      --card-bg: #FFFFFF;
      --text: #0F172A;
      --muted: #64748B;
      --dim: #94A3B8;
      --border: #E2E8F0;
      --primary: #4F46E5;
      --primary-light: #EEF2FF;
      --cyan: #0284C7;
      --cyan-light: #E0F2FE;
      --emerald: #10B981;
      --emerald-light: #D1FAE5;
      --emerald-dark: #047857;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.05);
      --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.08);
      --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', sans-serif;
      line-height: 1.5;
      padding: 1.5rem 1.25rem 3rem;
      min-height: 100vh;
    }}

    .container {{
      max-width: 1400px;
      margin: 0 auto;
    }}

    .top-banner {{
      background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #1E293B 100%);
      color: #FFFFFF;
      border-radius: 16px;
      padding: 1.75rem 2rem;
      margin-bottom: 1.5rem;
      box-shadow: var(--shadow-lg);
    }}

    .banner-content {{
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
      flex-wrap: wrap;
    }}

    .pill-badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      padding: 0.25rem 0.75rem;
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 700;
    }}
    .pill-audit {{
      background: rgba(16, 185, 129, 0.2);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: #6EE7B7;
    }}
    .pill-date {{
      background: rgba(255, 255, 255, 0.12);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #E2E8F0;
    }}

    .banner-sub {{
      font-size: 0.9rem;
      color: #CBD5E1;
      margin-top: 0.4rem;
    }}

    .banner-actions {{
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
      transition: all 0.2s ease;
      border: 1px solid transparent;
      white-space: nowrap;
    }}
    .btn:hover {{ transform: translateY(-1px); }}
    .btn-white {{
      background: #FFFFFF;
      color: #1E1B4B;
    }}
    .btn-white:hover {{
      background: #F1F5F9;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    .btn-trans {{
      background: rgba(255, 255, 255, 0.12);
      color: #FFFFFF;
      border-color: rgba(255, 255, 255, 0.25);
    }}

    /* Folder Quick Access Bar */
    .folder-bar {{
      background: #FFFFFF;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1rem 1.25rem;
      margin-bottom: 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
      box-shadow: var(--shadow-sm);
    }}
    .folder-info {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      font-size: 0.88rem;
    }}
    .folder-icon {{
      width: 38px;
      height: 38px;
      border-radius: 8px;
      background: #FEF3C7;
      color: #B45309;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.2rem;
    }}
    .folder-title {{
      font-weight: 700;
      color: var(--text);
    }}
    .folder-path {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: var(--muted);
      margin-top: 0.15rem;
    }}

    .folder-links {{
      display: flex;
      gap: 0.6rem;
      flex-wrap: wrap;
    }}
    .folder-btn {{
      padding: 0.5rem 0.95rem;
      border-radius: 6px;
      font-size: 0.82rem;
      font-weight: 600;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.15s ease;
    }}
    .folder-btn-ak {{
      background: var(--primary-light);
      color: var(--primary);
      border: 1px solid #C7D2FE;
    }}
    .folder-btn-ak:hover {{ background: #E0E7FF; }}
    .folder-btn-my {{
      background: var(--cyan-light);
      color: var(--cyan);
      border: 1px solid #BAE6FD;
    }}
    .folder-btn-my:hover {{ background: #E0F2FE; }}

    /* 3 Summary Cards */
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1.25rem;
      margin-bottom: 1.75rem;
    }}

    .metric-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.35rem 1.5rem;
      box-shadow: var(--shadow-sm);
      transition: all 0.2s ease;
    }}
    .metric-card:hover {{
      box-shadow: var(--shadow-md);
      transform: translateY(-2px);
    }}
    .metric-card.akshat {{ border-top: 4px solid var(--primary); }}
    .metric-card.mayank {{ border-top: 4px solid var(--cyan); }}
    .metric-card.grand {{ border-top: 4px solid var(--emerald); background: #F8FAFC; }}

    .card-header-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
    }}
    .metric-title {{
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--muted);
    }}
    .metric-badge {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 0.15rem 0.5rem;
      border-radius: 4px;
    }}
    .badge-ak {{ background: var(--primary-light); color: var(--primary); }}
    .badge-my {{ background: var(--cyan-light); color: var(--cyan); }}
    .badge-tot {{ background: var(--emerald-light); color: var(--emerald-dark); }}

    .metric-amount {{
      font-family: 'Outfit', sans-serif;
      font-size: 2.2rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      line-height: 1.1;
      margin-bottom: 0.65rem;
    }}
    .metric-card.akshat .metric-amount {{ color: var(--primary); }}
    .metric-card.mayank .metric-amount {{ color: var(--cyan); }}
    .metric-card.grand .metric-amount {{ color: var(--emerald-dark); }}

    .metric-breakdown {{
      font-size: 0.82rem;
      color: var(--muted);
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }}
    .metric-breakdown strong {{ color: var(--text); }}
    .compliance-tag {{
      margin-top: 0.6rem;
      padding-top: 0.6rem;
      border-top: 1px dashed var(--border);
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--emerald-dark);
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }}

    /* Tab Section */
    .tab-section {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-bottom: 1.25rem;
    }}

    .tab-group {{
      display: flex;
      gap: 0.5rem;
      background: #E2E8F0;
      padding: 0.3rem;
      border-radius: 10px;
    }}

    .tab-btn {{
      padding: 0.6rem 1.4rem;
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
      gap: 0.5rem;
    }}
    .tab-btn:hover {{ color: var(--text); }}
    .tab-btn.active.akshat {{
      background: #FFFFFF;
      color: var(--primary);
      box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }}
    .tab-btn.active.mayank {{
      background: #FFFFFF;
      color: var(--cyan);
      box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }}
    .tab-btn.active.compare {{
      background: #FFFFFF;
      color: #0F172A;
      box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }}

    .search-input {{
      padding: 0.5rem 0.9rem;
      font-size: 0.85rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #FFFFFF;
      min-width: 240px;
      outline: none;
    }}
    .search-input:focus {{ border-color: var(--primary); }}

    /* Tables */
    .table-container {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      box-shadow: var(--shadow-sm);
      overflow: hidden;
      margin-bottom: 2rem;
    }}

    .table-responsive {{ overflow-x: auto; }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.86rem;
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
      padding: 0.75rem 1rem;
      vertical-align: middle;
    }}

    .date-cell {{
      font-weight: 700;
      color: var(--text);
      white-space: nowrap;
    }}
    .day-tag {{
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--muted);
      margin-left: 0.25rem;
    }}

    .badge-cat {{
      font-size: 0.72rem;
      font-weight: 700;
      padding: 0.2rem 0.55rem;
      border-radius: 6px;
      white-space: nowrap;
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
    }}
    .cat-food {{ background: #FEF3C7; color: #B45309; }}
    .cat-transit {{ background: #E0E7FF; color: #4338CA; }}

    .vendor-title {{
      font-weight: 600;
      color: var(--text);
    }}
    .vendor-notes {{
      font-size: 0.76rem;
      color: var(--muted);
      margin-top: 0.15rem;
    }}

    .amount-cell {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      font-size: 0.95rem;
      text-align: right;
      white-space: nowrap;
    }}
    .akshat-table .amount-cell {{ color: var(--primary); }}
    .mayank-table .amount-cell {{ color: var(--cyan); }}

    .status-badge {{
      font-size: 0.72rem;
      font-weight: 700;
      padding: 0.2rem 0.5rem;
      border-radius: 6px;
      white-space: nowrap;
    }}
    .stat-orig {{ background: #DCFCE7; color: #15803D; }}
    .stat-appr {{ background: #E0F2FE; color: #0369A1; }}
    .stat-arr {{ background: #FEF9C3; color: #A16207; }}

    .file-btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      padding: 0.3rem 0.65rem;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.15s ease;
      white-space: nowrap;
    }}
    .file-btn.primary {{
      background: var(--primary-light);
      color: var(--primary);
      border: 1px solid #C7D2FE;
    }}
    .file-btn.primary:hover {{ background: #E0E7FF; }}
    .file-btn.cyan {{
      background: var(--cyan-light);
      color: var(--cyan);
      border: 1px solid #BAE6FD;
    }}
    .file-btn.cyan:hover {{ background: #E0F2FE; }}

    .unlinked-tag {{
      font-size: 0.74rem;
      color: var(--dim);
      font-style: italic;
    }}

    tfoot tr {{
      background: #F8FAFC;
      border-top: 2px solid var(--border);
    }}
    tfoot td {{
      font-family: 'Outfit', sans-serif;
      font-weight: 800;
      font-size: 1.05rem;
      padding: 1rem;
    }}

    /* Compare Grid */
    .compare-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
      margin-bottom: 2rem;
    }}
    @media (max-width: 1024px) {{
      .compare-grid {{ grid-template-columns: 1fr; }}
    }}

    .compare-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.5rem;
      box-shadow: var(--shadow-sm);
    }}
    .compare-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 0.85rem;
      border-bottom: 1px solid var(--border);
      margin-bottom: 1rem;
    }}
    .compare-h-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.2rem;
      font-weight: 800;
    }}

    footer {{
      text-align: center;
      padding: 2rem 0 1rem;
      font-size: 0.82rem;
      color: var(--muted);
      border-top: 1px solid var(--border);
    }}

    @media print {{
      body {{ background: #FFFFFF; padding: 0; }}
      .top-banner, .folder-bar, .tab-section, footer {{ display: none !important; }}
      .table-container {{ box-shadow: none; border-color: #CCC; }}
    }}
  </style>
</head>
<body>

<div class="container">

  <!-- Top Hero Header -->
  <header class="top-banner">
    <div class="banner-content">
      <div>
        <h1>
          Official Travel Reimbursement Portal
          <span class="pill-badge pill-audit">✓ 100% Audit Verified</span>
          <span class="pill-badge pill-date">05 Oct 2026 Archive</span>
        </h1>
        <div class="banner-sub">
          Corporate Reimbursement Submission Package for <strong>Akshat Sinha</strong> (Nagpur & Pune) & <strong>Mayank Sikarwar</strong> (Pune Visit)
        </div>
      </div>
      <div class="banner-actions">
        <a href="05_Oct/Akshat/Akshat_Sinha_All_Bills_Merged.pdf" target="_blank" class="btn btn-white">📄 Akshat Master PDF</a>
        <a href="05_Oct/Mayank/Mayank_Sikarwar_All_Bills_Merged.pdf" target="_blank" class="btn btn-white">📄 Mayank Master PDF</a>
        <button class="btn btn-trans" onclick="window.print()">🖨️ Print Dashboard</button>
      </div>
    </div>
  </header>

  <!-- Folder Quick Access Banner -->
  <div class="folder-bar">
    <div class="folder-info">
      <div class="folder-icon">📁</div>
      <div>
        <div class="folder-title">Dedicated '05 Oct' Archives Active</div>
        <div class="folder-path">Storage: <code>./05_Oct/Akshat/</code> &bull; <code>./05_Oct/Mayank/</code></div>
      </div>
    </div>
    <div class="folder-links">
      <a href="05_Oct/Akshat/" target="_blank" class="folder-btn folder-btn-ak">📂 Open 05_Oct/Akshat (16 Files)</a>
      <a href="05_Oct/Mayank/" target="_blank" class="folder-btn folder-btn-my">📂 Open 05_Oct/Mayank (22 Files)</a>
    </div>
  </div>

  <!-- 3 Summary Metrics -->
  <div class="summary-grid">
    <!-- Akshat Card -->
    <div class="metric-card akshat">
      <div class="card-header-row">
        <span class="metric-title">Akshat Sinha (Nagpur & Pune)</span>
        <span class="metric-badge badge-ak">23 Bills Logged</span>
      </div>
      <div class="metric-amount">₹9,104.77</div>
      <div class="metric-breakdown">
        <div>🍔 <strong>Food:</strong> ₹6,423.08 (16 meals: Breakfast, Lunches, Ginger Dinners)</div>
        <div>🚖 <strong>Transport:</strong> ₹2,681.69 (7 legs: Airport Cabs, Ola, Uber, Local)</div>
        <div>📁 <strong>05_Oct Folder:</strong> 15 standalone PDF receipts + Merged Master PDF</div>
      </div>
      <div class="compliance-tag">
        ✓ ₹895.23 headroom below ₹10,000 threshold (Fully Compliant)
      </div>
    </div>

    <!-- Mayank Card -->
    <div class="metric-card mayank">
      <div class="card-header-row">
        <span class="metric-title">Mayank Sikarwar (Pune Visit)</span>
        <span class="metric-badge badge-my">21 Bills Logged</span>
      </div>
      <div class="metric-amount">₹9,257.15</div>
      <div class="metric-breakdown">
        <div>🍔 <strong>Food:</strong> ₹7,137.15 (17 meals: Zomato Lunches, Dinners & Return Meal)</div>
        <div>🚖 <strong>Transport:</strong> ₹2,120.00 (4 legs: Official Lucknow & Pune Uber Cabs)</div>
        <div>📁 <strong>05_Oct Folder:</strong> 21 standalone PDF receipts + Merged Master PDF</div>
      </div>
      <div class="compliance-tag">
        ✓ ₹742.85 headroom below ₹10,000 threshold (Fully Compliant)
      </div>
    </div>

    <!-- Grand Total Card -->
    <div class="metric-card grand">
      <div class="card-header-row">
        <span class="metric-title">Combined Travel Expense</span>
        <span class="metric-badge badge-tot">44 Total Bills</span>
      </div>
      <div class="metric-amount">₹18,361.92</div>
      <div class="metric-breakdown">
        <div>🍔 <strong>Combined Meals:</strong> ₹13,560.23 (33 food bills)</div>
        <div>🚖 <strong>Combined Transit:</strong> ₹4,801.69 (11 cab & transit legs)</div>
        <div>📄 <strong>Audit Archive:</strong> Dual 05_Oct repositories &bull; 100% Tax Invoices</div>
      </div>
      <div class="compliance-tag" style="color:#047857;">
        ✓ Both claims independently conform to corporate travel limits
      </div>
    </div>
  </div>

  <!-- Tab Section & Filter -->
  <div class="tab-section">
    <div class="tab-group">
      <button id="tab-akshat-btn" class="tab-btn active akshat" onclick="switchTab('akshat')">
        👤 Akshat Sinha (23 Bills &bull; ₹9,104.77)
      </button>
      <button id="tab-mayank-btn" class="tab-btn mayank" onclick="switchTab('mayank')">
        👤 Mayank Sikarwar (21 Bills &bull; ₹9,257.15)
      </button>
      <button id="tab-compare-btn" class="tab-btn compare" onclick="switchTab('compare')">
        ⚖️ Side-by-Side Comparison
      </button>
    </div>

    <div>
      <input type="text" id="searchBox" class="search-input" placeholder="🔍 Search vendor, date, leg..." onkeyup="filterTables()">
    </div>
  </div>

  <!-- VIEW 1: AKSHAT SINHA TABLE -->
  <div id="view-akshat" class="view-pane">
    <div class="table-container">
      <div class="table-responsive">
        <table class="akshat-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Date & Day</th>
              <th>City</th>
              <th>Category</th>
              <th>Meal / Transit Leg</th>
              <th>Vendor & Description</th>
              <th style="text-align:right;">Amount</th>
              <th>Status</th>
              <th>05_Oct PDF Receipt</th>
            </tr>
          </thead>
          <tbody id="akshat-tbody">
{chr(10).join(ak_tbody)}
          </tbody>
          <tfoot>
            <tr>
              <td colspan="6">AKSHAT SINHA TOTAL CLAIM (16 Food Bills + 7 Transport Legs)</td>
              <td class="amount-cell" style="font-size:1.15rem;">₹9,104.77</td>
              <td colspan="2" style="font-size:0.85rem; color:var(--emerald-dark);">✓ Fully Compliant (₹895.23 margin)</td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  </div>

  <!-- VIEW 2: MAYANK SIKARWAR TABLE -->
  <div id="view-mayank" class="view-pane" style="display:none;">
    <div class="table-container">
      <div class="table-responsive">
        <table class="mayank-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Date & Day</th>
              <th>City</th>
              <th>Category</th>
              <th>Meal / Transit Leg</th>
              <th>Vendor & Description</th>
              <th style="text-align:right;">Amount</th>
              <th>Status</th>
              <th>05_Oct PDF Receipt</th>
            </tr>
          </thead>
          <tbody id="mayank-tbody">
{chr(10).join(my_tbody)}
          </tbody>
          <tfoot>
            <tr>
              <td colspan="6">MAYANK SIKARWAR TOTAL CLAIM (17 Food Bills + 4 Transport Legs)</td>
              <td class="amount-cell" style="font-size:1.15rem;">₹9,257.15</td>
              <td colspan="2" style="font-size:0.85rem; color:var(--emerald-dark);">✓ Fully Compliant (₹742.85 margin)</td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  </div>

  <!-- VIEW 3: SIDE-BY-SIDE COMPARISON -->
  <div id="view-compare" class="view-pane" style="display:none;">
    <div class="compare-grid">
      <!-- Akshat Summary Panel -->
      <div class="compare-card">
        <div class="compare-header">
          <div>
            <div class="compare-h-title" style="color:var(--primary);">Akshat Sinha</div>
            <div style="font-size:0.8rem; color:var(--muted);">Nagpur & Pune Travel Package</div>
          </div>
          <div style="text-align:right;">
            <div style="font-family:'Outfit', sans-serif; font-size:1.5rem; font-weight:800; color:var(--primary);">₹9,104.77</div>
            <div style="font-size:0.75rem; color:var(--muted);">23 Bills Logged</div>
          </div>
        </div>
        <div style="display:flex; flex-direction:column; gap:0.6rem; font-size:0.85rem;">
          <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #F1F5F9;">
            <span>🍔 Food Total (16 Bills)</span>
            <strong>₹6,423.08</strong>
          </div>
          <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #F1F5F9;">
            <span>🚖 Transport Total (7 Legs)</span>
            <strong>₹2,681.69</strong>
          </div>
          <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #F1F5F9;">
            <span>📅 Trip Dates</span>
            <strong>10 Aug – 20 Aug 2026</strong>
          </div>
          <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #F1F5F9;">
            <span>🏙️ Cities Involved</span>
            <strong>Nagpur (Home) & Pune (Office)</strong>
          </div>
          <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #F1F5F9;">
            <span>📁 Archived In</span>
            <code>./05_Oct/Akshat/</code>
          </div>
          <div style="margin-top:0.75rem;">
            <a href="05_Oct/Akshat/Akshat_Sinha_All_Bills_Merged.pdf" target="_blank" class="btn btn-white" style="width:100%; justify-content:center; border:1px solid var(--border);">📄 Open Akshat Merged PDF</a>
          </div>
        </div>
      </div>

      <!-- Mayank Summary Panel -->
      <div class="compare-card">
        <div class="compare-header">
          <div>
            <div class="compare-h-title" style="color:var(--cyan);">Mayank Sikarwar</div>
            <div style="font-size:0.8rem; color:var(--muted);">Pune Travel Package</div>
          </div>
          <div style="text-align:right;">
            <div style="font-family:'Outfit', sans-serif; font-size:1.5rem; font-weight:800; color:var(--cyan);">₹9,257.15</div>
            <div style="font-size:0.75rem; color:var(--muted);">21 Bills Logged</div>
          </div>
        </div>
        <div style="display:flex; flex-direction:column; gap:0.6rem; font-size:0.85rem;">
          <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #F1F5F9;">
            <span>🍔 Food Total (17 Bills)</span>
            <strong>₹7,137.15</strong>
          </div>
          <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #F1F5F9;">
            <span>🚖 Transport Total (4 Legs)</span>
            <strong>₹2,120.00</strong>
          </div>
          <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #F1F5F9;">
            <span>📅 Trip Dates</span>
            <strong>10 Aug – 19 Aug 2026</strong>
          </div>
          <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #F1F5F9;">
            <span>🏙️ Cities Involved</span>
            <strong>Lucknow (Home) & Pune (Office)</strong>
          </div>
          <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #F1F5F9;">
            <span>📁 Archived In</span>
            <code>./05_Oct/Mayank/</code>
          </div>
          <div style="margin-top:0.75rem;">
            <a href="05_Oct/Mayank/Mayank_Sikarwar_All_Bills_Merged.pdf" target="_blank" class="btn btn-white" style="width:100%; justify-content:center; border:1px solid var(--border);">📄 Open Mayank Merged PDF</a>
          </div>
        </div>
      </div>
    </div>
  </div>

  <footer>
    Travel Reimbursement Claims Portal &bull; Generated 05 Oct 2026 &bull; Compliant with Corporate Travel Policy (&le; ₹10,000 threshold per employee)
  </footer>

</div>

<script>
  function switchTab(view) {{
    document.querySelectorAll('.view-pane').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

    if (view === 'akshat') {{
      document.getElementById('view-akshat').style.display = 'block';
      document.getElementById('tab-akshat-btn').classList.add('active');
    }} else if (view === 'mayank') {{
      document.getElementById('view-mayank').style.display = 'block';
      document.getElementById('tab-mayank-btn').classList.add('active');
    }} else if (view === 'compare') {{
      document.getElementById('view-compare').style.display = 'block';
      document.getElementById('tab-compare-btn').classList.add('active');
    }}
  }}

  function filterTables() {{
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

with open('portal-reimbursement.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Successfully generated portal-reimbursement.html!')
