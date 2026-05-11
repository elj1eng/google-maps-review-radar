# Google Maps Fake Review Detector 🕵️‍♂️

An automated tool designed to identify potentially fraudulent or "purchased" reviews on Google Maps. By analyzing reviewer history and media engagement, this script provides a data-driven verdict on a business's review integrity.

---

## Features

*   **Automated Sorting:** Forces Google Maps to sort by **Newest** reviews to capture recent bot bursts.
*   **Burner Account Detection:** Identifies reviewers with very low history ($\le 3$ reviews).
*   **Image Engagement Analysis:** Checks for the presence of photos using specific Google UI metadata classes (`Tya61d`).
*   **Dynamic Scraper:** Uses Playwright for condition-based scrolling—moving as fast as the network allows without static timers.
*   **Bilingual Support:** Robust regex handling for both **English** and **Vietnamese** interfaces.

---

## The Algorithms

The script evaluates the sampled reviews based on two primary statistical thresholds:

### 1. Burner Density
Measures the proportion of "One-and-Done" accounts.
$$P_{Burner} = \frac{N_{\text{Reviewers with } \le 3 \text{ reviews}}}{N_{\text{Total Scanned}}}$$
*   **Threshold:** If $P_{Burner} > 40\%$, the spot is flagged for high burner density.

### 2. Image Engagement Ratio
Legitimate customer bases typically have a baseline level of photo uploads.
$$P_{Image} = \frac{N_{\text{Reviews with photos}}}{N_{\text{Total Scanned}}}$$
*   **Threshold:** If $P_{Image} < 10\%$, the spot is flagged for low organic engagement.

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
Run the script by passing the Google Maps URL as an argument:

```bash
uv run main.py <google_maps_url>
```
#### Example Output:
```bash
--- SPOT SUMMARY ---
Rating: 4.9 ⭐ | Total Reviews: 7482

--- ANALYSIS RESULTS (Sample: 50) ---
1. Burner Density: 45.2% -> ⚠️ FAKE
2. Image Density: 8.0% -> ⚠️ FAKE

OVERALL STATUS: 🚨 SUSPICIOUS (Likely Bot Activity)
```

## Project Structure
main.py: Entry point and UI coordinator.

scraper.py: Playwright logic for navigation, sorting, and dynamic scrolling.

analyzer.py: BeautifulSoup logic for data extraction and algorithmic math.

constants.py: Centralized "Control Center" for CSS selectors and thresholds.

.gitignore: Prevents temporary browser profiles and caches from being uploaded.

## Disclaimer
This tool is for educational and research purposes only.

## License
This project is licensed under the [MIT License](LICENSE).
