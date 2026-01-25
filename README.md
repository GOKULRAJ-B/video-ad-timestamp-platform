# Ad Insertion Recommendation Platform  

---

## Overview
This project implements an **industry-grade data platform** that recommends **optimal ad-insertion timestamps in videos** by analyzing **audio signals** and **video scene transitions**.

The primary focus is on:
- Scalable **data engineering pipelines**
- **Medallion architecture (Bronze / Silver / Gold)**
- Workflow orchestration using **Apache Airflow**
- **Dockerized workloads**
- **CI/CD with GitHub Actions**
- **Kubernetes-based deployment**

Machine Learning is treated as a **supporting component**, with emphasis on **rule-based and lightweight decision logic** commonly used in production ad-tech systems.

---

## Business Problem
Poorly placed ads negatively impact:
- Viewer experience
- Watch time
- Ad revenue

### Objective
Automatically detect **natural breakpoints** in videos where ads can be inserted without disrupting user experience, using:
- Audio silence and energy drops
- Video scene transitions and motion intensity

---

## High-Level Architecture

Raw Videos
↓
Ingestion Service
↓
🟤 Bronze Layer (Raw Data)
↓
Feature Extraction Jobs
↓
⚪ Silver Layer (Processed Features)
↓
Ad Slot Scoring Logic
↓
🟡 Gold Layer (Final Recommendations)
↓
Data Warehouse + API


---

## Tech Stack

### Data & Storage
- Object Storage: S3 / GCS / MinIO
- Data Lake Format: Parquet
- Data Warehouse: PostgreSQL / BigQuery / Snowflake
- Partitioning: date, video_id

### Processing & Orchestration
- Audio Processing: FFmpeg, Librosa
- Video Processing: OpenCV
- Workflow Orchestration: Apache Airflow
- Batch and parallel processing

### DevOps & Infrastructure
- Containerization: Docker
- CI/CD: GitHub Actions
- Orchestration: Kubernetes
- Monitoring: Prometheus, Grafana
- Logging: ELK / Loki
- Secrets Management: Kubernetes Secrets

---

## Data Lake Architecture (Medallion Pattern)

### Bronze – Raw & Immutable

bronze/
├── video_metadata/
├── audio_tracks/
└── video_frames/

- Raw inputs
- No transformations
- Append-only storage

---

### Silver – Cleaned & Feature-Ready

silver/
├── audio_features/
├── scene_transitions/
└── merged_features/

- Silence duration
- Audio energy
- Scene boundary timestamps
- Motion intensity

---

### Gold – Business Output

gold/
└── ad_recommendations/


Schema:
```sql
video_id
ad_start_time
ad_end_time
confidence_score
reason


Ad Recommendation Logic

This project avoids heavy ML models and instead uses interpretable rules and lightweight scoring logic.

Example Logic

Silence duration exceeds threshold

Scene transition detected

Low motion intensity


if silence > 1.5 and scene_change and motion < threshold:
    mark_as_ad_slot()


Airflow Pipeline Design

DAG Flow

ingest_videos
   ↓
extract_audio
extract_frames
   ↓
audio_features
video_features
   ↓
merge_features
   ↓
score_ad_slots
   ↓
load_to_warehouse


Repository Structure:

video-ad-platform/
├── ingestion/
│   ├── producer/
│   └── consumer/
├── processing/
│   ├── audio/
│   ├── video/
│   └── scoring/
├── airflow/
│   ├── dags/
│   └── plugins/
├── warehouse/
│   ├── ddl/
│   └── models/
├── api/
│   └── app.py
├── docker/
│   ├── airflow.Dockerfile
│   └── processor.Dockerfile
├── k8s/
│   ├── deployments/
│   ├── jobs/
│   ├── statefulsets/
│   └── secrets/
├── .github/workflows/
├── scripts/
└── README.md



Kubernetes Architecture

Component         ------------------------>	Kubernetes Object
Airflow Scheduler ------------------------>	Deployment
Airflow Webserver ------------------------>	Deployment
Feature Extraction------------------------>  Jobs	Job
Metadata Database ------------------------>	StatefulSet
Object Storage	  ------------------------>  PersistentVolume
