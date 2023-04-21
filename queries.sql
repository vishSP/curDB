CREATE TABLE companies
(
	company_id PRIMARY KEY,
	company_name varchar (50) NOT NULL
);

CREATE TABLE vacancies
(
	vacancy_id PRIMARY KEY,
	vacancy_name varchar(50),
	salary int,
	discription text,
	url varchar(100),
	company_id int REFERENCES companies(company_id)
)


