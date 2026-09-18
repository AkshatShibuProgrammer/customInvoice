import os
import pypdf
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

UBER_TRIPS = [
    {
        "filename": "01_10Aug_Lucknow_Uber_Home_to_Airport_432.pdf",
        "date_str": "Monday, August 10, 2026",
        "time_str": "11:42 AM",
        "rider": "Mayank Sikarwar",
        "service": "Uber Go",
        "fare": 432.00,
        "trip_fare": 372.41,
        "cgst": 9.31,
        "sgst": 9.31,
        "airport_fee": 40.97,
        "distance": "16.8 km",
        "duration": "38 min",
        "driver": "MOHD SHAKEEL",
        "plate": "UP32LN4821",
        "pickup": "Aliganj Sector B, Lucknow, Uttar Pradesh 226024",
        "pickup_time": "11:04 AM",
        "dropoff": "Chaudhary Charan Singh International Airport, Amausi, Lucknow",
        "dropoff_time": "11:42 AM"
    },
    {
        "filename": "02_10Aug_Pune_Uber_Airport_to_HotelNivant_618.pdf",
        "date_str": "Monday, August 10, 2026",
        "time_str": "05:48 PM",
        "rider": "Mayank Sikarwar",
        "service": "Uber Go",
        "fare": 618.00,
        "trip_fare": 532.76,
        "cgst": 13.32,
        "sgst": 13.32,
        "airport_fee": 58.60,
        "distance": "31.4 km",
        "duration": "1 h 18 min",
        "driver": "SANTOSH SHINDE",
        "plate": "MH12QW8923",
        "pickup": "Pune International Airport (PNQ), New Airport Rd, Lohegaon, Pune",
        "pickup_time": "04:30 PM",
        "dropoff": "Hotel Nivant Transit Quarters, Hinjawadi Phase 3, Pune 411057",
        "dropoff_time": "05:48 PM"
    },
    {
        "filename": "03_19Aug_Pune_Uber_HotelNivant_to_Airport_642.pdf",
        "date_str": "Wednesday, August 19, 2026",
        "time_str": "06:15 PM",
        "rider": "Mayank Sikarwar",
        "service": "Uber Go",
        "fare": 642.00,
        "trip_fare": 553.45,
        "cgst": 13.84,
        "sgst": 13.84,
        "airport_fee": 60.87,
        "distance": "31.4 km",
        "duration": "1 h 24 min",
        "driver": "RAMESH PAWAR",
        "plate": "MH14EX3159",
        "pickup": "Hotel Nivant Transit Quarters, Hinjawadi Phase 3, Pune 411057",
        "pickup_time": "04:51 PM",
        "dropoff": "Pune International Airport (PNQ), New Airport Rd, Lohegaon, Pune",
        "dropoff_time": "06:15 PM"
    },
    {
        "filename": "04_19Aug_Lucknow_Uber_Airport_to_Home_428.pdf",
        "date_str": "Wednesday, August 19, 2026",
        "time_str": "10:52 PM",
        "rider": "Mayank Sikarwar",
        "service": "Uber Go",
        "fare": 428.00,
        "trip_fare": 368.96,
        "cgst": 9.22,
        "sgst": 9.22,
        "airport_fee": 40.60,
        "distance": "16.8 km",
        "duration": "35 min",
        "driver": "DINESH KUMAR",
        "plate": "UP32KM9012",
        "pickup": "Chaudhary Charan Singh International Airport, Amausi, Lucknow",
        "pickup_time": "10:17 PM",
        "dropoff": "Aliganj Sector B, Lucknow, Uttar Pradesh 226024",
        "dropoff_time": "10:52 PM"
    }
]

def generate_uber_pdf(trip, out_path):
    c = canvas.Canvas(out_path, pagesize=letter)
    w, h = letter

    # Page 1: Official Receipt
    c.setFont("Helvetica-Bold", 26)
    c.drawString(45, h - 55, "Uber")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#555555"))
    c.drawRightString(w - 45, h - 55, trip["date_str"])

    c.setFont("Helvetica-Bold", 19)
    c.setFillColor(colors.black)
    c.drawString(45, h - 100, f"Here's your receipt for your ride, {trip['rider'].split()[0]}")

    c.setFont("Helvetica", 11)
    c.setFillColor(colors.HexColor("#555555"))
    c.drawString(45, h - 120, "We hope you enjoyed your ride this morning.")

    # Fare box
    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.setFillColor(colors.HexColor("#F9FAFB"))
    c.rect(45, h - 185, w - 90, 50, fill=True, stroke=True)

    c.setFont("Helvetica", 12)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawString(60, h - 165, "Total")

    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(colors.black)
    c.drawRightString(w - 60, h - 170, f"INR {trip['fare']:.2f}")

    # Fare Breakdown
    y = h - 220
    c.setFont("Helvetica-Bold", 13)
    c.drawString(45, y, "Fare Breakdown")
    y -= 25

    breakdown = [
        ("Trip Fare", f"INR {trip['trip_fare']:.2f}"),
        ("Central Goods and Services Tax (CGST 2.5%)", f"INR {trip['cgst']:.2f}"),
        ("State Goods and Services Tax (SGST 2.5%)", f"INR {trip['sgst']:.2f}"),
        ("Airport Access / Pickup Fee", f"INR {trip['airport_fee']:.2f}"),
        ("Rounding", "INR 0.00")
    ]

    c.setFont("Helvetica", 10.5)
    c.setFillColor(colors.HexColor("#333333"))
    for item, amt in breakdown:
        c.drawString(45, y, item)
        c.drawRightString(w - 45, y, amt)
        y -= 20

    c.setStrokeColor(colors.HexColor("#D1D5DB"))
    c.setLineWidth(1)
    c.line(45, y + 8, w - 45, y + 8)

    y -= 10
    c.setFont("Helvetica-Bold", 11)
    c.drawString(45, y, "Subtotal")
    c.drawRightString(w - 45, y, f"INR {trip['fare']:.2f}")

    y -= 35
    c.setFont("Helvetica-Bold", 13)
    c.drawString(45, y, "Payments")
    y -= 22
    c.setFont("Helvetica", 10.5)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawString(45, y, "Cash Payment")
    c.drawRightString(w - 45, y, f"INR {trip['fare']:.2f}")
    y -= 16
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor("#757575"))
    c.drawString(45, y, f"{trip['date_str']} {trip['time_str']}")

    y -= 35
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#888888"))
    c.drawString(45, y, "A digital copy of this receipt is also stored in your Uber rider account for personal and business records.")
    c.drawString(45, y - 12, "Fares include applicable central and state goods and services taxes. Uber India Technology Private Limited.")

    # Driver & Vehicle
    y -= 45
    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.rect(45, y - 50, w - 90, 60, fill=True, stroke=True)

    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.black)
    c.drawString(60, y - 12, f"You rode with {trip['driver']}")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#555555"))
    c.drawString(60, y - 28, f"{trip['service']} • License Plate: {trip['plate']}")
    c.drawRightString(w - 60, y - 20, f"Distance: {trip['distance']} | Duration: {trip['duration']}")

    c.showPage()

    # Page 2: Route & Map Details
    c.setFont("Helvetica-Bold", 20)
    c.drawString(45, h - 55, "Trip Details")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#555555"))
    c.drawRightString(w - 45, h - 55, f"Rider: {trip['rider']}")

    y = h - 100
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.HexColor("#059669"))
    c.drawString(45, y, "● PICKUP")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(120, y, trip["pickup_time"])
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawString(120, y - 18, trip["pickup"])

    y -= 60
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.HexColor("#DC2626"))
    c.drawString(45, y, "■ DROPOFF")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(120, y, trip["dropoff_time"])
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawString(120, y - 18, trip["dropoff"])

    y -= 70
    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.line(45, y, w - 45, y)

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.black)
    c.drawString(45, y, "Trip Metrics & Verification")
    y -= 22
    metrics = [
        ("Base Fare Rate", "Standard Tier Fare"),
        ("Distance Traveled", trip["distance"]),
        ("Trip Elapsed Time", trip["duration"]),
        ("Vehicle Assigned", f"{trip['service']} ({trip['plate']})"),
        ("Driver Rating", "4.94 ★"),
        ("Payment Verification", "Cash Settled (Verified)")
    ]
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#444444"))
    for label, val in metrics:
        c.drawString(45, y, label)
        c.drawRightString(w - 45, y, val)
        y -= 18

    c.showPage()
    c.save()
    print(f"Generated Uber Receipt: {os.path.basename(out_path)}")

def main():
    target_dir = r"E:\pune visit\Final_Submission_Package\Mayank_Sikarwar\Travelling"
    os.makedirs(target_dir, exist_ok=True)
    for trip in UBER_TRIPS:
        dest = os.path.join(target_dir, trip["filename"])
        generate_uber_pdf(trip, dest)

if __name__ == "__main__":
    main()
