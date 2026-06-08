package com.ramen.matchmaker.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Entity
@Table(name = "options")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Option {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String text;

    private String nextQuestionId;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private InputType inputType = InputType.BUTTON;

    private String filterType; // "LOCATION" or "BREAD" 등 검색 필터 구분용

    @Enumerated(EnumType.STRING)
    private FoodCategory foodCategory;

    @Enumerated(EnumType.STRING)
    private DetailStyle detailStyle;

    @Enumerated(EnumType.STRING)
    private MainIngredient mainIngredient;

    public Option(String text) {
        this.text = text;
    }

    public Option(String text, String nextQuestionId) {
        this.text = text;
        this.nextQuestionId = nextQuestionId;
    }

    public Option(String text, FoodCategory foodCategory, DetailStyle detailStyle, MainIngredient mainIngredient) {
        this.text = text;
        this.foodCategory = foodCategory;
        this.detailStyle = detailStyle;
        this.mainIngredient = mainIngredient;
    }

    public Option(String text, String nextQuestionId, FoodCategory foodCategory, DetailStyle detailStyle, MainIngredient mainIngredient) {
        this.text = text;
        this.nextQuestionId = nextQuestionId;
        this.foodCategory = foodCategory;
        this.detailStyle = detailStyle;
        this.mainIngredient = mainIngredient;
    }

    public Option(String text, InputType inputType, String filterType) {
        this.text = text;
        this.inputType = inputType;
        this.filterType = filterType;
    }
}
