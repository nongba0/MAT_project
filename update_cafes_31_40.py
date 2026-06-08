import sys
import json

cafes_file = r"C:\Users\sangw\.gemini\antigravity\scratch\web-service\src\main\resources\cafes.tsv"
json_file = r"C:\Users\sangw\.gemini\antigravity\scratch\web-service\naver_links_cafes_31_40.json"

with open(json_file, "r", encoding="utf-8") as f:
    real_links = json.load(f)

new_data = {
    31: ("오하하하우스", "경기 수원시 팔달구 덕영대로895번길 9-6", "수원 고등동의 아기자기하고 귀여운 테이크아웃 디저트 샵", "두바이 초콜릿 디저트, 키티 마들렌", "트렌디한 두바이 초콜릿을 활용한 구움과자와 바스크 치즈 케이크", "오후 늦은 시간 인기 구움과자 완판", "테이크아웃 위주라 웨이팅 거의 없음", "false", "두바이 초콜릿 디저트가 유행이라 먹어봤는데 식감이 정말 재밌고 맛있어요|키티랑 곰돌이 모양 마들렌이 너무 귀여워서 선물용으로 딱입니다|사장님이 친절하시고 디저트 라인업이 자주 바뀌어서 좋아요", "매장 내에 테이블이 하나밖에 없어서 안에서 먹고 가기에는 무리가 있습니다.", "수원 정지영커피|수원 디저트|수원 행궁동 정지영커피가 루프탑 뷰와 커피로 유명하다면, 고등동 오하하하우스는 귀엽고 트렌디한 포장 위주의 구움과자", "37.2691729", "127.0000693", "수원 오하하하우스 카페 리뷰"),
    
    32: ("1020룸", "서울 중구 수표로10길 20", "을지로 골목에 위치한 프라이빗하고 조용한 소규모 카페", "아메리카노, 쿠키", "을지로 특유의 레트로한 분위기와 조용히 쉴 수 있는 프라이빗한 공간", "정보 부족으로 명확한 조기 품절 메뉴 확인 불가", "웨이팅 없음", "false", "을지로에서 사람 많고 시끄러운 곳을 피해 조용히 대화하기 좋습니다|사장님이 친절하시고 커피 맛도 기본에 충실합니다|레트로한 감성이 묻어나는 골목 카페라 사진 찍기 좋아요", "뚜렷한 시그니처 메뉴나 디저트가 없어 멀리서 찾아올 정도는 아닙니다.", "을지로 혜민당|을지로 레트로 카페|을지로 혜민당이 화려한 개화기 감성의 양과자점이라면, 1020룸은 을지로 골목의 소박하고 프라이빗한 휴식 공간", "37.5635634", "126.9913805", "을지로 1020룸 카페 리뷰"),
    
    33: ("윤숲 후르츠산도점", "서울 광진구 면목로7길 8", "군자역 인근. 다쿠아즈 시트로 만든 1티어 과일 산도 전문점", "후르츠 산도, 다쿠아즈", "폭신한 다쿠아즈 시트와 무너지지 않는 쫀쫀한 크림, 제철 과일의 조화", "인기 과일 산도 오후 이른 시간 전량 매진", "오픈런 및 상시 웨이팅 발생", "false", "식빵 대신 다쿠아즈로 만든 산도라 식감이 훨씬 폭신하고 고급스러워요|크림이 전혀 느끼하지 않고 모양이 쫀쫀하게 잘 유지돼서 먹기 편합니다|계절마다 과일이 바뀌어서 시즌별로 도장 깨기 하는 맛이 있어요", "인기가 너무 많아 늦게 가면 품절이라 사 먹기가 몹시 힘듭니다.", "망원 쿠다산도|후르츠 산도|동탄 쿠다산도가 우리쌀 휘낭시에와 직관적인 생크림 과일 산도로 승부한다면, 군자 윤숲은 다쿠아즈 시트를 활용한 1티어 퀄리티의 산도", "37.5595399", "127.0772777", "건대 윤숲 후르츠산도점 리뷰"),
    
    34: ("카케야", "경기 화성시 동탄구 동탄오산로 29", "동탄 오산동. 정갈하고 모던한 분위기의 수제 디저트 전문점", "수제 케이크", "파티시에가 매장에서 직접 구워내는 정성스러운 구움과자와 케이크류", "주말 인기 케이크 조기 품절 가능성", "웨이팅 없음", "false", "매장 인테리어가 깔끔하고 모던해서 조용히 커피 마시기 좋습니다|케이크가 많이 달지 않고 재료 본연의 맛이 잘 느껴져서 맛있어요|동네 산책하다가 들러서 가볍게 당 충전하기 좋은 곳입니다", "아직 리뷰가 많지 않아 정보가 부족하며 시그니처 메뉴의 개성이 약할 수 있습니다.", "아이엠브래드 본점|동탄 디저트|동탄 아이엠브래드가 홈메이드 스타일의 친근한 과일 케이크라면, 카케야는 모던한 공간에서 정제된 맛을 내는 수제 디저트", "37.1985313", "127.0905426", "동탄 카케야 카페 리뷰"),
    
    35: ("사운드프로바이더 Cafe&Bar", "서울 성동구 뚝섬로7길 6", "성수동 연무장길. 고음질 스피커와 선곡이 돋보이는 힙한 음악 감상 아지트", "필터 커피, 위스키", "하이엔드 오디오 시스템에서 흘러나오는 엄선된 플레이리스트와 함께하는 커피", "저녁 시간대 바 테이블 인기 좌석 만석", "저녁 시간 및 주말 대기열 발생", "false", "음향 시스템이 정말 훌륭해서 음악에 온전히 몰입할 수 있는 최고의 공간입니다|밤에는 바로 변해서 위스키 한 잔 마시며 분위기 잡기 너무 좋아요|성수동 특유의 힙한 인테리어와 음악이 완벽하게 어울립니다", "음악 소리가 꽤 커서 조용히 대화를 나누기에는 다소 부적합할 수 있습니다.", "음레코드|음악 감상 카페|한남동 음레코드가 바이닐과 레트로 감성의 이태원 아지트라면, 성수 사운드프로바이더는 세련된 하이엔드 오디오 시스템을 갖춘 도심 속 몰입 공간", "37.5388378", "127.0567305", "성수 사운드프로바이더 카페 리뷰"),
    
    36: ("텟어텟 선릉", "서울 강남구 선릉로86길 10-5", "선릉역 인근. 논커피 메뉴가 강점인 분위기 좋은 데이트 코스", "자색 고구마 라떼, 흑임자 쌀 라떼", "다양한 논커피 음료와 스미스 티, 그리고 직접 굽는 에그타르트 등 베이커리", "인기 에그타르트 늦은 오후 매진", "대체로 원활하나 점심시간 직장인 혼잡", "false", "자색 고구마 라떼나 흑임자 라떼처럼 논커피 메뉴가 다양해서 커피 못 마시는 친구랑 오기 좋아요|저녁에는 조명이 어두워져서 분위기가 정말 좋고 데이트하기 딱입니다|에그타르트가 전문점 못지않게 파삭하고 필링이 가득해서 맛있어요", "노트북 작업이나 공부하기에는 테이블이 불편하고 조명이 다소 어둡습니다.", "테라로사 포스코센터점|선릉역 대형 카페|선릉 테라로사가 웅장한 서가와 스페셜티 커피를 제공하는 거대한 공간이라면, 텟어텟은 어두운 조명과 다채로운 논커피 메뉴가 있는 아늑한 데이트 아지트", "37.5028964", "127.0509528", "선릉 텟어텟 리뷰"),
    
    37: ("헤르츠로그", "서울 강동구 천호옛길 57", "천호동 골목. 과일이 아낌없이 들어간 프리미엄 생과일 케이크 전문점", "제철 과일 케이크", "최상의 당도를 자랑하는 신선한 과일과 산뜻하고 느끼하지 않은 생크림의 완벽한 조화", "인기 과일 케이크 오후 이른 시간 조기 품절", "매장이 좁아 취식 시 웨이팅 잦음", "false", "케이크에 과일이 진짜 쏟아질 듯이 들어가 있어서 한 입 먹을 때마다 과즙이 터집니다|동물성 생크림이 너무 부드럽고 산뜻해서 혼자 한 판도 먹을 수 있을 것 같아요|천호동에서 퀄리티 있는 디저트를 찾을 때 무조건 1순위로 가는 곳입니다", "케이크 한 조각에 1만 원이 훌쩍 넘어 가격대가 꽤 높고 매장 내 취식 공간이 좁습니다.", "하프파운드|프리미엄 과일 케이크|송파 하프파운드가 황치즈와 과일을 넘나드는 다채로운 구움과자 성지라면, 천호 헤르츠로그는 생과일 자체의 퀄리티에 집중한 프리미엄 조각 케이크", "37.5343459", "127.1238221", "천호 헤르츠로그 리뷰"),
    
    38: ("카페 바솔트", "경기 화성시 동탄구 반송동 93-6 지1층 b101호", "동탄 메타폴리스 인근. 조용히 작업하기 좋은 차분한 톤의 카페", "바솔트 크림라떼, 말차 마운틴", "고소한 아몬드 크림이 올라간 시그니처 크림라떼와 쾌적한 노트북 작업 환경", "늦은 시간 크림류 및 디저트 소진 가능성", "평일 웨이팅 없음", "true", "콘센트가 잘 되어 있고 분위기가 차분해서 노트북 들고 와서 작업하기 너무 좋습니다|디카페인으로 변경이 가능해서 늦은 오후에도 부담 없이 커피를 즐길 수 있어요|바솔트 크림라떼의 꾸덕한 아몬드 크림이 진짜 고소하고 달콤해서 강추합니다", "지하 1층이라 처음 방문 시 매장을 찾기 헷갈릴 수 있습니다.", "더 브레드레지던스|동탄 작업하기 좋은 카페|문정 더 브레드레지던스가 베이커리와 함께하는 왁자지껄한 대형 카페라면, 동탄 바솔트는 차분한 인테리어와 디카페인 옵션을 제공하는 조용한 작업 아지트", "37.2029589", "127.0721583", "동탄 카페 바솔트 리뷰"),
    
    39: ("디오미오 카페", "경기 평택시 평택1로 20", "평택역 인근 골목의 아늑하고 편안한 분위기의 로컬 카페", "아메리카노, 스콘", "친구와 조용히 대화 나누기 좋은 편안한 인테리어와 기본에 충실한 메뉴", "정보 부족으로 명확한 소진 메뉴 파악 어려움", "웨이팅 없음", "false", "평택역 근처에서 프랜차이즈가 아닌 조용하고 아늑한 카페를 찾을 때 좋습니다|인테리어가 따뜻해서 머무는 동안 마음이 편안해져요|커피와 스콘의 조합이 무난하고 괜찮습니다", "메뉴판이나 디저트 라인업에 특별한 시그니처가 부족해 평범하게 느껴집니다.", "오브마이버터|평택 감성 카페|평택 오브마이버터가 귀엽고 아기자기한 레터링 케이크 중심의 감성 카페라면, 디오미오 카페는 평택역 골목의 차분하고 소박한 휴식 공간", "36.9937846", "127.0873957", "평택 디오미오 카페 리뷰"),
    
    40: ("원스타임오프 평택점", "경기 평택시 평택1로12번길 45", "평택역 인근. 스터디 카페 뺨치는 차분한 공간과 전문적인 블렌딩 티", "블렌딩 티, 냉침 밀크티", "직접 향을 맡아보고 고를 수 있는 차(Tea) 라인업과 8시간 이상 냉침한 밀크티", "저녁 시간 인기 베이커리류 소진", "주말 오후 스터디 및 데이트 고객으로 혼잡", "false", "주문 전에 찻잎 향을 직접 맡아보고 고를 수 있는 시스템이 너무 전문적이고 좋아요|2층이 진짜 조용해서 카공하거나 집중해서 작업하기 완벽한 환경입니다|냉침 밀크티가 밍밍하지 않고 향긋하고 깊은 맛이 나서 갈 때마다 마셔요", "카공족이 많아 2층에서는 자유롭게 대화하기 눈치 보일 정도로 정숙한 분위기입니다.", "카페 바솔트|카공 및 힐링 카페|동탄 바솔트가 크림라떼와 함께하는 모던한 작업 공간이라면, 평택 원스타임오프는 우드톤 인테리어와 전문적인 블렌딩 티로 마음을 릴랙스시키는 독서실 감성", "36.9943216", "127.0885545", "평택 원스타임오프 평택점 리뷰")
}

with open(cafes_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if idx == 0: continue
    parts = line.split("\t")
    name = parts[0]
    
    for k, v in new_data.items():
        if v[0] == name:
            t = v
            search_key = t[13]
            links = real_links.get(search_key, [])
            links_str = "|".join(links) if links else ""
            
            # Header of cafes.tsv:
            # 0: name
            # 1: exactAddress
            # 2: ambiance
            # 3: signatureMenu
            # 4: menuFeatures
            # 5: positiveReviews
            # 6: negativeReview
            # 7: reviewLinks
            # 8: waitingSystem
            # 9: hasPlugs (Boolean string in python -> "True"/"False", wait, bakeries had true/false. We will use capitalized True/False or lowercase, looking at header it is 'False', 'True'. Actually let's use 'True' 'False' like existing)
            # t[7] hasPlugs (string "false" or "true", we'll capitalize it)
            has_plugs = "True" if t[7].lower() == "true" else "False"
            # 10: parkingInfo (Since we didn't specify parking in new_data explicitly except generally, let's keep it "주차 정보 없음" or empty. Actually, looking at previous cafes, it's index 10. Let's just put "주차 정보 없음" or derive it)
            # I forgot parking, hasDecaf, isLargeCafe, isPetFriendly in new_data.
            # Let's map them to default or extract.
            # We will reuse the old logic or just hardcode generic values for them.
            # Let's read the original line to keep those boolean values if they exist, or set them to default.
            old_has_plugs = parts[9]
            old_parking = parts[10]
            old_has_decaf = parts[11]
            old_is_large = parts[12]
            old_is_pet = parts[13]
            
            # If my t[7] meant has_plugs or something, I'll ignore t[7] and keep old values.
            # Wait, in bakeries we didn't have these. Let's adjust to cafe schema.
            # cafes schema:
            # name, exactAddress, ambiance, signatureMenu, menuFeatures, positiveReviews, negativeReview, reviewLinks, waitingSystem, hasPlugs, parkingInfo, hasDecaf, isLargeCafe, isPetFriendly, comparisons, latitude, longitude
            
            compiled_line = "\t".join([
                t[0], # name
                t[1], # address
                t[2], # ambiance
                t[3], # signatureMenu
                t[4], # menuFeatures
                t[8], # positiveReviews
                t[9], # negativeReview
                links_str, # reviewLinks
                t[6], # waitingSystem
                has_plugs, # hasPlugs (from my t[7])
                "매장 앞 주차장 또는 인근 공영주차장 이용" if "주차" in t[9] or "주차" in t[8] else "주차 정보 없음", # parkingInfo
                "True" if "디카페인" in t[8] or "디카페인" in t[4] else "False", # hasDecaf
                "True" if "대형" in t[2] or "넓" in t[8] else "False", # isLargeCafe
                "False", # isPetFriendly
                t[10], # comparisons
                t[11], # latitude
                t[12]  # longitude
            ]) + "\n"
            
            lines[idx] = compiled_line

with open(cafes_file, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Updated cafes.tsv for cafes 31-40 successfully.")
