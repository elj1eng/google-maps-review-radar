import re
from bs4 import BeautifulSoup
from constants import CSS_SELECTORS, THRESHOLDS

class ReviewAnalyzer:
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_spot_summary(self) -> dict:
        """Extracts the overall rating, total reviews, and name of the business."""
        summary = {"rating": "N/A", "total": "N/A", "name": "Unknown Place"}
        
        # 1. Extract Place Name
        place_name_el = self.soup.find('button', attrs={"data-bundle-id": True}).find('div', class_=CSS_SELECTORS["PLACE_NAME"])
        if place_name_el:
            summary["name"] = place_name_el.get_text().strip()

        header = self.soup.find("div", class_=CSS_SELECTORS["HEADER_CONTAINER"])
        
        if header:
            rating_el = header.find("div", class_=CSS_SELECTORS["RATING_VALUE"])
            total_el = header.find("div", class_=CSS_SELECTORS["TOTAL_REVIEWS"])
            
            if rating_el: summary["rating"] = rating_el.get_text().strip()
            if total_el:
                match = re.search(r"(\d+[\d,]*)", total_el.get_text())
                if match: summary["total"] = match.group(1).replace(",", "")
        return summary

    def analyze_reviews(self) -> dict:
        """Parses individual cards and applies detection algorithms."""
        cards = self.soup.find_all("div", class_=re.compile(CSS_SELECTORS["REVIEW_CARD"]))
        data = {"counts": [], "photo_count": 0, "total": 0, "ratings": []}

        # print("\n--- DATA EXTRACTION LOG ---")
        for card in cards:
            data["total"] += 1
            
            # 1. History Count (Burner Check)
            count = 1
            meta = card.find("div", class_=re.compile(CSS_SELECTORS["METADATA"]))
            if meta:
                match = re.search(r'(\d+)\s+(reviews|đánh giá)', meta.get_text().lower())
                if match: count = int(match.group(1))
            data["counts"].append(count)

            # 2. Image Detection (Refined to data-photo-index="0")
            has_photo = card.find(class_=re.compile(CSS_SELECTORS["PHOTO"]), attrs={"data-photo-index": "0"})
            img_status = "[IMAGE FOUND]" if has_photo else "[NO IMAGE]"
            if has_photo: data["photo_count"] += 1

            # 3. Extract Rating
            rating = None
            for span in card.find_all("span", attrs={"role": "img"}):
                if span.has_attr("aria-label"):
                    match = re.search(r'(\d+[,\.]?\d*)', span["aria-label"])
                    if match:
                        try:
                            r = float(match.group(1).replace(',', '.'))
                            if 1 <= r <= 5:
                                rating = r
                                break
                        except ValueError:
                            continue
                            
            data["ratings"].append({"count": count, "rating": rating})
            
            # print(f"Review {data['total']}: History {count} | {img_status} | Rating: {rating}")

        if data["total"] == 0: return {}

        # 4. Apply Algorithms
        low_hist_n = len([c for c in data["counts"] if c <= THRESHOLDS["BURNER_HISTORY_LIMIT"]])
        h_ratio = low_hist_n / data["total"]
        i_ratio = data["photo_count"] / data["total"]

        # 5. Real Reviewer Algorithm (> 3 reviews)
        real_reviews = [r["rating"] for r in data["ratings"] if r["count"] > 3 and r["rating"] is not None]
        real_avg_rating = sum(real_reviews) / len(real_reviews) if real_reviews else 0.0
        real_count = len(real_reviews)

        return {
            "h_ratio": h_ratio,
            "i_ratio": i_ratio,
            "is_fake_h": h_ratio > THRESHOLDS["BURNER_RATIO_MAX"],
            "is_fake_i": i_ratio < THRESHOLDS["IMAGE_RATIO_MIN"],
            "total_scanned": data["total"],
            "low_hist_n": low_hist_n,
            "img_n": data["photo_count"],
            "real_avg_rating": real_avg_rating,
            "real_count": real_count
        }