package com.ramen.matchmaker.model;

import jakarta.persistence.*;
import java.util.List;
import java.util.ArrayList;

@Entity
@Table(name = "bakeries")
public class Bakery {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    private String exactAddress;
    
    @Column(length = 1000)
    private String storeFeatures;

    private String signatureMenu;
    
    @Column(length = 1000)
    private String menuFeatures;

    @Column(length = 2000)
    private String positiveReviews;

    @Column(length = 1000)
    private String negativeReview;
    
    @ElementCollection
    @CollectionTable(name = "bakery_review_links", joinColumns = @JoinColumn(name = "bakery_id"))
    @Column(name = "link", length = 500)
    private List<String> reviewLinks = new ArrayList<>();

    @OneToOne(mappedBy = "bakery", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private BakeryOperation operation;

    @OneToMany(mappedBy = "bakery", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<BakeryComparison> comparisons = new ArrayList<>();

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getExactAddress() { return exactAddress; }
    public void setExactAddress(String exactAddress) { this.exactAddress = exactAddress; }
    
    public String getStoreFeatures() { return storeFeatures; }
    public void setStoreFeatures(String storeFeatures) { this.storeFeatures = storeFeatures; }
    
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
    
    public BakeryOperation getOperation() { return operation; }
    public void setOperation(BakeryOperation operation) { this.operation = operation; }
    
    public List<BakeryComparison> getComparisons() { return comparisons; }
    public void setComparisons(List<BakeryComparison> comparisons) { this.comparisons = comparisons; }
}
