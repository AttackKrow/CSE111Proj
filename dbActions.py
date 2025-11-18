# customer_registration.py
import sqlite3
from sqlite3 import Error
# Import the queries from the configuration file
from scripts.queries import QUERIES

DATABASE_NAME = "bikerentalshop.sqlite"

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def execute_sql(conn, sql_command, params=(), print_header=True):
    try:
        cur = conn.cursor()
        cur.execute(sql_command, params)
        
        # Check if the command was a SELECT (DQL)
        if cur.description is not None:
            rows = cur.fetchall()
            if rows:

                # 1. Get column names
                column_names = [desc[0] for desc in cur.description]
                
                # 2. Initialize max_widths with header lengths
                max_widths = [len(name) for name in column_names]
                
                # 3. Convert all rows to strings and find max width for each column
                str_rows = []
                for row in rows:
                    str_row = []
                    for i, value in enumerate(row):
                        # Convert value to string for length calculation
                        str_value = str(value)
                        str_row.append(str_value)
                        # Update max width if current value length is greater
                        max_widths[i] = max(max_widths[i], len(str_value))
                    str_rows.append(str_row)

                # Add a small padding (e.g., 2 spaces) to all widths
                total_width = sum(max_widths) + len(max_widths) * 2
                
                # 4. Create a format string for printing
                header_format = "".join([f"{{:<{width + 2}}}" for width in max_widths])
                
                if print_header:
                    # Use total_width for the main separator
                    print("-" * total_width) 
                    print("RESULTS:")
                
                # 🏆 Print the PADDED column names
                print(header_format.format(*column_names))
                
                # Print a second separator line for table structure
                print("-" * total_width) 
                
                # Print PADDED rows
                for str_row in str_rows:
                    print(header_format.format(*str_row))
                # Commit if a DML command returned rows (like RETURNING)
                if not sql_command.strip().upper().startswith("SELECT"):
                    conn.commit()
            else:
                print("Query successful, but returned no rows.")
            return rows
        
        # DML (INSERT, UPDATE, DELETE)
        conn.commit()

        command_type = sql_command.strip().upper().split()[0]
        
        if command_type == "INSERT" and cur.lastrowid > 0:
            print(f"Command successful: Last inserted ID is {cur.lastrowid}")
        else:
            print(f"Command successful: {cur.rowcount} rows affected.")
            
        return cur.rowcount
        
    except Error as e:
        # This will catch OperationalError if the table doesn't exist
        print(f"DATABASE ERROR: {e}")
        return None

def main():
    conn = create_connection(DATABASE_NAME)
    
    if conn is None:
        return

    print("\n--- SQLite Menu Interface ---")
    print(f"Connected to database: {DATABASE_NAME}")
    
    while True:
        print("\n-------------------------------------------")
        print("Please choose an operation:")
        
        # Print the menu using the imported QUERIES
        for key, query_data in QUERIES.items():
            print(f"[{key}] {query_data['label']}")
            
        print("[0] EXIT / QUIT")
        print("-------------------------------------------")
        
        choice = input("Enter option number: ").strip()
        
        if choice == '0':
            break
        
        if choice in QUERIES:
            query_data = QUERIES[choice]
            sql_commands = query_data['sql']

            if not isinstance(sql_commands, list):
                sql_commands = [sql_commands]

            required_params = query_data['params']
            
            user_input_params = []
            
            # Collect required parameters from the user
            for param_label in required_params:
                value = input(f"Enter value for '{param_label}': ").strip()
                user_input_params.append(value)
                
            print(f"\n-> Executing: {query_data['label']}")
            for i,sql in enumerate(sql_commands):
                should_print_header = (i == 0)
                if i > 0:
                    print()
                execute_sql(conn, sql, tuple(user_input_params),print_header=should_print_header)
            
            
        else:
            print("Invalid option. Please enter a number from the menu.")

    if conn:
        conn.close()
    print("Interface closed. Goodbye.")

if __name__ == '__main__':
    main()