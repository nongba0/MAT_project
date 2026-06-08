package com.ramen.matchmaker.model;

import jakarta.persistence.*;

@Entity
@Table(name = "bakery_comparisons")
public class BakeryComparison {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "bakery_id")
    @com.fasterxml.jackson.annotation.JsonIgnore
    private Bakery bakery;

    private String targetBakeryName;

    private String aspect;

    @Column(length = 1000)
    private String description;

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public Bakery getBakery() { return bakery; }
    public void setBakery(Bakery bakery) { this.bakery = bakery; }
    
    public String getTargetBakeryName() { return targetBakeryName; }
    public void setTargetBakeryName(String targetBakeryName) { this.targetBakeryName = targetBakeryName; }
    
    public String getAspect() { return aspect; }
    public void setAspect(String aspect) { this.aspect = aspect; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}
