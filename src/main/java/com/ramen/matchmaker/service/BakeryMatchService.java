package com.ramen.matchmaker.service;

import com.ramen.matchmaker.dto.BakeryMatchRequest;
import com.ramen.matchmaker.model.Bakery;
import com.ramen.matchmaker.repository.BakeryRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.List;

@Service
@RequiredArgsConstructor
public class BakeryMatchService {

    private final BakeryRepository bakeryRepository;

    public List<Bakery> matchBakeries(BakeryMatchRequest request) {
        if (request == null || request.getKeyword() == null || request.getKeyword().trim().isEmpty()) {
            return Collections.emptyList();
        }

        String keyword = request.getKeyword().trim();

        if ("LOCATION".equalsIgnoreCase(request.getSearchType())) {
            // 위치 기반 검색: 주소(exact_address)에서 키워드 검색
            return bakeryRepository.findByExactAddressContainingIgnoreCase(keyword);
        } else if ("BREAD".equalsIgnoreCase(request.getSearchType())) {
            // 빵 종류 검색: 시그니처 메뉴 또는 메뉴 특징에서 키워드 검색
            return bakeryRepository.findBySignatureMenuContainingIgnoreCaseOrMenuFeaturesContainingIgnoreCase(keyword, keyword);
        }

        return Collections.emptyList();
    }
}
