-- 4. Fragmentar las tablas de sucursales(branch) y préstamos(loan), el criterio de fragmentación: región

drop table loan;
drop table branch;
drop table auth_user;

drop view global_loan;
drop view global_branch;
drop synonym loan_reg1;
drop synonym loan_reg2;
drop synonym branch_reg1;
drop synonym branch_reg2;

CREATE TABLE "BRANCH" 
   (	"IDBRANCH" NVARCHAR2(10), 
	"NAME" NVARCHAR2(45), 
	"CITY" NVARCHAR2(45), 
	"ASSETS" FLOAT(126), 
	"REGION" NUMBER(11,0),
    CONSTRAINT IDBRANCH_PK PRIMARY KEY (IDBRANCH)
   );

 CREATE TABLE "LOAN" 
   (	"IDLOAN" NVARCHAR2(4), 
	"QUANTITY" FLOAT(126), 
	"DATE_CREATED" TIMESTAMP (6), 
	"APPROVED" NUMBER(1,0), 
	"IDBRANCH" NVARCHAR2(10), 
	"USER_ID" NUMBER(11,0),
    CONSTRAINT IDLOAN_PK PRIMARY KEY (IDLOAN),
    CONSTRAINT IDBRANCH_861CDD84 FOREIGN KEY (IDBRANCH)
	  REFERENCES BRANCH(IDBRANCH) DEFERRABLE INITIALLY DEFERRED ENABLE
   );
   
CREATE TABLE auth_user(
    ID NUMBER(11, 0),
    PASSWORD NVARCHAR2(128),
    LAST_LOGIN TIMESTAMP(6),
    IS_SUPERUSER NUMBER(1,0),
    USERNAME NVARCHAR2(150),
    FIRST_NAME NVARCHAR2(150),
    LAST_NAME NVARCHAR2(150),
    EMAIL NVARCHAR2(150),
    IS_STAFF NUMBER(1,0),
    IS_ACTIVE NUMBER(1,0),
    DATE_JOINED TIMESTAMP(6),
    CONSTRAINT ID_AUTH_USERS_PK PRIMARY KEY (ID)
);
   
ALTER TABLE LOAN ADD CONSTRAINT USERS_LOA_USER_ID_D22AEC39 FOREIGN KEY (USER_ID)
	  REFERENCES AUTH_USER (ID) DEFERRABLE INITIALLY DEFERRED ENABLE;


insert into branch	values ('S0001', 'Downtown',		'Brooklyn',	 	900000,1);
insert into branch	values ('S0002', 'Redwood',		'Palo Alto',	2100000, 1);
insert into branch	values ('S0003', 'Perryridge',	'Horseneck',	1700000, 1);
insert into branch	values('S0004', 'Mianus',		'Horseneck',	 40.0200, 1);
insert into branch	values('S0005', 'Round Hill',	'Horseneck',	8000.000, 1);
insert into branch	values ('S0006', 'Pownal',		'Bennington',	 400000,2);
insert into branch	values ('S0007', 'North Town',	'Rye',		3700000, 2);
insert into branch	values('S0008', 'Brighton',		'Brooklyn',		7000000, 2);
insert into branch	values('S0009', 'Central',		'Rye',		 400280, 2);

insert into loan	values ('L-17',	1000, '04-01-2017 23:03:20.234000', 1, 'S0001', 9);
insert into loan	values ('L-23',	2000, '04-01-2017 23:03:20.234000', 1, 'S0002', 8);
insert into loan	values ('L-15',	1500, '04-01-2017 23:03:20.234000', 1, 'S0003', 1);
insert into loan	values ('L-14',	1500, '04-01-2017 23:03:20.234000', 1, 'S0001', 9);
insert into loan	values ('L-93',	500, '04-07-2017 22:25:40.234000', 1, 'S0004', 4);
insert into loan	values ('L-11',	900, '04-01-2017 22:03:20.234000', 1, 'S0005', 5);
insert into loan	values ('L-16',	1300, '04-02-2017 13:03:20.234000', 1, 'S0003', 3);
insert into loan	values ('L-20',	7500, '04-02-2017 16:33:40.234000', 1, 'S0007', 7);
insert into loan	values ('L-21',	570, '04-02-2017 16:55:40.234000', 1, 'S0009', 9);




--5 Fragmentos de la región 1 en Site A y de la región 2 en el Site B
CREATE TABLE branch_region2
AS SELECT *
FROM branch
WHERE region = 2;

ALTER TABLE branch_region2 ADD CONSTRAINT BRANCH2_IDBRANCH_PK PRIMARY KEY (IDBRANCH);

CREATE TABLE loan_region2
AS SELECT *
FROM loan
WHERE branch_id IN (SELECT branch_id FROM branch WHERE region = 2);

ALTER TABLE loan_region2 ADD CONSTRAINT LOAN2_IDLOAN_PK PRIMARY KEY (IDLOAN);
ALTER TABLE loan_region2 ADD CONSTRAINT LOAN2_IDBRANCH_FK FOREIGN KEY (IDBRANCH) REFERENCES BRANCH_REGION1(IDBRANCH) DEFERRABLE INITIALLY DEFERRED ENABLE;

DROP TABLE loan;
DROP TABLE branch;

RENAME branch_region2 TO branch;
RENAME loan_region2 TO loan;

-- 6
CREATE VIEW global_loan AS
SELECT * FROM loan@linkOracle1
UNION ALL 
SELECT * FROM loan;

CREATE VIEW global_branch AS
SELECT * FROM branch@linkOracle1
UNION ALL 
SELECT * FROM branch;


--7
CREATE SYNONYM loan_reg1 FOR loan@linkOracle1;
CREATE SYNONYM loan_reg2 FOR loan;

CREATE SYNONYM branch_reg1 FOR branch@linkOracle1;
CREATE SYNONYM branch_reg2 FOR branch;


--8
CREATE OR REPLACE PROCEDURE new_branch (
   branch_id IN NVARCHAR2,
   branch_name IN VARCHAR2,
   branch_city IN VARCHAR2,
   branch_assets IN FLOAT,
   branch_region IN NUMBER
) AS
BEGIN
   IF branch_region = 2 THEN
      INSERT INTO branch_reg2 (idBranch, name, city, assets, region)
      VALUES (branch_id, branch_name, branch_city, branch_assets, branch_region);
   ELSE
      INSERT INTO branch (idBranch, name, city, assets, region)
      VALUES (branch_id, branch_name, branch_city, branch_assets,branch_region);
    END IF;
   COMMIT;
END;


--9 
CREATE OR REPLACE PROCEDURE new_loan (
    p_idLoan IN VARCHAR2,
    p_quantity IN FLOAT,
    p_date IN TIMESTAMP,
    p_approved IN NUMBER,
    p_idBranch IN VARCHAR2,
    p_idUser IN NUMBER
) AS
    v_region NUMBER;
BEGIN
    SELECT region INTO v_region
    FROM branch
    WHERE idBranch = p_idBranch;
    
    IF (v_region = 1) THEN
        INSERT INTO loan
        VALUES (p_idLoan, p_quantity, p_date,p_approved,p_idBranch,p_idUser);
    ELSIF (v_region = 2) THEN
        INSERT INTO loan_reg2
        VALUES (p_idLoan, p_quantity, p_date,p_approved,p_idBranch,p_idUser);
    ELSE
        RAISE_APPLICATION_ERROR(-20001, 'Región inválida');
    END IF;
END;


--10

create or replace NONEDITIONABLE TRIGGER loan_replication
AFTER INSERT OR UPDATE OR DELETE ON loan
FOR EACH ROW
DECLARE
    already loan.idLoan%TYPE;
    idloan_v  loan.idLoan%TYPE;
    quantity_v loan.quantity%TYPE;
    date_created_v loan.date_created%TYPE;
    approved_v loan.approved%TYPE;
    idbranch_v loan.idbranch%TYPE;
    user_id_v loan.user_id%TYPE;
    
BEGIN

   IF INSERTING THEN
      SELECT idloan INTO already FROM loan_reg1 WHERE idloan = :new.idloan;
   ELSIF UPDATING THEN
      SELECT idloan, quantity, date_created, approved, idbranch, user_id
      INTO idloan_v, quantity_v, date_created_v, approved_v, idbranch_v, user_id_v
      FROM loan_reg1 WHERE idLoan = :old.idLoan;
      IF quantity_v != :new.quantity OR date_created_v != :new.date_created 
      OR approved_v != :new.approved OR idbranch_v != :new.idbranch 
      OR user_id_v != :new.user_id THEN
          UPDATE loan_reg1
          SET Quantity = :new.Quantity, date_created = :new.date_created, approved = :new.approved, idBranch = :new.idBranch, user_id = :new.user_id
          WHERE idLoan = :old.idLoan;
      END IF;
   ELSIF DELETING THEN
      DELETE FROM loan_reg1 WHERE idloan = :old.idLoan;
   END IF;

   EXCEPTION 
   WHEN NO_DATA_FOUND THEN
     INSERT INTO loan_reg1 (idLoan, Quantity, date_created, approved, idBranch, user_id)
      VALUES (:new.idLoan, :new.Quantity, :new.date_created, :new.approved, :new.idBranch, :new.user_id);
END;

SET SERVEROUT ON
create or replace NONEDITIONABLE TRIGGER branch_replication
AFTER INSERT OR UPDATE OR DELETE ON branch
FOR EACH ROW
DECLARE
    already branch.idBranch%TYPE;
    idbranch_v  branch.idBranch%TYPE;
    name_v  branch.name%TYPE;
    city_v  branch.city%TYPE;
    assets_v  branch.assets%TYPE;
    region_v  branch.region%TYPE;
BEGIN
   IF INSERTING THEN
      SELECT idbranch INTO already FROM branch_reg1 WHERE idbranch = :new.idBranch;
   ELSIF UPDATING THEN
      SELECT idBranch, name, city, assets, region 
      INTO idBranch_v, name_v, city_v, assets_v, region_v 
      FROM  branch_reg1 WHERE idbranch = :old.idBranch;
      IF name_v != :new.name OR city_v != :new.city OR assets_v != :new.assets OR region_v != :new.region THEN
          UPDATE  branch_reg1
          SET name = :new.name, city = :new.city, assets = :new.assets, region = :new.region
          WHERE idBranch = :old.idBranch;
      END IF;
   ELSIF DELETING THEN
      DELETE FROM  branch_reg1 WHERE idBranch = :old.idBranch;
   END IF;   
   
   EXCEPTION 
   WHEN NO_DATA_FOUND THEN
     INSERT INTO branch_reg1 (idBranch, name, city, assets, region)
     VALUES (:new.idBranch, :new.name, :new.city, :new.assets, :new.region);
END;

--11
CREATE MATERIALIZED VIEW gv_branch
REFRESH COMPLETE ON DEMAND
AS
SELECT *FROM branch@linkOracle1
UNION ALL
SELECT * FROM branch;

--12
CREATE MATERIALIZED VIEW gv_loan
REFRESH COMPLETE ON DEMAND
AS
SELECT *FROM loan@linkOracle1
UNION ALL
SELECT * FROM loan;

--13
CREATE VIEW total_loan AS
SELECT SUM(QUANTITY) AS "LOAN TOTAL" FROM loan@linkOracle1
GROUP BY IDBRANCH;


