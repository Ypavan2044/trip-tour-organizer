import pymysql
from db import create_connection
from validation import get_positive_int

def book_tour(user_id):
    try:
        tour_id = int(input("Enter Tour ID: "))
    except ValueError:
        print("Please enter a valid Tour ID.")
        return
    people = get_positive_int("Number of people: ")
    conn = create_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT tour_name,price,available_seats FROM tours WHERE tour_id=%s AND status='Published' FOR UPDATE",(tour_id,))
            tour = cur.fetchone()
            if not tour:
                print("Tour not found or not available.")
                return
            if people > tour[2]:
                print(f"Only {tour[2]} seats are available.")
                return
            total = tour[1] * people
            print("\n========== BOOKING DETAILS ==========")
            print("Tour Name:",tour[0])
            print("Price per person:",tour[1])
            print("People:",people)
            print("Total Amount:",total)
            if input("Confirm booking? (yes/no): ").strip().lower() != "yes":
                print("Booking cancelled.")
                return
            cur.execute("INSERT INTO bookings (user_id,tour_id,number_of_people,status) VALUES (%s,%s,%s,'Confirmed')",(user_id,tour_id,people))
            cur.execute("UPDATE tours SET available_seats=available_seats-%s WHERE tour_id=%s",(people,tour_id))
        conn.commit()
        print("Booking successful! ✅")
    except pymysql.MySQLError as e:
        conn.rollback()
        print("Booking failed:",e)
    finally:
        conn.close()

def view_my_bookings(user_id):
    conn = create_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT b.booking_id,t.tour_name,t.destination,t.start_date,t.end_date,t.price,b.number_of_people,(t.price*b.number_of_people),b.booking_date,b.status FROM bookings b JOIN tours t ON b.tour_id=t.tour_id WHERE b.user_id=%s ORDER BY b.booking_date DESC",(user_id,))
            rows = cur.fetchall()
        if not rows:
            print("You have no bookings yet.")
            return
        for b in rows:
            print("\n--------------------------------")
            labels = ["Booking ID","Tour Name","Destination","Start Date","End Date","Price per person","People","Total Amount","Booking Date","Status"]
            for label,value in zip(labels,b):
                print(f"{label}: {value}")
    finally:
        conn.close()

def view_all_bookings(admin_id):
    conn = create_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT b.booking_id,u.name,u.email,t.tour_name,t.destination,b.number_of_people,(t.price*b.number_of_people),b.booking_date,b.status FROM bookings b JOIN users u ON b.user_id=u.user_id JOIN tours t ON b.tour_id=t.tour_id WHERE t.admin_id=%s ORDER BY b.booking_date DESC",(admin_id,))
            rows = cur.fetchall()
        if not rows:
            print("No bookings found.")
            return
        for b in rows:
            print("\n--------------------------------")
            labels = ["Booking ID","Customer Name","Customer Email","Tour Name","Destination","People","Total Amount","Booking Date","Status"]
            for label,value in zip(labels,b):
                print(f"{label}: {value}")
    finally:
        conn.close()

def cancel_booking(user_id):
    try:
        booking_id = int(input("Enter Booking ID: "))
    except ValueError:
        print("Please enter a valid Booking ID.")
        return
    conn = create_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT tour_id,number_of_people,status FROM bookings WHERE booking_id=%s AND user_id=%s FOR UPDATE",(booking_id,user_id))
            booking = cur.fetchone()
            if not booking:
                print("Booking not found.")
                return
            if booking[2] == "Cancelled":
                print("This booking is already cancelled.")
                return
            if input("Are you sure you want to cancel? (yes/no): ").strip().lower() != "yes":
                print("Cancellation stopped.")
                return
            cur.execute("UPDATE bookings SET status='Cancelled' WHERE booking_id=%s AND user_id=%s",(booking_id,user_id))
            cur.execute("UPDATE tours SET available_seats=available_seats+%s WHERE tour_id=%s",(booking[1],booking[0]))
        conn.commit()
        print("Booking cancelled successfully! ✅")
    except pymysql.MySQLError as e:
        conn.rollback()
        print("Database error:",e)
    finally:
        conn.close()
