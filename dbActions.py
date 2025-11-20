import sqlite3
from sqlite3 import Error
from scripts.queries import QUERIES

DATABASE_NAME = "bikerentalshop.sqlite"

def create_connection(db_file):
    # Create a database connection to the SQLite database specified by db_file
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def execute_sql(conn, sql_command, params=(), print_header=True):
    # Execute an SQL query and handle results
    try:
        cur = conn.cursor()
        cur.execute(sql_command, params)
        
        # Check if the command was a SELECT (DQL)
        if cur.description is not None:
            rows = cur.fetchall()
            if rows:

                # Print formatting for results
                column_names = [desc[0] for desc in cur.description]
                max_widths = [len(name) for name in column_names]
                str_rows = []
                for row in rows:
                    str_row = []
                    for i, value in enumerate(row):
                        str_value = str(value)
                        str_row.append(str_value)
                        max_widths[i] = max(max_widths[i], len(str_value))
                    str_rows.append(str_row)

                total_width = sum(max_widths) + len(max_widths) * 2
                
                header_format = "".join([f"{{:<{width + 2}}}" for width in max_widths])
                
                if print_header:
                    print("-" * total_width) 
                    print("RESULTS:")
                
                print(header_format.format(*column_names))
                
                print("-" * total_width) 
                
                for str_row in str_rows:
                    print(header_format.format(*str_row))
                # Commit if the query returned rows but is not a SELECT
                if not sql_command.strip().upper().startswith("SELECT"):
                    conn.commit()
            else:
                # No rows returned, likely a parameter was was misinput.
                print("Query successful, but returned no rows.")
            return rows
        
        # DML (INSERT, UPDATE, DELETE, etc.)
        conn.commit()

        # Print feedback based on affected rows
        if cur.rowcount > 0:
            print(f"Query successful. {cur.rowcount} row(s) affected.")
        elif cur.rowcount == 0:
            # This covers DELETE/UPDATE that matched no rows, or an INSERT without RETURNING
            print("Query successful. No rows were affected (0 rows modified/deleted.")
        else:
            # cur.rowcount is typically -1 for non-DML (like CREATE TABLE) or when not available
            print(f"Query successful. Transaction committed.") 
        
    except Error as e:
        # This will catch OperationalError if the table doesn't exist
        print(f"DATABASE ERROR: {e}")
        return None

def main():
    # Create a database connection, display the menu, and handle user input.
    # Run the queries selected by the user from the menu.
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
        
        # Exit option
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

            num_commands = len(sql_commands)
            # Execute each SQL command in sequence from the selected menu option
            for i, sql in enumerate(sql_commands):
                should_print_header = (i == 0)
                
                # Use the original parameter list for every step
                execute_sql(conn, sql, tuple(user_input_params), print_header=should_print_header)
                
                if i < num_commands - 1:
                    print()
            
        else:
            print("Invalid option. Please enter a value from the menu.")

    if conn:
        conn.close()
    print("Interface closed. Goodbye.")

if __name__ == '__main__':
    main()