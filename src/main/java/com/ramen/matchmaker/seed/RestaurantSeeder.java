package com.ramen.matchmaker.seed;

import com.ramen.matchmaker.model.*;
import com.ramen.matchmaker.repository.RestaurantRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Component;
import org.springframework.core.annotation.Order;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

@Component
@Order(1)
public class RestaurantSeeder implements CommandLineRunner {

    private final RestaurantRepository restaurantRepository;

    public RestaurantSeeder(RestaurantRepository restaurantRepository) {
        this.restaurantRepository = restaurantRepository;
    }

    @Override
    public void run(String... args) throws Exception {
        seedRestaurants();
    }

    private void seedRestaurants() {
        if (restaurantRepository.count() > 0) {
            restaurantRepository.deleteAll(); // Force update since schema changed
        }

        List<Restaurant> restaurants = new ArrayList<>();

        try (BufferedReader reader = new BufferedReader(new InputStreamReader(
                new ClassPathResource("restaurants.tsv").getInputStream(), StandardCharsets.UTF_8))) {

            String line;
            boolean isFirst = true;

            while ((line = reader.readLine()) != null) {
                if (isFirst) {
                    isFirst = false; // Skip header
                    continue;
                }
                
                if (line.trim().isEmpty()) continue;

                String[] columns = line.split("\t");
                if (columns.length < 9) {
                    System.out.println("Skip invalid line: " + line);
                    continue;
                }

                String name = columns[0];
                String location = columns[1];
                FoodCategory foodCategory = FoodCategory.valueOf(columns[2]);
                DetailStyle detailStyle = DetailStyle.valueOf(columns[3]);
                MainIngredient mainIngredient = MainIngredient.valueOf(columns[4]);
                String description = columns[5];
                String keywordTags = columns[6];
                String signatureMenus = columns[7];
                String menuDescription = columns[8];

                Restaurant r = new Restaurant(
                        name, location, foodCategory, detailStyle, mainIngredient,
                        description, keywordTags, signatureMenus, menuDescription
                );
                restaurants.add(r);
            }

            restaurantRepository.saveAll(restaurants);
            System.out.println(">> Seeded " + restaurants.size() + " restaurants successfully from TSV!");

        } catch (Exception e) {
            System.err.println("Failed to load restaurants.tsv");
            e.printStackTrace();
        }
    }
}
