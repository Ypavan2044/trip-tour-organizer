from users import register, login
from tours import add_tour, view_tours, view_available_tours, update_tour, delete_tour, search_tours, view_tour_details
from bookings import book_tour, view_my_bookings, view_all_bookings, cancel_booking

def admin_menu(user_id):
    while True:
        print("\n========== ADMIN PANEL ==========")
        print("1. Add Tour")
        print("2. View Tours")
        print("3. Update Tour")
        print("4. Delete Tour")
        print("5. View Bookings")
        print("6. Logout")
        choice = input("Enter your choice: ").strip()
        if choice == "1": add_tour(user_id)
        elif choice == "2": view_tours(user_id)
        elif choice == "3": update_tour(user_id)
        elif choice == "4": delete_tour(user_id)
        elif choice == "5": view_all_bookings(user_id)
        elif choice == "6": break
        else: print("Invalid choice.")

def viewer_menu(user_id):
    while True:
        print("\n========== VIEWER DASHBOARD ==========")
        print("1. View Available Tours")
        print("2. Search Tours")
        print("3. View Tour Details")
        print("4. Select / Book Tour")
        print("5. My Bookings")
        print("6. Cancel Booking")
        print("7. Logout")
        choice = input("Enter your choice: ").strip()
        if choice == "1": view_available_tours()
        elif choice == "2": search_tours()
        elif choice == "3": view_tour_details()
        elif choice == "4": book_tour(user_id)
        elif choice == "5": view_my_bookings(user_id)
        elif choice == "6": cancel_booking(user_id)
        elif choice == "7": break
        else: print("Invalid choice.")

def main():
    while True:
        print("\n================================")
        print("         TRIP ORGANIZER")
        print("================================")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1": register()
        elif choice == "2":
            user_id, role = login()
            if user_id:
                if role == "admin": admin_menu(user_id)
                else: viewer_menu(user_id)
        elif choice == "3":
            print("Thank you for using Trip Organizer!")
            break
        else: print("Invalid choice.")

if __name__ == "__main__":
    main()
