// Everything the pages say about Sidanta, in one place.
// Facts come from the current portfolio and the October 2026 resume.

export const person = {
  name: 'Sidanta Parajuli',
  title: 'Data Analytics Engineer',
  org: 'Northern Kentucky Water District',
  place: 'Erlanger, KY',
  email: 'sidantaparajuli@gmail.com',
  summary:
    'I build medallion pipelines on Azure Databricks with PySpark and Delta Lake, and the Power BI reports seven departments open each morning. Before that I worked with data at an FAA-regulated airline, a clinical research company and a freight broker, and fine-tuned a 1.5B-parameter language model in a university lab. On the side I am building comply., a system of record for DOT drug and alcohol testing.',
  focus: ['Azure Databricks', 'Medallion pipelines', 'Data quality', 'Dimensional modeling', 'Power BI', 'LLM fine-tuning'],
};

export const links = [
  { k: 'github', label: 'GitHub', value: 'sidantap', href: 'https://github.com/sidantap' },
  { k: 'linkedin', label: 'LinkedIn', value: 'Sidanta Parajuli', href: 'https://www.linkedin.com/in/sid2003' },
  { k: 'comply', label: 'comply.', value: 'complydot.org', href: 'https://www.complydot.org' },
  { k: 'email', label: 'Email', value: 'sidantaparajuli@gmail.com', href: 'mailto:sidantaparajuli@gmail.com' },
];


export const experience = [
  {
    when: '02/2026–Current', role: 'Data Analytics Engineer',
    logo: { text: 'NKWD', label: 'Northern Kentucky Water District' }, org: 'Northern Kentucky Water District · Erlanger, KY',
    text: 'Medallion (bronze, silver, gold) pipelines on Azure Databricks with PySpark and Delta Lake, loading raw data incrementally and modeling gold facts and dimensions with SCD Type 1 and 2. Config-driven ingestion from SQL Server sources (CIS, Lucity, LIMS, Antero) and REST APIs (Paycor, KnowBe4, CivicPlus, ServiceDesk Plus), orchestrated with Azure Data Factory, ADLS Gen2 and Key Vault and shipped through Azure DevOps CI/CD with pytest, black and pylint. Built 10–20 Power BI reports for seven departments and migrated 40–50 Crystal Reports, saving 20–40 staff hours a week.',
    links: [{ t: 'Lakehouse', post: 'projects/databricks-lakehouse/' }],
  },
  {
    when: '05/2025–12/2025', role: 'Data Analysis and Process Solutions Intern',
    logo: { src: 'logos/atlas.svg', ar: 5.85, label: 'Atlas Air' }, org: 'Atlas Air Worldwide · Erlanger, KY',
    text: 'Built the FAA drug and alcohol testing app in R Shiny: eligibility filtering, randomized selection, rollover, deduplication and SharePoint audit logging through Microsoft Graph. Power Automate flows for the pilot Master Training Schedule, crew scheduling and immigration reporting, part of about 25–30 staff hours saved a week. Logged usage across three internal tools into Power BI.',
    links: [{ t: 'FAA randomizer', post: 'projects/faa-randomizer/' }],
  },
  {
    when: 'Fall 2025', role: 'Teaching Assistant and Research Assistant',
    logo: { src: 'logos/nku.svg', ar: 4.11, label: 'Northern Kentucky University' }, org: 'NKU College of Informatics',
    text: 'TA for web development (INF 286): grading, an exam review quiz and office hours. Web scraping, machine learning and NLP in faculty research with Dr. Junxiu Zhou.',
    links: [{ t: 'Nurse sentiment', post: 'projects/nurse-sentiment/' }],
  },
  {
    when: 'Fall 2025', role: 'Innovation Fellow',
    logo: { src: 'logos/kcv.png', ar: 2.98, label: 'Kentucky Commercialization Ventures' }, org: 'Kentucky Commercialization Ventures',
    text: 'One of ten fellows in the Fall 2025 cohort. With Team #2, took Vidvo, an AI short-form video tool for small businesses, from concept to a commercialization plan: customer discovery, SWOT, lean canvas, failure-mode analysis and a go-to-market plan.',
    links: [{ t: 'Vidvo', post: 'projects/vidvo/' }, { t: 'KCV announcement', href: 'https://www.kycommercializationventures.com/post/ten-graduate-from-fall-2025-innovation-fellowship-cohort' }],
  },
  {
    when: '08/2024–12/2024', role: 'Data Science Intern',
    logo: { src: 'logos/medpace.svg', ar: 6.95, label: 'Medpace' }, org: 'Medpace · Cincinnati, OH',
    text: 'dbt and SQL transformations on Snowflake, and cleaning and validating millions of clinical trial records with Python, SQL and R. An R Shiny map of global clinical studies for proposals, and monthly dashboard design sessions for 10+ analysts in the US and UK.',
    links: [{ t: 'Study map', post: 'projects/clinical-study-map/' }],
  },
  {
    when: '01/2024–08/2024', role: 'Data Analytics Intern',
    logo: { src: 'logos/motus.png', ar: 3.75, label: 'Motus Freight' }, org: 'Motus Freight · Bellevue, KY',
    text: 'Tableau Cloud dashboards on Turvo data, including a CO2 dashboard that contributed to a 12.4% drop in emissions and a regional dashboard across 4 regions and 49 states that contributed to a 15% rise in profit.',
    links: [{ t: 'Dashboards', post: 'projects/motus-dashboards/' }],
  },
];

export const selected = [
  {
    when: '2026–', title: 'comply.', tags: 'React · TypeScript · Vitest · three.js',
    text: 'A system of record for DOT drug and alcohol random testing. It syncs employees from the HR system, routes every pool change through approval, runs random selections anyone can re-run to prove they were fair, and tracks each test to its MRO result. Live for FAA (14 CFR Part 120); the other DOT agencies are next.',
    img: 'img/comply.jpg', cap: 'complydot.org', links: [{ t: 'complydot.org', href: 'https://www.complydot.org' }, { t: 'project page', post: 'projects/comply/' }],
  },
  {
    when: '2026', title: 'A data pipeline that runs every night for $0', tags: 'Python · DuckDB · dbt · GitHub Actions',
    text: 'Cincinnati 311 requests, NOAA weather and NHTSA vehicle complaints, loaded incrementally, tested and modeled with dbt into a star schema every night. Bad rows go to quarantine with a reason; a small open-source model classifies new complaints and is scored against NHTSA’s own labels.',
    img: 'img/nightly-overview.jpg', cap: 'Nightly 311 dashboard', links: [{ t: 'dashboard', href: 'https://sidantap.github.io/nightly-311-pipeline/' }, { t: 'code', href: 'https://github.com/sidantap/nightly-311-pipeline' }, { t: 'project page', post: 'projects/nightly-311/' }],
  },
  {
    when: '2024', title: 'An NKU chatbot on a fine-tuned GPT-2', tags: 'Python · GPT-2 (1.5B) · Jina · GPT-4o',
    text: '1,611 training samples built from the NKU website, formatted as instruction, input and output with GPT-4o and manual review, used to fine-tune GPT-2. It answered NKU questions 10–15% better than ChatGPT on our test set.',
    links: [{ t: 'project page', post: 'projects/nku-chatbot/' }],
  },
  {
    when: '2025', title: 'First-year nurse sentiment', tags: 'Python · NLTK · scikit-learn · R Shiny',
    text: 'A pipeline that scrapes forum posts from first-year nurses, cleans them, and classifies stress, depression, workplace and wellbeing themes, with an R Shiny dashboard of how sentiment changes over time.',
    links: [{ t: 'project page', post: 'projects/nurse-sentiment/' }],
  },
  {
    when: '2025', title: 'Cargo After COVID', tags: 'R Shiny · BTS data',
    text: 'Two decades of Bureau of Transportation Statistics air cargo data, 2003 to 2025, made explorable in a few clicks.',
    links: [{ t: 'live app', href: 'https://sidantap.shinyapps.io/CargoAfterCOVID/' }, { t: 'project page', post: 'projects/cargo-after-covid/' }],
  },
];

export const skills = [
  ['Data engineering', 'Azure Databricks, PySpark, Delta Lake, medallion architecture, Unity Catalog, Azure Data Factory, ADLS Gen2, Key Vault, dbt, Snowflake'],
  ['SQL', 'T-SQL, SQL Server, stored procedures, SSIS, SQL Server Agent, dimensional modeling, SCD Type 1 and 2'],
  ['Quality and delivery', 'pytest, black, pylint, Azure DevOps CI/CD, Git, data validation and reconciliation'],
  ['Languages', 'Python, PySpark, SQL, R, TypeScript, DAX'],
  ['Reporting and apps', 'Power BI, Tableau, R Shiny, Power Apps, Power Automate, Microsoft Graph'],
  ['AI and ML', 'LLM fine-tuning (GPT-2), NLP, scikit-learn, embeddings, Claude Code and agents'],
];

// Digital design work (minor in Digital Design, NKU). Descriptions from Sid's Adobe Portfolio.
// kind: 'img' or 'video' (muted loop; poster shown until it plays).
export const design = [
  { title: 'The Porsche Experience', part: 'Garage screen', meta: 'GUI design · game start screen', kind: 'img', src: 'design/porsche-garage.webp',
    text: 'A start screen for a game called The Porsche Experience: a garage to browse and pick cars, a workshop for colors and stats, menus for the store, maps and career, a social hub with multiplayer, inbox and a music player, and a push-to-start button.' },
  { title: 'The Porsche Experience', part: 'Title and push-to-start', meta: 'GUI design · title and button', kind: 'img', src: 'design/porsche-title-button.webp',
    text: 'The game title stands on the left of the screen; the start button borrows from a real car\'s push-to-start, so the game begins the way a drive does.' },
  { title: 'Shapes', part: 'Final animation', meta: 'Autodesk Maya · 3D animation', kind: 'video', src: 'design/maya-shapes.mp4', poster: 'design/maya-shapes.webp',
    text: 'A 3D animation built from simple shapes: a globe made of cubes with a ring around it, a wall of blocks that collapses, and a tunnel of tiles that closes on a thank-you. Excerpts, muted.' },
  { title: 'DFX 394 final project', part: 'Short film', meta: 'Video · compositing', kind: 'video', src: 'design/dfx394-final.mp4', poster: 'design/dfx394-final.webp',
    text: 'A short film for DFX 394: an action figure composited into a night ride, a crash and painted city scenes, with animated lyric captions. Excerpt, muted.' },
  { title: 'Wing It', part: 'Evolution of the spoiler', meta: 'Editorial design', kind: 'img', src: 'design/wingit-evolution.webp',
    text: 'A visual history of classic car spoilers, from the towering wing of the 1970 Plymouth Superbird, built for NASCAR stability, to the 1980s Porsche 911 and its "whale-tail".' },
  { title: 'Wing It', part: 'The 1980 Ford Sierra Cosworth', meta: 'Editorial design', kind: 'img', src: 'design/wingit-ford.webp',
    text: 'The Sierra Cosworth\'s "snow shovel" spoiler: an outsized piece of 1980s styling that also did real aerodynamic work.' },
  { title: 'Humble Beginnings', part: 'Logo', meta: 'Brand identity · logo design', kind: 'img', src: 'design/humble-logo.webp',
    text: 'A logo for a personal brand about growth and resilience: every journey starts with a single step. It went from rough sketches to finished marks.' },
  { title: 'Humble Beginnings', part: 'Banner', meta: 'Brand identity · logo design', kind: 'img', src: 'design/humble-banner.webp',
    text: 'The same identity as a soft, wide banner version of the mark.' },
  { title: 'GTR Skyline: Urban Hue Shift', part: 'Color correction', meta: 'Adobe Photoshop · color correction', kind: 'img', src: 'design/gtr-hue-shift.webp',
    text: 'Recoloring a Skyline GTR so it belongs to the city behind it, using Hue/Saturation and Curves with a palette pulled from the scene.' },
].map((d, i) => ({ ...d, n: String(i + 1).padStart(2, '0') }));
