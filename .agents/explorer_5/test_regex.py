import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

def test_extract():
    corpus = "여기 소금빵이랑 바닐라라떼가 저희 카페의 시그니처 메뉴입니다. 캐치테이블로 예약 가능해요."
    common_items = ["라떼", "아메리카노", "크로플", "스콘", "케이크", "소금빵", "마카롱", "빙수", "에스프레소", "밀크티", "크루아상", "드립커피", "디카페인", "베이글", "샌드위치"]
    
    sig_menu = "정보 없음"
    match = re.search(r'(.{0,15})(시그니처|대표|인기)(.{0,15})', corpus)
    if match:
        context = match.group(0)
        found = [item for item in common_items if item in context]
        if found:
            sig_menu = found[0]
    if sig_menu == "정보 없음":
        found = [item for item in common_items if item in corpus]
        if found:
            sig_menu = found[0]
            
    print("SIG_MENU:", sig_menu)
    
test_extract()
