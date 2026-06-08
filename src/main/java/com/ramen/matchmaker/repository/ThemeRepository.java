package com.ramen.matchmaker.repository;

import com.ramen.matchmaker.model.Theme;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ThemeRepository extends JpaRepository<Theme, String> {
}
