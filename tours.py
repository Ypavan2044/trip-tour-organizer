import pymysql
from db import create_connection
from validation import get_positive_int, get_positive_float, get_date_range

def add_tour(admin_id):
    print("\n========== ADD TOUR ==========")
    name = input("Tour name: ").strip()
    destination = input("Destination: ").strip()
    if not name or not destination:
        print("Tour name and destination cannot be empty.")
        return
    start, end = get_date_range()
    price = get_positive_float("Price: ")
    seats = get_positive_int("Available seats: ")
    description = input("Description: ").strip()
    conn = None
    try:
        conn = create_connection()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tours (admin_id,tour_name,destination,start_date,end_date,price,available_seats,description,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'Published')",
                (admin_id,name,destination,start,end,price,seats,description)
            )
        conn.commit()
        print("Tour published successfully! ✅")
    except pymysql.MySQLError as e:
        if conn: conn.rollback()
        print("Database error:", e)
    finally:
        if conn: conn.close()

def view_tours(admin_id):
    conn = create_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT tour_id,tour_name,destination,start_date,end_date,price,available_seats,description,status FROM tours WHERE admin_id=%s ORDER BY start_date",(admin_id,))
            rows = cur.fetchall()
        if not rows:
            print("No tours found.")
            return
        for t in rows:
            print("\n--------------------------------")
            labels = ["Tour ID","Tour Name","Destination","Start Date","End Date","Price","Available Seats","Description","Status"]
            for label,value in zip(labels,t):
                print(f"{label}: {value}")
    finally:
        conn.close()

def view_available_tours():
    conn = create_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT tour_id,tour_name,destination,start_date,end_date,price,available_seats FROM tours WHERE status='Published' AND available_seats>0 ORDER BY start_date")
            rows = cur.fetchall()
        if not rows:
            print("No tours are currently available.")
            return
        for t in rows:
            print("\n--------------------------------")
            labels = ["Tour ID","Tour Name","Destination","Start Date","End Date","Price","Available Seats"]
            for label,value in zip(labels,t):
                print(f"{label}: {value}")
    finally:
        conn.close()

def search_tours():
    keyword = input("Enter tour name or destination: ").strip()
    if not keyword:
        print("Search keyword cannot be empty.")
        return
    conn = create_connection()
    try:
        with conn.cursor() as cur:
            k = f"%{keyword}%"
            cur.execute("SELECT tour_id,tour_name,destination,start_date,end_date,price,available_seats FROM tours WHERE status='Published' AND available_seats>0 AND (tour_name LIKE %s OR destination LIKE %s)",(k,k))
            rows = cur.fetchall()
        if not rows:
            print("No tours found.")
            return
        for t in rows:
            print("\n--------------------------------")
            labels = ["Tour ID","Tour Name","Destination","Start Date","End Date","Price","Available Seats"]
            for label,value in zip(labels,t):
                print(f"{label}: {value}")
    finally:
        conn.close()

def view_tour_details():
    try:
        tour_id = int(input("Enter Tour ID: "))
    except ValueError:
        print("Please enter a valid Tour ID.")
        return
    conn = create_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT tour_id,tour_name,destination,start_date,end_date,price,available_seats,description,status FROM tours WHERE tour_id=%s AND status='Published'",(tour_id,))
            t = cur.fetchone()
        if not t:
            print("Tour not found.")
            return
        print("\n========== TOUR DETAILS ==========")
        labels = ["Tour ID","Tour Name","Destination","Start Date","End Date","Price","Available Seats","Description","Status"]
        for label,value in zip(labels,t):
            print(f"{label}: {value}")
    finally:
        conn.close()

def update_tour(admin_id):
    try:
        tour_id = int(input("Enter Tour ID: "))
    except ValueError:
        print("Please enter a valid Tour ID.")
        return
    conn = create_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT tour_id FROM tours WHERE tour_id=%s AND admin_id=%s",(tour_id,admin_id))
            if not cur.fetchone():
                print("Tour not found or permission denied.")
                return
        name = input("Tour name: ").strip()
        destination = input("Destination: ").strip()
        if not name or not destination:
            print("Tour name and destination cannot be empty.")
            return
        start,end = get_date_range()
        price = get_positive_float("Price: ")
        seats = get_positive_int("Available seats: ")
        description = input("Description: ").strip()
        with conn.cursor() as cur:
            cur.execute("UPDATE tours SET tour_name=%s,destination=%s,start_date=%s,end_date=%s,price=%s,available_seats=%s,description=%s WHERE tour_id=%s AND admin_id=%s",(name,destination,start,end,price,seats,description,tour_id,admin_id))
        conn.commit()
        print("Tour updated successfully! ✅")
    except pymysql.MySQLError as e:
        conn.rollback()
        print("Database error:", e)
    finally:
        conn.close()

def delete_tour(admin_id):
    try:
        tour_id = int(input("Enter Tour ID: "))
    except ValueError:
        print("Please enter a valid Tour ID.")
        return
    conn = create_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT tour_name FROM tours WHERE tour_id=%s AND admin_id=%s",(tour_id,admin_id))
            tour = cur.fetchone()
            if not tour:
                print("Tour not found or permission denied.")
                return
            cur.execute("SELECT COUNT(*) FROM bookings WHERE tour_id=%s AND status='Confirmed'",(tour_id,))
            if cur.fetchone()[0] > 0:
                print("Tour has confirmed bookings and cannot be deleted.")
                return
        if input(f"Delete '{tour[0]}'? (yes/no): ").strip().lower() != "yes":
            print("Deletion cancelled.")
            return
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tours WHERE tour_id=%s AND admin_id=%s",(tour_id,admin_id))
        conn.commit()
        print("Tour deleted successfully! ✅")
    except pymysql.MySQLError as e:
        conn.rollback()
        print("Database error:", e)
    finally:
        conn.close()
