# Validation Guide

## Testing Procedures for Real-World Targets

### DVWA (Damn Vulnerable Web Application)

#### Setup
```bash
docker run -d -p 80:80 vulnerables/web-dvwa
```

#### Configuration
- Target: `http://localhost:80`
- Credentials: `admin` / `password`

#### Expected Results

| Tool | Expected Findings |
|------|------------------|
| **Nmap** | Port 80 open, Apache service detected |
| **HTTPX** | Status 200, title "Damn Vulnerable Web Application", tech: PHP, Apache |
| **Nuclei** | SQLi templates, XSS templates, multiple high-severity findings |
| **AI Analysis** | Risk score 60-80, critical assets identified, actionable recommendations |

### OWASP Juice Shop

#### Setup
```bash
docker run -d -p 3000:3000 bkimminich/juice-shop
```

#### Configuration
- Target: `http://localhost:3000`

#### Expected Results

| Tool | Expected Findings |
|------|------------------|
| **Nmap** | Port 3000 open, Node.js service |
| **HTTPX** | Status 200, tech: Express, JavaScript |
| **Nuclei** | Multiple critical vulnerabilities, CVE matches |
| **AI Analysis** | Risk score 70-90, extensive attack paths |

### Metasploitable 2

#### Setup
Download from SourceForge and import into VirtualBox/VMware.

#### Configuration
- Target: `192.168.x.x` (VM IP)

#### Expected Results

| Tool | Expected Findings |
|------|------------------|
| **Nmap** | 20+ open ports, multiple services: vsftpd, Apache, Samba, PostgreSQL |
| **HTTPX** | Multiple web services on ports 80, 8080 |
| **Nuclei** | Critical findings: UnrealIRCd backdoor, vsftpd backdoor, Samba CVE |
| **AI Analysis** | Risk score 80-95, multiple critical assets |

### Metasploitable 3

#### Setup
Download from SourceForge, build with Packer.

#### Configuration
- Target: `192.168.x.x` (VM IP)

#### Expected Results

| Tool | Expected Findings |
|------|------------------|
| **Nmap** | 20+ open ports, Windows services, IIS, SMB, RDP |
| **HTTPX** | IIS web server detected |
| **Nuclei** | Multiple critical Windows vulnerabilities |
| **AI Analysis** | Risk score 75-90 |

### False Positives

Known false positives across targets:
- **Nuclei info-severity findings** — May flag standard HTTP headers as "missing security headers" (X-Frame-Options, CSP). Verify manually.
- **Nmap OS detection** — May incorrectly identify containers vs. full OS.
- **HTTPX tech detection** — May miss obfuscated JavaScript frameworks.

### Limitations

- Scans are network-speed dependent. Full port scans (`-p-`) on remote targets can take 30+ minutes.
- Nuclei requires template updates: `nuclei -update-templates`
- AI analysis is rules-based. It does not use LLMs for the current version.
- Target validation requires the target to be reachable from the OffenSec AI host.
