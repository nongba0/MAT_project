package com.ramen.matchmaker.repository;

import com.ramen.matchmaker.model.Bakery;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface BakeryRepository extends JpaRepository<Bakery, Long> {
    
    // 위치 기반 검색 (시/구/동 텍스트 매칭)
    List<Bakery> findByExactAddressContainingIgnoreCase(String keyword);

    // 빵 종류 검색 (시그니처 메뉴 또는 메뉴 특징 텍스트 매칭)
    List<Bakery> findBySignatureMenuContainingIgnoreCaseOrMenuFeaturesContainingIgnoreCase(String menuKeyword, String featureKeyword);
}
