# Google Maps CSS Selectors
CSS_SELECTORS = {
    "REVIEW_CARD": "jftiEf",
    "METADATA": "RfnDt",
    "PHOTO": "Tya61d",
    "SORT_BUTTON": "span.GMtm7c",
    "NEWEST_OPTION": "div.mLuXec",
    "SCROLL_PANE": 'div[role="main"] div[tabindex="-1"]',
    "HEADER_CONTAINER": "jANrlb",
    "RATING_VALUE": "fontDisplayLarge",
    "TOTAL_REVIEWS": "fontBodySmall",
    "BUSINESS_TITLE": "h1",
    "REVIEWS_TAB": "div.Gpq6kf.NlVald"
}

# Detection Algorithm Thresholds
THRESHOLDS = {
    "BURNER_HISTORY_LIMIT": 3,
    "BURNER_RATIO_MAX": 0.4,  # 40%
    "IMAGE_RATIO_MIN": 0.1,   # 10%
}

# Scraper Configuration
BROWSER_CONFIG = {
    "VIEWPORT": {'width': 1280, 'height': 900},
    "TIMEOUT": 10000,
    "SCROLL_LIMIT": 20,
    "DYNAMIC_WAIT_MS": 4000
}