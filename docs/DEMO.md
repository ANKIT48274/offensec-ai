# Demo Script

**Duration:** 5–10 minutes

---

## Step 1: Introduction (30 seconds)

**Narration:** "Welcome to OffenSec AI — an open-source, AI-powered offensive security platform. Today I'll demonstrate how to set up a project, run a multi-tool scan pipeline, and view the AI-analysed results."

**Screen:** Terminal with `docker compose up` or browser at `http://localhost:8000/docs`

---

## Step 2: Register & Login (1 minute)

**Narration:** "First, create an account and log in to generate your JWT token."

**Action:**
1. Open `http://localhost:3000/auth/login`
2. Click "Register" link
3. Enter email, username, password
4. Submit — user created
5. Login with credentials

**Expected Screen:** Redirected to Projects page

**Talking Points:**
- JWT token auto-saved in localStorage
- All subsequent API calls authenticated

---

## Step 3: Create Project (30 seconds)

**Narration:** "Create a project to organise your assessments."

**Action:**
1. Click "New Project"
2. Enter: "Internal Pentest Q3"
3. Add description: "First assessment of internal network"
4. Submit

**Expected Screen:** Project detail with empty assessment list

---

## Step 4: Run Scan Pipeline (2 minutes)

**Narration:** "The pipeline runs Nmap, HTTPX, and Nuclei in sequence — one click."

**Action:**
1. Navigate to Pipeline → New Pipeline Scan
2. Enter target: `192.168.1.1` (or a target of your choice)
3. Click "Start Pipeline"

**Expected Screen:** Progress bar showing Nmap → HTTPX → Nuclei steps

**Talking Points:**
- Pipeline status updates asynchronously
- Each step shows pending → running → completed
- Failed steps show error messages

---

## Step 5: Nmap Results (30 seconds)

**Narration:** "Nmap discovered open ports and services."

**Action:**
1. Navigate to Scans
2. Click the completed scan

**Expected Screen:** Port table showing port, protocol, state, service, version

**Talking Points:**
- Only open ports shown (filtered ports excluded)
- OS detection, service version, and script results included

---

## Step 6: HTTPX Results (30 seconds)

**Narration:** "HTTPX probed the discovered web services."

**Expected Screen:** HTTPX results table with URLs, status codes, titles, server headers, technology stack

**Talking Points:**
- Technology detection identifies frameworks, servers, and libraries
- Favicon hash can be used for asset fingerprinting

---

## Step 7: Nuclei Results (1 minute)

**Narration:** "Nuclei ran hundreds of vulnerability templates against our targets."

**Action:**
1. Navigate to Nuclei → Results
2. Filter by severity: "Critical"
3. Click a finding to expand details

**Expected Screen:** Findings table with severity badge, template name, matched URL, CVE IDs, CVSS scores

**Talking Points:**
- Severity counts shown at top (critical, high, medium, low, info)
- Filter and search available
- Each finding includes description and remediation

---

## Step 8: Assets (30 seconds)

**Narration:** "Discovered assets are automatically tracked and deduplicated."

**Action:**
1. Navigate to Assets

**Expected Screen:** Asset cards showing IP/hostname, open ports, technologies, OS guesses, scan count, first/last seen timestamps

**Talking Points:**
- Assets are merged across scans
- Ports and technologies accumulated over time
- Evidence linked per asset

---

## Step 9: AI Correlation (1 minute)

**Narration:** "The AI engine correlates all collected evidence to produce an executive summary, risk score, attack paths, and recommendations."

**Action:**
1. Navigate to AI → Run Analysis
2. View the report

**Expected Screen:** Risk score (0–100), executive summary, critical assets, top risks, attack paths, recommendations

**Talking Points:**
- Risk score computed from vulnerability severity, exposure, and asset criticality
- Attack paths show potential breach chains
- Recommendations are actionable

---

## Step 10: Reports (30 seconds)

**Narration:** "Export findings in professional formats."

**Action:**
1. Navigate to Reports
2. Select style: Executive, Technical, OWASP, or PTES
3. Download

**Expected Screen:** Report preview or download prompt

**Talking Points:**
- CSV and JSON export available for data processing
- Multiple report styles for different audiences

---

## Step 11: Swagger API (30 seconds)

**Narration:** "All 39 endpoints are documented in Swagger."

**Action:**
1. Open `http://localhost:8000/docs`

**Expected Screen:** Interactive Swagger UI with all API endpoints grouped by resource

**Talking Points:**
- Try endpoints directly from the browser
- Authentication required via Authorize button

---

## Step 12: Conclusion (30 seconds)

**Narration:** "OffenSec AI provides a complete, open-source security assessment platform — from reconnaissance to reporting, powered by AI-driven correlation. Deploy it today and take control of your security assessments."

**Action:** End demo

---

## Common Questions

**Q: How long do scans take?**  
A: Depends on target. Quick Nmap (top 100 ports) ~30s. Full pipeline with all tools ~5-10 min.

**Q: Can I scan external targets?**  
A: Yes. Any reachable IP or hostname. Ensure you have authorisation.

**Q: What if a tool isn't installed?**  
A: The engine handles missing binaries gracefully and reports the error.

**Q: Is the AI using an LLM?**  
A: Currently it's a rules-based correlation engine. LLM support is planned.
