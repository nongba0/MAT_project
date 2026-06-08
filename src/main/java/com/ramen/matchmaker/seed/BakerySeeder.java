package com.ramen.matchmaker.seed;

import com.ramen.matchmaker.model.Bakery;
import com.ramen.matchmaker.model.BakeryComparison;
import com.ramen.matchmaker.model.BakeryOperation;
import com.ramen.matchmaker.repository.BakeryRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Arrays;

@Component
public class BakerySeeder implements CommandLineRunner {

    private final BakeryRepository bakeryRepository;

    public BakerySeeder(BakeryRepository bakeryRepository) {
        this.bakeryRepository = bakeryRepository;
    }

    @Override
    public void run(String... args) throws Exception {
        bakeryRepository.deleteAll();

        try (BufferedReader br = new BufferedReader(new InputStreamReader(
                new ClassPathResource("bakeries.tsv").getInputStream(), java.nio.charset.StandardCharsets.UTF_8))) {

            String line;
            boolean firstLine = true;
            while ((line = br.readLine()) != null) {
                if (firstLine) {
                    firstLine = false;
                    continue;
                }

                String[] data = line.split("\t", -1);
                if (data.length < 12) {
                    System.err.println("Skipping invalid line (columns: " + data.length + "): " + line);
                    continue;
                }

                Bakery bakery = new Bakery();
                bakery.setName(data[0]);
                bakery.setExactAddress(data[1]);
                bakery.setStoreFeatures(data[2]);
                bakery.setSignatureMenu(data[3]);
                bakery.setMenuFeatures(data[4]);
                
                String positiveReviewsStr = data[8];
                bakery.setPositiveReviews(positiveReviewsStr);
                bakery.setNegativeReview(data[9]);

                String linksStr = data[10];
                if (!linksStr.isEmpty()) {
                    bakery.setReviewLinks(Arrays.asList(linksStr.split("\\|")));
                }

                BakeryOperation op = new BakeryOperation();
                op.setBakery(bakery);
                op.setSoldOutInfo(data[5]);
                op.setWaitingSystem(data[6]);
                op.setHasDineIn(Boolean.parseBoolean(data[7]));
                bakery.setOperation(op);

                String compStr = data[11];
                if (!compStr.isEmpty()) {
                    String[] compData = compStr.split("\\|");
                    if (compData.length >= 3) {
                        BakeryComparison comp = new BakeryComparison();
                        comp.setBakery(bakery);
                        comp.setTargetBakeryName(compData[0]);
                        comp.setAspect(compData[1]);
                        comp.setDescription(compData[2]);
                        bakery.getComparisons().add(comp);
                    }
                }

                bakeryRepository.save(bakery);
            }
        }
        System.out.println(">> Seeded bakeries successfully!");
    }
}
