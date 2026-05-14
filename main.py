import sys
import requests
from urllib.parse import urlparse
from scraper import MapsScraper
from analyzer import ReviewAnalyzer

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def is_google_maps_responsive(url: str) -> bool:
    """Sends a HEAD request to check for 302 Found (Redirects) or 200 OK."""
    try:
        # We use allow_redirects=False to specifically catch the 302 status
        response = requests.head(url, timeout=5, allow_redirects=False)
        
        # Checking for 302 (Shortened/Mobile links) or 200 (Direct Desktop links)
        if response.status_code in [200, 301, 302]:
            return True
        return False
    except Exception:
        return False

def main():
    # 1. Handle URL input
    if len(sys.argv) > 1:
        target_url = sys.argv[1].strip()
    else:
        target_url = input("Enter Google Maps URL: ").strip()

    if not target_url:
        print("❌ Error: No URL provided.")
        return

    # 2. HTTP Validation Filter
    print(f"🔍 Validating URL...")
    if not is_google_maps_responsive(target_url):
        print(f"❌ Error: The URL provided did not return a valid response.")
        print("Ensure the link is a valid, reachable Google Maps place.")
        return

    # 3. Scrape
    print(f"🚀 Initializing Scraper for: {target_url}")
    scraper = MapsScraper(target_url)
    html_content = scraper.fetch_html()

    # 4. Analyze
    analyzer = ReviewAnalyzer(html_content)
    summary = analyzer.get_spot_summary()
    report = analyzer.analyze_reviews()

    if not report:
        print("⚠️ Analysis failed: No review cards found.")
        return

    # 5. Print Report
    final_status = "🚨 SUSPICIOUS" if (report['is_fake_h'] or report['is_fake_i']) else "✅ TRUSTWORTHY"
    reply_msg = (
        f"{summary['name']}\n\n"
        f"--- SPOT SUMMARY ---\n"
        f"Rating: {summary['rating']} ⭐ | Total Reviews: {summary['total']}\n\n"
        f"--- VERDICT (Sample Size: {report['total_scanned']}) ---\n"
        f"1. Burner Density: {report['h_ratio']*100:.1f}% -> {'⚠️ FAKE' if report['is_fake_h'] else '✅ OK'}\n"
        f"2. Image Density: {report['i_ratio']*100:.1f}% -> {'⚠️ FAKE' if report['is_fake_i'] else '✅ OK'}\n"
        f"3. Real Reviewer Metric (>3 reviews): Avg {report['real_avg_rating']:.2f} ⭐ | Count {report['real_count']} - {report['real_count']/report['total_scanned']*100:.1f}%\n\n"
        f"OVERALL STATUS: {final_status}"
    )
    print(f"\n{reply_msg}")

if __name__ == "__main__":
    main()