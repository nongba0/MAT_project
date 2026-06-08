package com.ramen.matchmaker.model;

import jakarta.persistence.*;
import com.fasterxml.jackson.annotation.JsonIgnore;

@Entity
@Table(name = "cafe_comparisons")
public class CafeComparison {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "cafe_id")
    @JsonIgnore
    private Cafe cafe;

    private String targetCafeName;
    
    private String aspect;
    
    @Column(length = 500)
    private String description;

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public Cafe getCafe() { return cafe; }
    public void setCafe(Cafe cafe) { this.cafe = cafe; }
    
    public String getTargetCafeName() { return targetCafeName; }
    public void setTargetCafeName(String targetCafeName) { this.targetCafeName = targetCafeName; }
    
    public String getAspect() { return aspect; }
    public void setAspect(String aspect) { this.aspect = aspect; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}
