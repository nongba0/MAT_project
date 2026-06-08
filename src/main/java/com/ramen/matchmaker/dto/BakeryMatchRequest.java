package com.ramen.matchmaker.dto;

import lombok.Data;

@Data
public class BakeryMatchRequest {
    // "LOCATION" 또는 "BREAD"
    private String searchType;
    
    // 검색할 키워드 (예: "마포구", "성수동", "소금빵" 등)
    private String keyword;
}
