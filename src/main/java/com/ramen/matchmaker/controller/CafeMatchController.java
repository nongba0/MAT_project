package com.ramen.matchmaker.controller;

import com.ramen.matchmaker.model.Cafe;
import com.ramen.matchmaker.repository.CafeRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/match/cafe")
public class CafeMatchController {

    private final CafeRepository cafeRepository;

    public CafeMatchController(CafeRepository cafeRepository) {
        this.cafeRepository = cafeRepository;
    }

    @PostMapping
    public List<Cafe> matchCafes(@RequestBody Map<String, String> request) {
        String searchType = request.get("searchType");
        String keyword = request.get("keyword");

        if (keyword == null) keyword = "";

        Boolean isLargeCafe = null;
        Boolean hasDecaf = null;
        Boolean hasPlugs = null;

        if ("CAFE_SEARCH_DRIVE".equals(searchType)) {
            isLargeCafe = true;
        } else if ("CAFE_SEARCH_STUDY".equals(searchType)) {
            hasPlugs = true;
        } else if ("CAFE_SEARCH_COFFEE".equals(searchType)) {
            // No strict filter for now, maybe decaf could be prioritized but let's keep it null for broad search
        } else if ("CAFE_SEARCH_VIBE".equals(searchType)) {
            // Broad search
        }

        return cafeRepository.searchCafes(keyword, isLargeCafe, hasDecaf, hasPlugs);
    }
}
