package com.ramen.matchmaker.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
@Entity
@Table(name = "restaurants", indexes = {
    @Index(name = "idx_restaurant_name", columnList = "name"),
    @Index(name = "idx_restaurant_location", columnList = "location")
})
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Restaurant {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String location;

@Enumerated(EnumType.STRING)
    private FoodCategory foodCategory;

    @Enumerated(EnumType.STRING)
    private DetailStyle detailStyle;

    @Enumerated(EnumType.STRING)
    private MainIngredient mainIngredient;

    @Column(length = 1000)
    private String description;

    @Column(length = 500)
    private String keywordTags;

    @Column(length = 500)
    private String signatureMenus;

    @Column(length = 1000)
    private String menuDescription;

    public Restaurant(String name, String location, FoodCategory foodCategory, DetailStyle detailStyle, MainIngredient mainIngredient, String description, String keywordTags, String signatureMenus, String menuDescription) {
        this.name = name;
        this.location = location;
this.foodCategory = foodCategory;
        this.detailStyle = detailStyle;
        this.mainIngredient = mainIngredient;
        this.description = description;
        this.keywordTags = keywordTags;
        this.signatureMenus = signatureMenus;
        this.menuDescription = menuDescription;
    }
}
