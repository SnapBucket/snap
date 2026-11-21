"""The day's news, as data. Every item below happened or was first reported on
20 November 2026 (UTC). Region and field counts on the page are derived from
these lists, never typed by hand.

Text is kept short on purpose: the renderer measures every string against its
column and refuses to draw one that would be clipped. Cards sit six across, so
a card headline gets about 26 characters and its deck about 16.

Fields: politics, war, economy, climate, disaster, technology, science, sport,
culture, health.
"""

PAPER = "THE WORLD IN ONE DAY"
DAY_LONG = "20 NOVEMBER 2026"
WEEKDAY = "FRIDAY"

REGIONS = ["Europe", "Asia", "Middle East", "Africa", "Americas", "Oceania", "Global"]

REGION_COLOR = {
    "Europe":      "#2F6BD8",
    "Asia":        "#C8452B",
    "Middle East": "#A87410",
    "Africa":      "#1F7F63",
    "Americas":    "#7B3FA0",
    "Oceania":     "#126E75",
    "Global":      "#4A5568",
}

FIELD_LABEL = {
    "politics": "POLITICS",
    "war": "WAR & SECURITY",
    "economy": "ECONOMY",
    "climate": "CLIMATE",
    "disaster": "DISASTER",
    "technology": "TECHNOLOGY",
    "science": "SCIENCE",
    "sport": "SPORT",
    "culture": "CULTURE",
    "health": "HEALTH",
}

# Four leads. pin = (lon, lat) on the world map.
LEADS = [
    {
        "region": "Europe",
        "field": "war",
        "headline": "Russia's Biggest Barrage Hits Ukraine",
        "deck": "400 drones, 110 missiles; eight killed, two in Poland.",
        "sure": "CONFIRMED",
        "outlets": "Reuters, AP, CBS",
        "pin": (30.5, 50.4),
        "icon": "strike",
    },
    {
        "region": "Middle East",
        "field": "war",
        "headline": "Iran Seeks a Deal; Trump Says No",
        "deck": "Araqchi seeks guarantees; Trump calls terms unacceptable.",
        "sure": "CONFIRMED",
        "outlets": "Reuters, AP",
        "pin": (51.4, 35.7),
        "icon": "talks",
    },
    {
        "region": "Europe",
        "field": "politics",
        "headline": "EU and UK Sign Brussels Reset",
        "deck": "Food checks cut and carbon markets linked after five years.",
        "sure": "OFFICIAL",
        "outlets": "Commission, gov.uk",
        "pin": (4.35, 50.85),
        "icon": "handshake",
    },
    {
        "region": "Global",
        "field": "economy",
        "headline": "Tech Rout Wipes $9tn Off Stocks",
        "deck": "Nasdaq -5.3%; Taiwan's worst week since 1990.",
        "sure": "CONFIRMED",
        "outlets": "Reuters, AP",
        "pin": (-74.0, 40.7),
        "icon": "chart",
    },
]

# Twelve numbered cards: 01-12, six across.
CARDS = [
    {
        "region": "Asia",
        "field": "disaster",
        "headline": "Akvan Hits Odisha",
        "deck": "372k evacuated",
        "sure": "OFFICIAL",
        "outlets": "IMD",
        "pin": (84.9, 19.3),
    },
    {
        "region": "Americas",
        "field": "politics",
        "headline": "Trump Attacks Iran, AI",
        "deck": "90-min briefing",
        "sure": "CONFIRMED",
        "outlets": "CNN",
        "pin": (-77.0, 38.9),
    },
    {
        "region": "Africa",
        "field": "health",
        "headline": "581 Women Killed, Jul-Sep",
        "deck": "Police figures",
        "sure": "CONFIRMED",
        "outlets": "BBC",
        "pin": (28.0, -26.2),
    },
    {
        "region": "Asia",
        "field": "economy",
        "headline": "Japan Core Inflation 2.2%",
        "deck": "A 2026 high",
        "sure": "OFFICIAL",
        "outlets": "Jiji",
        "pin": (139.7, 35.7),
    },
    {
        "region": "Oceania",
        "field": "climate",
        "headline": "Tonga Drought Crisis",
        "deck": "Drought, 28 days",
        "sure": "OFFICIAL",
        "outlets": "RNZ",
        "pin": (-175.2, -21.1),
    },
    {
        "region": "Middle East",
        "field": "war",
        "headline": "Saudi Strikes Hodeidah",
        "deck": "Houthis threaten",
        "sure": "CONFIRMED",
        "outlets": "AP",
        "pin": (42.95, 14.8),
    },
    {
        "region": "Europe",
        "field": "politics",
        "headline": "Italy Strike: 1.5 Million",
        "deck": "CGIL v budget",
        "sure": "CONFIRMED",
        "outlets": "ANSA",
        "pin": (12.5, 41.9),
    },
    {
        "region": "Americas",
        "field": "technology",
        "headline": "Anthropic Falls 12%",
        "deck": "Day two selloff",
        "sure": "CONFIRMED",
        "outlets": "CNBC, Axios",
        "pin": (-73.6, 40.9),
    },
    {
        "region": "Asia",
        "field": "politics",
        "headline": "Beijing Warns Tokyo",
        "deck": "Taiwan words",
        "sure": "OFFICIAL",
        "outlets": "AFP",
        "pin": (116.4, 39.9),
    },
    {
        "region": "Global",
        "field": "climate",
        "headline": "COP31 Runs Past Deadline",
        "deck": "No deal; new text",
        "sure": "CONFIRMED",
        "outlets": "UN News",
        "pin": (30.7, 36.9),
    },
    {
        "region": "Middle East",
        "field": "war",
        "headline": "Iraqi Forces Enter Jurf",
        "deck": "Kataib Hezbollah",
        "sure": "CONFIRMED",
        "outlets": "AP",
        "pin": (44.2, 32.9),
    },
    {
        "region": "Oceania",
        "field": "disaster",
        "headline": "Nassau Emergency",
        "deck": "Cyclone nears",
        "sure": "OFFICIAL",
        "outlets": "RNZ",
        "pin": (-165.4, -11.6),
    },
]

# Digest briefs, numbered on from the cards (13-24).
BRIEFS = [
    {"region": "Global", "field": "science", "text": "BepiColombo nears Mercury"},
    {"region": "Africa", "field": "health", "text": "Keto diet cut liver fat 67%"},
    {"region": "Oceania", "field": "sport", "text": "Barrett: 150th All Blacks test"},
    {"region": "Asia", "field": "culture", "text": "Swift named artist of the year"},
    {"region": "Global", "field": "science", "text": "CERN sees rare particle decay"},
    {"region": "Global", "field": "science", "text": "Voyager 1: 24 light-hours out"},
    {"region": "Europe", "field": "health", "text": "1,144 Ukraine child casualties"},
    {"region": "Global", "field": "technology", "text": "Robot arms talks miss deadline"},
    {"region": "Americas", "field": "technology", "text": "Trump: no data centres abroad"},
    {"region": "Asia", "field": "economy", "text": "Malaysia trade surplus 41.8bn"},
    {"region": "Americas", "field": "economy", "text": "Argentina risk above 1,000"}
]

# Six stamps, chronological in UTC, 24-hour clock.
TIMELINE = [
    ("00:30", "Missiles hit Kyiv; two land in Poland"),
    ("02:30", "Akvan makes landfall in Odisha"),
    ("03:30", "Japan core inflation 2.2%"),
    ("09:00", "EU and UK sign Brussels reset"),
    ("15:00", "COP31 deadline passes, no deal"),
    ("18:35", "Trump: Iran terms unacceptable"),
]

# Reported figures only; each appears in a story above.
STATS = [
    ("8", "killed in Ukraine"),
    ("400+", "drones in one night"),
    ("$9tn", "wiped off stocks"),
    ("372,000", "evacuated in Odisha"),
    ("581", "women killed Jul-Sep"),
]

LEFT_OUT = [
    ("19 Nov", "Somalia expels UAE envoy"),
    ("19 Nov", "ICJ: Myanmar genocide"),
    ("19 Nov", "Anthropic's $81bn IPO debut"),
    ("17 Nov", "PAHO revokes US measles status"),
    ("18 Nov", "Senegal boat capsizes"),
]

NOT_YET = [
    ("21 Nov", "COP31 third draft"),
    ("21 Nov", "BepiColombo enters orbit"),
    ("21 Nov", "All Blacks v England"),
]

SOURCES_LINE = (
    "Reuters, AP, AFP, BBC, UN News, ANSA, Jiji, PTI, SAPS, IMD, "
    "European Commission, gov.uk, RNZ, CNN, FT."
)
