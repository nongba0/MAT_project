package com.ramen.matchmaker.controller;

import com.ramen.matchmaker.model.*;
import com.ramen.matchmaker.repository.RestaurantRepository;
import org.springframework.web.bind.annotation.*;
import java.util.List;


@RestController
@RequestMapping("/api/restaurants")
@CrossOrigin(origins = "*")
public class RestaurantController {

    private final RestaurantRepository restaurantRepository;

    public RestaurantController(RestaurantRepository restaurantRepository) {
        this.restaurantRepository = restaurantRepository;
    }

    @GetMapping
    public List<Restaurant> getAllRestaurant() {
        return restaurantRepository.findAll();
    }

    @GetMapping("/search/partition")
    public List<Restaurant> getRestaurantsByPartition(
            @RequestParam(required = false) FoodCategory foodCategory,
            @RequestParam(required = false) DetailStyle detailStyle,
            @RequestParam(required = false) MainIngredient mainIngredient) {
        
        if (foodCategory == null && detailStyle == null && mainIngredient == null) {
            return restaurantRepository.findAll();
        }
        return restaurantRepository.findByPartition(foodCategory, detailStyle, mainIngredient);
    }

    @GetMapping("/search/location")
    public List<Restaurant> getRestaurantsByLocation(@RequestParam String location) {
        return restaurantRepository.findByLocationContaining(location);
    }

    @GetMapping("/search/name")
    public List<Restaurant> getRestaurantsByName(@RequestParam String name) {
        return restaurantRepository.findByNameContaining(name);
    }


}
