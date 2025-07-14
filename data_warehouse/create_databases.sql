CREATE TABLE IF NOT EXISTS dim_restaurants(
	sk_restaurant_id SERIAL PRIMARY KEY,
	restaurant_id INT NOT NULL,
	name VARCHAR(50) NOT NULL,
	address VARCHAR(50) NOT NULL,
	rating DECIMAL(2,2) NOT NULL,
	city INT NOT NULL,
	median_price INT NOT NULL,
	review_count INT NOT NULL,
	free_delivery BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_categories(
	sk_category_id SERIAL PRIMARY KEY,
	category_id INT NOT NULL,
	category_name VARCHAR(20) NOT NULL,
	restaurant_id INT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_items(
	sk_item_id SERIAL PRIMARY KEY,
	item_id INT NOT NULL,
	item_name VARCHAR(30) NOT NULL,
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
	sk_customize_id SERIAL PRIMARY KEY,
	customize_id INT NOT NULL,
	customize_item_name VARCHAR(50) NOT NULL,
	item_id INT NOT NULL,
	is_required BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_customize_options(
	sk_customize_option_id SERIAL PRIMARY KEY,
	customize_option_id INT NOT NULL,
	customize_option_name VARCHAR(50) NOT NULL,
	customize_option_price INT NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_menu_snapshot(
	sk_restaurant_id INT NOT NULL,
	sk_item_id INT NOT NULL,
	price INT NOT NULL,
	snapshot_date DATE NOT NULL DEFAULT NOW(),
	is_activate BOOLEAN NOT NULL
);

ALTER TABLE fact_menu_snapshot
ADD FOREIGN KEY(sk_restaurant_id) REFERENCES dim_restaurants(sk_restaurant_id),
ADD FOREIGN KEY(sk_item_id) REFERENCES dim_items(sk_item_id)