package com.ramen.matchmaker.seed;

import com.ramen.matchmaker.model.*;
import com.ramen.matchmaker.repository.ThemeRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import org.springframework.core.annotation.Order;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Component
@Order(2)
public class ThemeSeeder implements CommandLineRunner {

    private final ThemeRepository themeRepository;

    public ThemeSeeder(ThemeRepository themeRepository) {
        this.themeRepository = themeRepository;
    }

    @Override
    public void run(String... args) throws Exception {
        seedThemes();
    }

    private void seedThemes() {
        if (themeRepository.count() > 0) {
            themeRepository.deleteAll(); // Force update
        }

        List<Theme> themes = new ArrayList<>();

        // 1. 비오는데 뭐드실?
        List<Question> rainyQuestions = new ArrayList<>();

        // Step 1: Q1 (rainy_q1)
        List<Option> q1RainyOptions = Arrays.asList(
            new Option("소리부터 맛있다! 지글지글 고소한 전 🥞", "rainy_q2_jeon"),
            new Option("온몸을 사르르 녹여줄 뜨끈뜨끈 국물요리 🍲", "rainy_q2_soup")
        );
        rainyQuestions.add(new Question("rainy_q1", "비 내리는 오늘, 당신의 본능이 이끄는 맛은?", q1RainyOptions));

        // [Jeon Branch (전 코스)]
        // Step 2: Q2_jeon (rainy_q2_jeon)
        List<Option> q2JeonOptions = Arrays.asList(
            new Option("고기나 해물이 듬뿍 올라간 든든한 전", "rainy_q3_jeon_topping"),
            new Option("김치, 감자, 녹두 본연의 깔끔하고 바삭한 전", "rainy_q3_jeon_base")
        );
        rainyQuestions.add(new Question("rainy_q2_jeon", "어떤 스타일의 전이 오늘 가장 당기시나요?", q2JeonOptions));

        // Step 3: Q3_jeon_topping (rainy_q3_jeon_topping)
        List<Option> q3JeonToppingOptions = Arrays.asList(
            new Option("육즙 가득하고 고소한 고기 맛 (육전)", null, FoodCategory.JEON, DetailStyle.STANDARD, MainIngredient.BEEF),
            new Option("신선한 해물과 야채의 조화", "rainy_q4_jeon_seafood")
        );
        rainyQuestions.add(new Question("rainy_q3_jeon_topping", "전 위에 올라갈 핵심 고명 스타일은?", q3JeonToppingOptions));

        // Step 3: Q3_jeon_base (rainy_q3_jeon_base)
        List<Option> q3JeonBaseOptions = Arrays.asList(
            new Option("새콤매콤 개운함 (김치전)", null, FoodCategory.JEON, DetailStyle.STANDARD, MainIngredient.KIMCHI),
            new Option("담백하면서도 씹을수록 고소함", "rainy_q4_jeon_plain")
        );
        rainyQuestions.add(new Question("rainy_q3_jeon_base", "선호하는 맛의 분위기는?", q3JeonBaseOptions));

        // Step 4 (해물파전 vs 부추전)
        // rainy_q4_jeon_seafood
        List<Option> q4JeonSeafoodOptions = Arrays.asList(
            new Option("통통한 오징어/새우와 두툼한 쪽파의 조화 (해물파전)", null, FoodCategory.JEON, DetailStyle.STANDARD, MainIngredient.SCALLION),
            new Option("얇고 바삭한 반죽에 향긋한 부추가 가득한 맛 (부추전)", null, FoodCategory.JEON, DetailStyle.STANDARD, MainIngredient.CHIVE)
        );
        rainyQuestions.add(new Question("rainy_q4_jeon_seafood", "해물/채소 고명의 디테일 선택은?", q4JeonSeafoodOptions));

        // Step 4 (감자전 vs 녹두빈대떡)
        // rainy_q4_jeon_plain
        List<Option> q4JeonPlainOptions = Arrays.asList(
            new Option("감자를 갈아내 겉바속촉 쫀득한 감자전", null, FoodCategory.JEON, DetailStyle.STANDARD, MainIngredient.POTATO),
            new Option("녹두를 곱게 갈아 두툼하게 부친 녹두빈대떡", null, FoodCategory.JEON, DetailStyle.STANDARD, MainIngredient.MUNG_BEAN)
        );
        rainyQuestions.add(new Question("rainy_q4_jeon_plain", "담백한 맛의 주재료 선택은?", q4JeonPlainOptions));

        // [Soup Branch (국물 코스)]
        // Step 2: Q2_soup (rainy_q2_soup)
        List<Option> q2RainySoupOptions = Arrays.asList(
            new Option("한 그릇으로 호로록 끝내는 면 요리 (칼국수/수제비)", "rainy_q3_soup_noodle"),
            new Option("든든하게 속을 채워줄 밥 and 국물 (국밥/찌개/전골)", "rainy_q3_soup_rice")
        );
        rainyQuestions.add(new Question("rainy_q2_soup", "오늘 원하는 국물의 형태는?", q2RainySoupOptions));

        // Step 3: Q3_soup_noodle (rainy_q3_soup_noodle)
        List<Option> q3SoupNoodleOptions = Arrays.asList(
            new Option("자극 없이 맑고 개운한 국물", "rainy_q4_noodle_white"),
            new Option("칼칼하고 얼큰해 땀이 쫙 나는 매운 국물", "rainy_q4_noodle_red")
        );
        rainyQuestions.add(new Question("rainy_q3_soup_noodle", "면 요리 중 끌리는 육수의 텐션은?", q3SoupNoodleOptions));

        // Step 4: Q4_noodle_white (rainy_q4_noodle_white)
        List<Option> q4NoodleWhiteOptions = Arrays.asList(
            new Option("매끈하고 쫄깃하게 썰어낸 긴 면발 (바지락칼국수)", null, FoodCategory.CLEAR_SOUP, DetailStyle.KALGUKSU, MainIngredient.SEAFOOD),
            new Option("반죽을 얇고 쫀득하게 뜯어 넣은 불규칙한 식감 (감자수제비)", null, FoodCategory.CLEAR_SOUP, DetailStyle.SUJEBI, MainIngredient.POTATO)
        );
        rainyQuestions.add(new Question("rainy_q4_noodle_white", "맑은 육수 중 선호하는 면의 종류는?", q4NoodleWhiteOptions));

        // Step 4: Q4_noodle_red (rainy_q4_noodle_red)
        List<Option> q4NoodleRedOptions = Arrays.asList(
            new Option("고추장 베이스로 묵직하고 구수한 육수 (장칼국수)", null, FoodCategory.CLEAR_SOUP, DetailStyle.KALGUKSU, MainIngredient.NONE),
            new Option("해산물 베이스로 얼큰하고 시원한 육수 (얼큰수제비)", null, FoodCategory.CLEAR_SOUP, DetailStyle.SUJEBI, MainIngredient.SEAFOOD)
        );
        rainyQuestions.add(new Question("rainy_q4_noodle_red", "매운 면 육수의 베이스 선택은?", q4NoodleRedOptions));

        // Step 3: Q3_soup_rice (rainy_q3_soup_rice)
        List<Option> q3SoupRiceOptions = Arrays.asList(
            new Option("뚝배기에 담겨 밥을 말아 한 그릇 뚝딱 (국밥)", "rainy_q4_rice_gukbap"),
            new Option("식탁 위에서 보글보글 끓여 덜어먹는 (찌개/전골)", "rainy_q4_rice_jjigae")
        );
        rainyQuestions.add(new Question("rainy_q3_soup_rice", "원하는 식사의 차림 형태는?", q3SoupRiceOptions));

        // Step 4: Q4_rice_gukbap (rainy_q4_rice_gukbap)
        List<Option> q4RiceGukbapOptions = Arrays.asList(
            new Option("돼지 사골을 푹 고아 뽀얗고 묵직한 육수", "rainy_q5_gukbap_pork"),
            new Option("소갈비나 등뼈를 우려내 깊고 든든한 육수", "rainy_q5_gukbap_beef")
        );
        rainyQuestions.add(new Question("rainy_q4_rice_gukbap", "국밥의 육수 베이스 선택은?", q4RiceGukbapOptions));

        // Step 5 (돼지국밥 vs 순대국밥)
        // rainy_q5_gukbap_pork
        List<Option> q5GukbapPorkOptions = Arrays.asList(
            new Option("정통 뽀얀 사골의 돼지 살코기 돼지국밥", null, FoodCategory.RICH_SOUP, DetailStyle.GUKBAP, MainIngredient.PORK),
            new Option("머리고기와 피순대가 조화로운 다대기 순대국밥", null, FoodCategory.RICH_SOUP, DetailStyle.GUKBAP, MainIngredient.SUNDAE)
        );
        rainyQuestions.add(new Question("rainy_q5_gukbap_pork", "돼지 사골 국밥의 상세 건더기는?", q5GukbapPorkOptions));

        // Step 5 (갈비탕 vs 뼈해장국)
        // rainy_q5_gukbap_beef
        List<Option> q5GukbapBeefOptions = Arrays.asList(
            new Option("커다란 갈비뼈를 고아 깊고 개운한 갈비탕", null, FoodCategory.CLEAR_SOUP, DetailStyle.GUKBAP, MainIngredient.BEEF),
            new Option("돼지등뼈와 시래기를 얼큰하게 끓인 뼈해장국", null, FoodCategory.RICH_SOUP, DetailStyle.GUKBAP, MainIngredient.PORK_BONE)
        );
        rainyQuestions.add(new Question("rainy_q5_gukbap_beef", "소/돼지 뼈 우린 육수 중 선택은?", q5GukbapBeefOptions));

        // Step 4: Q4_rice_jjigae (rainy_q4_rice_jjigae)
        List<Option> q4RiceJjigaeOptions = Arrays.asList(
            new Option("얼큰/칼칼해 밥 한 공기 비우는 친근한 찌개", "rainy_q5_jjigae_common"),
            new Option("건더기가 풍성해 안주로도 좋은 묵직한 전골/탕", "rainy_q5_jjigae_heavy")
        );
        rainyQuestions.add(new Question("rainy_q4_rice_jjigae", "찌개/전골 요리의 성격은?", q4RiceJjigaeOptions));

        // Step 5 (김치찌개 vs 부대찌개)
        // rainy_q5_jjigae_common
        List<Option> q5JjigaeCommonOptions = Arrays.asList(
            new Option("신김치와 돼지고기를 푹 끓여 개운한 김치찌개", null, FoodCategory.CLEAR_SOUP, DetailStyle.JJIGAE, MainIngredient.KIMCHI),
            new Option("햄, 소시지, 치즈가 들어가 리치하고 얼큰한 부대찌개", null, FoodCategory.RICH_SOUP, DetailStyle.JJIGAE, MainIngredient.HAM_SAUSAGE)
        );
        rainyQuestions.add(new Question("rainy_q5_jjigae_common", "밥반찬용 찌개 상세 선택은?", q5JjigaeCommonOptions));

        // Step 5 (곱창전골 vs 꼬치어묵탕)
        // rainy_q5_jjigae_heavy
        List<Option> q5JjigaeHeavyOptions = Arrays.asList(
            new Option("곱창의 묵직한 기름맛과 곱이 녹아든 곱창전골", null, FoodCategory.RICH_SOUP, DetailStyle.JJIGAE, MainIngredient.PORK),
            new Option("꼬치어묵이 가득해 포장마차 갬성 돋는 꼬치어묵탕", null, FoodCategory.RICH_SOUP, DetailStyle.JJIGAE, MainIngredient.AMUK)
        );
        rainyQuestions.add(new Question("rainy_q5_jjigae_heavy", "전골/탕 요리 상세 선택은?", q5JjigaeHeavyOptions));

        themes.add(new Theme("rainy_day", "비오는데 뭐드실?", "비오는 날에 어울리는 따끈한 국물 요리 추천", "GENERAL", rainyQuestions));

        // 2. 오늘은 이거 먹고 죽자 그냥
        themes.add(new Theme("eat_and_die", "오늘은 이거 먹고 죽자 그냥", "스트레스를 날려버릴 진하고 헤비한 음식 추천", "GENERAL", new ArrayList<>()));

        // 3. 자기야 오늘 뭐먹을래?
        List<Question> honeyQuestions = new ArrayList<>();
        
        List<Option> q1Options = Arrays.asList(
            new Option("인스타 감성 뿜뿜! 예쁘고 사진 찍기 좋은 핫플 📸"),
            new Option("우리끼리 오붓하게 대화할 수 있는 조용하고 프라이빗한 곳 🍷"),
            new Option("분위기는 무슨! 무조건 맛이 보장된 노포 찐맛집 🤤")
        );
        honeyQuestions.add(new Question("honey_q1", "오랜만에 하는 데이트! 오늘따라 끌리는 식당 분위기는?", q1Options));

        List<Option> q2Options = Arrays.asList(
            new Option("달달한 디저트는 필수지! 빵이나 케이크가 맛있는 감성 카페 🍰"),
            new Option("배불러서 더는 못 먹어! 깔끔하게 아메리카노만 테이크아웃 ☕"),
            new Option("소화시킬 겸 근처 공원이나 거리를 좀 걷자 🚶‍♂️🚶‍♀️")
        );
        honeyQuestions.add(new Question("honey_q2", "식사를 마친 후, 우리의 다음 코스는?", q2Options));

        themes.add(new Theme("honey_what_to_eat", "자기야 오늘 뭐먹을래?", "연인과의 데이트 코스 및 맛집 추천", "GENERAL", honeyQuestions));

        // 4. 라오타의 라멘 추천 (엄격한 리터럴 타입 파티션 매칭 알고리즘 트리 적용)
        List<Question> monsterQuestions = new ArrayList<>();

        // Q1: 오늘 위장에 채워 넣을 라멘의 형태는?
        List<Option> q1MonsterOptions = Arrays.asList(
            new Option("찐득한 비빔 (국물 없음)", "monster_q2_bibim"),
            new Option("국물 드링킹 (뜨끈한 국물)", "monster_q2_soup")
        );
        monsterQuestions.add(new Question("monster_q1", "오늘 위장에 채워 넣을 라멘의 형태는?", q1MonsterOptions));

        // Q2_bibim: 비빔 라멘의 스타일은?
        List<Option> q2BibimOptions = Arrays.asList(
            new Option("찍먹 (츠케멘)", "monster_q3_tsukemen", FoodCategory.TSUKEMEN, null, null),
            new Option("비빔 (마제 / 아부라)", "monster_q3_maze_abura")
        );
        monsterQuestions.add(new Question("monster_q2_bibim", "비빔 라멘의 스타일은?", q2BibimOptions));

        // Q3_tsukemen: 니보시(멸치)/교카이(어패류) 풍미를 좋아하시나요?
        List<Option> q3TsukemenOptions = Arrays.asList(
            new Option("YES (바다 풍미)", null, null, null, MainIngredient.SEAFOOD),
            new Option("NO (고기/간장 베이스)", null)
        );
        monsterQuestions.add(new Question("monster_q3_tsukemen", "니보시(멸치)/교카이(어패류) 풍미를 좋아하시나요?", q3TsukemenOptions));

        // Q3_maze_abura: 고명 중심인가요, 아니면 기름과 타래 중심인가요?
        List<Option> q3MazeAburaOptions = Arrays.asList(
            new Option("민찌 중심 꾸덕 비빔 (마제소바)", null, FoodCategory.MAJESOBA, null, null),
            new Option("기름+타래 중심 묵직 비빔 (아부라)", null, FoodCategory.ABURASOBA, null, null)
        );
        monsterQuestions.add(new Question("monster_q3_maze_abura", "고명 중심인가요, 아니면 기름과 타래 중심인가요?", q3MazeAburaOptions));

        // Q2_soup: 육수의 텐션 / 농도는?
        List<Option> q2SoupOptions = Arrays.asList(
            new Option("A. 깔끔 (청탕)", "monster_q3_clear", FoodCategory.CLEAR_SOUP, null, null),
            new Option("B. 든든 (토리파이탄 / 미소)", "monster_q3_rich", FoodCategory.RICH_SOUP, null, null),
            new Option("C. 혈관 파괴 (하드코어)", "monster_q3_hardcore", FoodCategory.RICH_SOUP, null, null)
        );
        monsterQuestions.add(new Question("monster_q2_soup", "육수의 텐션 / 농도는?", q2SoupOptions));

        // Q3_clear: 맑은 육수의 중심 타래/재료는?
        List<Option> q3ClearOptions = Arrays.asList(
            new Option("소금의 직관적인 쨍함 (시오)", null, null, DetailStyle.SHIO, null),
            new Option("깊은 풍미와 밸런스 (쇼유)", null, null, DetailStyle.SHOYU, null),
            new Option("도미/굴/오리 등 독특한 이색 재료", null, null, null, MainIngredient.SEAFOOD)
        );
        monsterQuestions.add(new Question("monster_q3_clear", "맑은 육수의 중심 타래/재료는?", q3ClearOptions));

        // Q3_rich: 고기 백탕 vs 된장 베이스?
        List<Option> q3RichOptions = Arrays.asList(
            new Option("크리미하게 우려낸 닭 백탕 (파이탄)", null, null, DetailStyle.TORI_PAITAN, null),
            new Option("구수하게 지지는 일본식 된장 (미소)", "monster_q4_miso", null, DetailStyle.MISO, null)
        );
        monsterQuestions.add(new Question("monster_q3_rich", "고기 백탕 vs 된장 베이스?", q3RichOptions));

        // Q4_miso: 미소 라멘의 디테일 취향은?
        List<Option> q4MisoOptions = Arrays.asList(
            new Option("정통 미소의 깊은 구수함", null),
            new Option("카레 풍미가 섞인 독특한 킥", null, null, DetailStyle.CURRY, null)
        );
        monsterQuestions.add(new Question("monster_q4_miso", "미소 라멘의 디테일 취향은?", q4MisoOptions));

        // Q3_hardcore: 바다 풍미 (니보시/교카이) 선호?
        List<Option> q3HardcoreOptions = Arrays.asList(
            new Option("YES (바다파)", "monster_q4_seafood"),
            new Option("NO (고기파)", "monster_q4_meat")
        );
        monsterQuestions.add(new Question("monster_q3_hardcore", "바다 풍미 (니보시/교카이) 선호?", q3HardcoreOptions));

        // Q4_seafood: 기름+짠 타격감 vs 진짜 파괴?
        List<Option> q4SeafoodOptions = Arrays.asList(
            new Option("기름+짠맛의 밸런스 (타격감)", null, null, null, MainIngredient.SEAFOOD),
            new Option("시멘트빛 멸치 진액 (완전파괴)", null, null, null, MainIngredient.SEAFOOD)
        );
        monsterQuestions.add(new Question("monster_q4_seafood", "기름+짠 타격감 vs 진짜 파괴?", q4SeafoodOptions));

        // Q4_meat: 이에케/돈코츠 vs 숙주폭탄 지로계?
        List<Option> q4MeatOptions = Arrays.asList(
            new Option("기름+짠맛의 묵직함 (타격감)", null, null, DetailStyle.IEKEI, null),
            new Option("산더미 숙주와 비계 덩어리 (지로)", null, null, DetailStyle.JIRO, null)
        );
        monsterQuestions.add(new Question("monster_q4_meat", "이에케/돈코츠 vs 숙주폭탄 지로계?", q4MeatOptions));

        themes.add(new Theme("ramen_monster", "라오타의 라멘 추천", "라멘 매니아들을 위한 깊고 매니악한 라멘 추천", "EXPERT", monsterQuestions));

        // 5. 멕시칸 타코 추천
        List<Question> tacoQuestions = new ArrayList<>();

        // taco_q1: 또르띠아 선호도
        List<Option> q1TacoOptions = Arrays.asList(
            new Option("옥수수 또르띠아 (정통 멕시칸의 구수한 옥수수 향과 묵직한 질감)", "taco_q2_authentic", FoodCategory.TACO, DetailStyle.AUTHENTIC, null),
            new Option("밀가루 또르띠아 (텍스멕스/국경식의 부드럽고 쫄깃한 식감)", "taco_q2_texmex", FoodCategory.TACO, DetailStyle.TEX_MEX, null)
        );
        tacoQuestions.add(new Question("taco_q1", "타코의 기본 베이스인 또르띠아(Tortilla) 원료는 어떤 것이 좋은가요?", q1TacoOptions));

        // taco_q2_authentic: 정통 타코 육류 스타일
        List<Option> q2TacoAuthenticOptions = Arrays.asList(
            new Option("라드(Lard)에 오랜 시간 저온 조리하거나 화로 직화한 돼지고기 (까르니따스/알빠스또르)", "taco_q3_authentic_pork"),
            new Option("건고추 향신료와 함께 푹 삶아내어 육즙이 풍부한 소고기 (바르바코아/비리아)", "taco_q3_authentic_beef"),
            new Option("살사와 이색 소스(몰레)를 곁들인 부드러운 닭고기 (치킨)", null, null, null, MainIngredient.CHICKEN)
        );
        tacoQuestions.add(new Question("taco_q2_authentic", "정통 옥수수 타코에 들어갈 메인 고기의 익힘 스타일은?", q2TacoAuthenticOptions));

        // taco_q3_authentic_pork: 돼지고기 부위 및 정통성 상세
        List<Option> q3TacoAuthenticPorkOptions = Arrays.asList(
            new Option("돼지 부속(위, 혀, 껍데기 등)을 포함하여 현지 풍미를 극대화한 내장 부위", null, null, null, MainIngredient.PORK),
            new Option("크리스피 오겹살이나 수직 회전 화로(Trompo)로 구워 대중적인 살코기 부위", null, null, null, MainIngredient.PORK)
        );
        tacoQuestions.add(new Question("taco_q3_authentic_pork", "선호하시는 돼지고기 타코의 세부 부위와 질감은?", q3TacoAuthenticPorkOptions));

        // taco_q3_authentic_beef: 소고기 세부 가이드
        List<Option> q3TacoAuthenticBeefOptions = Arrays.asList(
            new Option("고추 육수에 고아낸 소고기를 치즈와 굽고 진한 콘소메 스프에 찍어 먹는 비리아", null, null, null, MainIngredient.BEEF),
            new Option("전통 공법의 수제 맷돌 또르띠아와 특수 부위(소혀 등)를 다루는 다이닝 스타일", null, null, null, MainIngredient.BEEF)
        );
        tacoQuestions.add(new Question("taco_q3_authentic_beef", "소고기 타코 중 원하시는 조리 방식과 다이닝 성향은?", q3TacoAuthenticBeefOptions));

        // taco_q2_texmex: 텍스멕스 메인 재료
        List<Option> q2TacoTexMexOptions = Arrays.asList(
            new Option("바삭한 흰살 생선 또는 새우 튀김에 상큼한 양배추 슬로우 (바하 스타일)", null, null, null, MainIngredient.SEAFOOD),
            new Option("그릴에 구운 소고기 스테이크(아사다)와 멜팅 치즈, 사워크림 (비프/퀘사디아)", null, null, null, MainIngredient.BEEF)
        );
        tacoQuestions.add(new Question("taco_q2_texmex", "밀가루 또르띠아 타코에 올릴 선호 고명은 무엇인가요?", q2TacoTexMexOptions));

        themes.add(new Theme("taco_lover", "멕시칸 타코 추천", "정통 멕시칸부터 텍스멕스까지 완벽한 타코 매칭", "EXPERT", tacoQuestions));

        // 6. 빵집 추천 (프로토타입: 텍스트 입력 분기점 적용)
        List<Question> bakeryQuestions = new ArrayList<>();

        List<Option> q1BakeryOptions = Arrays.asList(
            new Option("나의 현재 위치 주변 빵집 📍", InputType.TEXT_INPUT, "LOCATION"),
            new Option("내가 가고 싶은 동네의 빵집 🗺️", InputType.TEXT_INPUT, "LOCATION"),
            new Option("내가 먹고 싶은 빵 종류로 찾기 🥐", InputType.TEXT_INPUT, "BREAD")
        );
        bakeryQuestions.add(new Question("bakery_q1", "어떤 방식으로 빵집을 추천받고 싶으신가요?", q1BakeryOptions));

        themes.add(new Theme("bakery_recommend", "빵집 추천", "전국 최고 빵지순례 핫플 21곳을 취향과 위치에 맞게 추천", "DESSERT", bakeryQuestions));

        // 7. 카페 추천 (객관식 목적 선택 -> 텍스트 입력 하이브리드)
        List<Question> cafeQuestions = new ArrayList<>();

        List<Option> q2CafeDriveOptions = Arrays.asList(new Option("검색할 지역을 입력해주세요 🚗", InputType.TEXT_INPUT, "CAFE_SEARCH_DRIVE"));
        cafeQuestions.add(new Question("cafe_q_drive", "원하시는 지역이나 키워드를 검색해주세요.", q2CafeDriveOptions));

        List<Option> q2CafeStudyOptions = Arrays.asList(new Option("검색할 동네를 입력해주세요 💻", InputType.TEXT_INPUT, "CAFE_SEARCH_STUDY"));
        cafeQuestions.add(new Question("cafe_q_study", "어느 동네 주변에서 작업하실 건가요?", q2CafeStudyOptions));

        List<Option> q2CafeVibeOptions = Arrays.asList(new Option("검색할 지역을 입력해주세요 📸", InputType.TEXT_INPUT, "CAFE_SEARCH_VIBE"));
        cafeQuestions.add(new Question("cafe_q_vibe", "어느 지역의 감성 카페를 원하시나요?", q2CafeVibeOptions));

        List<Option> q2CafeCoffeeOptions = Arrays.asList(new Option("검색할 지역을 입력해주세요 ☕", InputType.TEXT_INPUT, "CAFE_SEARCH_COFFEE"));
        cafeQuestions.add(new Question("cafe_q_coffee", "어디 근처의 커피 맛집을 찾아볼까요?", q2CafeCoffeeOptions));

        List<Option> q1CafeOptions = Arrays.asList(
            new Option("드라이브 겸 탁 트인 외곽 나들이 🚗", "cafe_q_drive"),
            new Option("노트북 들고 집중하기 좋은 카공/작업 💻", "cafe_q_study"),
            new Option("사진 찍기 좋은 예쁜 감성 분위기 📸", "cafe_q_vibe"),
            new Option("무조건 커피 맛! 스페셜티 로스터리 탐방 ☕", "cafe_q_coffee")
        );
        cafeQuestions.add(new Question("cafe_q1", "오늘 카페를 방문하시는 가장 큰 목적은 무엇인가요?", q1CafeOptions));

        themes.add(new Theme("cafe_recommend", "카페 매칭 테스트", "목적(카공, 데이트, 드라이브)에 맞는 완벽한 카페 큐레이션", "DESSERT", cafeQuestions));

        themeRepository.saveAll(themes);
        System.out.println(">> Seeded themes, questions, and partition-based decision logic successfully!");
    }
}
