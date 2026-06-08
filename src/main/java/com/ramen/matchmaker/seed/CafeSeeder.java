package com.ramen.matchmaker.seed;

import com.ramen.matchmaker.model.Cafe;
import com.ramen.matchmaker.model.CafeComparison;
import com.ramen.matchmaker.model.CafeOperation;
import com.ramen.matchmaker.repository.CafeRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

@Component
public class CafeSeeder implements CommandLineRunner {

    private final CafeRepository cafeRepository;

    public CafeSeeder(CafeRepository cafeRepository) {
        this.cafeRepository = cafeRepository;
    }

    @Override
    public void run(String... args) throws Exception {
        // if (cafeRepository.count() > 0) {
        //     System.out.println(">> Cafes already seeded.");
        //     return;
        // }
        
        cafeRepository.deleteAll(); // 개발 중이므로 새 데이터 구조 반영을 위해 강제 초기화

        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(new ClassPathResource("cafes.tsv").getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            br.readLine(); // skip header
            while ((line = br.readLine()) != null) {
                if (line.trim().isEmpty()) continue;
                String[] data = line.split("\t", -1);
                
                Cafe cafe = new Cafe();
                cafe.setName(data[0]);
                cafe.setExactAddress(data[1]);
                cafe.setAmbiance(data[2]);
                cafe.setSignatureMenu(data[3]);
                cafe.setMenuFeatures(data[4]);
                cafe.setPositiveReviews(data[5]);
                cafe.setNegativeReview(data[6]);
                if (!data[7].isEmpty()) {
                    cafe.setReviewLinks(Arrays.asList(data[7].split("\\|")));
                }
                
                if (data.length > 15 && !data[15].isEmpty()) {
                    cafe.setLatitude(Double.parseDouble(data[15]));
                }
                if (data.length > 16 && !data[16].isEmpty()) {
                    cafe.setLongitude(Double.parseDouble(data[16]));
                }

                CafeOperation operation = new CafeOperation();
                operation.setWaitingSystem(data[8]);
                operation.setHasPlugs(Boolean.parseBoolean(data[9]));
                operation.setParkingInfo(data[10]);
                operation.setHasDecaf(Boolean.parseBoolean(data[11]));
                operation.setLargeCafe(Boolean.parseBoolean(data[12]));
                operation.setPetFriendly(Boolean.parseBoolean(data[13]));
                
                operation.setCafe(cafe);
                cafe.setOperation(operation);

                if (!data[14].isEmpty()) {
                    String[] comps = data[14].split("\\|");
                    if (comps.length >= 3) {
                        CafeComparison comp = new CafeComparison();
                        comp.setTargetCafeName(comps[0]);
                        comp.setAspect(comps[1]);
                        comp.setDescription(comps[2]);
                        comp.setCafe(cafe);
                        cafe.getComparisons().add(comp);
                    }
                }

                cafeRepository.save(cafe);
            }
            System.out.println(">> Seeded cafes successfully!");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
