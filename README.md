# Google Maps Fake Review Detector

An automated tool designed to identify potentially fraudulent or "purchased" reviews on Google Maps. By analyzing reviewer history and media engagement, this script provides a data-driven verdict on a business's review integrity.

---

## Features

*   **Automated Sorting:** Forces Google Maps to sort by **Newest** reviews to capture recent bot bursts.
*   **Burner Account Detection:** Identifies reviewers with very low history ($\le 3$ reviews).
*   **Image Engagement Analysis:** Checks for the presence of photos using specific Google UI metadata classes (`Tya61d`).
*   **Real Reviewer Filtering:** Calculates the true average rating by filtering out "burner" accounts, considering only reviews from users with more than 3 reviews.
*   **Telegram Bot Integration:** Includes a fully functional Telegram bot interface for remote, easy access.

---

## The Algorithms

The script evaluates the sampled reviews based on three primary statistical metrics:

### 1. Burner Density
Measures the proportion of "One-and-Done" accounts.
$$P_{Burner} = \frac{N_{\text{Reviewers with } \le 3 \text{ reviews}}}{N_{\text{Total Scanned}}}$$
*   **Threshold:** If $P_{Burner} > 40\%$, the spot is flagged for high burner density.

### 2. Image Engagement Ratio
Legitimate customer bases typically have a baseline level of photo uploads.
$$P_{Image} = \frac{N_{\text{Reviews with photos}}}{N_{\text{Total Scanned}}}$$
*   **Threshold:** If $P_{Image} < 10\%$, the spot is flagged for low organic engagement.

### 3. Real Reviewer Metric
Calculates the average rating by excluding suspicious, low-history accounts.
$$Avg_{\text{Real}} = \frac{\sum \text{Ratings of Reviewers with } > 3 \text{ reviews}}{N_{\text{Reviewers with } > 3 \text{ reviews}}}$$
*   **Logic:** Isolates reviewers who have submitted $> 3$ reviews across Google Maps and recalculates the average star rating and their percentage of the total scanned.

---

## Installation
```bash
git clone https://github.com/elj1eng/google-maps-review-radar
cd google-maps-review-radar
pip install uv
uv sync
uv run playwright install chromium
```

## Usage

### 1. Local CLI
Run the script by passing the Google Maps URL as an argument:

```bash
uv run main.py <google_maps_url>
```
#### Example Output:
```text
📍 Boia De

--- SPOT SUMMARY ---
Rating: 4.6 ⭐️ | Total Reviews: 831

--- VERDICT (Sample Size: 210) ---
1. Burner Density: 9.0% -> ✅ OK
2. Image Density: 29.0% -> ✅ OK
3. Real Reviewer Metric (>3 reviews): Avg 4.33 ⭐️ | Count 191 - 91.0%

OVERALL STATUS: ✅ TRUSTWORTHY
```

### 2. Telegram Bot
1. Go to [t.me/gmaps_radar_bot](https://t.me/gmaps_radar_bot).
2. Click **Start**.
3. Input a Google Maps place URL to receive the analysis report.

---

## Project Structure
`main.py`: Entry point and CLI coordinator.

`bot.py`: Entry point for the Telegram Bot integration.

`scraper.py`: Playwright logic for navigation, sorting, and dynamic scrolling.

`analyzer.py`: BeautifulSoup logic for data extraction and algorithmic math.

`constants.py`: Centralized "Control Center" for CSS selectors and thresholds.

`.env.example`: Template for environment variables.

`.gitignore`: Prevents temporary browser profiles and caches from being uploaded.

---

## Disclaimer
This tool is for educational and research purposes only.

## License
This project is licensed under the [MIT License](LICENSE).
