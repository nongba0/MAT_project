package com.ramen.matchmaker.controller;

import com.ramen.matchmaker.model.Theme;
import com.ramen.matchmaker.repository.ThemeRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/themes")
@CrossOrigin(origins = "*")
public class ThemeController {

    private final ThemeRepository themeRepository;

    public ThemeController(ThemeRepository themeRepository) {
        this.themeRepository = themeRepository;
    }

    @GetMapping
    public List<Theme> getAllThemes() {
        return themeRepository.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Theme> getThemeById(@PathVariable String id) {
        return themeRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}
