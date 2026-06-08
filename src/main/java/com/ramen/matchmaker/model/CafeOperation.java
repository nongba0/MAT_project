package com.ramen.matchmaker.model;

import jakarta.persistence.*;
import com.fasterxml.jackson.annotation.JsonIgnore;

@Entity
@Table(name = "cafe_operations")
public class CafeOperation {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "cafe_id")
    @JsonIgnore
    private Cafe cafe;

    private String waitingSystem;

    private boolean hasPlugs;

    private String parkingInfo;

    private boolean hasDecaf;
    
    private boolean isLargeCafe;

    private boolean isPetFriendly;

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public Cafe getCafe() { return cafe; }
    public void setCafe(Cafe cafe) { this.cafe = cafe; }
    
    public String getWaitingSystem() { return waitingSystem; }
    public void setWaitingSystem(String waitingSystem) { this.waitingSystem = waitingSystem; }
    
    public boolean isHasPlugs() { return hasPlugs; }
    public void setHasPlugs(boolean hasPlugs) { this.hasPlugs = hasPlugs; }
    
    public String getParkingInfo() { return parkingInfo; }
    public void setParkingInfo(String parkingInfo) { this.parkingInfo = parkingInfo; }
    
    public boolean isHasDecaf() { return hasDecaf; }
    public void setHasDecaf(boolean hasDecaf) { this.hasDecaf = hasDecaf; }
    
    public boolean isLargeCafe() { return isLargeCafe; }
    public void setLargeCafe(boolean isLargeCafe) { this.isLargeCafe = isLargeCafe; }
    
    public boolean isPetFriendly() { return isPetFriendly; }
    public void setPetFriendly(boolean isPetFriendly) { this.isPetFriendly = isPetFriendly; }
}
