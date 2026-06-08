package com.ramen.matchmaker.model;

import jakarta.persistence.*;
import java.util.List;
import java.util.ArrayList;

@Entity
@Table(name = "cafes")
public class Cafe {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    private String exactAddress;
    
    @Column(length = 500)
    private String ambiance;

    private String signatureMenu;
    
    @Column(length = 1000)
    private String menuFeatures;

    @Column(length = 2000)
    private String positiveReviews;

    @Column(length = 1000)
    private String negativeReview;
    
    @ElementCollection
    @CollectionTable(name = "cafe_review_links", joinColumns = @JoinColumn(name = "cafe_id"))
    @Column(name = "link", length = 500)
    private List<String> reviewLinks = new ArrayList<>();

    private Double latitude;
    private Double longitude;

    @OneToOne(mappedBy = "cafe", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private CafeOperation operation;

    @OneToMany(mappedBy = "cafe", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<CafeComparison> comparisons = new ArrayList<>();

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getExactAddress() { return exactAddress; }
    public void setExactAddress(String exactAddress) { this.exactAddress = exactAddress; }
    
    public String getAmbiance() { return ambiance; }
    public void setAmbiance(String ambiance) { this.ambiance = ambiance; }
    
    public String getSignatureMenu() { return signatureMenu; }
    public void setSignatureMenu(String signatureMenu) { this.signatureMenu = signatureMenu; }
    
    public String getMenuFeatures() { return menuFeatures; }
    public void setMenuFeatures(String menuFeatures) { this.menuFeatures = menuFeatures; }
    
    public String getPositiveReviews() { return positiveReviews; }
    public void setPositiveReviews(String positiveReviews) { this.positiveReviews = positiveReviews; }
    
    public String getNegativeReview() { return negativeReview; }
    public void setNegativeReview(String negativeReview) { this.negativeReview = negativeReview; }
    
    public List<String> getReviewLinks() { return reviewLinks; }
    public void setReviewLinks(List<String> reviewLinks) { this.reviewLinks = reviewLinks; }

    public Double getLatitude() { return latitude; }
    public void setLatitude(Double latitude) { this.latitude = latitude; }

    public Double getLongitude() { return longitude; }
    public void setLongitude(Double longitude) { this.longitude = longitude; }
    
    public CafeOperation getOperation() { return operation; }
    public void setOperation(CafeOperation operation) { this.operation = operation; }
    
    public List<CafeComparison> getComparisons() { return comparisons; }
    public void setComparisons(List<CafeComparison> comparisons) { this.comparisons = comparisons; }
}
