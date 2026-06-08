package com.ramen.matchmaker.repository;

import com.ramen.matchmaker.model.BakeryOperation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface BakeryOperationRepository extends JpaRepository<BakeryOperation, Long> {
}
