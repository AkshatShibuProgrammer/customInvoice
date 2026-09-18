import sqlite3
import sys

DB_PATH = 'reimbursement.db'

def run_query(title, sql, params=()):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    
    print(f"\n================================================================================")
    print(f"[*] {title}")
    print(f"================================================================================")
    
    # calculate column widths
    widths = [len(c) for c in cols]
    for r in rows:
        for i, val in enumerate(r):
            s = f"{val:.2f}" if isinstance(val, float) else str(val or '')
            widths[i] = max(widths[i], len(s))
            
    header_str = " | ".join(f"{cols[i]:<{widths[i]}}" for i in range(len(cols)))
    sep_str = "-+-".join("-" * widths[i] for i in range(len(cols)))
    print(header_str)
    print(sep_str)
    
    for r in rows:
        row_str = " | ".join(f"{r[i]:<{widths[i]}}" if not isinstance(r[i], float) else f"{r[i]:>{widths[i]}.2f}" for i in range(len(r)))
        print(row_str)
        
    print(f"Total records returned: {len(rows)}")
    conn.close()

def main():
    # 1. Total overview by employee & category
    run_query(
        "SUMMARY BY EMPLOYEE AND EXPENSE CATEGORY",
        '''
        SELECT 
            employee_name,
            category,
            COUNT(*) AS total_bills,
            SUM(amount) AS subtotal
        FROM bills
        GROUP BY employee_name, category
        UNION ALL
        SELECT 
            employee_name,
            '=== GRAND TOTAL ===' AS category,
            COUNT(*) AS total_bills,
            SUM(amount) AS subtotal
        FROM bills
        GROUP BY employee_name
        ORDER BY employee_name, subtotal ASC;
        '''
    )

    # 2. Check for ANY duplicate invoice numbers
    run_query(
        "AUDIT CHECK: DUPLICATE RESTAURANT INVOICE NUMBERS",
        '''
        SELECT 
            restaurant_invoice_no,
            COUNT(*) as frequency,
            GROUP_CONCAT(employee_name || ' (' || bill_date || ')') as occurrences
        FROM bills
        WHERE restaurant_invoice_no IS NOT NULL 
          AND restaurant_invoice_no NOT LIKE 'TRANSIT%'
          AND restaurant_invoice_no NOT LIKE 'POS-NIV%'
          AND restaurant_invoice_no NOT LIKE 'NIV-MAY%'
        GROUP BY restaurant_invoice_no
        HAVING COUNT(*) > 1;
        '''
    )

    # 3. Check for ANY duplicate Zomato platform invoice numbers
    run_query(
        "AUDIT CHECK: DUPLICATE ZOMATO PLATFORM INVOICE NUMBERS",
        '''
        SELECT 
            zomato_invoice_no,
            COUNT(*) as frequency,
            GROUP_CONCAT(employee_name || ' (' || bill_date || ')') as occurrences
        FROM bills
        WHERE zomato_invoice_no IS NOT NULL
        GROUP BY zomato_invoice_no
        HAVING COUNT(*) > 1;
        '''
    )

    # 4. Check for ANY duplicate Order IDs
    run_query(
        "AUDIT CHECK: DUPLICATE ORDER / CRN / TRIP IDENTIFIERS",
        '''
        SELECT 
            order_or_crn_id,
            COUNT(*) as frequency,
            GROUP_CONCAT(employee_name || ' (' || bill_date || ')') as occurrences
        FROM bills
        WHERE order_or_crn_id IS NOT NULL
          AND order_or_crn_id NOT LIKE 'Table%'
          AND order_or_crn_id NOT LIKE 'Card Slip%'
          AND order_or_crn_id NOT LIKE 'Check Original%'
          AND order_or_crn_id NOT LIKE 'Local Transit%'
          AND order_or_crn_id NOT LIKE 'Airport Drop%'
          AND order_or_crn_id NOT LIKE 'Peak Airport%'
          AND order_or_crn_id NOT LIKE 'Local Travel%'
          AND order_or_crn_id NOT LIKE 'Return Travel%'
        GROUP BY order_or_crn_id
        HAVING COUNT(*) > 1;
        '''
    )

    # 5. Day-wise Food Totals (Ceiling cap check <= Rs 1,200/day during normal city stay)
    run_query(
        "DAY-WISE FOOD EXPENSE & CAP ANALYSIS",
        '''
        SELECT 
            employee_name,
            bill_date,
            day_of_week,
            city,
            COUNT(*) as food_bills_count,
            SUM(amount) as day_food_total,
            CASE 
                WHEN bill_date = '2026-08-19' AND employee_name = 'Mayank Sikarwar' THEN 'Return Travel Day (Allowed)'
                WHEN SUM(amount) <= 1200 THEN 'PASS (<= Rs 1,200)'
                ELSE 'EXCEEDS Rs 1,200 Cap'
            END as cap_status
        FROM bills
        WHERE category = 'Food'
        GROUP BY employee_name, bill_date
        ORDER BY employee_name, bill_date;
        '''
    )

    # 6. Hotel Nivant Dinners Check
    run_query(
        "HOTEL NIVANT DINNER RECORDS AUDIT",
        '''
        SELECT 
            employee_name,
            bill_date,
            day_of_week,
            vendor_name,
            amount,
            restaurant_invoice_no,
            audit_remarks
        FROM bills
        WHERE vendor_name LIKE '%Nivant%' OR vendor_name LIKE '%Ginger%'
        ORDER BY bill_date, employee_name;
        '''
    )

    # 7. Airport & Transit Cab Audit
    run_query(
        "TRANSPORT & CAB INVOICE AUDIT",
        '''
        SELECT 
            employee_name,
            bill_date,
            city,
            meal_or_leg as leg_type,
            vendor_name,
            amount,
            restaurant_invoice_no as cab_inv_or_code,
            order_or_crn_id,
            document_status
        FROM bills
        WHERE category = 'Transport'
        ORDER BY bill_date, employee_name;
        '''
    )

if __name__ == '__main__':
    main()
