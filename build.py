#!/usr/bin/env python3
"""Build script: Populates lead_audit_spa_template.html for Urban Platter.

Re-evaluated: March 16, 2026 — fresh mobile-first UX evaluation at 375×812,
fresh PSI PageSpeed data (pagespeed.web.dev, Slow 4G throttling), 3-dimension finding selection algorithm.
"""

import re, os

TEMPLATE = "/Users/growisto/Documents/Claude_Code/_cro_audit_system/templates/lead_audit_spa_template.html"
OUTPUT   = "/Users/growisto/Documents/Claude_Code/_audit_reports/urbanplatter-lead/index.html"

# Read template
with open(TEMPLATE, "r") as f:
    html = f.read()

# ── Simple variable replacements ──────────────────────────
replacements = {
    "{{CLIENT_NAME}}": "Urban Platter",
    "{{CLIENT_URL}}": "urbanplatter.com",
    "{{REPORT_DATE}}": "March 2026",
    "{{REPORT_PASSWORD}}": "urbanplatter2026",
    "{{INDUSTRY_CATEGORY}}": "Food & Beverage",
    "{{INDUSTRY_CATEGORY_SHORT}}": "food",

    # Section 01 — Audit Overview
    "{{SEVERITY_CRITICAL_COUNT}}": "3",
    "{{SEVERITY_IMPORTANT_COUNT}}": "5",
    "{{SEVERITY_OPPORTUNITY_COUNT}}": "2",
    "{{FINDING_COUNT_TOTAL}}": "10",
    "{{COMPETITOR_COUNT}}": "3",
    "{{APPS_PRESENT_COUNT}}": "13",
    "{{FINDING_COUNT_HOMEPAGE}}": "2",
    "{{FINDING_COUNT_COLLECTION}}": "2",
    "{{FINDING_COUNT_PDP}}": "4",
    "{{FINDING_COUNT_CART}}": "2",

    # Section 02 — Traffic & Conversion Context
    "{{PROXY_TIER_NAME}}": "Tier 3: Scale",
    "{{PROXY_TIER_SESSIONS}}": "50K–200K",
    "{{PROXY_PRODUCT_COUNT}}": "1,736",
    "{{PROXY_REVIEW_COUNT}}": "5,000+",
    "{{PROXY_INSTAGRAM}}": "85K+",
    "{{PROXY_APP_COUNT}}": "13",
    "{{PROXY_ESTIMATED_REVENUE}}": "50000000",
    "{{PROXY_TIER_NARRATIVE}}": 'Based on Urban Platter\'s extensive catalog of 1,736 products across 108 collections, strong review volume (5,000+ across products via Judge.me), 85K+ Instagram following, and presence of 13 marketing integrations, we estimate this is a <strong>Tier 3 (Scale)</strong> store with 50K–200K monthly sessions. The proxy signals all point to a mature store that has outgrown basic optimizations and would benefit significantly from data-driven CRO.',

    # Funnel benchmarks (Food & Bev — from Appendix C/D)
    "{{INDUSTRY_PDP_VIEW_RATE_P25}}": "60.4%",
    "{{INDUSTRY_PDP_VIEW_RATE}}": "89.6%",
    "{{INDUSTRY_PDP_VIEW_RATE_P75}}": "115.9%",
    "{{INDUSTRY_ATC_RATE_P25}}": "6.42%",
    "{{INDUSTRY_ATC_RATE}}": "11.95%",
    "{{INDUSTRY_ATC_RATE_P75}}": "20.27%",
    "{{INDUSTRY_CART_TO_CHECKOUT_P25}}": "22.8%",
    "{{INDUSTRY_CART_TO_CHECKOUT}}": "29.8%",
    "{{INDUSTRY_CART_TO_CHECKOUT_P75}}": "40.5%",
    "{{INDUSTRY_CHECKOUT_COMPLETION_P25}}": "12.3%",
    "{{INDUSTRY_CHECKOUT_COMPLETION}}": "20.7%",
    "{{INDUSTRY_CHECKOUT_COMPLETION_P75}}": "32.1%",
    "{{INDUSTRY_CVR_P25}}": "1.32%",
    "{{INDUSTRY_CVR_P50}}": "2.05%",
    "{{INDUSTRY_CVR_P75}}": "2.99%",
    "{{INDUSTRY_CVR_P50_RAW}}": "2.05",

    # Section 03: Performance & Speed (PSI lab data via pagespeed.web.dev — March 16, 2026)
    "{{PS_CLIENT_MOBILE_SCORE}}": "27",
    "{{PS_CLIENT_MOBILE_CLASS}}": "poor",
    "{{PS_CLIENT_MOBILE_VERDICT}}": "Poor — Urban Platter scores 27 on Google PageSpeed Insights (mobile, Slow 4G throttling). Lab LCP is 18.6s and TBT is 3,910ms — the page takes nearly 19 seconds to render its largest element and the main thread is frozen for almost 4 seconds. Desktop fares slightly better at 36 but remains in the red zone. However, CrUX field data tells a more nuanced story: real-user LCP is 2.1s and FCP is 1.7s — Google's CDN and caching help actual visitors. The critical CrUX failure is INP at 704ms (threshold: 200ms) — the site feels unresponsive to taps and clicks.",

    # Core Web Vitals (PSI lab data + CrUX field data)
    "{{PS_CLIENT_LCP}}": "18.6s",
    "{{PS_CLIENT_LCP_CLASS}}": "poor",
    "{{PS_CLIENT_LCP_STATUS}}": "fail",
    "{{PS_CLIENT_LCP_LABEL}}": "Fail (lab) · 2.1s field",
    "{{PS_CLIENT_FCP}}": "4.1s",
    "{{PS_CLIENT_FCP_CLASS}}": "poor",
    "{{PS_CLIENT_FCP_STATUS}}": "fail",
    "{{PS_CLIENT_FCP_LABEL}}": "Fail (lab) · 1.7s field",
    "{{PS_CLIENT_TBT}}": "3,910ms",
    "{{PS_CLIENT_TBT_CLASS}}": "poor",
    "{{PS_CLIENT_TBT_STATUS}}": "fail",
    "{{PS_CLIENT_TBT_LABEL}}": "Fail",
    "{{PS_CLIENT_CLS}}": "0.001",
    "{{PS_CLIENT_CLS_CLASS}}": "good",
    "{{PS_CLIENT_CLS_STATUS}}": "pass",
    "{{PS_CLIENT_CLS_LABEL}}": "Pass",
    "{{PS_CLIENT_INP}}": "704ms",
    "{{PS_CLIENT_INP_CLASS}}": "poor",
    "{{PS_CLIENT_INP_STATUS}}": "fail",
    "{{PS_CLIENT_INP_LABEL}}": "Fail (CrUX field)",

    "{{CWV_SUMMARY_CLASS}}": "poor",
    "{{CWV_PASS_ICON}}": "✗",
    "{{CWV_PASS_COUNT}}": "1",

    "{{PS_COMBINED_NARRATIVE}}": "Urban Platter's mobile performance is critically poor under Google's Slow 4G lab conditions: PSI score 27, LCP 18.6s, FCP 4.1s, TBT 3,910ms. However, real-world field data (CrUX) is significantly better — actual users see LCP 2.1s (good) and FCP 1.7s (good), thanks to CDN caching and repeat visits. The critical CrUX failure is <strong>INP at 704ms</strong> (threshold: 200ms) — meaning the site feels sluggish and unresponsive to taps and clicks. This is the worst INP in the competitive set. CLS is excellent at 0.001 (lab) / 0.02 (field). Desktop lab score is 36 with LCP 6.9s and TBT 1,410ms. The competition faces similar lab challenges: Vahdam scores 38, Sleepy Owl 34, Blue Tokai 12. But Blue Tokai and Sleepy Owl both pass CrUX CWV assessment while Urban Platter fails — the gap is in INP. The path to improvement: defer or remove non-critical third-party scripts (GoAffPro double-loads, InstaVid loads but doesn't render, PushOwl) to reduce main-thread blocking and improve INP.",

    # Section 05: Technology Assessment
    "{{TECH_HEALTH_CLASS}}": "warning",
    "{{TECH_HEALTH_ICON}}": "⚠",
    "{{TECH_HEALTH_SUMMARY}}": "3 of 6 technology areas are well-configured — 3 areas need attention",
    "{{TECH_PLATFORM_STATUS}}": "good",
    "{{TECH_PLATFORM_STATUS_LABEL}}": "Modern Platform",
    "{{PLATFORM}}": "Shopify",
    "{{PLATFORM_NOTES}}": "Shopify — auto-scaling, PCI-compliant, 99.99% uptime. Solid foundation for a high-SKU food brand with 1,736 products across 108 collections.",
    "{{TECH_THEME_STATUS}}": "warning",
    "{{TECH_THEME_STATUS_LABEL}}": "Custom Theme",
    "{{THEME_NAME}}": "New Rebuy &lt;&gt; Enterprise",
    "{{THEME_TYPE}}": "Custom-built (Rebuy Enterprise fork)",
    "{{THEME_VERSION_NOTE}}": "OS 2.0 compatible — custom fork of Rebuy Enterprise theme",
    "{{THEME_FEATURE_NOTE}}": "Custom theme has a broken sticky ATC panel (DOM element present but permanently invisible). Each new feature requires dev work instead of theme settings.",
    "{{TECH_CHECKOUT_STATUS}}": "warning",
    "{{TECH_CHECKOUT_STATUS_LABEL}}": "Shopflo Override",
    "{{CHECKOUT_TYPE}}": "Shopflo Checkout (Custom)",
    "{{CHECKOUT_GUEST_NOTE}}": "Guest checkout: Enabled via Shopflo",
    "{{CHECKOUT_EXPRESS_NOTE}}": "Express checkout: Shopflo handles payment routing — UPI/GPay available but no visible express buttons in cart",
    "{{CHECKOUT_FRICTION_NOTE}}": "Shopflo overrides native Shopify checkout — active JS errors detected (DialogContent missing DialogTitle, fetch failures to ngrok endpoint)",
    "{{TECH_PAYMENTS_STATUS}}": "good",
    "{{TECH_PAYMENTS_STATUS_LABEL}}": "Comprehensive",
    "{{PAYMENT_GATEWAY}}": "Razorpay (via Shopflo)",
    "{{PAYMENT_METHODS_NOTE}}": "UPI, Cards, Netbanking, Wallets via Shopflo + Razorpay",
    "{{PAYMENT_COD_NOTE}}": "COD: Available",
    "{{PAYMENT_BNPL_NOTE}}": "BNPL: Not detected",
    "{{TECH_CDN_STATUS}}": "warning",
    "{{TECH_CDN_STATUS_LABEL}}": "Needs Optimization",
    "{{CDN_PROVIDER}}": "Shopify CDN (Cloudflare)",
    "{{CDN_IMAGE_NOTE}}": "Images: Mix of WebP and JPEG — CrUX field LCP is 2.1s (good) but lab LCP is 18.6s under Slow 4G. Heavy JS bundles cause 3,910ms TBT",
    "{{CDN_COMPRESSION_NOTE}}": "Compression: Brotli/Gzip enabled but 13 third-party scripts not deferred or code-split",
    "{{CDN_CACHING_NOTE}}": "Browser caching: Standard Shopify headers — GoAffPro, InstaVid, PushOwl scripts blocking main thread",
    "{{TECH_SECURITY_STATUS}}": "good",
    "{{TECH_SECURITY_STATUS_LABEL}}": "Secure",
    "{{SECURITY_SSL_STATUS}}": "SSL/TLS Active",
    "{{SECURITY_HTTPS_NOTE}}": "HTTPS: All pages secured",
    "{{SECURITY_PCI_NOTE}}": "PCI DSS: Compliant (via Shopify)",
    "{{SECURITY_COOKIE_NOTE}}": "Cookie consent: Not found — consider adding for compliance",
    "{{TECH_NARRATIVE}}": "Urban Platter runs on Shopify with a custom fork of the Rebuy Enterprise theme (\"New Rebuy <> Enterprise\"). The platform is solid — auto-scaling, PCI-compliant, 99.99% uptime — but the custom theme has issues. Notably, the sticky ATC panel exists in the DOM but is permanently set to <code>visibility: hidden</code> — a broken feature that should be active on mobile. The checkout uses Shopflo, which overrides native Shopify checkout. During testing, we detected active JavaScript errors from Shopflo (<code>DialogContent requires a DialogTitle</code>) and failed fetch requests to an ngrok endpoint — these indicate integration instability. Other JS errors: <code>$ is not defined</code> (jQuery not loaded), GoAffPro double-loading, and missing modal elements. Payment stack via Razorpay covers all major Indian methods (UPI, Cards, Netbanking, Wallets, COD) but BNPL is missing. The core performance issue is 13 third-party scripts causing a PSI lab TBT of 3,910ms on mobile and a CrUX INP of 704ms — the worst interactivity score in the competitive set.",

    # Section 06: App Ecosystem
    "{{APPS_MISSING_COUNT}}": "5",
    "{{APPS_BENCHMARK_CONTEXT}}": "Top Food & Bev stores in our benchmark average 8–12 purpose-built apps — Urban Platter has 13 apps but is missing critical revenue-driving categories and has performance overhead from non-essential scripts",
    "{{APP_STACK_NARRATIVE}}": "Urban Platter has 13 apps covering reviews (Judge.me), checkout (Shopflo), email (Brevo), WhatsApp (WATI), push notifications (PushOwl), affiliate marketing (GoAffPro), cart recovery (CartBot), analytics (GTM, GA4, Clarity, Facebook Pixel, Logbase), and video (InstaVid). The analytics stack is comprehensive — a strong foundation for data-driven optimization. However, critical revenue-driving categories are missing. No subscription app despite selling highly replenishable products (spices, superfoods, snacks). No loyalty/rewards program to drive repeat purchases. No delivery estimation app (pincode checker). Additionally, the 13 scripts contribute to a PSI lab TBT of 3,910ms and a CrUX INP of 704ms — GoAffPro loads twice (double-load error in console), InstaVid loads but fails to render, and PushOwl adds another blocking script. A script audit and prioritization could improve both performance and INP simultaneously.",

    # JS nav
    "{{UX_FINDING_1_SHORT_TITLE}}": "UX & Conversion Findings",
}

for key, val in replacements.items():
    html = html.replace(key, val)

# ── Competition table rows (3 competitors — PSI data via pagespeed.web.dev, March 16, 2026) ──
comp_rows = """<tr class="client-row">
                                <td>Urban Platter</td>
                                <td class="score-cell-poor">27</td>
                                <td class="score-cell-poor">36</td>
                                <td class="score-cell-poor">18.6s</td>
                                <td class="score-cell-good">0.001</td>
                                <td class="score-cell-poor">3,910ms</td>
                            </tr>
                            <tr>
                                <td>Vahdam</td>
                                <td class="score-cell-poor">38</td>
                                <td class="score-cell-moderate">64</td>
                                <td class="score-cell-poor">7.7s</td>
                                <td class="score-cell-good">0.089</td>
                                <td class="score-cell-poor">1,190ms</td>
                            </tr>
                            <tr>
                                <td>Blue Tokai</td>
                                <td class="score-cell-poor">12</td>
                                <td class="score-cell-poor">39</td>
                                <td class="score-cell-poor">18.3s</td>
                                <td class="score-cell-poor">0.485</td>
                                <td class="score-cell-poor">1,070ms</td>
                            </tr>
                            <tr>
                                <td>Sleepy Owl</td>
                                <td class="score-cell-poor">34</td>
                                <td class="score-cell-moderate">58</td>
                                <td class="score-cell-poor">9.0s</td>
                                <td class="score-cell-good">0</td>
                                <td class="score-cell-poor">6,970ms</td>
                            </tr>"""
html = html.replace("{{PS_COMPETITION_TABLE_ROWS}}", comp_rows)

# ── Finding cards ─────────────────────────────────────────

def card(header, client_img, client_label, bench_img, bench_label, observations, recommendations, benchmark_tag, layout="desktop"):
    obs_li = "\n".join(f"                                                    <li>{o}</li>" for o in observations)
    rec_li = "\n".join(f"                                                    <li>{r}</li>" for r in recommendations)
    ss_class = "finding-screenshots desktop-screenshots" if layout == "desktop" else "finding-screenshots"
    return f"""<div class="finding-card">
                                    <div class="finding-card-header">
                                        {header}
                                    </div>
                                    <div class="finding-card-body">
                                        <div class="{ss_class}">
                                            <div class="finding-screenshot">
                                                <img src="{client_img}" alt="Urban Platter">
                                                <div class="finding-screenshot-label client-label">{client_label}</div>
                                            </div>
                                            <div class="finding-screenshot">
                                                <img src="{bench_img}" alt="{bench_label}">
                                                <div class="finding-screenshot-label benchmark-label">{bench_label}</div>
                                            </div>
                                        </div>
                                        <div class="finding-analysis">
                                            <div class="finding-observations">
                                                <span class="finding-section-header observations-header">Observations</span>
                                                <ul>
{obs_li}
                                                </ul>
                                            </div>
                                            <div class="finding-recommendations">
                                                <span class="finding-section-header recommendations-header">Recommendations</span>
                                                <ul>
{rec_li}
                                                </ul>
                                                <span class="finding-benchmark-tag">{benchmark_tag}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>"""

# ═══════════════════════════════════════════════════════════
# HOMEPAGE (2 cards) — Announcement bar (#6, 2.70), USP icon strip (#5, 2.70)
# ═══════════════════════════════════════════════════════════
hp_cards = "\n\n".join([
    card(
        "A discount-led announcement bar can lift first-session conversion by 5–8% — Urban Platter's bar wastes this space on a generic tagline",
        "screenshots/hp_mobile_firstfold.jpeg", "Urban Platter — Mobile",
        "screenshots/bench_hp_announcement_offer.jpeg", "Chomps",
        [
            "The announcement bar reads \"Elevate Your Everyday Pantry\" — a brand tagline, not a conversion driver. This is prime real estate seen by every visitor",
            "No shipping offer, discount code, or urgency element in the bar — first-time visitors get no immediate incentive to stay and shop",
            "8 out of 10 top Food & Bev stores use the announcement bar for a concrete offer: free shipping threshold, first-order discount, or limited-time deal",
            "Chomps uses \"FREE SHIPPING on orders $50+ | Subscribe & Save 15%\" — immediately communicates value and drives higher AOV",
        ],
        [
            "Replace the tagline with a conversion-focused message: \"Free Shipping Over ₹499 | Use code WELCOME10 for 10% Off Your First Order\"",
            "Add a secondary rotating message about delivery speed or trust: \"Trusted by 30 Lakh+ Customers | Fresh Delivery in 3–5 Days\"",
        ],
        "Standard — 8/10 stores use offer-driven announcement bars",
    ),
    card(
        "Trust badges and USP icons on the homepage can reduce bounce rate by 8–12% for first-time visitors",
        "screenshots/hp_mobile_firstfold.jpeg", "Urban Platter — Mobile",
        "screenshots/hp_f1_benchmark_trust.jpeg", "Yogabar",
        [
            "Urban Platter's homepage has no visible trust indicators (certifications, quality badges, shipping promises) as a standalone USP strip in the first fold",
            "First-time visitors see product banners but no concise reason to trust the brand — no \"100% Natural\", \"FSSAI Certified\", or \"Free Shipping\" badge strip",
            "7 out of 10 top Food & Bev brands display a dedicated USP icon strip prominently on the homepage — Yogabar shows \"100% Clean\", \"No Preservatives\", \"High Protein\" with icons",
        ],
        [
            "Add a horizontal USP icon strip below the hero banner: \"100% Natural\", \"FSSAI Certified\", \"1,700+ Products\", \"Free Shipping Over ₹499\"",
            "Use simple icons with short text — scannable in under 2 seconds. Place immediately below the hero carousel for maximum visibility",
        ],
        "Growing — 7/10 stores have USP icons",
    ),
])

# ═══════════════════════════════════════════════════════════
# COLLECTION (2 cards) — Dietary filters (#15, 2.40), Variant swatches (#3, 3.00)
# ═══════════════════════════════════════════════════════════
col_cards = "\n\n".join([
    card(
        "Dietary filters help health-conscious shoppers find products 3x faster — Urban Platter's filter drawer has none",
        "screenshots/col_mobile_filter_drawer.jpeg", "Urban Platter — Mobile",
        "screenshots/bench_col_dietary_filters.jpeg", "Athletic Brewing",
        [
            "The filter drawer offers only generic options: Sort by, Price, Product type, Brand, Country, Availability — no dietary or health filters",
            "Urban Platter sells superfoods, organic products, vegan items, and gluten-free options — but shoppers can't filter by these attributes",
            "Health-conscious buyers — Urban Platter's core segment — actively look for dietary filters (Vegan, Gluten-Free, Organic, No Preservatives, Keto)",
            "6 out of 10 top Food & Bev stores offer dietary-specific filters — Athletic Brewing filters by calories, flavor, and dietary attributes",
        ],
        [
            "Add dietary attribute filters: Vegan, Gluten-Free, Organic, No Preservatives, Keto-Friendly, Sugar-Free — tag products with Shopify metafields",
            "Add a \"Diet\" or \"Dietary Preference\" filter group at the top of the filter drawer — this is the #1 filter used by health-conscious Food & Bev shoppers",
        ],
        "Growing — 6/10 stores have dietary filters",
    ),
    card(
        "Variant swatches on product cards help shoppers browse faster and increase add-to-cart rates by 5–8%",
        "screenshots/col_mobile_grid.jpeg", "Urban Platter — Mobile",
        "screenshots/col_f2_benchmark_swatches.jpeg", "Yogabar",
        [
            "Collection page product cards show \"Choose options\" text for multi-variant products but no visual swatches for size/weight",
            "For a food brand with multiple pack sizes (100g, 250g, 500g, 1kg), visual weight indicators on cards save clicks and reduce friction",
            "9 out of 10 top Food & Bev stores show flavor/variant selectors directly on product cards — users can pick a size without leaving the grid",
        ],
        [
            "Add weight/size variant pills directly on collection page product cards — e.g., \"250g | 500g | 1kg\" as clickable badges",
            "Show the corresponding price for each variant on hover or selection — helps users compare without extra clicks into the PDP",
        ],
        "Standard — 9/10 stores have variant selectors on cards",
    ),
])

# ═══════════════════════════════════════════════════════════
# PDP (4 cards) — Sticky ATC broken (UX), Nutritional info (#4, 2.70), Subscription (#10, 2.65), Delivery estimation (#16, 2.40)
# ═══════════════════════════════════════════════════════════
pdp_cards = "\n\n".join([
    card(
        "A sticky Add to Cart on mobile can boost conversions by 3–5% — Urban Platter's is broken and invisible",
        "screenshots/pdp_mobile_specs.jpeg", "Urban Platter — Mobile PDP (scrolled)",
        "screenshots/bench_pdp_sticky_atc_olipop.jpeg", "Olipop — Mobile Sticky ATC",
        [
            "Urban Platter's theme includes a <code>&lt;sticky-atc-panel&gt;</code> element — but it has CSS class <code>invisible</code> and <code>visibility: hidden</code>, making it permanently non-functional",
            "On mobile, scrolling past the ATC button means users completely lose access to the primary conversion action — they must scroll back up to add to cart",
            "This is a broken feature, not a missing one — the sticky ATC was built but never activated or has a CSS/JS bug preventing it from appearing",
            "9 out of 10 top Food & Bev stores have a working sticky ATC on mobile PDPs — Olipop shows a persistent bottom bar with price + ATC that stays visible through the entire scroll",
        ],
        [
            "Fix the sticky ATC panel: investigate why the <code>sticky-atc-panel--out</code> class keeps the <code>invisible</code> state — likely a CSS transition or JS scroll-listener bug",
            "The panel already has the right HTML structure (product image, name, price, ATC button) — it just needs the visibility toggle fixed",
        ],
        "Standard — 9/10 stores have sticky ATC on mobile",
        layout="mobile",
    ),
    card(
        "Structured nutritional information tables increase buyer confidence and reduce returns for food products",
        "screenshots/pdp_mobile_specs.jpeg", "Urban Platter — Mobile",
        "screenshots/pdp_f4_benchmark_nutrition.jpeg", "Olipop",
        [
            "Product descriptions mention nutrients (\"rich in selenium\", \"loaded with magnesium and zinc\") but provide no structured nutritional facts table",
            "The specification section shows Net Weight, Dimensions, Shelf Life, Origin, SKU, Packaging, Brand, Ingredients — but no calories, macros, or daily value percentages",
            "Health-conscious buyers — a large Urban Platter segment — actively look for structured nutrition tables before purchasing premium-priced superfoods",
            "8 out of 10 top Food & Bev stores display a structured nutrition facts panel directly on the PDP",
        ],
        [
            "Add a structured nutritional information table to all food product PDPs: calories, protein, fat, carbs, fiber per serving with %DV",
            "Include allergen declarations and dietary badges (vegan, gluten-free, no preservatives) — these are trust-building signals for health-conscious buyers",
        ],
        "Standard for Food & Bev — 8/10 stores have nutrition tables",
    ),
    card(
        "Subscription options for consumable products can increase LTV by 40–60% and create predictable revenue",
        "screenshots/pdp_mobile_atc_area.jpeg", "Urban Platter — Mobile",
        "screenshots/pdp_f5_benchmark_subscription.jpeg", "Olipop",
        [
            "No subscribe-and-save option despite selling highly replenishable products — spices, superfoods, nuts, snacks, and pantry staples",
            "The ATC area shows only a one-time purchase flow: quantity selector + Add to Cart button — no toggle for \"Subscribe & Save\" or frequency selector",
            "Urban Platter's product categories are natural fits for auto-replenish: customers buy Brazil nuts, olive oil, and spice mixes on a regular cycle",
            "5 out of 10 top Food & Bev stores offer subscription options with 10–15% discount incentives — Olipop shows a prominent Subscribe toggle with 15% savings",
        ],
        [
            "Implement a subscribe-and-save option on eligible PDPs with a 10–15% discount incentive — start with top-selling replenishable SKUs",
            "Use apps like Recharge or Loop Subscriptions — offer frequency options (every 2 weeks, monthly, bi-monthly) based on product consumption rate",
        ],
        "Growing — 5/10 stores offer subscription on consumables",
    ),
    card(
        "Delivery date estimation on the PDP reduces cart abandonment by 15–20% by setting clear expectations",
        "screenshots/pdp_mobile_atc_area.jpeg", "Urban Platter — Mobile",
        "screenshots/pdp_f3_benchmark_delivery.jpeg", "Vahdam",
        [
            "No delivery estimation or pincode checker anywhere on the product page — users don't know when they'll receive the product before adding to cart",
            "Delivery uncertainty is a top-3 reason for cart abandonment in Indian e-commerce — especially for food products where freshness matters",
            "The PDP shows shelf life (270 days) in specifications but nothing about delivery timeline — the information gap is exactly at the purchase decision point",
            "5 out of 10 India Food & Bev stores have a pincode-based delivery checker — Vahdam shows \"Expected delivery\" with date range directly below the ATC button",
        ],
        [
            "Add a pincode-based delivery estimator directly below the ATC button: \"Enter pincode to check delivery date\"",
            "Show estimated delivery date range (e.g., \"Delivers by Mar 20–22\") and serviceability status — use Shiprocket or similar APIs for real-time data",
        ],
        "Growing — 5/10 India stores have pincode delivery check",
    ),
])

# ═══════════════════════════════════════════════════════════
# CART (2 cards) — Express checkout (#13, 2.65), Bundle/combo (#11, 2.65)
# Note: Cart drawer DOES exist (Shopflo overlay) — removed as finding.
#       Trust badges at checkout EXIST in Shopflo drawer — removed as finding.
# ═══════════════════════════════════════════════════════════
cart_cards = "\n\n".join([
    card(
        "Express checkout options (GPay, Shop Pay) can reduce checkout friction and lift conversion by 10–15%",
        "screenshots/cart_mobile_checkout.jpeg", "Urban Platter — Mobile",
        "screenshots/cart_f1_benchmark_express.jpeg", "Blue Tokai",
        [
            "The cart page Order Summary shows only a single \"Checkout\" button that routes through Shopflo — no express checkout buttons (GPay, Shop Pay, PhonePe) visible",
            "Express checkout reduces the process from 4+ steps to 1–2 taps — critical for mobile users who make up 80–90% of Indian e-commerce traffic",
            "While Shopflo supports UPI/GPay on the backend, the cart page doesn't surface these as one-tap express options — users must enter the full checkout flow first",
            "8 out of 10 top Food & Bev stores show express payment buttons directly on the cart — Blue Tokai displays Shop Pay + GPay alongside the standard checkout",
        ],
        [
            "Enable Shopify's dynamic checkout buttons (Shop Pay, Google Pay) directly on the cart page alongside the existing Shopflo checkout",
            "For the Indian market, surface UPI express payment as a prominent one-tap option — reducing checkout steps from 4 to 1 for returning users",
        ],
        "Growing — 8/10 stores have express checkout buttons visible",
    ),
    card(
        "Bundle and combo offers can increase average order value by 10–20% — Urban Platter has cross-sell but no bundles",
        "screenshots/cart_mobile_checkout.jpeg", "Urban Platter — Mobile",
        "screenshots/bench_cart_bundle.jpeg", "Chomps",
        [
            "The cart page has a \"You may also like\" cross-sell section — which is good — but no structured bundle or combo deals",
            "For a pantry brand with 1,736 SKUs, bundles are a natural fit: \"Baking Essentials Kit\", \"Healthy Snacking Combo\", \"Spice Starter Pack\"",
            "Bundle pricing creates perceived value and encourages multi-category purchases — especially effective for first-time buyers exploring the range",
            "Chomps offers curated variety packs and subscribe-and-save bundles directly on the cart — encouraging larger basket sizes",
        ],
        [
            "Create 5–10 curated bundles for popular use cases: \"Baking Kit\", \"Protein Snack Box\", \"Italian Cooking Essentials\" — with 10–15% bundle discount",
            "Surface bundle suggestions contextually in cart: if a user has olive oil, suggest the \"Mediterranean Cooking Kit\" that includes it plus complementary items",
        ],
        "Growing — 5/10 stores offer bundle/combo deals",
    ),
])

html = html.replace("{{FINDING_CARDS_HOMEPAGE}}", hp_cards)
html = html.replace("{{FINDING_CARDS_COLLECTION}}", col_cards)
html = html.replace("{{FINDING_CARDS_PDP}}", pdp_cards)
html = html.replace("{{FINDING_CARDS_CART}}", cart_cards)

# ── Apps HTML (13 present apps — fresh detection March 16, 2026) ────────────
apps_present = """<div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Judge.me Reviews</div>
                                    <div class="app-category">Reviews & Social Proof</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Shopflo Checkout</div>
                                    <div class="app-category">Checkout Optimization</div>
                                    <div class="app-benchmark-tag">Active JS errors: DialogContent missing DialogTitle, fetch failures to ngrok endpoint</div>
                                </div>
                                <span class="app-quality" title="Needs attention">⚠</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Brevo (Sendinblue)</div>
                                    <div class="app-category">Email Marketing</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">WATI — WhatsApp Business</div>
                                    <div class="app-category">WhatsApp Commerce</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">PushOwl — Web Push Notifications</div>
                                    <div class="app-category">Push Notifications</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">GoAffPro — Affiliate Marketing</div>
                                    <div class="app-category">Affiliate Program</div>
                                    <div class="app-benchmark-tag">Double-loading error detected: "Goaffpro is already loaded" — adds unnecessary JS overhead</div>
                                </div>
                                <span class="app-quality" title="Needs attention">⚠</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">CartBot — Cart Recovery</div>
                                    <div class="app-category">Revenue Recovery</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Logbase Analytics</div>
                                    <div class="app-category">Advanced Analytics</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">InstaVid / Quinn — Shoppable Video</div>
                                    <div class="app-category">Video Commerce</div>
                                    <div class="app-benchmark-tag">Loads but "NOT RENDERING - Conditions not met" on most pages — adds script weight without visible output</div>
                                </div>
                                <span class="app-quality" title="Needs attention">⚠</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Google Tag Manager</div>
                                    <div class="app-category">Analytics & Tracking</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">GA4 (gtag.js)</div>
                                    <div class="app-category">Analytics & Tracking</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Facebook Pixel</div>
                                    <div class="app-category">Ads & Attribution</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>
                            <div class="app-item present">
                                <div class="app-icon">&#10003;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Microsoft Clarity</div>
                                    <div class="app-category">Heatmaps & Session Recording</div>
                                </div>
                                <span class="app-quality" title="Good choice">✓</span>
                            </div>"""

apps_missing = """<div class="app-item missing">
                                <div class="app-icon">&#10007;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Subscription App (Recharge/Loop) <span class="app-priority-badge critical-priority">Critical</span></div>
                                    <div class="app-category">Recurring Revenue</div>
                                    <div class="app-impact-tag revenue">💰 LTV +40–60%</div>
                                    <div class="app-benchmark-tag">Present on 5/10 top Food & Bev stores — natural fit for replenishable pantry products</div>
                                </div>
                            </div>
                            <div class="app-item missing">
                                <div class="app-icon">&#10007;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Loyalty / Rewards Program <span class="app-priority-badge critical-priority">Critical</span></div>
                                    <div class="app-category">Customer Retention</div>
                                    <div class="app-impact-tag retention">🔄 Repeat Rate +15–25%</div>
                                    <div class="app-benchmark-tag">Present on 5/10 top Food & Bev stores</div>
                                </div>
                            </div>
                            <div class="app-item missing">
                                <div class="app-icon">&#10007;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Pincode Delivery Checker <span class="app-priority-badge critical-priority">Critical</span></div>
                                    <div class="app-category">Delivery Transparency</div>
                                    <div class="app-impact-tag conversion">📈 Reduces cart abandonment 15–20%</div>
                                    <div class="app-benchmark-tag">Present on 3/5 top India Food & Bev stores</div>
                                </div>
                            </div>
                            <div class="app-item missing">
                                <div class="app-icon">&#10007;</div>
                                <div class="app-item-details">
                                    <div class="app-name">Search Enhancement (Boost/Searchanise) <span class="app-priority-badge recommended-priority">Recommended</span></div>
                                    <div class="app-category">Product Discovery</div>
                                    <div class="app-impact-tag conversion">📈 Search converts 2-3x higher</div>
                                    <div class="app-benchmark-tag">Critical for stores with 1,700+ SKUs</div>
                                </div>
                            </div>
                            <div class="app-item missing">
                                <div class="app-icon">&#10007;</div>
                                <div class="app-item-details">
                                    <div class="app-name">BNPL / Pay Later (Simpl/LazyPay) <span class="app-priority-badge recommended-priority">Recommended</span></div>
                                    <div class="app-category">Payment Flexibility</div>
                                    <div class="app-impact-tag conversion">📈 Checkout conversion +5–10%</div>
                                    <div class="app-benchmark-tag">Growing in India D2C — reduces checkout abandonment for higher AOV orders</div>
                                </div>
                            </div>"""

html = html.replace("{{APPS_PRESENT_HTML}}", apps_present)
html = html.replace("{{APPS_MISSING_HTML}}", apps_missing)

# ── Strip remaining template comments ─────────────────────
html = re.sub(r'<!--\s*POPULATE:.*?-->', '', html, flags=re.DOTALL)
html = re.sub(r'<!--\s*VIDEO FINDING CARD PATTERN.*?-->', '', html, flags=re.DOTALL)

# ── Verify no template variables remain ───────────────────
remaining = re.findall(r'\{\{[A-Z_]+\}\}', html)
if remaining:
    print(f"⚠ WARNING: {len(remaining)} unreplaced variables found:")
    for v in sorted(set(remaining)):
        print(f"   {v}")
else:
    print("✓ All template variables replaced successfully")

# ── Write output ──────────────────────────────────────────
with open(OUTPUT, "w") as f:
    f.write(html)

lines = html.count('\n') + 1
print(f"✓ Written to {OUTPUT}")
print(f"  Total lines: {lines}")
print(f"  File size: {len(html):,} bytes")
