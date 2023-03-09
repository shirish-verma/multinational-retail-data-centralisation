# Data Centralization Project: SQL Statements

## M3: Create the database schema <br>

### Task 1: Cast columns of orders_table

```sql
ALTER TABLE orders_table ALTER COLUMN DATE_UUID TYPE UUID USING date_uuid::uuid;
ALTER TABLE orders_table ALTER COLUMN USER_UUID TYPE UUID USING user_uuid::uuid;
ALTER TABLE orders_table ALTER COLUMN CARD_NUMBER TYPE VARCHAR(20);
ALTER TABLE orders_table ALTER COLUMN STORE_CODE TYPE VARCHAR(12);
ALTER TABLE orders_table ALTER COLUMN PRODUCT_CODE TYPE VARCHAR(12);
ALTER TABLE orders_table ALTER COLUMN PRODUCT_QUANTITY TYPE SMALLINT;
```

### Task 2: Cast columns of dim_users_table
```sql
ALTER TABLE DIM_USERS ALTER COLUMN FIRST_NAME TYPE VARCHAR(255);
ALTER TABLE DIM_USERS ALTER COLUMN LAST_NAME TYPE VARCHAR(255);
ALTER TABLE DIM_USERS ALTER COLUMN DATE_OF_BIRTH TYPE DATE;
ALTER TABLE DIM_USERS ALTER COLUMN COUNTRY_CODE TYPE VARCHAR(2);
ALTER TABLE DIM_USERS ALTER COLUMN USER_UUID TYPE UUID USING USER_UUID::UUID;
ALTER TABLE DIM_USERS ALTER COLUMN JOIN_DATE TYPE DATE;
```

### Task 3: Update dim_store_details table
```sql
ALTER TABLE dim_store_details ALTER COLUMN longitude TYPE FLOAT;
ALTER TABLE dim_store_details ALTER COLUMN locality TYPE VARCHAR(255);
ALTER TABLE dim_store_details ALTER COLUMN store_code TYPE VARCHAR(12);
ALTER TABLE dim_store_details ALTER COLUMN staff_numbers TYPE SMALLINT;
ALTER TABLE dim_store_details ALTER COLUMN opening_date TYPE DATE;
ALTER TABLE dim_store_details ALTER COLUMN store_type TYPE VARCHAR(255);
ALTER TABLE dim_store_details ALTER COLUMN store_type TYPE VARCHAR(255);
ALTER TABLE dim_store_details ALTER COLUMN latitude TYPE FLOAT;
ALTER TABLE dim_store_details ALTER COLUMN country_code TYPE VARCHAR(2);
ALTER TABLE dim_store_details ALTER COLUMN continent TYPE VARCHAR(255);
```

### Task 4: Make changes to dim_products table
```sql
UPDATE dim_products SET product_price = REPLACE(product_price, '£', '');
ALTER TABLE DIM_PRODUCTS ADD WEIGHT_CLASS VARCHAR(15);
UPDATE DIM_PRODUCTS
SET WEIGHT_CLASS = 
    CASE
        WHEN WEIGHT_GRAMS < 2000 THEN 'Light'
		WHEN WEIGHT_GRAMS BETWEEN 2000 AND 40000 THEN 'Mid_Sized'
		WHEN WEIGHT_GRAMS BETWEEN 40001 AND 140000 THEN 'Heavy'
		ELSE 'Truck_Required'
	END;
```

### Task 5: Update dim_products table
```sql
ALTER TABLE DIM_PRODUCTS ALTER COLUMN product_price TYPE FLOAT USING product_price::double precision;
ALTER TABLE DIM_PRODUCTS ALTER COLUMN weight_grams TYPE FLOAT USING weight_grams::double precision;
ALTER TABLE DIM_PRODUCTS ALTER COLUMN "EAN" TYPE VARCHAR(18);
ALTER TABLE DIM_PRODUCTS ALTER COLUMN product_code TYPE VARCHAR(12);
ALTER TABLE DIM_PRODUCTS ALTER COLUMN date_added TYPE DATE;
ALTER TABLE DIM_PRODUCTS ALTER COLUMN uuid TYPE UUID USING uuid::uuid;
-- ALTER TABLE dim_products RENAME COLUMN removed TO still_available;
ALTER TABLE DIM_PRODUCTS ADD COLUMN STILL_AVAILABLE BOOL;
UPDATE DIM_PRODUCTS
SET STILL_AVAILABLE = CAST(
							(CASE
								WHEN REMOVED = 'Removed' THEN 0
								ELSE 1
							END) AS BOOL);
```

### Task 6: Update dim_date_times table
```sql
ALTER TABLE DIM_DATE_TIMES ALTER COLUMN MONTH TYPE CHAR(2);
ALTER TABLE DIM_DATE_TIMES ALTER COLUMN YEAR TYPE CHAR(4);
ALTER TABLE DIM_DATE_TIMES ALTER COLUMN DAY TYPE CHAR(2);
ALTER TABLE DIM_DATE_TIMES ALTER COLUMN TIME_PERIOD TYPE VARCHAR(10);
ALTER TABLE DIM_DATE_TIMES ALTER COLUMN DATE_UUID TYPE UUID USING DATE_UUID::UUID;
```

### Task 7: Update dim_card_details table
```sql
ALTER TABLE DIM_CARD_DETAILS ALTER COLUMN card_number TYPE VARCHAR(20);
ALTER TABLE DIM_CARD_DETAILS ALTER COLUMN expiry_date TYPE VARCHAR(5);
ALTER TABLE DIM_CARD_DETAILS ALTER COLUMN date_payment_confirmed TYPE DATE;
```

### Task 8: Create primary keys in the dimension tables
```sql
ALTER TABLE dim_products ADD PRIMARY KEY (product_code);
ALTER TABLE dim_card_details ADD PRIMARY KEY (card_number);
ALTER TABLE dim_date_times ADD PRIMARY KEY (date_uuid);
ALTER TABLE dim_store_details ADD PRIMARY KEY (store_code);
ALTER TABLE dim_users ADD PRIMARY KEY (user_uuid);
```

### Task 9: Finalizing the star based schema and adding foreign keys to the orders table
```sql
ALTER TABLE orders_table ADD FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid);
ALTER TABLE orders_table ADD FOREIGN KEY (product_code) REFERENCES dim_products(product_code);
ALTER TABLE orders_table ADD FOREIGN KEY (store_code) REFERENCES dim_store_details(store_code);
ALTER TABLE orders_table ADD FOREIGN KEY (user_uuid) REFERENCES dim_users(user_uuid);
ALTER TABLE orders_table ADD FOREIGN KEY (card_number) REFERENCES dim_card_details(card_number);
```

## M4: Querying the data <br>

### Task 1: How many stores does the business have and in which countries?
```sql
SELECT COUNTRY_CODE AS COUNTRY,
	COUNT(*) AS TOTAL_NO_STORES
FROM DIM_STORE_DETAILS
GROUP BY COUNTRY
ORDER BY 2 DESC
```

### Task 2: Which locations have the most stores?
```sql
SELECT LOCALITY, COUNT(*) AS total_no_stores
FROM DIM_STORE_DETAILS
GROUP BY LOCALITY
HAVING COUNT(*) >= 10
ORDER BY 2 DESC
```

### Task 3: Which months produce the most sales typically?
```sql
SELECT DATE_PART('month', dd.datetime) AS new_month, CAST(SUM(dp.product_price * ot.product_quantity) AS INT) AS total_sales
FROM orders_table AS ot
JOIN dim_products AS dp
ON ot.product_code = dp.product_code
JOIN dim_date_times AS dd
ON dd.date_uuid = ot.date_uuid
GROUP BY new_month
ORDER BY 2 DESC
```

### Task 4: How many sales are coming from online?
```sql
SELECT (CASE WHEN ds.store_type = 'Web Portal' THEN 'Web' ELSE 'Offline' END) AS location, COUNT(*) AS number_of_sales, SUM(ot.product_quantity) AS product_quantity_count
FROM dim_store_details AS ds
JOIN orders_table AS ot
ON ot.store_code = ds.store_code
JOIN dim_products AS dp
ON dp.product_code = ot.product_code
GROUP BY location
ORDER BY 1 DESC
```

### Task 5: What percentage of sales come through each type of store?
```sql
SELECT DS.STORE_TYPE,
	CAST(SUM(OT.PRODUCT_QUANTITY * DP.PRODUCT_PRICE) AS INT) AS TOTAL_SALES,
	CAST(SUM(OT.PRODUCT_QUANTITY * DP.PRODUCT_PRICE) * 100 / SUM(SUM(OT.PRODUCT_QUANTITY * DP.PRODUCT_PRICE)) OVER () AS NUMERIC(8,2)) AS "percentage_total(%)"
FROM DIM_STORE_DETAILS AS DS
JOIN ORDERS_TABLE AS OT ON OT.STORE_CODE = DS.STORE_CODE
JOIN DIM_PRODUCTS AS DP ON DP.PRODUCT_CODE = OT.PRODUCT_CODE
GROUP BY DS.STORE_TYPE
ORDER BY 2 DESC
```

### Task 6: Which month in each year produced the most sales?
```sql
SELECT DT."year",
	DT."month",
	CAST(SUM(OT.PRODUCT_QUANTITY * DP.PRODUCT_PRICE) AS INT) AS TOTAL_SALES
FROM ORDERS_TABLE AS OT
JOIN DIM_PRODUCTS AS DP ON DP.PRODUCT_CODE = OT.PRODUCT_CODE
JOIN DIM_DATE_TIMES AS DT ON DT.DATE_UUID = OT.DATE_UUID
GROUP BY DT."year",
	DT."month"
ORDER BY 1 DESC, 2
```

### Task 7: What is our staff headcount?
```sql
SELECT 	
		CASE
			WHEN STORE_TYPE = 'Web Portal' THEN 'Web'
			ELSE COUNTRY_CODE
		END AS COUNTRY_CODE_2,
		SUM(STAFF_NUMBERS)
FROM DIM_STORE_DETAILS
GROUP BY COUNTRY_CODE_2
ORDER BY 2 DESC
```

### Task 8: Which German store type is selling the most?
```sql
SELECT ds.store_type, ds.country_code, COUNT(*) AS total_sales
FROM dim_store_details AS ds
JOIN orders_table AS ot ON ot.store_code = ds.store_code
JOIN dim_products AS dp ON dp.product_code = ot.product_code
WHERE country_code = 'DE'
GROUP BY store_type, country_code
ORDER BY 3 DESC
```

### Task 9: How quickly is the company making sales?
```sql
WITH 
	sub_table AS (
		SELECT dt.year, AVG(dt.actual_time_taken)
	FROM ORDERS_TABLE AS ot
	JOIN (
		SELECT *, (datetime - LEAD(datetime) OVER(ORDER BY datetime DESC)) AS actual_time_taken
		FROM dim_date_times
		) AS dt
		ON dt.date_uuid = ot.date_uuid
	GROUP BY dt.year
	ORDER BY 2 DESC
	)
SELECT year, 
	CONCAT(
		'"hours": ', 
		CAST(EXTRACT(hour FROM avg) AS TEXT), 
		', "minutes": ',
		CAST(EXTRACT(minute FROM avg) AS TEXT), 
		', "seconds": ',
		CAST(EXTRACT(second FROM avg)::INT AS TEXT),
		', "milliseconds": ',
		CAST(EXTRACT(millisecond FROM avg)::INT AS TEXT)
	) AS actual_time_taken
FROM sub_table;
```
