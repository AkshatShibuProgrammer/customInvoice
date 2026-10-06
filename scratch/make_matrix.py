import json

# Full calendar dates for the business tour: 10 Aug to 20 Aug 2026
calendar_dates = [
    ('2026-08-10', '10 Aug', 'Mon', 'Travel / Pune Arrival'),
    ('2026-08-11', '11 Aug', 'Tue', 'Pune Office Day 1'),
    ('2026-08-12', '12 Aug', 'Wed', 'Pune Office Day 2'),
    ('2026-08-13', '13 Aug', 'Thu', 'Pune Office Day 3'),
    ('2026-08-14', '14 Aug', 'Fri', 'Pune Office Day 4'),
    ('2026-08-15', '15 Aug', 'Sat', 'Independence Day (Weekend)'),
    ('2026-08-16', '16 Aug', 'Sun', 'Pune Weekend Stay'),
    ('2026-08-17', '17 Aug', 'Mon', 'Pune Office Day 5'),
    ('2026-08-18', '18 Aug', 'Tue', 'Pune Office Day 6'),
    ('2026-08-19', '19 Aug', 'Wed', 'Pune Departure / Return'),
    ('2026-08-20', '20 Aug', 'Thu', 'Nagpur Final Transit Day')
]

# AKSHAT SINHA FOOD LEDGER (Structured by BF, Lunch, Snacks, Dinner)
akshat_food_matrix = {
    '2026-08-10': {
        'bf': {'vendor': 'Royal Mint Restaurant', 'amt': 494.00, 'pdf': '05_10Aug_Nagpur_RoyalMint_Breakfast_494.pdf', 'status': 'Original Tax Invoice', 'note': 'Departure Breakfast (GSTIN-27AKMPG5967E2ZT)'},
        'lunch': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Transit / In-flight'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Complimentary Tea'},
        'dinner': {'vendor': 'The Chinese Katta', 'amt': 288.75, 'pdf': None, 'status': 'Arranged PDF', 'note': 'Pune arrival dinner (Hinjawadi)'}
    },
    '2026-08-11': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel Nivant buffet breakfast included'},
        'lunch': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'TCS SP2 Hinjawadi cafeteria (self)'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Office tea/coffee'},
        'dinner': {'vendor': 'The Chinese Katta', 'amt': 288.75, 'pdf': None, 'status': 'Arranged PDF', 'note': 'Hinjawadi local dinner'}
    },
    '2026-08-12': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel Nivant breakfast'},
        'lunch': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Office cafeteria'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Not claimed'},
        'dinner': {'vendor': 'Roots Corp (Ginger Hotel - Nivant)', 'amt': 282.45, 'pdf': '06_12Aug_Pune_GingerHotel_BuffetDinner_282.pdf', 'status': 'Original POS Scan', 'note': 'Hotel Buffet Dinner (10:02 PM POS Card Slip)'}
    },
    '2026-08-13': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel breakfast'},
        'lunch': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Office cafeteria'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Not claimed'},
        'dinner': {'vendor': 'Roots Corp (Ginger Hotel - Nivant)', 'amt': 564.90, 'pdf': '07_13Aug_Pune_GingerHotel_BuffetDinner_2Covers_565.pdf', 'status': 'Original POS Scan', 'note': 'Ginger Buffet 2 Covers (Akshat + Mayank)'}
    },
    '2026-08-14': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel breakfast'},
        'lunch': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Office cafeteria'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Not claimed'},
        'dinner': {'vendor': 'Roots Corp (Ginger Hotel - Nivant)', 'amt': 282.45, 'pdf': '08_14Aug_Pune_GingerHotel_BuffetDinner_282.pdf', 'status': 'Original POS Scan', 'note': 'Ginger Hotel Buffet Dinner (09:30 PM)'}
    },
    '2026-08-15': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel breakfast'},
        'lunch': {'vendor': 'GharSe - Homestyle Tiffins', 'amt': 388.00, 'pdf': None, 'status': 'Arranged PDF', 'note': 'Independence Day lunch delivery'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Not claimed'},
        'dinner': {'vendor': 'Nawabs of North', 'amt': 202.65, 'pdf': None, 'status': 'Arranged PDF', 'note': 'Independence Day special dinner'}
    },
    '2026-08-16': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel breakfast'},
        'lunch': {'vendor': 'Pizza Hut Hinjewadi', 'amt': 419.00, 'pdf': '09_16Aug_Pune_PizzaHut_Hinjewadi_AkshatSinha_419.pdf', 'status': 'Arranged PDF', 'note': 'Weekend personal lunch bill on file'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Not claimed'},
        'dinner': {'vendor': 'Roots Corp (Ginger Hotel - Nivant)', 'amt': 282.45, 'pdf': '10_16Aug_Pune_GingerHotel_BuffetDinner_282.pdf', 'status': 'Original POS Scan', 'note': 'Ginger Hotel Buffet Dinner'}
    },
    '2026-08-17': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel breakfast'},
        'lunch': {'vendor': 'WOW! Momo Hinjawadi', 'amt': 388.48, 'pdf': None, 'status': 'Arranged PDF', 'note': 'TCS SP2 Hinjawadi office lunch delivery'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Not claimed'},
        'dinner': {'vendor': 'Roots Corp (Ginger Hotel - Nivant)', 'amt': 282.45, 'pdf': '11_17Aug_Pune_GingerHotel_BuffetDinner_282.pdf', 'status': 'Original POS Scan', 'note': 'Ginger Hotel Buffet Dinner (10:35 PM)'}
    },
    '2026-08-18': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel breakfast'},
        'lunch': {'vendor': 'WOW! Momo Hinjawadi', 'amt': 388.00, 'pdf': '12_18Aug_Pune_Zomato_WowMomo_AkshatSinha_388.pdf', 'status': 'Arranged PDF', 'note': 'Office lunch invoice on file'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Not claimed'},
        'dinner': {'vendor': 'The Chinese Katta', 'amt': 288.75, 'pdf': None, 'status': 'Arranged PDF', 'note': 'Pune farewell dinner'}
    },
    '2026-08-19': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel breakfast check-out'},
        'lunch': {'vendor': 'Royal Mint Restaurant', 'amt': 499.00, 'pdf': '13_19Aug_Nagpur_RoyalMint_Lunch_499.pdf', 'status': 'Original Scan', 'note': 'Nagpur arrival lunch (Table: 12)'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Not claimed'},
        'dinner': {'vendor': 'Royal Mint Restaurant', 'amt': 693.00, 'pdf': '14_19Aug_Nagpur_RoyalMint_Dinner_693.pdf', 'status': 'Original Scan', 'note': 'Nagpur arrival dinner (Table: 18)'}
    },
    '2026-08-20': {
        'bf': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Home breakfast'},
        'lunch': {'vendor': 'Royal Mint Restaurant', 'amt': 719.00, 'pdf': '15_20Aug_Nagpur_RoyalMint_Lunch_719.pdf', 'status': 'Original Scan', 'note': 'Nagpur office day lunch (Table: 15)'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Not claimed'},
        'dinner': {'vendor': 'Royal Mint Restaurant', 'amt': 478.00, 'pdf': '16_20Aug_Nagpur_RoyalMint_Dinner_478.pdf', 'status': 'Original Scan', 'note': 'Nagpur departure dinner (Table: 09)'}
    }
}

# MAYANK SIKARWAR FOOD LEDGER
mayank_food_matrix = {
    '2026-08-10': {
        'bf': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Home breakfast before Lucknow airport'},
        'lunch': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'In-flight / Transit'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Airport tea/coffee'},
        'dinner': {'vendor': 'Hotel Nivant (Roots Corp)', 'amt': 282.45, 'pdf': None, 'status': 'Original Tax Invoice', 'note': 'Arrival night buffet dinner'}
    },
    '2026-08-11': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel buffet breakfast included'},
        'lunch': {'vendor': 'GharSe - Homestyle Tiffins', 'amt': 388.00, 'pdf': '01_11Aug_Pune_Zomato_GharSe_Lunch_Mayank_388.pdf', 'status': 'Arranged PDF', 'note': 'Homestyle lunch delivery'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Office tea'},
        'dinner': {'vendor': 'The Chinese Katta', 'amt': 289.00, 'pdf': '02_11Aug_Pune_Zomato_ChineseKatta_Dinner_Mayank_289.pdf', 'status': 'Arranged PDF', 'note': 'Hinjawadi dinner'}
    },
    '2026-08-12': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel breakfast'},
        'lunch': {'vendor': 'WOW! Momo Hinjawadi', 'amt': 388.00, 'pdf': '03_12Aug_Pune_Zomato_WowMomo_Lunch_Mayank_388.pdf', 'status': 'Arranged PDF', 'note': 'Office lunch'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Not claimed'},
        'dinner': {'vendor': 'Hotel Nivant (Roots Corp)', 'amt': 564.90, 'pdf': None, 'status': 'Original Tax Invoice', 'note': 'Dinner buffet (Shared/2 Covers bill)'}
    },
    '2026-08-13': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel breakfast'},
        'lunch': {'vendor': 'GharSe - Homestyle Tiffins', 'amt': 388.00, 'pdf': '05_13Aug_Pune_Zomato_GharSe_Lunch_Mayank_388.pdf', 'status': 'Arranged PDF', 'note': 'Homestyle lunch delivery'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Not claimed'},
        'dinner': {'vendor': 'Hotel Nivant (Roots Corp)', 'amt': 282.45, 'pdf': None, 'status': 'Original Tax Invoice', 'note': 'Hotel buffet dinner'}
    },
    '2026-08-14': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel breakfast'},
        'lunch': {'vendor': 'WOW! Momo Hinjawadi', 'amt': 388.00, 'pdf': '07_14Aug_Pune_Zomato_WowMomo_Lunch_Mayank_388.pdf', 'status': 'Arranged PDF', 'note': 'Office lunch'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Not claimed'},
        'dinner': {'vendor': 'Hotel Nivant (Roots Corp)', 'amt': 282.45, 'pdf': None, 'status': 'Original Tax Invoice', 'note': 'Hotel buffet dinner'}
    },
    '2026-08-15': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel breakfast'},
        'lunch': {'vendor': 'Nawabs of North', 'amt': 388.00, 'pdf': '09_15Aug_Pune_Zomato_NawabsOfNorth_Lunch_Mayank_203.pdf', 'status': 'Arranged PDF', 'note': 'Independence Day lunch meal'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Not claimed'},
        'dinner': {'vendor': 'GharSe - Homestyle Tiffins', 'amt': 388.00, 'pdf': '10_15Aug_Pune_Zomato_GharSe_Dinner_Mayank_388.pdf', 'status': 'Arranged PDF', 'note': 'Independence Day dinner'}
    },
    '2026-08-16': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel breakfast'},
        'lunch': {'vendor': 'Pizza Hut Hinjewadi', 'amt': 419.00, 'pdf': '11_16Aug_Pune_PizzaHut_Hinjewadi_Lunch_Mayank_419.pdf', 'status': 'Arranged PDF', 'note': 'Weekend lunch on file'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Not claimed'},
        'dinner': {'vendor': 'Hotel Nivant (Roots Corp)', 'amt': 282.45, 'pdf': None, 'status': 'Original Tax Invoice', 'note': 'Hotel buffet dinner'}
    },
    '2026-08-17': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel breakfast'},
        'lunch': {'vendor': 'WOW! Momo Hinjawadi', 'amt': 388.00, 'pdf': '13_17Aug_Pune_Zomato_WowMomo_Lunch_Mayank_388.pdf', 'status': 'Arranged PDF', 'note': 'Office lunch'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Not claimed'},
        'dinner': {'vendor': 'Hotel Nivant (Roots Corp)', 'amt': 282.45, 'pdf': None, 'status': 'Original Tax Invoice', 'note': 'Hotel buffet dinner'}
    },
    '2026-08-18': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel breakfast'},
        'lunch': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Cafeteria / Meeting'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Not claimed'},
        'dinner': {'vendor': 'The Chinese Katta', 'amt': 289.00, 'pdf': '16_18Aug_Pune_Zomato_ChineseKatta_Dinner_Mayank_289.pdf', 'status': 'Arranged PDF', 'note': 'Farewell dinner'}
    },
    '2026-08-19': {
        'bf': {'vendor': 'Complimentary', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Hotel breakfast check-out'},
        'lunch': {'vendor': 'WOW! Momo Hinjawadi', 'amt': 388.00, 'pdf': '17_19Aug_Pune_Zomato_WowMomo_Lunch_Mayank_388.pdf', 'status': 'Arranged PDF', 'note': 'Departure day Hinjawadi lunch'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Airport tea'},
        'dinner': {'vendor': 'Lucknow Local Dining / Travel Meal', 'amt': 1478.00, 'pdf': None, 'status': 'Arranged PDF', 'note': 'Return Travel Meal / Family Dinner on arrival'}
    },
    '2026-08-20': {
        'bf': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'Home in Lucknow (Trip concluded)'},
        'lunch': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'N/A'},
        'snacks': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'N/A'},
        'dinner': {'vendor': 'Not Claimed', 'amt': 0.0, 'pdf': None, 'status': 'N/A', 'note': 'N/A'}
    }
}

# TRANSPORT MATRIX (Structured by Date, From, To, Vehicle/Vendor, Amount, PDF, Status)
akshat_transport = [
    {'date': '2026-08-10', 'day': 'Mon', 'city': 'Nagpur', 'from': 'Nagpur Station & Home', 'to': 'Nagpur Office', 'type': 'Local Transit Cab', 'vendor': 'Local Cab / Auto', 'amt': 300.00, 'pdf': None, 'status': 'Approved Transit', 'notes': 'Station to Office (₹175) + Home to Office (₹125)'},
    {'date': '2026-08-10', 'day': 'Mon', 'city': 'Nagpur', 'from': 'Office', 'to': 'Nagpur Airport (NAG)', 'type': 'Airport Cab', 'vendor': 'Commercial Cab', 'amt': 294.00, 'pdf': None, 'status': 'Approved Transit', 'notes': 'Departure cab to airport'},
    {'date': '2026-08-10', 'day': 'Mon', 'city': 'Pune', 'from': 'Pune Airport (PNQ)', 'to': 'Hotel Nivant Hinjawadi', 'type': 'Airport Cab', 'vendor': 'Ola Prime Plus (White Tour S)', 'amt': 597.00, 'pdf': '05B_10Aug_Pune_Ola_Airport_to_HotelNivant_597.pdf', 'status': 'Original E-Invoice', 'notes': 'Airport arrival cab (31 km, 1h 32m, CRN11167857851)'},
    {'date': '2026-08-19', 'day': 'Wed', 'city': 'Pune', 'from': 'Hotel Nivant Hinjawadi', 'to': 'Pune Airport (PNQ)', 'type': 'Airport Cab', 'vendor': 'Commercial Airport Cab', 'amt': 752.00, 'pdf': None, 'status': 'Approved Transit', 'notes': 'Evening peak airport transit (Option A)'},
    {'date': '2026-08-19', 'day': 'Wed', 'city': 'Nagpur', 'from': 'Nagpur Airport (NAG)', 'to': 'Kalmana Home', 'type': 'Airport Return Cab', 'vendor': 'Ola Prime Sedan (White Dzire)', 'amt': 438.00, 'pdf': '14B_19Aug_Nagpur_Ola_Airport_to_Home_438.pdf', 'status': 'Original E-Invoice', 'notes': 'Airport arrival cab to home (17.3 km, CRN11205677115)'},
    {'date': '2026-08-20', 'day': 'Thu', 'city': 'Nagpur', 'from': 'Kalmana Home', 'to': 'Nagpur Office', 'type': 'Local Transit Cab', 'vendor': 'Local Transit Cab', 'amt': 128.07, 'pdf': None, 'status': 'Approved Transit', 'notes': 'Reconciled local transit commute'},
    {'date': '2026-08-20', 'day': 'Thu', 'city': 'Nagpur', 'from': 'Kalmana Home', 'to': 'Nagpur Railway Station', 'type': 'Station Cab', 'vendor': 'Uber Go Non AC (MH01DR5713)', 'amt': 172.62, 'pdf': '16B_20Aug_Nagpur_Uber_Home_to_Station_173.pdf', 'status': 'Original E-Invoice', 'notes': 'Station drop cab (9.8 km, Receipt_20Aug_191922)'}
]

mayank_transport = [
    {'date': '2026-08-10', 'day': 'Mon', 'city': 'Lucknow', 'from': 'Indira Nagar Home', 'to': 'Lucknow Airport (LKO)', 'type': 'Airport Cab', 'vendor': 'Uber Go (UP32)', 'amt': 432.00, 'pdf': '01_10Aug_Lucknow_Uber_Home_to_Airport_432.pdf', 'status': 'Official Uber PDF', 'notes': 'Home to airport departure cab (24 km)'},
    {'date': '2026-08-10', 'day': 'Mon', 'city': 'Pune', 'from': 'Pune Airport (PNQ)', 'to': 'Hotel Nivant Hinjawadi', 'type': 'Airport Cab', 'vendor': 'Uber Go (MH12)', 'amt': 618.00, 'pdf': '02_10Aug_Pune_Uber_Airport_to_HotelNivant_618.pdf', 'status': 'Official Uber PDF', 'notes': 'Pune airport arrival to Hinjawadi (32 km)'},
    {'date': '2026-08-19', 'day': 'Wed', 'city': 'Pune', 'from': 'Hotel Nivant Hinjawadi', 'to': 'Pune Airport (PNQ)', 'type': 'Airport Cab', 'vendor': 'Uber Go (MH14)', 'amt': 642.00, 'pdf': '03_19Aug_Pune_Uber_HotelNivant_to_Airport_642.pdf', 'status': 'Official Uber PDF', 'notes': 'Hotel Nivant Hinjawadi to Pune airport return cab (32 km)'},
    {'date': '2026-08-19', 'day': 'Wed', 'city': 'Lucknow', 'from': 'Lucknow Airport (LKO)', 'to': 'Indira Nagar Home', 'type': 'Airport Cab', 'vendor': 'Uber Go (UP32)', 'amt': 428.00, 'pdf': '04_19Aug_Lucknow_Uber_Airport_to_Home_428.pdf', 'status': 'Official Uber PDF', 'notes': 'Lucknow airport to home arrival cab (24 km)'}
]

with open('scratch/matrix_dataset.json', 'w', encoding='utf-8') as f:
    json.dump({
        'calendar': calendar_dates,
        'akshat_food': akshat_food_matrix,
        'mayank_food': mayank_food_matrix,
        'akshat_transport': akshat_transport,
        'mayank_transport': mayank_transport
    }, f, indent=2)

print('Successfully exported matrix_dataset.json!')
