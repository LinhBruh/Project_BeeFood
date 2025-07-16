from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col

spark = SparkSession.builder.appName("Transform_data")\
        .master("spark://spark-master:7077")\
        .config("spark.sql.warehouse.dir", "/tmp/spark-artifacts") \
        .config("spark.sql.artifacts.dir", "/tmp/spark-artifacts") \
        .config("spark.local.dir", "/tmp/spark-artifacts") \
        .getOrCreate()


def transform_data(df):
    restaurant_data = df.select("restaurant_id","name","address","rating","city","median_price","review_count","free_delivery")
    df_explode_detail_restaurant = df.withColumn("detail_restaurant", explode(col("detail_restaurant")))

    categories_data = df_explode_detail_restaurant.select(col("detail_restaurant.category_id").alias("category_id"),
                           col("detail_restaurant.category_name").alias("category_name"),
                           col("restaurant_id")
                           )
    
    categories_data =  categories_data.dropDuplicates(["category_id"])
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

    customize_item_data = customize_item_data.dropDuplicates(["customize_id"])
    df_explode_customize = df_explode_item.withColumn("customize_options", explode(col("customize_item.customize_options")))
    customize_option_data = df_explode_customize.select(col("customize_options.customize_option_id").alias("customize_option_id"),
                                                        col("customize_options.customize_option_name").alias("customize_option_name"),
                                                        col("customize_options.customize_price").alias("customize_option_price"),
                                                        col("customize_item.customize_id")
                                                        )
    customize_option_data = customize_option_data.dropDuplicates(["customize_option_id"])
    data_fact = df_explode_item.select("restaurant_id",
                                        col("items.restaurant_item_id").alias("item_id"),
                                        col("items.price").alias("price"),
                                        col("customize_item.customize_id").alias("customize_id")
                                           )
    return restaurant_data, categories_data, item_data, customize_item_data, customize_option_data, data_fact

