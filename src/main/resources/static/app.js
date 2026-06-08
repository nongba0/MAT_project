// API Base URL (동일 오리진인 경우 상대 경로 사용)
const API_BASE = '/api';

// 상태 관리 변수
let themes = [];
let allRestaurants = [];
let currentTheme = null;
let currentQuestion = null;
let accumulatedPreferences = {
    foodCategory: null,
    detailStyle: null,
    mainIngredient: null
};
let questionsMap = new Map();
let quizStepCount = 0;
let quizHistory = []; // { question: Question, accumulatedPreferences: Object }



// DOM 엘리먼트
const views = {
    theme: document.getElementById('theme-view'),
    quiz: document.getElementById('quiz-view'),
    result: document.getElementById('result-view')
};

const themeList = document.getElementById('theme-list');
const questionText = document.getElementById('question-text');
const optionsList = document.getElementById('options-list');
const questionIdBadge = document.getElementById('question-id-badge');
const progressIndicator = document.getElementById('progress-indicator');
const accumulatedTagsContainer = document.getElementById('accumulated-tags');
const shopsList = document.getElementById('shops-list');
const btnBackQuestion = document.getElementById('btn-back-question');
const shopsTitle = document.getElementById('shops-title');

// 버튼 이벤트 바인딩
document.getElementById('btn-back-to-themes').addEventListener('click', resetQuiz);
btnBackQuestion.addEventListener('click', handleBackQuestion);
document.getElementById('btn-retry').addEventListener('click', () => {
    if (currentTheme) {
        startTheme(currentTheme.id);
    } else {
        resetQuiz();
    }
});

// 초기 구동
window.addEventListener('DOMContentLoaded', init);

async function init() {
    try {
        const [themesResponse, restaurantsResponse] = await Promise.all([
            fetch(`${API_BASE}/themes`),
            fetch(`${API_BASE}/restaurants`)
        ]);
        
        if (!themesResponse.ok) throw new Error('테마 목록을 불러오지 못했습니다.');
        if (!restaurantsResponse.ok) throw new Error('맛집 목록을 불러오지 못했습니다.');
        
        themes = await themesResponse.json();
        allRestaurants = await restaurantsResponse.json();
        
        renderThemes(themes);
    } catch (error) {
        console.error(error);
        themeList.innerHTML = `<div class="no-results">오류가 발생했습니다: ${error.message}</div>`;
    }
}

// 1. 테마 렌더링
function renderThemes(themesList) {
    if (themesList.length === 0) {
        themeList.innerHTML = '<div class="no-results">등록된 테마가 없습니다.</div>';
        return;
    }

    themeList.innerHTML = '';

    // GENERAL 테마, EXPERT 테마, DESSERT 테마로 그룹화
    const generalThemes = themesList.filter(t => t.category === 'GENERAL' || !t.category);
    const expertThemes = themesList.filter(t => t.category === 'EXPERT');
    const dessertThemes = themesList.filter(t => t.category === 'DESSERT');

    // 일반 맛집 매칭 테마 섹션
    if (generalThemes.length > 0) {
        const generalHeader = document.createElement('h3');
        generalHeader.className = 'category-title';
        generalHeader.innerHTML = '오늘 뭐먹지? 맛집 매칭 테마';
        themeList.appendChild(generalHeader);

        const generalContainer = document.createElement('div');
        generalContainer.className = 'grid-container';
        generalThemes.forEach(theme => {
            const card = createThemeCard(theme);
            generalContainer.appendChild(card);
        });
        themeList.appendChild(generalContainer);
    }

    // 디저트 추천 테마 섹션
    if (dessertThemes.length > 0) {
        const dessertHeader = document.createElement('h3');
        dessertHeader.className = 'category-title';
        dessertHeader.innerHTML = '🍰 달콤한 디저트 추천 테마';
        themeList.appendChild(dessertHeader);

        const dessertContainer = document.createElement('div');
        dessertContainer.className = 'grid-container';
        dessertThemes.forEach(theme => {
            const card = createThemeCard(theme);
            dessertContainer.appendChild(card);
        });
        themeList.appendChild(dessertContainer);
    }

    // 전문가 취향 매칭 테마 섹션
    if (expertThemes.length > 0) {
        const expertHeader = document.createElement('h3');
        expertHeader.className = 'category-title';
        expertHeader.innerHTML = '🍜 찐 전문가를 위한 맛집';
        themeList.appendChild(expertHeader);

        const expertContainer = document.createElement('div');
        expertContainer.className = 'grid-container';
        expertThemes.forEach(theme => {
            const card = createThemeCard(theme);
            expertContainer.appendChild(card);
        });
        themeList.appendChild(expertContainer);
    }
}

function createThemeCard(theme) {
    const card = document.createElement('div');
    card.className = 'theme-card';
    card.innerHTML = `
        <div class="theme-title">${escapeHtml(theme.title)}</div>
        <div class="theme-desc">${escapeHtml(theme.description || '이 테마에 대한 설명이 없습니다.')}</div>
    `;
    card.addEventListener('click', () => startTheme(theme.id));
    return card;
}

// 2. 퀴즈 시작
function startTheme(themeId) {
    currentTheme = themes.find(t => t.id === themeId);
    if (!currentTheme || !currentTheme.questions || currentTheme.questions.length === 0) {
        alert('이 테마에는 질문이 존재하지 않습니다.');
        return;
    }

    // 질문 매핑 및 상태 초기화
    questionsMap.clear();
    currentTheme.questions.forEach(q => {
        questionsMap.set(q.id, q);
    });

    accumulatedPreferences = {
        foodCategory: null,
        detailStyle: null,
        mainIngredient: null
    };
    quizHistory = [];
    quizStepCount = 0;
    
    // 첫 질문 가져오기 (보통 id가 _q1 로 끝나거나 리스트의 첫 번째 항목)
    let firstQuestion = currentTheme.questions[0];
    const q1Candidate = currentTheme.questions.find(q => q.id.endsWith('_q1'));
    if (q1Candidate) {
        firstQuestion = q1Candidate;
    }

    showView('quiz');
    renderQuestion(firstQuestion);
}

// 3. 질문 렌더링
function renderQuestion(question) {
    currentQuestion = question;
    quizStepCount = quizHistory.length + 1;

    questionIdBadge.textContent = `Question ${quizStepCount}`;
    questionText.textContent = question.questionText;

    // 이전 질문 버튼 표시 여부
    if (quizHistory.length > 0) {
        btnBackQuestion.style.display = 'block';
    } else {
        btnBackQuestion.style.display = 'none';
    }

    // 진행률 업데이트 (동적 트리이므로 대략적인 게이지 표시)
    let progress = Math.min((quizStepCount / 4) * 100, 95); 
    progressIndicator.style.width = `${progress}%`;

    optionsList.style.display = 'flex';
    document.getElementById('text-input-container').style.display = 'none';
    optionsList.innerHTML = '';
    question.options.forEach(option => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.textContent = option.text;
        btn.addEventListener('click', () => selectOption(option));
        optionsList.appendChild(btn);
    });
}

// 4. 선택지 선택
function selectOption(option) {
    // 현재 상태를 히스토리에 저장
    quizHistory.push({
        question: currentQuestion,
        accumulatedPreferences: { ...accumulatedPreferences }
    });

    if (option.inputType === 'TEXT_INPUT') {
        const textContainer = document.getElementById('text-input-container');
        const keywordInput = document.getElementById('keyword-input');
        const btnSearch = document.getElementById('btn-search');
        
        optionsList.style.display = 'none';
        textContainer.style.display = 'flex';
        
        let placeholder = '검색어를 입력하세요';
        if (option.filterType === 'LOCATION') {
            placeholder = '시/구/동을 입력하세요 (예: 마포구, 연남동)';
        } else if (option.filterType === 'BREAD') {
            placeholder = '빵 이름을 입력하세요 (예: 소금빵, 베이글)';
        } else if (option.filterType.startsWith('CAFE_SEARCH')) {
            placeholder = '지역명(예: 성수, 파주) 또는 매장명을 입력하세요';
        }
        keywordInput.placeholder = placeholder;
        keywordInput.value = '';
        keywordInput.focus();

        const newBtnSearch = btnSearch.cloneNode(true);
        btnSearch.parentNode.replaceChild(newBtnSearch, btnSearch);
        
        newBtnSearch.addEventListener('click', () => {
            const keyword = keywordInput.value.trim();
            if (!keyword) {
                alert('검색어를 입력해주세요.');
                return;
            }
            
            if (option.filterType.startsWith('CAFE_SEARCH')) {
                fetchCafeMatch(option.filterType, keyword);
            } else {
                fetchBakeryMatch(option.filterType, keyword);
            }
        });
        
        keywordInput.onkeyup = function(e) {
            if (e.key === 'Enter') {
                newBtnSearch.click();
            }
        };
        
        return;
    }

    // 프리퍼런스 누적
    if (option.foodCategory) {
        accumulatedPreferences.foodCategory = option.foodCategory;
    }
    if (option.detailStyle) {
        accumulatedPreferences.detailStyle = option.detailStyle;
    }
    if (option.mainIngredient) {
        accumulatedPreferences.mainIngredient = option.mainIngredient;
    }

    console.log(`선택됨: ${option.text}, 누적 취향:`, accumulatedPreferences);

    // 다음 라우팅
    if (option.nextQuestionId) {
        const nextQ = questionsMap.get(option.nextQuestionId);
        if (nextQ) {
            renderQuestion(nextQ);
        } else {
            console.error(`다음 질문 ID를 찾을 수 없습니다: ${option.nextQuestionId}`);
            showResults();
        }
    } else {
        // 단말 노드 도달 -> 결과 화면
        showResults();
    }
}

// 4-1. 이전 질문으로 돌아가기
function handleBackQuestion() {
    if (quizHistory.length === 0) return;
    
    const prevState = quizHistory.pop();
    accumulatedPreferences = prevState.accumulatedPreferences;
    renderQuestion(prevState.question);
}

// 5. 결과 화면 출력
const PREFERENCE_TAGS = {
    'CLEAR_SOUP': '#맑은국물',
    'RICH_SOUP': '#진한국물',
    'MAJESOBA': '#마제소바',
    'ABURASOBA': '#아부라소바',
    'TSUKEMEN': '#츠케멘',
    'JEON': '#전',
    'TACO': '#타코',
    'SHIO': '#시오',
    'SHOYU': '#쇼유',
    'MISO': '#미소',
    'IEKEI': '#이에케',
    'JIRO': '#지로계',
    'AUTHENTIC': '#정통멕시칸',
    'TEX_MEX': '#텍스멕스',
    'TONKOTSU': '#돈코츠',
    'TORI_PAITAN': '#토리파이탄',
    'CURRY': '#카레',
    'CHUKA_SOBA': '#중화소바',
    'FUSION': '#퓨전',
    'KALGUKSU': '#칼국수',
    'SUJEBI': '#수제비',
    'GUKBAP': '#국밥',
    'JJIGAE': '#찌개전골',
    'CHICKEN': '#닭',
    'PORK': '#돼지',
    'SEAFOOD': '#해산물',
    'BEEF': '#소고기',
    'PORK_BONE': '#돼지등뼈',
    'SUNDAE': '#순대',
    'AMUK': '#어묵',
    'HAM_SAUSAGE': '#햄소시지',
    'CHIVE': '#부추',
    'SCALLION': '#쪽파',
    'KIMCHI': '#김치',
    'POTATO': '#감자',
    'MUNG_BEAN': '#녹두'
};

async function showResults() {
    progressIndicator.style.width = '100%';
    showView('result');

    // 태그 리스트 영역 렌더링
    accumulatedTagsContainer.innerHTML = '';
    const activeTags = [];

    if (accumulatedPreferences.foodCategory) {
        activeTags.push(PREFERENCE_TAGS[accumulatedPreferences.foodCategory] || ('#' + accumulatedPreferences.foodCategory));
    }
    if (accumulatedPreferences.detailStyle && accumulatedPreferences.detailStyle !== 'STANDARD') {
        activeTags.push(PREFERENCE_TAGS[accumulatedPreferences.detailStyle] || ('#' + accumulatedPreferences.detailStyle));
    }
    if (accumulatedPreferences.mainIngredient && accumulatedPreferences.mainIngredient !== 'NONE') {
        activeTags.push(PREFERENCE_TAGS[accumulatedPreferences.mainIngredient] || ('#' + accumulatedPreferences.mainIngredient));
    }

    if (activeTags.length === 0) {
        accumulatedTagsContainer.innerHTML = '<span class="tag-pill">선택된 취향 없음</span>';
    } else {
        activeTags.forEach(tag => {
            const pill = document.createElement('span');
            pill.className = 'tag-pill accent';
            pill.textContent = tag;
            accumulatedTagsContainer.appendChild(pill);
        });
    }
    
    // 음식 카테고리 판별 (메인 타이틀용)
    let resultFoodName = '맛집';
    if (accumulatedPreferences.foodCategory === 'JEON') {
        resultFoodName = '전';
    } else if (accumulatedPreferences.foodCategory === 'TACO') {
        resultFoodName = '타코';
    } else if (accumulatedPreferences.detailStyle === 'GUKBAP') {
        resultFoodName = '국밥';
    } else if (accumulatedPreferences.detailStyle === 'JJIGAE') {
        resultFoodName = '찌개/전골';
    } else if (accumulatedPreferences.detailStyle === 'KALGUKSU') {
        resultFoodName = '칼국수';
    } else if (accumulatedPreferences.detailStyle === 'SUJEBI') {
        resultFoodName = '수제비';
    } else if (currentTheme && currentTheme.id === 'ramen_monster') {
        resultFoodName = '라멘';
    }

    const mainResultTitle = document.getElementById('main-result-title');
    if (mainResultTitle) {
        mainResultTitle.textContent = `당신의 ${resultFoodName} 취향 분석 완료!`;
    }

    // 결과 샵 서브타이틀 텍스트 동적 수정
    if (currentTheme && currentTheme.id === 'rainy_day') {
        shopsTitle.textContent = `비오는 날에 어울리는 추천 ${resultFoodName}`;
    } else if (currentTheme && currentTheme.id === 'ramen_monster') {
        shopsTitle.textContent = '당신에게 매칭된 맛집 추천';
    } else {
        shopsTitle.textContent = `당신에게 매칭된 추천 ${resultFoodName}`;
    }

    // 결과 샵 검색
    shopsList.innerHTML = '<div class="loading">취향에 매칭되는 맛집 검색 중...</div>';
    
    try {
        let filteredShops = allRestaurants;
        
        if (accumulatedPreferences.foodCategory) {
            filteredShops = filteredShops.filter(shop => shop.foodCategory === accumulatedPreferences.foodCategory);
        }
        if (accumulatedPreferences.detailStyle) {
            filteredShops = filteredShops.filter(shop => shop.detailStyle === accumulatedPreferences.detailStyle);
        }
        if (accumulatedPreferences.mainIngredient) {
            filteredShops = filteredShops.filter(shop => shop.mainIngredient === accumulatedPreferences.mainIngredient);
        }
        
        // 검색 결과를 렌더링 (UI 로딩 효과를 자연스럽게 하기 위해 300ms 지연)
        setTimeout(() => {
            renderShops(filteredShops);
        }, 300);
    } catch (error) {
        console.error(error);
        shopsList.innerHTML = `<div class="no-results">오류가 발생했습니다: ${error.message}</div>`;
    }
}

// 6. 결과 라멘 샵 리스트 렌더링
function renderShops(shops) {
    if (shops.length === 0) {
        shopsList.innerHTML = `
            <div class="no-results">
                당신의 취향을 모두 만족하는 완벽한 맛집을 아직 찾지 못했습니다. 😢<br>
                <span style="font-size: 0.85rem; color: #64748b; display:inline-block; margin-top:10px;">다른 조합으로 다시 테스트해 보세요!</span>
            </div>`;
        return;
    }

    shopsList.innerHTML = '';
    shops.forEach(shop => {
        const card = document.createElement('div');
        card.className = 'shop-card';

        let tagsHtml = '';
        if (shop.keywordTags) {
            const tagsArray = shop.keywordTags.split(' ').filter(t => t.trim() !== '');
            tagsHtml = tagsArray.map(t => `<span class="shop-tag">${escapeHtml(t)}</span>`).join(' ');
        }
        
        let descHtml = '';
        if (shop.description) {
            descHtml = `<div class="shop-description" style="font-size: 0.9rem; color: #475569; margin-top: 8px; line-height: 1.4;">${escapeHtml(shop.description)}</div>`;
        }

        const searchQ = shop.name;
        const mapUrl = `https://map.naver.com/p/search/${encodeURIComponent(searchQ)}`;

        let menuHtml = '';
        if (shop.signatureMenus && shop.menuDescription) {
            menuHtml = `
                <div class="menu-info-container">
                    <span class="menu-tooltip-icon" onclick="toggleMenuInfo(this)" title="대표 메뉴 보기">❔</span>
                    <div class="menu-details hidden">
                        <strong>대표 메뉴:</strong> ${escapeHtml(shop.signatureMenus)}<br>
                        <span class="menu-desc">${escapeHtml(shop.menuDescription)}</span>
                    </div>
                </div>
            `;
        }

        card.innerHTML = `
            <div class="shop-header">
                <div class="shop-name-wrapper" style="display: flex; align-items: center; gap: 8px;">
                    <span class="shop-name">${escapeHtml(shop.name)}</span>
                    ${menuHtml}
                </div>
                <a href="${mapUrl}" target="_blank" rel="noopener noreferrer" class="shop-location" title="네이버 지도에서 보기">📍 ${escapeHtml(shop.location)}</a>
            </div>
            ${descHtml}
            <div class="shop-tags" style="margin-top: 10px;">
                ${tagsHtml}
            </div>
        `;
        shopsList.appendChild(card);
    });
}

// 뷰 전환
function showView(viewId) {
    Object.keys(views).forEach(key => {
        if (key === viewId) {
            views[key].classList.add('active');
        } else {
            views[key].classList.remove('active');
        }
    });
}

function resetQuiz() {
    currentTheme = null;
    currentQuestion = null;
    accumulatedPreferences = {
        foodCategory: null,
        detailStyle: null,
        mainIngredient: null
    };
    quizHistory = [];
    showView('theme');
    init(); // 테마 리스트 갱신
}

// HTML 이스케이프 유틸리티
function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// 대표 메뉴 툴팁 토글
window.toggleMenuInfo = function(iconElement) {
    const detailsDiv = iconElement.nextElementSibling;
    if (detailsDiv.classList.contains('hidden')) {
        detailsDiv.classList.remove('hidden');
    } else {
        detailsDiv.classList.add('hidden');
    }
};

window.toggleNegativeReview = function(buttonElement) {
    const contentDiv = buttonElement.nextElementSibling;
    if (contentDiv.classList.contains('show')) {
        contentDiv.classList.remove('show');
        buttonElement.innerHTML = '⚠️ 아쉬운 점 보기';
    } else {
        contentDiv.classList.add('show');
        buttonElement.innerHTML = '⚠️ 숨기기';
    }
};

async function fetchBakeryMatch(searchType, keyword) {
    showView('result');
    const mainResultTitle = document.getElementById('main-result-title');
    if (mainResultTitle) {
        mainResultTitle.textContent = `당신의 빵집 취향 분석 완료!`;
    }
    shopsTitle.textContent = `'${keyword}' (으)로 검색된 빵집 추천`;
    
    accumulatedTagsContainer.innerHTML = '';
    const pill = document.createElement('span');
    pill.className = 'tag-pill accent';
    pill.textContent = searchType === 'LOCATION' ? '#위치검색' : '#빵종류검색';
    accumulatedTagsContainer.appendChild(pill);
    
    shopsList.innerHTML = '<div class="loading">빵집을 검색 중입니다...</div>';

    try {
        const response = await fetch(`${API_BASE}/match/bakery`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ searchType, keyword })
        });

        if (!response.ok) {
            throw new Error('빵집 검색에 실패했습니다.');
        }

        const bakeries = await response.json();
        
        setTimeout(() => {
            renderBakeries(bakeries);
        }, 300);
    } catch (error) {
        console.error(error);
        shopsList.innerHTML = `<div class="no-results">오류가 발생했습니다: ${error.message}</div>`;
    }
}

function renderBakeries(bakeries) {
    if (bakeries.length === 0) {
        shopsList.innerHTML = `
            <div class="no-results">
                해당 조건에 맞는 빵집을 찾지 못했습니다. 😢<br>
                <span style="font-size: 0.85rem; color: #64748b; display:inline-block; margin-top:10px;">다른 검색어로 다시 시도해 보세요!</span>
            </div>`;
        return;
    }

    shopsList.innerHTML = '';
    bakeries.forEach(bakery => {
        const card = document.createElement('div');
        card.className = 'bakery-card';

        const mapUrl = `https://map.naver.com/p/search/${encodeURIComponent(bakery.name)}`;
        
        let opHtml = '';
        if (bakery.operation) {
            opHtml += `<div class="bakery-operation">`;
            if (bakery.operation.waitingSystem) {
                opHtml += `<span class="op-badge">⏳ ${escapeHtml(bakery.operation.waitingSystem)}</span>`;
            }
            if (bakery.operation.soldOutInfo) {
                opHtml += `<span class="op-badge highlight">🔥 ${escapeHtml(bakery.operation.soldOutInfo)}</span>`;
            }
            opHtml += `<span class="op-badge">${bakery.operation.hasDineIn ? '🍽️ 매장 식사 가능' : '🛍️ 포장 전문'}</span>`;
            opHtml += `</div>`;
        }

        let featuresHtml = '';
        if (bakery.storeFeatures) {
            featuresHtml = `<div class="bakery-features"><strong>✨ 매장 특징:</strong><br>${escapeHtml(bakery.storeFeatures)}</div>`;
        }

        let reviewHtml = '';
        if (bakery.positiveReviews || bakery.negativeReview) {
            reviewHtml += `<div class="review-section">`;
            if (bakery.positiveReviews) {
                // Split positive reviews by pipe symbol and render as bullets
                const reviews = bakery.positiveReviews.split('|').map(r => r.trim()).filter(r => r.length > 0);
                const reviewBullets = reviews.map(r => `• ${escapeHtml(r)}`).join('<br>');
                reviewHtml += `<div class="positive-review"><strong>👍 긍정적 리뷰 요약:</strong><br>${reviewBullets}</div>`;
            }
            if (bakery.negativeReview) {
                reviewHtml += `
                    <div class="negative-review-wrapper">
                        <button class="negative-review-toggle" onclick="toggleNegativeReview(this)">⚠️ 아쉬운 점 보기</button>
                        <div class="negative-review-content">${escapeHtml(bakery.negativeReview)}</div>
                    </div>
                `;
            }
            reviewHtml += `</div>`;
        }

        let comparisonHtml = '';
        if (bakery.comparisons && bakery.comparisons.length > 0) {
            comparisonHtml += `<div class="comparison-section"><strong>💡 타 빵집 비교:</strong>`;
            bakery.comparisons.forEach(comp => {
                comparisonHtml += `<div class="comparison-item">- [${escapeHtml(comp.targetBakeryName)}] ${escapeHtml(comp.aspect)}: ${escapeHtml(comp.description)}</div>`;
            });
            comparisonHtml += `</div>`;
        }

        card.innerHTML = `
            <div class="shop-header">
                <div class="shop-name-wrapper" style="display: flex; flex-direction: column; gap: 4px;">
                    <span class="shop-name">${escapeHtml(bakery.name)}</span>
                    <span style="font-size: 0.9rem; color: #d97706; font-weight: 600;">👑 시그니처: ${escapeHtml(bakery.signatureMenu)}</span>
                </div>
                <a href="${mapUrl}" target="_blank" rel="noopener noreferrer" class="shop-location" title="네이버 지도에서 보기" style="align-self: flex-start;">📍 지도보기</a>
            </div>
            ${opHtml}
            ${featuresHtml}
            <div style="font-size: 0.9rem; color: #475569; margin-top: 12px; line-height: 1.5;">
                <strong>🥐 메뉴 특징:</strong><br>${escapeHtml(bakery.menuFeatures)}
            </div>
            ${comparisonHtml}
            ${reviewHtml}
        `;
        shopsList.appendChild(card);
    });
}

// ==========================================
// 카페 렌더링 로직 추가
// ==========================================
async function fetchCafeMatch(searchType, keyword) {
    showView('result');
    const mainResultTitle = document.getElementById('main-result-title');
    if (mainResultTitle) {
        mainResultTitle.textContent = `당신의 카페 취향 분석 완료!`;
    }
    shopsTitle.textContent = `'${keyword}' (으)로 검색된 카페 추천`;
    
    accumulatedTagsContainer.innerHTML = '';
    const pill = document.createElement('span');
    pill.className = 'tag-pill accent';
    pill.textContent = '#카페매칭';
    accumulatedTagsContainer.appendChild(pill);
    
    shopsList.innerHTML = '<div class="loading">카페를 검색 중입니다...</div>';

    try {
        const response = await fetch(`${API_BASE}/match/cafe`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ searchType, keyword })
        });

        if (!response.ok) {
            throw new Error('카페 검색에 실패했습니다.');
        }

        const cafes = await response.json();
        
        setTimeout(() => {
            renderCafes(cafes);
        }, 300);
    } catch (error) {
        console.error(error);
        shopsList.innerHTML = `<div class="no-results">오류가 발생했습니다: ${error.message}</div>`;
    }
}

function renderCafes(cafes) {
    if (cafes.length === 0) {
        shopsList.innerHTML = `
            <div class="no-results">
                해당 조건에 맞는 카페를 찾지 못했습니다. 😢<br>
                <span style="font-size: 0.85rem; color: #64748b; display:inline-block; margin-top:10px;">다른 키워드로 다시 시도해 보세요!</span>
            </div>`;
        return;
    }

    shopsList.innerHTML = '';
    cafes.forEach(cafe => {
        const card = document.createElement('div');
        card.className = 'cafe-card';

        const mapUrl = `https://map.naver.com/p/search/${encodeURIComponent(cafe.name)}`;
        
        let opHtml = '';
        if (cafe.operation) {
            opHtml += `<div class="cafe-operation">`;
            if (cafe.operation.isLargeCafe) {
                opHtml += `<span class="op-badge highlight">🏰 대형카페</span>`;
            }
            if (cafe.operation.hasPlugs) {
                opHtml += `<span class="op-badge">💻 콘센트 넉넉</span>`;
            }
            if (cafe.operation.hasDecaf) {
                opHtml += `<span class="op-badge">☕ 디카페인 가능</span>`;
            }
            if (cafe.operation.isPetFriendly) {
                opHtml += `<span class="op-badge" style="color:#059669; background:rgba(16,185,129,0.1); border-color:rgba(16,185,129,0.2);">🐶 반려동물 동반</span>`;
            }
            opHtml += `<span class="op-badge">🚗 ${escapeHtml(cafe.operation.parkingInfo)}</span>`;
            opHtml += `</div>`;
        }

        let ambianceHtml = '';
        if (cafe.ambiance) {
            ambianceHtml = `<div class="cafe-features"><strong>✨ 분위기:</strong><br>${escapeHtml(cafe.ambiance)}</div>`;
        }

        let reviewHtml = '';
        if (cafe.positiveReviews || cafe.negativeReview) {
            reviewHtml += `<div class="review-section">`;
            if (cafe.positiveReviews) {
                const reviews = cafe.positiveReviews.split('|').map(r => r.trim()).filter(r => r.length > 0);
                const reviewBullets = reviews.map(r => `• ${escapeHtml(r)}`).join('<br>');
                reviewHtml += `<div class="positive-review"><strong>👍 방문자 요약:</strong><br>${reviewBullets}</div>`;
            }
            if (cafe.negativeReview) {
                reviewHtml += `
                    <div class="negative-review-wrapper">
                        <button class="negative-review-toggle" onclick="toggleNegativeReview(this)">⚠️ 아쉬운 점 보기</button>
                        <div class="negative-review-content">${escapeHtml(cafe.negativeReview)}</div>
                    </div>
                `;
            }
            reviewHtml += `</div>`;
        }

        let comparisonHtml = '';
        if (cafe.comparisons && cafe.comparisons.length > 0) {
            comparisonHtml += `<div class="comparison-section"><strong>💡 타 카페 비교:</strong>`;
            cafe.comparisons.forEach(comp => {
                comparisonHtml += `<div class="comparison-item">- [${escapeHtml(comp.targetCafeName)}] ${escapeHtml(comp.aspect)}: ${escapeHtml(comp.description)}</div>`;
            });
            comparisonHtml += `</div>`;
        }

        card.innerHTML = `
            <div class="shop-header">
                <div class="shop-name-wrapper" style="display: flex; flex-direction: column; gap: 4px;">
                    <span class="shop-name">${escapeHtml(cafe.name)}</span>
                    <span style="font-size: 0.9rem; color: #8b5cf6; font-weight: 600;">👑 시그니처: ${escapeHtml(cafe.signatureMenu)}</span>
                </div>
                <a href="${mapUrl}" target="_blank" rel="noopener noreferrer" class="shop-location" title="네이버 지도에서 보기" style="align-self: flex-start;">📍 지도보기</a>
            </div>
            ${opHtml}
            ${ambianceHtml}
            <div style="font-size: 0.9rem; color: #475569; margin-top: 12px; line-height: 1.5;">
                <strong>☕ 메뉴 설명:</strong><br>${escapeHtml(cafe.menuFeatures)}
            </div>
            ${comparisonHtml}
            ${reviewHtml}
        `;
        shopsList.appendChild(card);
    });
}
