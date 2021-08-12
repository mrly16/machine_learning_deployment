LOAD_RAW_DATA = """SELECT a.community_id, city_id, community_name, address, lat, lng, district_id, area_id, building_type, real_estate_type, completion_time, tags, developer, property_company, property_management_fee, completion_year, total_area, plot_ratio, landscaping_ratio, total_household_num, parking, community_type, url, photo_num, video_num, image_url, sale_num, rent_num, month_change, market_sentiment, evaluation_description, overall_score, shopping_score, traffic_score, impression_score, a.price 
FROM spider_anjuke_community_price_20210706 a 
LEFT JOIN
  (SELECT b.community_id, city_id, community_name, address, lat, lng, district_id, area_id, building_type, real_estate_type, completion_time, tags, developer, property_company, property_management_fee, completion_year, total_area, plot_ratio, landscaping_ratio, total_household_num, parking, community_type, url, photo_num, video_num, image_url, sale_num, rent_num, month_change, market_sentiment, evaluation_description, overall_score, shopping_score, traffic_score, impression_score
   FROM
     (SELECT community_id, city_id, community_name, address, lat, lng, district_id, area_id, building_type, real_estate_type, completion_time, tags
      FROM spider_anjuke_community_basic
      WHERE is_valid = TRUE) b
   LEFT JOIN
     (SELECT community_id, developer, property_company, property_management_fee, completion_year, total_area, plot_ratio, landscaping_ratio, total_household_num, parking, community_type, url, photo_num, video_num, image_url, sale_num, rent_num, month_change, market_sentiment, evaluation_description, overall_score, shopping_score, traffic_score, impression_score
      FROM spider_anjuke_community_extend
      WHERE is_valid = TRUE) c ON b.community_id = c.community_id) d ON a.community_id = d.community_id
LIMIT {sample_size}"""
