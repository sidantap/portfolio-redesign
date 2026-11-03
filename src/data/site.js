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
  { k: 'resume', label: 'Résumé', value: 'One-page résumé', href: 'profile/#top' },
];

// Home "work" list: year · title · where it lives
export const work = [
  { year: '2026', title: 'comply., a system of record for DOT drug and alcohol testing', where: 'complydot.org', href: 'https://www.complydot.org' },
  { year: '2026', title: 'A data pipeline that runs every night for $0', where: 'live dashboard', href: 'https://sidantap.github.io/nightly-311-pipeline/' },
  { year: '2026', title: 'Medallion lakehouse on Azure Databricks', where: 'NKWD' },
  { year: '2025', title: 'FAA drug and alcohol testing randomizer in R Shiny', where: 'Atlas Air' },
  { year: '2025', title: 'Reading how first-year nurses feel, with NLP', where: 'NKU research' },
  { year: '2025', title: 'Cargo After COVID: two decades of U.S. air cargo', where: 'live app', href: 'https://sidantap.shinyapps.io/CargoAfterCOVID/' },
  { year: '2024', title: 'An NKU chatbot on a fine-tuned GPT-2', where: 'research poster' },
];

export const experience = [
  {
    when: '02/2026–Current', role: 'Data Analytics Engineer',
    logo: { text: 'NKWD', label: 'Northern Kentucky Water District' }, org: 'Northern Kentucky Water District · Erlanger, KY',
    text: 'Medallion (bronze, silver, gold) pipelines on Azure Databricks with PySpark and Delta Lake, loading raw data incrementally and modeling gold facts and dimensions with SCD Type 1 and 2. Config-driven ingestion from SQL Server sources (CIS, Lucity, LIMS, Antero) and REST APIs (Paycor, KnowBe4, CivicPlus, ServiceDesk Plus), orchestrated with Azure Data Factory, ADLS Gen2 and Key Vault and shipped through Azure DevOps CI/CD with pytest, black and pylint. Built 10–20 Power BI reports for seven departments and migrated 40–50 Crystal Reports, saving 20–40 staff hours a week.',
    links: [{ t: 'Power BI write-up (soon)' }],
  },
  {
    when: '05/2025–12/2025', role: 'Data Analysis and Process Solutions Intern',
    logo: { src: 'logos/atlas.svg', ar: 5.85, label: 'Atlas Air' }, org: 'Atlas Air Worldwide · Erlanger, KY',
    text: 'Built the FAA drug and alcohol testing app in R Shiny: eligibility filtering, randomized selection, rollover, deduplication and SharePoint audit logging through Microsoft Graph. Power Automate flows for the pilot Master Training Schedule, crew scheduling and immigration reporting, part of about 25–30 staff hours saved a week. Logged usage across three internal tools into Power BI.',
    links: [],
  },
  {
    when: 'Fall 2025', role: 'Teaching Assistant and Research Assistant',
    logo: { src: 'logos/nku.svg', ar: 4.11, label: 'Northern Kentucky University' }, org: 'NKU College of Informatics',
    text: 'TA for web development (INF 286): grading, an exam review quiz and office hours. Web scraping, machine learning and NLP in faculty research with Dr. Junxiu Zhou.',
    links: [],
  },
  {
    when: 'Fall 2025', role: 'Innovation Fellow',
    logo: { src: 'logos/kcv.png', ar: 2.98, label: 'Kentucky Commercialization Ventures' }, org: 'Kentucky Commercialization Ventures',
    text: 'One of ten fellows in the Fall 2025 cohort. Customer discovery, SWOT, failure-mode assessment and a commercialization plan for VIDVO.',
    links: [{ t: 'KCV announcement', href: 'https://www.kycommercializationventures.com/post/ten-graduate-from-fall-2025-innovation-fellowship-cohort' }],
  },
  {
    when: '08/2024–12/2024', role: 'Data Science Intern',
    logo: { src: 'logos/medpace.svg', ar: 6.95, label: 'Medpace' }, org: 'Medpace · Cincinnati, OH',
    text: 'dbt and SQL transformations on Snowflake, and cleaning and validating millions of clinical trial records with Python, SQL and R. An R Shiny map of global clinical studies for proposals, and monthly dashboard design sessions for 10+ analysts in the US and UK.',
    links: [],
  },
  {
    when: '01/2024–08/2024', role: 'Data Analytics Intern',
    logo: { src: 'logos/motus.png', ar: 3.75, label: 'Motus Freight' }, org: 'Motus Freight · Bellevue, KY',
    text: 'Tableau Cloud dashboards on Turvo data, including a CO2 dashboard that contributed to a 12.4% drop in emissions and a regional dashboard across 4 regions and 49 states that contributed to a 15% rise in profit.',
    links: [],
  },
];

export const selected = [
  {
    when: '2026–', title: 'comply.', tags: 'React · TypeScript · Vitest · three.js',
    text: 'A system of record for DOT drug and alcohol random testing. It syncs employees from the HR system, routes every pool change through approval, runs random selections anyone can re-run to prove they were fair, and tracks each test to its MRO result. Live for FAA (14 CFR Part 120); the other DOT agencies are next.',
    img: 'img/comply.jpg', cap: 'complydot.org', links: [{ t: 'complydot.org', href: 'https://www.complydot.org' }],
  },
  {
    when: '2026', title: 'A data pipeline that runs every night for $0', tags: 'Python · DuckDB · dbt · GitHub Actions',
    text: 'Cincinnati 311 requests, NOAA weather and NHTSA vehicle complaints, loaded incrementally, tested and modeled with dbt into a star schema every night. Bad rows go to quarantine with a reason; a small open-source model classifies new complaints and is scored against NHTSA’s own labels.',
    img: 'img/nightly-overview.jpg', cap: 'Nightly 311 dashboard', links: [{ t: 'dashboard', href: 'https://sidantap.github.io/nightly-311-pipeline/' }, { t: 'code', href: 'https://github.com/sidantap/nightly-311-pipeline' }, { t: 'write-up', post: 'writing/nightly-311/' }],
  },
  {
    when: '2024', title: 'An NKU chatbot on a fine-tuned GPT-2', tags: 'Python · GPT-2 (1.5B) · Jina · GPT-4o',
    text: '1,611 training samples built from the NKU website, formatted as instruction, input and output with GPT-4o and manual review, used to fine-tune GPT-2. It answered NKU questions 10–15% better than ChatGPT on our test set.',
    links: [{ t: 'write-up', post: 'writing/nku-chatbot/' }],
  },
  {
    when: '2025', title: 'First-year nurse sentiment', tags: 'Python · NLTK · scikit-learn · R Shiny',
    text: 'A pipeline that scrapes forum posts from first-year nurses, cleans them, and classifies stress, depression, workplace and wellbeing themes, with an R Shiny dashboard of how sentiment changes over time.',
    links: [],
  },
  {
    when: '2025', title: 'Cargo After COVID', tags: 'R Shiny · BTS data',
    text: 'Two decades of Bureau of Transportation Statistics air cargo data, 2003 to 2025, made explorable in a few clicks.',
    links: [{ t: 'live app', href: 'https://sidantap.shinyapps.io/CargoAfterCOVID/' }],
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

// Placeholders until the real digital design pieces arrive.
export const design = Array.from({ length: 8 }, (_, i) => ({
  n: String(i + 1).padStart(2, '0'),
  title: 'Design piece ' + String(i + 1).padStart(2, '0'),
  meta: 'Tool · Year',
}));
