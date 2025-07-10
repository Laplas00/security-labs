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

> **Note:** This repo is under active development. 

---

## Table of Contents

1. [Getting Started](#getting-started)  
2. [Architecture Overview](#architecture-overview)  
3. [Lab Modules](#lab-modules)  
4. [Administration](#administration)  
5. [Contributing](#contributing)  
6. [License](#license)  

---
