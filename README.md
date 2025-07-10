# Cybersecurity Labs Platform

![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Traefik](https://img.shields.io/badge/traefik-%2324CEC3.svg?style=for-the-badge&logo=traefik&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Django](https://img.shields.io/badge/Django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

This repository hosts a **Cybersecurity Education Platform** built to provide hands-on interactive labs for learners at all levels. Each lab spins up in its own isolated Docker container, accessible via dynamic subdomains managed by Traefik and Nginx. The core components include:

- **Django** for the user portal, registration, lab catalog and administration interface  
- **Flask** microservice (edge-server) for lab orchestration (start/stop, health checks)  
- **Traefik** as an automated reverse proxy and router for lab containers  
- **Nginx** for serving static assets and acting as the entrypoint  
- **Docker** to encapsulate each lab environment in a clean, reproducible container  

> [!NOTE]
>  This repo is under active development. 

---

## Table of Contents

1. [Getting Started](#getting-started)  
2. [Architecture Overview](#architecture-overview)  
3. [Lab Modules](#lab-modules)  
4. [Administration](#administration)  
5. [Contributing](#contributing)  
6. [License](#license)  

---

## Getting Started

```bash
git pull <this-repo>
```
I've setup all processes via pm2, so can you. 
For better understanding i will use terms **siteA** and **siteB**

SiteA: 
- Run clientSite

SiteB:
- Setup traefic via docker-compose.yml
- Run afk_killer.y
- Run image-manager.py 

---

## Architecture Overview


Four core processes spread across two servers:

| # | Component | Host | Role |
|---|-----------|------|------|
| 1 | **ClientSite** (Django) | **Server A** | Public site with auth, catalog, admin |
| 2 | **image-manager** (Flask) | **Server B** | Starts / stops lab containers, provides status API |
| 3 | **Traefik** | **Server B** | Reverse-proxy; routes `https://<user>-<lab>.<domain>` to lab |
| 4 | **AFK killer** | **Server B** | Removes idle labs after `AFK_TIMEOUT_MINUTES` |

### Lab categories inside *image-manager*

| Folder | Purpose |
|--------|---------|
| **CoreBlog** | Multi-vuln image; vulnerability toggled via env flag |
| **SpecialLabs** | Stand-alone labs with custom logic |

To register a *SpecialLab*:

1. Add its name to `SPECIAL_LABS` in `vps-labs-api/image-manager.py`.
2. Build it: `docker build -t <container_name> <path/to/folder>`
3. If it needs port **9000**, append its name to `labs_to_open_9000port`.

---

## Lab Modules
> [!NOTE]
> Below is written container names that specified in admin panel

#### Access control:
- idor_bac
- basic_csrf
- http_parameter_pollution_priv_esc
- circumbent_via_header

#### Authentication:
- session_fixation
- auth_bypass_forgotten_cookie
- 2fa_bypass_weak_logic
- brute_force

#### Cross-site scripting:
- xss_angular_sandbox_escape
- ssti_via_jinja2
- reflected_xss
- stored_xss

#### DOM-based vulnerabilities:
- clobbering_dom_attr_to_bp_html_filters
- dom_xss_polyglot
- dom_based_cookie_manipulation
- dom_based_open_redirection

#### HTTP request smuggling:
- http_request_smuggling_cache_poison
- poc_confirming_cl_te
- poc_confirming_te_cl
- front_end_request_rewriting

#### Insecure deserialization:
- insecure_deserialization
- modifying_serialized_objects
- modifying_serialized_data_types 
- using_app_func_to_exploit_insecure_deserialization

#### OS command injection:
- command_injection_basic
- blind_command_injection_time_delay
- blind_command_injection_oob_interaction
- command_injection_filter_bypass

#### SQL injection:
- sql_inj_classic
- sql_union_column_number_discovery    
- blind_sql_injection_conditional          
- blind_sql_injection_time_delay

#### Server-side request forgery (SSRF):
- open_redirect_to_ssrf_chain
- ssrf_whitelist_based_bypass
- blind_ssrf_shellshock
- ssrf_blacklist_bypass_ipv6 

#### XML external entity (XXE) injection:
- xxe_via_xml_post
- xxe_repurpose_local_dtd
- blind_xxe_to_retrieve_data_via_error_messages
- xxe_to_perform_ssrf_attacks
  
---

## Administration

Add or edit labs via Django Admin:

| Field | Description |
|-------|-------------|
| **Lab name** | Display title |
| **Container name** | Must match Docker image / `SPECIAL_LABS` entry |
| **Tier** | Difficulty / points |
| **Description** | Shown on card list |
| **Category** | Used for sidebar grouping |
| **Full description** | Rendered on lab detail page |

---

## License

MIT License © 2025 Cybersecurity Labs Platform contributors
