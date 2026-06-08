package com.ramen.matchmaker.repository;

import com.ramen.matchmaker.model.BakeryComparison;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface BakeryComparisonRepository extends JpaRepository<BakeryComparison, Long> {
}
