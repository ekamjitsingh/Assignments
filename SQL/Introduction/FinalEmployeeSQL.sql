--Part 2: Data Engineering:
--The following section of the code creates each table with the primary key/foreign key scheme 
--as layed out in the enclosed ERD
--Please note: The individual CSVs were imported into the tables using the pgAdmin 4 GUI

CREATE TABLE "departments" (
    "dept_no" VARCHAR   NOT NULL,
    "dept_name" VARCHAR   NOT NULL,
    CONSTRAINT "pk_departments" PRIMARY KEY (
        "dept_no"
     )
);

CREATE TABLE "employees" (
    "emp_no" INTEGER   NOT NULL,
    "birth_date" VARCHAR   NOT NULL,
    "first_name" VARCHAR   NOT NULL,
    "last_name" VARCHAR   NOT NULL,
    "gender" VARCHAR   NOT NULL,
    "hire_date" VARCHAR   NOT NULL,
    CONSTRAINT "pk_employees" PRIMARY KEY (
        "emp_no"
     )
);

CREATE TABLE "salaries" (
    "emp_no" INTEGER   NOT NULL,
    "salary" INTEGER   NOT NULL,
    "from_date" VARCHAR   NOT NULL,
    "to_date" VARCHAR   NOT NULL,
	FOREIGN KEY (emp_no) REFERENCES employees(emp_no)
);

CREATE TABLE "dept_manager" (
    "dept_no" VARCHAR   NOT NULL,
    "emp_no" INTEGER   NOT NULL,
	"from_date" VARCHAR NOT NULL,
	"to_date" VARCHAR NOT NULL,
	FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
	FOREIGN KEY (dept_no) REFERENCES departments(dept_no)
);

CREATE TABLE "dept_emp" (
    "emp_no" INTEGER   NOT NULL,
    "dept_no" VARCHAR   NOT NULL,
    "from_date" VARCHAR   NOT NULL,
    "to_date" VARCHAR   NOT NULL,
	FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
	FOREIGN KEY (dept_no) REFERENCES departments(dept_no)
);

CREATE TABLE "titles" (
    "emp_no" INTEGER   NOT NULL,
    "title" VARCHAR   NOT NULL,
    "from_date" VARCHAR   NOT NULL,
    "to_date" VARCHAR   NOT NULL,
	FOREIGN KEY (emp_no) REFERENCES employees(emp_no)
);

--Part 3: Data Analysis:
--Each individual question is indicated by its comment. Check query history to view results.
--List the following details of each employee: employee number, last name, first name, gender, and salary.
select e.emp_no, last_name, first_name, gender, salary
from employees as e
inner join salaries as s ON e.emp_no=s.emp_no;

--List employees who were hired in 1986.
select *
from employees
where hire_date Like '1986%';

--List the manager of each department with the following information: department number, department name,
--the manager's employee number, last name, first name, and start and end employment dates.
--Note: I think the to_date comes up as 9999-01-01 if the employee is still with the company
select m.dept_no, d.dept_name, m.emp_no, e.last_name, e.first_name, p.from_date, p.to_date
from dept_manager as m
inner join departments as d on m.dept_no=d.dept_no
inner join employees as e on m.emp_no=e.emp_no
inner join dept_emp as p on m.emp_no=p.emp_no;

--List the department of each employee with the following information: employee number, last name, 
--first name, and department name.
select e.emp_no, e.last_name, e.first_name, d.dept_name
from employees as e
inner join dept_emp as p on e.emp_no=p.emp_no
inner join departments as d on p.dept_no=d.dept_no;

--List all employees whose first name is "Hercules" and last names begin with "B."
select *
from employees
where first_name='Hercules' and last_name like 'B%';

--List all employees in the Sales department, including their employee number, last name, 
--first name, and department name.
select e.emp_no, e.last_name, e.first_name, d.dept_name
from employees as e
inner join dept_emp as p on e.emp_no=p.emp_no
inner join departments as d on p.dept_no=d.dept_no
where d.dept_name='Sales';

--List all employees in the Sales and Development departments, 
--including their employee number, last name, first name, and department name.
select e.emp_no, e.last_name, e.first_name, d.dept_name
from employees as e
inner join dept_emp as p on e.emp_no=p.emp_no
inner join departments as d on p.dept_no=d.dept_no
where d.dept_name='Sales' or d.dept_name='Development';

--In descending order, list the frequency count of employee last names,
--i.e., how many employees share each last name.
select last_name, count(last_name)
from employees
group by last_name
order by count(last_name) DESC;

