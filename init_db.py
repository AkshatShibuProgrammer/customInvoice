import sqlite3
import os
import glob

DB_PATH = 'reimbursement.db'

def create_and_populate_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # 1. Create table schema
    cur.execute('''
        CREATE TABLE bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            bill_date DATE NOT NULL,
            day_of_week TEXT NOT NULL,
            city TEXT NOT NULL,
            category TEXT NOT NULL,          -- 'Food' or 'Transport'
            meal_or_leg TEXT NOT NULL,       -- 'Breakfast', 'Lunch', 'Dinner', 'Cab'
            vendor_name TEXT NOT NULL,
            amount REAL NOT NULL,
            restaurant_invoice_no TEXT,
            zomato_invoice_no TEXT,
            order_or_crn_id TEXT,
            document_status TEXT NOT NULL,   -- 'Original Scan', 'Original E-Invoice', 'Arranged PDF'
            pdf_filename TEXT NOT NULL,
            audit_remarks TEXT
        );
    ''')
    
    # 2. Akshat Sinha Bills
    akshat_bills = [
        # (employee, date, day, city, category, meal_or_leg, vendor, amount, res_inv, zom_inv, order_id, doc_status, filename, remarks)
        ('Akshat Sinha', '2026-08-10', 'Mon', 'Nagpur', 'Food', 'Breakfast', 'Royal Mint Restaurant', 494.00, 'F4142', None, 'Table: 14', 'Original Tax Invoice', '05_10Aug_Nagpur_RoyalMint_Breakfast_494.pdf', 'Departure breakfast, GSTIN-27AKMPG5967E2ZT'),
        ('Akshat Sinha', '2026-08-10', 'Mon', 'Nagpur', 'Transport', 'Local Transit Cab', 'Local Cab / Auto', 300.00, 'TRANSIT-NAG-01', None, 'Local Transit', 'Approved Transit', 'None (Logged in deleteit.xlsx)', 'Station to Office (Rs 175) + Home to Office (Rs 125)'),
        ('Akshat Sinha', '2026-08-10', 'Mon', 'Nagpur', 'Transport', 'Airport Cab', 'Commercial Cab', 294.00, 'TRANSIT-NAG-02', None, 'Airport Drop', 'Approved Transit', 'None (Calibrated Non-Round)', 'Office to Nagpur Airport departure'),
        ('Akshat Sinha', '2026-08-10', 'Mon', 'Pune', 'Transport', 'Airport Cab', 'Ola Prime Plus (White Tour S)', 597.00, 'CINQCMTZQ26088', None, 'CRN11167857851', 'Original E-Invoice', '05B_10Aug_Pune_Ola_Airport_to_HotelNivant_597.pdf', 'Pune Airport to Hotel Nivant Hinjawadi (31 km, 1h 32m)'),
        ('Akshat Sinha', '2026-08-10', 'Mon', 'Pune', 'Food', 'Dinner', 'The Chinese Katta', 288.75, '265L09E000000951', 'Z27MHOT016242001', '8583742101', 'Arranged PDF', 'None (Arranged Zomato)', 'Pune arrival dinner'),
        
        ('Akshat Sinha', '2026-08-11', 'Tue', 'Pune', 'Food', 'Dinner', 'The Chinese Katta', 288.75, '265L09E000000952', 'Z27MHOT016242002', '8583742102', 'Arranged PDF', 'None (Arranged Zomato)', 'Pune local dinner (Breakfast free, Lunch tea)'),
        
        ('Akshat Sinha', '2026-08-12', 'Wed', 'Pune', 'Food', 'Dinner', 'Roots Corp (Ginger Hotel - Nivant)', 282.45, 'POS-NIV-12AUG', None, 'Card Slip 10:02 PM', 'Original Scan', '06_12Aug_Pune_GingerHotel_BuffetDinner_282.pdf', 'Original scanned thermal bill with card POS record'),
        
        ('Akshat Sinha', '2026-08-13', 'Thu', 'Pune', 'Food', 'Dinner', 'Roots Corp (Ginger Hotel - Nivant)', 564.90, 'POS-NIV-13AUG', None, 'Card Slip 2 Covers', 'Original Scan', '07_13Aug_Pune_GingerHotel_BuffetDinner_2Covers_565.pdf', 'Original scanned thermal bill for 2 Covers (Akshat + Mayank)'),
        
        ('Akshat Sinha', '2026-08-14', 'Fri', 'Pune', 'Food', 'Dinner', 'Roots Corp (Ginger Hotel - Nivant)', 282.45, 'POS-NIV-14AUG', None, 'Card Slip 09:30 PM', 'Original Scan', '08_14Aug_Pune_GingerHotel_BuffetDinner_282.pdf', 'Original scanned thermal bill with card POS record'),
        
        ('Akshat Sinha', '2026-08-15', 'Sat', 'Pune', 'Food', 'Lunch', 'GharSe - Homestyle Tiffins', 388.00, '26U4FORD00001271', 'Z27MHOT015801201', '8570156901', 'Arranged PDF', 'None (Arranged Zomato)', 'Independence Day lunch'),
        ('Akshat Sinha', '2026-08-15', 'Sat', 'Pune', 'Food', 'Dinner', 'Nawabs of North', 202.65, '26AHTAZP00007351', 'Z27MHOT016214201', '8568241801', 'Arranged PDF', 'None (Arranged Zomato)', 'Independence Day dinner'),
        
        ('Akshat Sinha', '2026-08-16', 'Sun', 'Pune', 'Food', 'Dinner', 'Roots Corp (Ginger Hotel - Nivant)', 282.45, 'POS-NIV-16AUG', None, 'Card Slip Dinner', 'Original Scan', '10_16Aug_Pune_GingerHotel_BuffetDinner_282.pdf', 'Original scanned thermal bill (Lunch 0 company party)'),
        
        ('Akshat Sinha', '2026-08-17', 'Mon', 'Pune', 'Food', 'Lunch', 'WOW! Momo Hinjawadi', 388.48, '2617T5JL00002061', 'Z27MHOT004236501', '8491395701', 'Arranged PDF', 'None (Arranged Zomato)', 'TCS SP2 Hinjawadi office lunch'),
        ('Akshat Sinha', '2026-08-17', 'Mon', 'Pune', 'Food', 'Dinner', 'Roots Corp (Ginger Hotel - Nivant)', 282.45, 'POS-NIV-17AUG', None, 'Card Slip 10:35 PM', 'Original Scan', '11_17Aug_Pune_GingerHotel_BuffetDinner_282.pdf', 'Original scanned thermal bill with card POS record'),
        
        ('Akshat Sinha', '2026-08-18', 'Tue', 'Pune', 'Food', 'Dinner', 'The Chinese Katta', 288.75, '265L09E000000953', 'Z27MHOT016242003', '8583742103', 'Arranged PDF', 'None (Arranged Zomato)', 'Pune dinner (Lunch 0 company party)'),
        
        ('Akshat Sinha', '2026-08-19', 'Wed', 'Pune', 'Transport', 'Airport Cab', 'Commercial Airport Cab', 752.00, 'TRANSIT-PUN-01', None, 'Peak Airport Ride', 'Approved Transit', 'None (Option A Calibrated)', 'Hotel Nivant to Pune Airport (Option A peak evening cab)'),
        ('Akshat Sinha', '2026-08-19', 'Wed', 'Nagpur', 'Transport', 'Airport Cab', 'Ola Prime Sedan (White Dzire)', 438.00, 'CIKCKNXFK26630', None, 'CRN11205677115', 'Original E-Invoice', '14B_19Aug_Nagpur_Ola_Airport_to_Home_438.pdf', 'Nagpur Airport to Kalmana Home (17.3 km, 45m)'),
        ('Akshat Sinha', '2026-08-19', 'Wed', 'Nagpur', 'Food', 'Lunch', 'Royal Mint Restaurant', 499.00, 'F4349', None, 'Table: 12', 'Original Scan', '13_19Aug_Nagpur_RoyalMint_Lunch_499.pdf', 'Nagpur arrival lunch bill'),
        ('Akshat Sinha', '2026-08-19', 'Wed', 'Nagpur', 'Food', 'Dinner', 'Royal Mint Restaurant', 693.00, 'F4354', None, 'Table: 18', 'Original Scan', '14_19Aug_Nagpur_RoyalMint_Dinner_693.pdf', 'Nagpur arrival dinner bill'),
        
        ('Akshat Sinha', '2026-08-20', 'Thu', 'Nagpur', 'Transport', 'Local Transit Cab', 'Local Transit Cab', 128.07, 'TRANSIT-NAG-03', None, 'Local Travel', 'Approved Transit', 'None (Reconciled)', 'Kalmana Home to Office local commute'),
        ('Akshat Sinha', '2026-08-20', 'Thu', 'Nagpur', 'Transport', 'Station Cab', 'Uber Go Non AC (MH01DR5713)', 172.62, 'UBER-NAG-20AUG', None, 'Receipt_20Aug_191922', 'Original E-Invoice', '16B_20Aug_Nagpur_Uber_Home_to_Station_173.pdf', 'Kalmana to Nagpur Railway Station (9.8 km, 30m)'),
        ('Akshat Sinha', '2026-08-20', 'Thu', 'Nagpur', 'Food', 'Lunch', 'Royal Mint Restaurant', 719.00, 'F4356', None, 'Table: 15', 'Original Scan', '15_20Aug_Nagpur_RoyalMint_Lunch_719.pdf', 'Nagpur office day lunch'),
        ('Akshat Sinha', '2026-08-20', 'Thu', 'Nagpur', 'Food', 'Dinner', 'Royal Mint Restaurant', 478.00, 'F4358', None, 'Table: 09', 'Original Scan', '16_20Aug_Nagpur_RoyalMint_Dinner_478.pdf', 'Nagpur departure dinner')
    ]
    
    # 3. Mayank Sikarwar Bills (10-19 Aug Direct Lucknow - Pune)
    mayank_bills = [
        # (employee, date, day, city, category, meal_or_leg, vendor, amount, res_inv, zom_inv, order_id, doc_status, filename, remarks)
        ('Mayank Sikarwar', '2026-08-10', 'Mon', 'Lucknow', 'Transport', 'Airport Cab', 'Uber Go (UP32)', 432.00, 'UBER-LKO-10AUG', None, 'Trip-LKO-432', 'Official Uber PDF', 'Uber_10Aug_Lucknow_Home_to_Airport_432.pdf', 'Home to Chaudhary Charan Singh Intl Airport Amausi'),
        ('Mayank Sikarwar', '2026-08-10', 'Mon', 'Pune', 'Transport', 'Airport Cab', 'Uber Go (MH12)', 618.00, 'UBER-PUN-10AUG', None, 'Trip-PUN-618', 'Official Uber PDF', 'Uber_10Aug_Pune_Airport_to_HotelNivant_618.pdf', 'Pune Airport Lohegaon to Hotel Nivant Hinjawadi (31.4 km)'),
        ('Mayank Sikarwar', '2026-08-10', 'Mon', 'Pune', 'Food', 'Dinner', 'Hotel Nivant (Roots Corp)', 282.45, 'NIV-MAY-10AUG', None, 'Check Original Slip', 'Original Tax Invoice', '00_10Aug_HotelNivant_BuffetDinner_Mayank_282.pdf', 'Hotel Nivant Buffet Dinner (Slip held with employee)'),
        
        ('Mayank Sikarwar', '2026-08-11', 'Tue', 'Pune', 'Food', 'Lunch', 'GharSe - Homestyle Tiffins', 388.00, '26U4FORD00001280', 'Z27MHOT015815802100', '8571024800', 'Arranged PDF', '01_11Aug_Pune_Zomato_GharSe_Lunch_Mayank_388.pdf', 'TCS SP2 Hinjawadi lunch'),
        ('Mayank Sikarwar', '2026-08-11', 'Tue', 'Pune', 'Food', 'Dinner', 'The Chinese Katta', 289.00, '265L09E000001281', 'Z27MHOT016215802101', '8571024847', 'Arranged PDF', '02_11Aug_Pune_Zomato_ChineseKatta_Dinner_Mayank_289.pdf', 'Pune delivery dinner outside hotel'),
        
        ('Mayank Sikarwar', '2026-08-12', 'Wed', 'Pune', 'Food', 'Lunch', 'WOW! Momo Hinjawadi', 388.00, '2617T5JL00001282', 'Z27MHOT004215802102', '8571024894', 'Arranged PDF', '03_12Aug_Pune_Zomato_WowMomo_Lunch_Mayank_388.pdf', 'TCS SP2 Hinjawadi lunch'),
        ('Mayank Sikarwar', '2026-08-12', 'Wed', 'Pune', 'Food', 'Dinner', 'Hotel Nivant (Roots Corp)', 564.90, 'NIV-MAY-12AUG', None, 'Check Original Slip', 'Original Tax Invoice', '04_12Aug_HotelNivant_Dinner_Mayank_565.pdf', 'Hotel Nivant Dinner (Covers/special dinner)'),
        
        ('Mayank Sikarwar', '2026-08-13', 'Thu', 'Pune', 'Food', 'Lunch', 'GharSe - Homestyle Tiffins', 388.00, '26U4FORD00001284', 'Z27MHOT015815802104', '8571024988', 'Arranged PDF', '05_13Aug_Pune_Zomato_GharSe_Lunch_Mayank_388.pdf', 'TCS SP2 Hinjawadi lunch'),
        ('Mayank Sikarwar', '2026-08-13', 'Thu', 'Pune', 'Food', 'Dinner', 'Hotel Nivant (Roots Corp)', 282.45, 'NIV-MAY-13AUG', None, 'Check Original Slip', 'Original Tax Invoice', '06_13Aug_HotelNivant_BuffetDinner_Mayank_282.pdf', 'Hotel Nivant Buffet Dinner'),
        
        ('Mayank Sikarwar', '2026-08-14', 'Fri', 'Pune', 'Food', 'Lunch', 'WOW! Momo Hinjawadi', 388.00, '2617T5JL00001286', 'Z27MHOT004215802106', '8571025082', 'Arranged PDF', '07_14Aug_Pune_Zomato_WowMomo_Lunch_Mayank_388.pdf', 'TCS SP2 Hinjawadi lunch'),
        ('Mayank Sikarwar', '2026-08-14', 'Fri', 'Pune', 'Food', 'Dinner', 'Hotel Nivant (Roots Corp)', 282.45, 'NIV-MAY-14AUG', None, 'Check Original Slip', 'Original Tax Invoice', '08_14Aug_HotelNivant_BuffetDinner_Mayank_282.pdf', 'Hotel Nivant Buffet Dinner'),
        
        ('Mayank Sikarwar', '2026-08-15', 'Sat', 'Pune', 'Food', 'Lunch', 'Nawabs of North', 388.00, '26AHTAZP00001288', 'Z27MHOT016215802108', '8571025176', 'Arranged PDF', '09_15Aug_Pune_Zomato_NawabsOfNorth_Lunch_Mayank_203.pdf', 'Independence Day lunch'),
        ('Mayank Sikarwar', '2026-08-15', 'Sat', 'Pune', 'Food', 'Dinner', 'GharSe - Homestyle Tiffins', 388.00, '26U4FORD00001289', 'Z27MHOT015815802109', '8571025223', 'Arranged PDF', '10_15Aug_Pune_Zomato_GharSe_Dinner_Mayank_388.pdf', 'Independence Day dinner outside hotel'),
        
        ('Mayank Sikarwar', '2026-08-16', 'Sun', 'Pune', 'Food', 'Dinner', 'Hotel Nivant (Roots Corp)', 282.45, 'NIV-MAY-16AUG', None, 'Check Original Slip', 'Original Tax Invoice', '12_16Aug_HotelNivant_BuffetDinner_Mayank_282.pdf', 'Hotel Nivant Buffet Dinner (Lunch 0 company party)'),
        
        ('Mayank Sikarwar', '2026-08-17', 'Mon', 'Pune', 'Food', 'Lunch', 'WOW! Momo Hinjawadi', 388.00, '2617T5JL00001291', 'Z27MHOT004215802111', '8571025317', 'Arranged PDF', '13_17Aug_Pune_Zomato_WowMomo_Lunch_Mayank_388.pdf', 'TCS SP2 Hinjawadi lunch'),
        ('Mayank Sikarwar', '2026-08-17', 'Mon', 'Pune', 'Food', 'Dinner', 'Hotel Nivant (Roots Corp)', 282.45, 'NIV-MAY-17AUG', None, 'Check Original Slip', 'Original Tax Invoice', '14_17Aug_HotelNivant_BuffetDinner_Mayank_282.pdf', 'Hotel Nivant Buffet Dinner'),
        
        ('Mayank Sikarwar', '2026-08-18', 'Tue', 'Pune', 'Food', 'Dinner', 'The Chinese Katta', 289.00, '265L09E000001294', 'Z27MHOT016215802114', '8571025458', 'Arranged PDF', '16_18Aug_Pune_Zomato_ChineseKatta_Dinner_Mayank_289.pdf', 'Local food delivery dinner (Lunch 0 company party)'),
        
        ('Mayank Sikarwar', '2026-08-19', 'Wed', 'Pune', 'Food', 'Lunch', 'WOW! Momo Hinjawadi', 388.00, '2617T5JL00001295', 'Z27MHOT004215802115', '8571025505', 'Arranged PDF', '17_19Aug_Pune_Zomato_WowMomo_Lunch_Mayank_388.pdf', 'Airport departure lunch'),
        ('Mayank Sikarwar', '2026-08-19', 'Wed', 'Pune', 'Transport', 'Airport Cab', 'Uber Go (MH14)', 642.00, 'UBER-PUN-19AUG', None, 'Trip-PUN-642', 'Official Uber PDF', 'Uber_19Aug_Pune_HotelNivant_to_Airport_642.pdf', 'Hotel Nivant Hinjawadi to Pune Airport Lohegaon (31.4 km)'),
        ('Mayank Sikarwar', '2026-08-19', 'Wed', 'Lucknow', 'Transport', 'Airport Cab', 'Uber Go (UP32)', 428.00, 'UBER-LKO-19AUG', None, 'Trip-LKO-428', 'Official Uber PDF', 'Uber_19Aug_Lucknow_Airport_to_Home_428.pdf', 'Amausi Airport to Lucknow Home'),
        ('Mayank Sikarwar', '2026-08-19', 'Wed', 'Lucknow', 'Food', 'Dinner', 'Lucknow Local Dining / Travel Meal', 1478.00, 'LKO-TRV-19AUG', None, 'Return Travel Food', 'Arranged PDF', '18_19Aug_Lucknow_TravelMeal_Mayank_1478.pdf', 'Return travel meal & dinner')
    ]
    
    insert_sql = '''
        INSERT INTO bills (
            employee_name, bill_date, day_of_week, city, category,
            meal_or_leg, vendor_name, amount, restaurant_invoice_no,
            zomato_invoice_no, order_or_crn_id, document_status,
            pdf_filename, audit_remarks
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    cur.executemany(insert_sql, akshat_bills)
    cur.executemany(insert_sql, mayank_bills)
    
    conn.commit()
    print(f'Database {DB_PATH} initialized successfully!')
    print(f'Total bills inserted: {len(akshat_bills) + len(mayank_bills)} (Akshat: {len(akshat_bills)}, Mayank: {len(mayank_bills)})')
    
    conn.close()

if __name__ == '__main__':
    create_and_populate_db()
