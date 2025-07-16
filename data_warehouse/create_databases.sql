CREATE TABLE IF NOT EXISTS dim_restaurants(
	restaurant_id INT PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	address VARCHAR(255) NOT NULL,
	rating DECIMAL(10,2) NOT NULL,
	city INT NOT NULL,
	median_price INT NOT NULL,
	review_count INT NOT NULL,
	free_delivery BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_categories(
	category_id INT PRIMARY KEY,
	category_name VARCHAR(255) NOT NULL,
	restaurant_id INT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_items(
	item_id INT PRIMARY KEY,
	item_name VARCHAR(255) NOT NULL,
	price INT NOT NULL,
	old_price INT NOT NULL,
	restaurant_id INT NOT NULL,
	category_id INT NOT NULL,
	calories INT NOT NULL,
	fats INT NOT NULL,
	order_count INT NOT NULL,
	proteins INT NOT NULL,
	like_count INT NOT NULL,
	dislike_count INT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_customize_groups(
	customize_id INT PRIMARY KEY,
	customize_item_name VARCHAR(255) NOT NULL,
	item_id INT NOT NULL,
	is_required BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_customize_options(
	customize_option_id INT PRIMARY KEY,
	customize_option_name VARCHAR(255) NOT NULL,
	customize_option_price INT NOT NULL,
	customize_id INT NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_menu_snapshot(
	restaurant_id INT NOT NULL,
	item_id INT NOT NULL,
	customize_id INT,
	price INT NOT NULL,
	snapshot_date DATE NOT NULL DEFAULT NOW(),
	is_activate BOOLEAN NOT NULL DEFAULT TRUE
);

ALTER TABLE fact_menu_snapshot
ADD FOREIGN KEY(restaurant_id) REFERENCES dim_restaurants(restaurant_id),
ADD FOREIGN KEY(item_id) REFERENCES dim_items(item_id),
ADD FOREIGN KEY(customize_id) REFERENCES dim_customize_groups(customize_id);

ALTER TABLE dim_customize_options
ADD FOREIGN KEY (customize_id) REFERENCES dim_customize_groups(customize_id)