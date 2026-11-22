"""The day's news as data: Saturday 21 November 2026.

Every item here happened, or was first reported, on 21 November 2026 in some
time zone. The counts printed on the page (stories, regions, fields) are
derived from these lists at render time, never typed by hand.

Each story carries a confidence tag and the outlets that carried it. The tag
legend is on the page: CONFIRMED means two or more independent outlets,
OFFICIAL means a government or agency statement, REPORTED means one outlet so
far, CLAIM means one party's account, FORECAST means a prediction.

Text is deliberately terse. The renderer measures every string against the
column it will sit in and refuses to draw one that would be clipped, so a
longer phrase here means a shorter phrase somewhere else.
"""

PAPER = "THE WORLD IN ONE DAY"
DAY_WORDS = "SATURDAY"
DAY_REST = "21 NOVEMBER 2026"
DAY_LINE = "Saturday 21 November 2026"

REGIONS = [
    "Europe",
    "Asia",
    "Middle East",
    "Africa",
    "Americas",
    "Oceania",
    "Global",
]

REGION_COLOR = {
    "Europe": "#2F5FA8",
    "Asia": "#B23A22",
    "Middle East": "#96700F",
    "Africa": "#1C7355",
    "Americas": "#6E3A93",
    "Oceania": "#0F6A70",
    "Global": "#3D4657",
}

FIELD_LABEL = {
    "politics": "POLITICS",
    "war": "WAR",
    "economy": "ECONOMY",
    "climate": "CLIMATE",
    "disaster": "DISASTER",
    "technology": "TECH",
    "science": "SCIENCE",
    "sport": "SPORT",
    "culture": "CULTURE",
    "health": "HEALTH",
}

# Four leads. pin = (longitude, latitude) for the map.
LEADS = [
    {
        "region": "Global",
        "field": "climate",
        "headline": "Climate Talks Run Overtime",
        "deck": "Antalya draft drops fossil fuels; EU may walk out.",
        "sure": "CONFIRMED",
        "outlets": "AP, AFP, Al Jazeera",
        "pin": (30.7, 36.9),
        "icon": "dome",
    },
    {
        "region": "Americas",
        "field": "war",
        "headline": "Cartel Boss Taken; 11 Killed",
        "deck": "El Chapo Isidro held in Sinaloa; FBI had him listed.",
        "sure": "CONFIRMED",
        "outlets": "AP, AFP",
        "pin": (-108.5, 25.6),
        "icon": "badge",
    },
    {
        "region": "Middle East",
        "field": "war",
        "headline": "Iran Hits Three Oil Tankers",
        "deck": "Strikes near Hormuz; a new launcher shown.",
        "sure": "CONFIRMED",
        "outlets": "AP, LA Times",
        "pin": (56.3, 26.6),
        "icon": "tanker",
    },
    {
        "region": "Africa",
        "field": "disaster",
        "headline": "Funeral Boat Capsizes, 24 Die",
        "deck": "Bayelsa, Nigeria: 24 rescued, search continues.",
        "sure": "CONFIRMED",
        "outlets": "AP, AFP, Reuters",
        "pin": (6.1, 4.8),
        "icon": "boat",
    },
]

# Twelve numbered cards, four across.
CARDS = [
    {
        "region": "Europe",
        "field": "war",
        "headline": "Strike Hits Central Ukraine",
        "deck": "Kryvyi Rih: 2 dead, 60 hurt",
        "sure": "CONFIRMED",
        "outlets": "AP, DW",
        "pin": (33.4, 47.9),
    },
    {
        "region": "Europe",
        "field": "politics",
        "headline": "NATO Vows to Defend Poland",
        "deck": "Rutte in Warsaw after 3 objects",
        "sure": "CONFIRMED",
        "outlets": "Reuters, Al Jazeera",
        "pin": (21.0, 52.2),
    },
    {
        "region": "Americas",
        "field": "technology",
        "headline": "FBI Probes Data Breach",
        "deck": "Crime records system hit again",
        "sure": "CONFIRMED",
        "outlets": "AP, CNN",
        "pin": (-77.0, 38.9),
    },
    {
        "region": "Europe",
        "field": "politics",
        "headline": "Sixth Saturday of Protests",
        "deck": "France: rallies over living costs",
        "sure": "CONFIRMED",
        "outlets": "AFP, France 24",
        "pin": (2.35, 48.85),
    },
    {
        "region": "Asia",
        "field": "health",
        "headline": "Toxic Brew Kills 16 in India",
        "deck": "Manipur: about 600 in hospital",
        "sure": "CONFIRMED",
        "outlets": "PTI, Indian Express",
        "pin": (93.9, 24.8),
    },
    {
        "region": "Asia",
        "field": "sport",
        "headline": "India 486-4, Lead 118",
        "deck": "Rahul 136, Gill 98 in Wellington",
        "sure": "CONFIRMED",
        "outlets": "AFP, BBC",
        "pin": (174.8, -41.3),
    },
    {
        "region": "Asia",
        "field": "technology",
        "headline": "Seoul Backs AI Data Centres",
        "deck": "Lee tours a $5.2bn Ulsan site",
        "sure": "OFFICIAL",
        "outlets": "Yonhap, Reuters",
        "pin": (129.3, 35.5),
    },
    {
        "region": "Americas",
        "field": "economy",
        "headline": "Trump Backs a 10% Card Cap",
        "deck": "Would work with Democrats, he says",
        "sure": "CONFIRMED",
        "outlets": "AP, Axios",
        "pin": (-74.5, 41.5),
    },
    {
        "region": "Africa",
        "field": "war",
        "headline": "Villagers Killed in Sudan",
        "deck": "Kordofan: 3,670 displaced",
        "sure": "REPORTED",
        "outlets": "IOM, Dar Hamar",
        "pin": (28.4, 12.2),
    },
    {
        "region": "Global",
        "field": "science",
        "headline": "Probe Reaches Mercury",
        "deck": "Eight years to the inner planet",
        "sure": "CONFIRMED",
        "outlets": "ESA, Nature",
        "pin": (8.65, 49.87),
    },
    {
        "region": "Americas",
        "field": "disaster",
        "headline": "6.7 Quake Shakes Peru",
        "deck": "Junin: no deaths reported",
        "sure": "CONFIRMED",
        "outlets": "USGS, AP",
        "pin": (-75.98, -10.86),
    },
    {
        "region": "Oceania",
        "field": "climate",
        "headline": "Cyclone Xavier Weakens",
        "deck": "Nassau: all 84 residents safe",
        "sure": "CONFIRMED",
        "outlets": "RNZ, PINA",
        "pin": (-165.4, -11.6),
    },
]

# Digest briefs, numbered on from the cards (13-26).
BRIEFS = [
    {"region": "Asia", "field": "culture", "text": "Khadam sweeps Malaysian film awards"},
    {"region": "Africa", "field": "health", "text": "DR Congo Ebola deaths pass 5,700"},
    {"region": "Africa", "field": "economy", "text": "Kenya starts drilling in Turkana"},
    {"region": "Asia", "field": "economy", "text": "Japan raises bluefin tuna quota 25%"},
    {"region": "Asia", "field": "politics", "text": "Japan LDP may replace a minister"},
    {"region": "Americas", "field": "politics", "text": "Guyana rules out talks with Venezuela"},
    {"region": "Americas", "field": "economy", "text": "Argentina backs $50bn gas export plan"},
    {"region": "Americas", "field": "politics", "text": "Canada sees no shift in US military ties"},
    {"region": "Europe", "field": "climate", "text": "UK has its coldest night since January"},
    {"region": "Europe", "field": "politics", "text": "Students march in 25 countries"},
    {"region": "Middle East", "field": "war", "text": "Qatar mediators hold talks in Tehran"},
    {"region": "Middle East", "field": "war", "text": "Gaza aid van strike kills three"},
    {"region": "Asia", "field": "economy", "text": "Prabowo brings home Rp1,600tn pledges"},
    {"region": "Middle East", "field": "economy", "text": "Saudi sets 15% minimum tax for 2027"},
    {"region": "Europe", "field": "politics", "text": "De Gennaro found dead in Naples"},
    {"region": "Middle East", "field": "disaster", "text": "Basra power station fire kills 4"},
    {"region": "Asia", "field": "disaster", "text": "Vietnam floods kill 41, nine missing"},
    {"region": "Asia", "field": "health", "text": "Delhi air stays in the poor band"},
    {"region": "Asia", "field": "politics", "text": "China tells Japan to change attitude"},
]

# Eight stamps in UTC, chronological, 24-hour clock.
TIMELINE = [
    ("00:09", "Quake M6.7 in Peru"),
    ("13:00", "Rallies fill Paris"),
    ("14:03", "NATO on Poland"),
    ("15:00", "COP31: no new text"),
    ("17:39", "FBI probes records"),
    ("18:24", "Probe at Mercury"),
    ("21:00", "24 dead in Nigeria"),
    ("23:36", "COP31 second day"),
]

# Reported figures only; each one traces to a story above.
STATS = [
    ("24", "dead in Nigeria boat"),
    ("11", "killed in Sinaloa"),
    ("60", "wounded in Kryvyi Rih"),
    ("5,700", "Ebola deaths, DR Congo"),
    ("6.7", "Peru quake magnitude"),
    ("84", "safe on Nassau"),
]

# News that belongs to 18-20 November and was left out on purpose.
LEFT_OUT = [
    ("20 Nov", "Italy general strike"),
    ("20 Nov", "S&P 500 falls 3.7%"),
    ("19 Nov", "Anthropic debuts; AI stocks slide"),
    ("18 Nov", "Eritrea retakes Badme"),
]

# Scheduled for 22 November, so not yet news on the day.
NOT_YET = [
    ("22 Nov", "COP31: a fourth draft"),
    ("22 Nov", "India v NZ, final day"),
]

SURE_LEGEND = [
    ("CONFIRMED", "2+ outlets"),
    ("OFFICIAL", "official statement"),
    ("REPORTED", "one outlet"),
    ("CLAIM", "one side's account"),
    ("FORECAST", "a prediction"),
]

FOOTER = "Every story here happened, or was first reported, on 21 November 2026."

SOURCES_LINE = (
    "Sources: AP, AFP, Reuters, BBC, Al Jazeera, DW, CNN, USGS, ESA, "
    "PTI, RNZ, PINA, Axios, IOM."
)
