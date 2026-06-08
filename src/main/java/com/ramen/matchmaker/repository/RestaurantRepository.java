package com.ramen.matchmaker.repository;

import com.ramen.matchmaker.model.*;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface RestaurantRepository extends JpaRepository<Restaurant, Long> {
    List<Restaurant> findByLocationContaining(String location);

    List<Restaurant> findByNameContaining(String name);

    @Query("SELECT r FROM Restaurant r WHERE " +
           "(:foodCategory IS NULL OR r.foodCategory = :foodCategory) AND " +
           "(:detailStyle IS NULL OR r.detailStyle = :detailStyle) AND " +
           "(:mainIngredient IS NULL OR r.mainIngredient = :mainIngredient)")
    List<Restaurant> findByPartition(
        @Param("foodCategory") FoodCategory foodCategory,
        @Param("detailStyle") DetailStyle detailStyle,
        @Param("mainIngredient") MainIngredient mainIngredient
    );
}
