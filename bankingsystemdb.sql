create table customer(
    customer_id number primary key,
    name varchar2(30) not null,
    dob date not null,
    gender varchar2(10) check(gender in('Male','Female','Other')),
    address varchar2(100) not null,
    phone varchar2(15) not null,
    email varchar(30) unique
);

create table account(
    account_id number primary key,
    customer_id number references customer(customer_id),
    account_type varchar2(20) not null,
    balance number default 0,
    opened_on date default sysdate,
    status varchar2(20) default 'active'
);

create table transactions(
    txn_id number primary key,
    account_id number references account(account_id),
    txn_type varchar2(20) not null,
    amount number not null,
    txn_date date default sysdate,
    description varchar2(100)
);

CREATE SEQUENCE txn_seq
START WITH 1
INCREMENT BY 1
NOCACHE;

CREATE TABLE Employee
(
    employee_id  number primary key,
    full_name   VARCHAR2(100) NOT NULL,                         
    dob  DATE NOT NULL,                                   
    gender  VARCHAR2(10) CHECK (gender IN ('Male','Female','Other')),
    email  VARCHAR2(100) UNIQUE,
    phone_number  VARCHAR2(15) UNIQUE NOT NULL,
    address  VARCHAR2(255),
    hire_date  DATE DEFAULT trunc(SYSDATE),
    job_role  VARCHAR2(50) NOT NULL,                           
    branch_id   NUMBER default 1,                                 
    salary   NUMBER(12,2) CHECK (salary >= 0)                        
);

CREATE TABLE loan (
    loan_id        INT PRIMARY KEY,
    customer_id    INT NOT NULL,
    account_id     INT NOT NULL,
    loan_type      VARCHAR2(50) NOT NULL,
    principal_amount NUMBER(15,2) NOT NULL,
    annual_interest_rate  NUMBER(5,2) NOT NULL,
    interest_amount number(15,2) not null,
    monthly_interest_rate NUMBER(8,4),
    tenure_months  INT NOT NULL,
    start_date     DATE DEFAULT trunc(SYSDATE),
    end_date       DATE,
    status         VARCHAR2(20) DEFAULT 'Active',

    CONSTRAINT fk_loan_customer FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    CONSTRAINT fk_loan_account FOREIGN KEY (account_id) REFERENCES account(account_id)
);
select * from loan;





CREATE SEQUENCE loan_id_seq
    START WITH 1
    INCREMENT BY 1
    NOCACHE;

CREATE TABLE loan_payment (
    payment_id     INT PRIMARY KEY,
    loan_id        INT NOT NULL,
    customer_id    INT NOT NULL,
    account_id     INT NOT NULL,
    payment_date   DATE DEFAULT trunc(SYSDATE),
    amount_paid    NUMBER(15,2) NOT NULL,
    balance_left   NUMBER(15,2) NOT NULL,
    payment_mode   VARCHAR2(30), 
    status         VARCHAR2(20) DEFAULT 'Successful',
    
    CONSTRAINT fk_loan_payment_loan FOREIGN KEY (loan_id) REFERENCES loan(loan_id),
    CONSTRAINT fk_loan_payment_customer FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    CONSTRAINT fk_loan_payment_account FOREIGN KEY (account_id) REFERENCES account(account_id)
);

CREATE SEQUENCE payment_id_seq
    START WITH 1
    INCREMENT BY 1
    NOCACHE;

CREATE TABLE loan_request (
    request_id     INT PRIMARY KEY,
    customer_id    INT NOT NULL,
    account_id     INT NOT NULL,
    loan_type      VARCHAR2(50) NOT NULL,
    principal_amount NUMBER(15,2) NOT NULL,
    tenure_months  INT NOT NULL,
    income         NUMBER(15,2),
    employment_status VARCHAR2(50),
    application_date DATE DEFAULT (SYSDATE),
    status         VARCHAR2(20) DEFAULT 'pending', 
    remarks        VARCHAR2(255),

    CONSTRAINT fk_req_customer FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    CONSTRAINT fk_req_account FOREIGN KEY (account_id) REFERENCES account(account_id)
);

CREATE SEQUENCE request_id_seq
    START WITH 1
    INCREMENT BY 1
    NOCACHE;

create table users(
    user_id number primary key,
    username varchar2(30) unique not null,
    password varchar2(50) not null,
    role varchar2(20),
    customer_id  number references customer(customer_id),
    employee_id number references employee(employee_id)
);


-- Insert Customers
INSERT INTO customer (customer_id, name, dob, gender, address, phone, email)
VALUES (1, 'Nithin', DATE '1998-05-10', 'Male', 'Chennai', '9876543210', 'nithin@example.com');

INSERT INTO customer (customer_id, name, dob, gender, address, phone, email)
VALUES (2, 'Vetri', DATE '1997-11-15', 'Male', 'Coimbatore', '9876543211', 'vetri@example.com');

INSERT INTO customer (customer_id, name, dob, gender, address, phone, email)
VALUES (3, 'Vijay', DATE '1996-03-22', 'Male', 'Madurai', '9876543212', 'vijay@example.com');

INSERT INTO customer (customer_id, name, dob, gender, address, phone, email)
VALUES (4, 'Udhaya', DATE '1999-08-19', 'Male', 'Trichy', '9876543213', 'udhaya@example.com');

INSERT INTO customer (customer_id, name, dob, gender, address, phone, email)
VALUES (5, 'Pari', DATE '2000-01-05', 'Male', 'Salem', '9876543214', 'pari@example.com');


-- Insert Employees
INSERT INTO employee (employee_id, full_name, dob, gender, email, phone_number, address, job_role, salary)
VALUES (1, 'Nivass', DATE '1990-02-11', 'Male', 'nivass@example.com', '9876543215', 'Chennai', 'Teller', 30000);

INSERT INTO employee (employee_id, full_name, dob, gender, email, phone_number, address, job_role, salary)
VALUES (2, 'Nithish', DATE '1992-06-21', 'Male', 'nithish@example.com', '9876543216', 'Coimbatore', 'Customer Service', 35000);

INSERT INTO employee (employee_id, full_name, dob, gender, email, phone_number, address, job_role, salary)
VALUES (3, 'Vishruthi', DATE '1993-09-15', 'Female', 'vishruthi@example.com', '9876543217', 'Madurai', 'Loan Officer', 40000);

INSERT INTO employee (employee_id, full_name, dob, gender, email, phone_number, address, job_role, salary)
VALUES (4, 'Vishal', DATE '1994-12-25', 'Male', 'vishal@example.com', '9876543218', 'Trichy', 'Relationship Manager', 45000);

INSERT INTO employee (employee_id, full_name, dob, gender, email, phone_number, address, job_role, salary)
VALUES (5, 'Suriya', DATE '1991-07-07', 'Male', 'suriya@example.com', '9876543219', 'Salem', 'Teller', 32000);


-- Insert Accounts for Customers
INSERT INTO account (account_id, customer_id, account_type, balance, status)
VALUES (1, 1, 'Savings', 5000, 'Active');

INSERT INTO account (account_id, customer_id, account_type, balance, status)
VALUES (2, 2, 'Current', 10000, 'Active');

INSERT INTO account (account_id, customer_id, account_type, balance, status)
VALUES (3, 3, 'Savings', 7000, 'Active');

INSERT INTO account (account_id, customer_id, account_type, balance, status)
VALUES (4, 4, 'Current', 15000, 'Active');

INSERT INTO account (account_id, customer_id, account_type, balance, status)
VALUES (5, 5, 'Savings', 3000, 'Active');


-- Insert Loan Requests
INSERT INTO loan_request (request_id, customer_id, account_id, loan_type, principal_amount, tenure_months, income, employment_status, remarks)
VALUES (1, 1, 1, 'Home Loan', 1000000, 120, 60000, 'Salaried', 'Need home loan approval');

INSERT INTO loan_request (request_id, customer_id, account_id, loan_type, principal_amount, tenure_months, income, employment_status, remarks)
VALUES (2, 2, 2, 'Personal Loan', 500000, 60, 45000, 'Self-Employed', 'Personal expenses');

INSERT INTO loan_request (request_id, customer_id, account_id, loan_type, principal_amount, tenure_months, income, employment_status, remarks)
VALUES (3, 3, 3, 'Business Loan', 2000000, 84, 80000, 'Business Owner', 'Business expansion');

INSERT INTO loan_request (request_id, customer_id, account_id, loan_type, principal_amount, tenure_months, income, employment_status, remarks)
VALUES (4, 4, 4, 'Education Loan', 300000, 48, 30000, 'Student', 'Higher studies');

INSERT INTO loan_request (request_id, customer_id, account_id, loan_type, principal_amount, tenure_months, income, employment_status, remarks)
VALUES (5, 5, 5, 'Personal Loan', 200000, 36, 25000, 'Salaried', 'Medical emergency');

-- Customer Users
INSERT INTO users (user_id, username, password, role, customer_id, employee_id)
VALUES (1, 'nithin_cust', 'pass123', 'customer', 1, NULL);

INSERT INTO users (user_id, username, password, role, customer_id, employee_id)
VALUES (2, 'vetri_cust', 'pass123', 'customer', 2, NULL);

INSERT INTO users (user_id, username, password, role, customer_id, employee_id)
VALUES (3, 'vijay_cust', 'pass123', 'customer', 3, NULL);

INSERT INTO users (user_id, username, password, role, customer_id, employee_id)
VALUES (4, 'udhaya_cust', 'pass123', 'customer', 4, NULL);

INSERT INTO users (user_id, username, password, role, customer_id, employee_id)
VALUES (5, 'pari_cust', 'pass123', 'customer', 5, NULL);


INSERT INTO users (user_id, username, password, role, customer_id, employee_id)
VALUES (6, 'nivass_emp', 'admin123', 'employee', NULL, 1);

INSERT INTO users (user_id, username, password, role, customer_id, employee_id)
VALUES (7, 'nithish_emp', 'admin123', 'employee', NULL, 2);

INSERT INTO users (user_id, username, password, role, customer_id, employee_id)
VALUES (8, 'vishruthi_emp', 'admin123', 'employee', NULL, 3);

INSERT INTO users (user_id, username, password, role, customer_id, employee_id)
VALUES (9, 'vishal_emp', 'admin123', 'employee', NULL, 4);

INSERT INTO users (user_id, username, password, role, customer_id, employee_id)
VALUES (10, 'suriya_emp', 'admin123', 'employee', NULL, 5);

DROP SEQUENCE txn_seq;
DROP SEQUENCE loan_id_seq;
DROP SEQUENCE payment_id_seq;
DROP SEQUENCE request_id_seq;



TRUNCATE table employee;
TRUNCATE TABLE users;
TRUNCATE TABLE loan_payment;
TRUNCATE TABLE loan_request;
TRUNCATE TABLE loan;
TRUNCATE TABLE transactions;
TRUNCATE TABLE account;
TRUNCATE TABLE customer;



select * from CUSTOMER;
select * from ACCOUNT;
select * from transactions;
select * from users;
select * from employee;
select * from loan;
select * from loan_payment;
select * from loan_request;

drop table users;
drop table employee;
drop table loan_payment;
drop table loan;
drop table transactions;
drop table account;
drop table customer;




COMMIT;


DROP TABLE users CASCADE CONSTRAINTS;
DROP TABLE loan_payment CASCADE CONSTRAINTS;
DROP TABLE loan_request CASCADE CONSTRAINTS;
DROP TABLE transactions CASCADE CONSTRAINTS;
DROP TABLE loan CASCADE CONSTRAINTS;
DROP TABLE account CASCADE CONSTRAINTS;
DROP TABLE employee CASCADE CONSTRAINTS;
DROP TABLE customer CASCADE CONSTRAINTS;

-- Drop sequences
DROP SEQUENCE txn_seq;
DROP SEQUENCE loan_id_seq;
DROP SEQUENCE payment_id_seq;
DROP SEQUENCE request_id_seq;
