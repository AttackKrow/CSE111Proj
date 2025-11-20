# Query Dictionary for Bike Rental System, run from dbActions.py
# 
#  Formatting Guide
#
#   #(Number) -- Query Number
#   'key': { -- String key to reference the query, currently numbers from the ScriptIdeas.txt file. Replace key with value.
#       'label': -- Short description of the query, displayed to the user in the menu. Comma after each field except params.
#       'sql': -- The Query(s) to be executed. Can be a single string or a list of strings for multiple queries.
#                 Queries must all the the full amount of parameters specified in 'params', can use dummy bindings if needed.
#                 Include Brackets [] around all the queries if using multiple queries, separated by commas. See #5 or #6 for example.
#       'params':[] -- List of parameter descriptions, in order, to prompt the user for. Use either '?' for inorder references,
#                    or '?1', '?2', etc. for specific parameter references in the SQL. See #1 or #2 for example.
#   }, -- End of Query, comma if not last
#
#
#   Triple quotes for multi-line python strings. """string here"""
#

QUERIES = {
    #1
    '1': {
        'label': 'Register New Customer',
        'sql': "INSERT INTO customers(c_name, c_email, c_phone) VALUES(?, ?, ?)",
        'params': ['Name', 'Email', 'Phone Number']
    },
    #2
    '2': {
        'label': 'Edit Customer Info from Email (name, email, or phone)',
        'sql': """  UPDATE Customers
                    SET 
                        c_name = CASE UPPER(?1) WHEN 'NAME' THEN ?2 ELSE c_name END,
                        c_email = CASE UPPER(?1) WHEN 'EMAIL' THEN ?2 ELSE c_email END,
                        c_phone = CASE UPPER(?1) WHEN 'PHONE' THEN ?2 ELSE c_phone END
                    WHERE 
                        c_email = ?3
                        AND UPPER(?1) IN ('NAME', 'EMAIL', 'PHONE');""",
        'params': ['Field (Name, Email, or Phone)','New Field Value','Current Email of Customer on File']
    },
    #3
    "3": {
        'label': "Add New Bike",
        'sql': """INSERT INTO Bikes (b_id, b_type, b_model, b_hourlyrate)
            SELECT
                -- Calculate the new b_id (Lowest Available Gap logic)
                COALESCE(
                    -- Check for the lowest available gap (e.g., ID 105 if removed)
                    (
                        SELECT
                            B1.b_id + 1
                        FROM
                            Bikes AS B1
                        LEFT JOIN
                            Bikes AS B2 ON B2.b_id = B1.b_id + 1
                        WHERE
                            -- Restrict search to IDs starting with the correct prefix
                            B1.b_id / 100 = (
                                CASE ?1
                                    WHEN 'Adult' THEN 1
                                    WHEN 'Child' THEN 2
                                    WHEN 'Electric' THEN 3
                                    WHEN 'Road' THEN 4
                                    WHEN 'Tandem' THEN 5
                                    WHEN 'Racing' THEN 6
                                    ELSE 9
                                END
                            ) AND
                            B2.b_id IS NULL -- Find the first missing sequential number
                        ORDER BY
                            B1.b_id
                        LIMIT 1
                    ),
                    -- Fallback: If no gaps found, use MAX ID + 1
                    (
                        SELECT
                            (
                                CASE ?1
                                    WHEN 'Adult' THEN 1
                                    WHEN 'Child' THEN 2
                                    WHEN 'Electric' THEN 3
                                    WHEN 'Road' THEN 4
                                    WHEN 'Tandem' THEN 5
                                    WHEN 'Racing' THEN 6
                                    ELSE 9
                                END
                            ) * 100 + COALESCE(MAX(b_id % 100), 0) + 1
                        FROM
                            Bikes
                        WHERE
                            b_id / 100 = (
                                CASE ?1
                                    WHEN 'Adult' THEN 1
                                    WHEN 'Child' THEN 2
                                    WHEN 'Electric' THEN 3
                                    WHEN 'Road' THEN 4
                                    WHEN 'Tandem' THEN 5
                                    WHEN 'Racing' THEN 6
                                    ELSE 9
                                END
                            )
                    )
                ) AS new_b_id,
                
                -- b_type
                ?1,
                
                -- b_model
                ?2,
                
                -- b_hourlyrate
                CASE ?1
                    WHEN 'Adult' THEN 10.0
                    WHEN 'Child' THEN 8.0
                    WHEN 'Electric' THEN 18.0
                    WHEN 'Road' THEN 12.0
                    WHEN 'Tandem' THEN 18.0
                    WHEN 'Racing' THEN 18.0
                    ELSE 0.0
                END
            -- Return the b_id that was just inserted
            RETURNING b_id;""",
    "params": ["Type", "Model"]
    },
    #4
    '4': {
        'label': 'Remove Bike by ID',
        'sql': "DELETE FROM Bikes WHERE b_id = ?",
        'params': ['Bike ID']
    },
    #5
    '5': {
        'label': 'Find Customer Payments by Email',
        'sql':["SELECT * FROM Customers WHERE c_email = ?",
               "SELECT * FROM Payments WHERE p_c_id = (SELECT c_id FROM Customers WHERE c_email = ?)" ],
        'params': ['Email Address']
    },
    #6
    '6': {
        'label': 'Find Customer Rental History by Email',
        'sql':[ "SELECT * FROM Customers WHERE c_email = ?",
                "SELECT * FROM Rentals WHERE r_c_id = (SELECT c_id FROM Customers WHERE c_email = ?)",
                "SELECT * FROM Rental_Bikes WHERE rb_r_id IN (SELECT r_id FROM Rentals WHERE r_c_id = (SELECT c_id FROM Customers WHERE c_email = ?))" ],
        'params': ['Email Address']
    },
    #7
    '7': {
        'label':'Find Customers Most Recent Rental by Email',
        'sql':  "SELECT * FROM Rentals WHERE r_c_id = (SELECT c_id FROM Customers WHERE c_email = ?) ORDER BY r_startdate DESC LIMIT 1",
        'params': ['Email Address']
    },
    #8
    '8': {
        'label':'View Mainenance History for a Bike by Bike ID',
        'sql':  """SELECT * FROM Maintenance WHERE m_b_id = ?""",
        'params': ['Bike ID']
    },
    #9
    '9': {
        'label':'Find Available Bikes for a Given Date/Time Range',
        'sql':  """SELECT B.* FROM Bikes B 
        WHERE B.b_type = ?
        AND NOT EXISTS (
            SELECT 1 FROM Rentals R
            JOIN Rental_Bikes RB ON R.r_id = RB.rb_r_id
            WHERE RB.rb_b_id = B.b_id
            AND R.r_startdate < ?
            AND R.r_startdate > ?
            )""",
        'params': ['Bike Type', 'Rental End Date/Time (YYYY-MM-DD HH:MM)', 'Rental Start Date/Time (YYYY-MM-DD HH:MM)']
    },
    #10
    '10': {
        'label':'Add new Employee',
        'sql':  """INSERT INTO Employees (e_name, e_position) VALUES (?, ?)""",
        'params': ['Name', 'Position']
    },
    #11
    '11': {
        'label':'Remove Employee by ID',
        'sql':  "DELETE FROM Employees WHERE e_id = ?",
        'params': ['Employee ID']
    },
    #12 
    '12': {
        'label':'Add New Rental and Link Bikes',
        'sql': [
            """
            WITH Cust AS (SELECT c_id FROM Customers WHERE c_email = ?1),
            Emp AS (SELECT e_id FROM Employees WHERE e_id = ?4),
            Calc AS (
                SELECT
                    CEIL((julianday(?3) - julianday(?2)) * 24.0) AS billable_hours,
                    CEIL((julianday(?3) - julianday(?2)) * 24.0) * (
                        SELECT SUM(b_hourlyrate)
                        FROM Bikes
                        WHERE b_id IN (SELECT value FROM json_each('["' || REPLACE(?5, ',', '","') || '"]')) -- ?5 is Bike IDs
                    ) AS total_cost
            )
            INSERT INTO Rentals (r_c_id, r_startdate, r_enddate, r_billablehours, r_totalcost, r_e_id)
            SELECT
                T2.c_id, ?2, ?3, T1.billable_hours, T1.total_cost, T3.e_id
            FROM Calc T1, Cust T2, Emp T3;
            """,

            """
            INSERT INTO Rental_Bikes (rb_r_id, rb_b_id)
            SELECT
                (SELECT MAX(r_id) FROM Rentals),
                value
            FROM json_each('["' || REPLACE(?5, ',', '","') || '"]'), (SELECT ?1, ?2, ?3, ?4) AS dummy_bindings; 
            """
        ],
        'params': ['Customer Email', 'Start Date (YYYY-MM-DD HH:MM)', 'End Date (YYYY-MM-DD HH:MM)', 'Employee ID', 'Bike IDs (Comma Separated)']
    },
    #13
    '13': {
        'label':'Add Payment for a Rental by Rental ID',
        'sql':  """ """,
        'params': ['Rental ID', 'Method']
        # Get customer and employee from rental ID, date from datetime() or similar for the current date/time, amount from rental ID too
    },
    #14
    '14': {
        'label':'Schedule Bike Maintenance',
        'sql':  """INSERT INTO Maintenance (m_b_id, m_startdate, m_type) VALUES (?, ?, ?)""",
        'params': ['Bike ID', 'Start Date/Time (YYYY-MM-DD HH:MM)', 'Type of Maintenance']
    },
    #15
    '15': {
        'label':'Finish Bike Maintenance',
        'sql':  """UPDATE Maintenance 
                    SET m_enddate = ?, m_e_id = ? 
                    WHERE m_b_id = ? AND m_enddate IS NULL""",
        'params': ['End Date/Time (YYYY-MM-DD HH:MM)', 'Employee ID', 'Bike ID']
    },

    #17
    '17': {
        'label':'View Rental History of a Bike by ID',
        'sql':  """SELECT R.* FROM Rentals R
                    JOIN Rental_Bikes RB ON R.r_id = RB.rb_r_id
                    WHERE RB.rb_b_id = ?""",
        'params': ['Bike ID']
    },
}