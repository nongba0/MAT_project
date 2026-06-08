package com.ramen.matchmaker.repository;

import com.ramen.matchmaker.model.Cafe;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface CafeRepository extends JpaRepository<Cafe, Long> {

    @Query("SELECT c FROM Cafe c JOIN FETCH c.operation op WHERE " +
           "(UPPER(c.exactAddress) LIKE UPPER(CONCAT('%', :keyword, '%')) " +
           "OR UPPER(c.name) LIKE UPPER(CONCAT('%', :keyword, '%')) " +
           "OR UPPER(c.ambiance) LIKE UPPER(CONCAT('%', :keyword, '%'))) " +
           "AND (:isLargeCafe IS NULL OR op.isLargeCafe = :isLargeCafe) " +
           "AND (:hasDecaf IS NULL OR op.hasDecaf = :hasDecaf) " +
           "AND (:hasPlugs IS NULL OR op.hasPlugs = :hasPlugs)")
    List<Cafe> searchCafes(
            @Param("keyword") String keyword,
            @Param("isLargeCafe") Boolean isLargeCafe,
            @Param("hasDecaf") Boolean hasDecaf,
            @Param("hasPlugs") Boolean hasPlugs
    );
}
