CREATE TABLE Customers (
    c_id INTEGER PRIMARY KEY AUTOINCREMENT,
    c_name TEXT NOT NULL,
    c_email TEXT UNIQUE NOT NULL,
    c_phone TEXT
);

CREATE TABLE Employees (
    e_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    e_name TEXT NOT NULL,
    e_position TEXT
);

CREATE TABLE Payments (
    p_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    p_method TEXT,
    p_transactiondate DATETIME,
    p_amount DECIMAL(10, 2),
    p_c_id INT NOT NULL,
    p_e_id INT NOT NULL,
    FOREIGN KEY (p_c_id) REFERENCES Customers(c_id),
    FOREIGN KEY (p_e_id) REFERENCES Employees(e_id)
);


CREATE TABLE Rentals (
    r_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    r_c_id INT NOT NULL,
    r_startdate DATETIME NOT NULL,
    r_enddate DATETIME,
    r_billablehours INT,
    r_totalcost DECIMAL(10, 2),
    r_p_id INT,
    r_e_id INT NOT NULL,
    FOREIGN KEY (r_c_id) REFERENCES Customers(c_id),
    FOREIGN KEY (r_p_id) REFERENCES Payments(p_id),
    FOREIGN KEY (r_e_id) REFERENCES Employees(e_id)
);


CREATE TABLE Bikes (
    b_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    b_type TEXT NOT NULL,
    b_model TEXT NOT NULL,
    b_hourlyrate DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Rental_Bikes (
    rb_r_id INT NOT NULL,
    rb_b_id INT NOT NULL,
    FOREIGN KEY (rb_r_id) REFERENCES Rentals(r_id),
    FOREIGN KEY (rb_b_id) REFERENCES Bikes(b_id)
);

CREATE TABLE Maintenance (
    m_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    m_b_id INT NOT NULL,
    m_startdate DATETIME NOT NULL,
    m_enddate DATETIME NOT NULL,
    m_type TEXT,
    FOREIGN KEY (m_b_id) REFERENCES Bikes(b_id)
);

CREATE TABLE Maintenance_Assignments (
    ma_m_id INT NOT NULL,
    ma_e_id INT NOT NULL,
    ma_role TEXT,
    FOREIGN KEY (ma_m_id) REFERENCES Maintenance(m_id),
    FOREIGN KEY (ma_e_id) REFERENCES Employees(e_id)
);