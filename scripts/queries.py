QUERIES = {
    #1
    '1': {
        'label': 'Register New Customer',
        'sql': "INSERT INTO customers(c_name, c_email, c_phone) VALUES(?, ?, ?)",
        'params': ['Name', 'Email', 'Number']
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
        'params': ['BikeID']
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
    }

}