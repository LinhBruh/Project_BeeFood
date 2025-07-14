from pyspark.sql import SparkSession
from extract import extract_data
from pyspark.sql.functions import explode, col

spark = SparkSession.builder.appName("Transform_data")\
        .master("spark://spark-master:7077")\
        .config("spark.sql.warehouse.dir", "/tmp/spark-artifacts") \
        .config("spark.sql.artifacts.dir", "/tmp/spark-artifacts") \
        .config("spark.local.dir", "/tmp/spark-artifacts") \
        .getOrCreate()

df = extract_data()

def transform_data(df):
    restaurant_data = df.select("restaurant_id","name","address","rating","city","median_price","review_count","free_delivery")
    df_explode_detail_restaurant = df.withColumn("detail_restaurant", explode(col("detail_restaurant")))

    categories_data = df_explode_detail_restaurant.select(col("detail_restaurant.category_id").alias("category_id"),
                           col("detail_restaurant.category_name").alias("category_name"),
                           col("restaurant_id")
                           )
    df_explode_category = df_explode_detail_restaurant.withColumn("items", explode(col("detail_restaurant.items")))

    item_data = df_explode_category.select(col("items.restaurant_item_id").alias("item_id"),
                                           col("items.item_name").alias("item_name"),
                                           col("items.price").alias("price"),
                                           col("items.old_price").alias("old_price"),
                                           col("restaurant_id"),
                                           col("detail_restaurant.category_id").alias("category_id"),
                                           col("items.calories").alias("calories"),
                                           col("items.fats").alias("fats"),
                                           col("items.order_count").alias("order_count"),
                                           col("items.proteins").alias("proteins"),
                                           col("items.like_count").alias("like_count"),
                                           col("items.dislike_count").alias("dislike_count")
                                               )
    
    df_explode_item = df_explode_category.withColumn("customize_item", explode(col("items.customize_item")))
    customize_item_data = df_explode_item.select(col("customize_item.customize_id").alias("customize_id"),
                                                 col("customize_item.customize_item_name").alias("customize_item_name"),
                                                 col("items.restaurant_item_id").alias("item_id"),
                                                 col("customize_item.is_required").alias("is_required")
                                                 )

    df_explode_customize = df_explode_item.withColumn("customize_option", explode(col("customize_item.customize_option")))
    customize_option_data = df_explode_customize.select()
    return restaurant_data, categories_data, item_data


restaurant, categories,  item = transform_data(df)

print(restaurant)
print(categories)
item.show(5)