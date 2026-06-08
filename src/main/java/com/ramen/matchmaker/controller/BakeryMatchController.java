package com.ramen.matchmaker.controller;

import com.ramen.matchmaker.dto.BakeryMatchRequest;
import com.ramen.matchmaker.model.Bakery;
import com.ramen.matchmaker.service.BakeryMatchService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/match")
@RequiredArgsConstructor
public class BakeryMatchController {

    private final BakeryMatchService bakeryMatchService;

    @PostMapping("/bakery")
    public ResponseEntity<List<Bakery>> matchBakeries(@RequestBody BakeryMatchRequest request) {
        List<Bakery> matchedBakeries = bakeryMatchService.matchBakeries(request);
        return ResponseEntity.ok(matchedBakeries);
    }
}
