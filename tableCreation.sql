CREATE TABLE Customers (
    c_id INT PRIMARY KEY ,
    c_name VARCHAR(100) NOT NULL,
    c_email VARCHAR(100) UNIQUE NOT NULL,
    c_phone VARCHAR(15)
);

CREATE TABLE Employees (
    e_id INT PRIMARY KEY ,
    e_name VARCHAR(100) NOT NULL,
    e_position VARCHAR(50)
);

CREATE TABLE Payments (
    p_id INT PRIMARY KEY ,
    p_amount DECIMAL(10, 2),
    p_c_id INT NOT NULL,
    p_e_id INT NOT NULL,
    p_method VARCHAR(50),
    p_transactiondate DATETIME,
    FOREIGN KEY (p_c_id) REFERENCES Customers(c_id),
    FOREIGN KEY (p_e_id) REFERENCES Employees(e_id)
);


CREATE TABLE Rentals (
    r_id INT PRIMARY KEY ,
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
    b_id INT PRIMARY KEY ,
    b_type VARCHAR(50) NOT NULL,
    b_model VARCHAR(100) NOT NULL,
    b_hourlyrate DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Rental_Bikes (
    rb_r_id INT NOT NULL,
    rb_b_id INT NOT NULL,
    FOREIGN KEY (rb_r_id) REFERENCES Rentals(r_id),
    FOREIGN KEY (rb_b_id) REFERENCES Bikes(b_id)
);

CREATE TABLE Maintenance (
    m_id INT PRIMARY KEY ,
    m_b_id INT NOT NULL,
    m_startdate DATETIME NOT NULL,
    m_enddate DATETIME NOT NULL,
    m_type TEXT,
    FOREIGN KEY (m_b_id) REFERENCES Bikes(b_id)
);

CREATE TABLE Maintenance_Assignments (
    ma_m_id INT NOT NULL,
    ma_e_id INT NOT NULL,
    ma_role VARCHAR(50),
    FOREIGN KEY (ma_m_id) REFERENCES Maintenance(m_id),
    FOREIGN KEY (ma_e_id) REFERENCES Employees(e_id)
);