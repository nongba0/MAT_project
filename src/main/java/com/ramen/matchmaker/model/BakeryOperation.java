package com.ramen.matchmaker.model;

import jakarta.persistence.*;

@Entity
@Table(name = "bakery_operations")
public class BakeryOperation {
    @Id
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @MapsId
    @JoinColumn(name = "bakery_id")
    @com.fasterxml.jackson.annotation.JsonIgnore
    private Bakery bakery;

    @Column(length = 500)
    private String soldOutInfo;

    @Column(length = 500)
    private String waitingSystem;

    private Boolean hasDineIn;

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public Bakery getBakery() { return bakery; }
    public void setBakery(Bakery bakery) { this.bakery = bakery; }
    
    public String getSoldOutInfo() { return soldOutInfo; }
    public void setSoldOutInfo(String soldOutInfo) { this.soldOutInfo = soldOutInfo; }
    
    public String getWaitingSystem() { return waitingSystem; }
    public void setWaitingSystem(String waitingSystem) { this.waitingSystem = waitingSystem; }
    
    public Boolean getHasDineIn() { return hasDineIn; }
    public void setHasDineIn(Boolean hasDineIn) { this.hasDineIn = hasDineIn; }
}
