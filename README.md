# 🎬 Movie Recommendation System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" />
  <img src="https://img.shields.io/badge/TMDB-API-01D277?style=for-the-badge&logo=themoviedatabase&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

<p align="center">
A content-based movie recommender that suggests the top 5 most similar movies to any title you pick — powered by TMDB metadata, NLP feature engineering, and cosine similarity.
</p>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Demo](#-demo)
- [System Architecture](#-system-architecture)
- [ML Pipeline](#-ml-pipeline)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Limitations](#-limitations)
- [Future Improvements](#-future-improvements)

---

## 🧠 Overview

This project is a **content-based movie recommendation system** built with Python and Streamlit, using the **TMDB 5000 Movie Dataset**.

The system analyzes movie **overview, genres, keywords, cast, and director** metadata, combines them into a unified `tags` field, vectorizes them with `CountVectorizer`, and computes pairwise **cosine similarity** across all 4,806 movies. When a user selects a movie, the app returns the 5 most similar titles along with posters fetched live from the **TMDB API**.

---

## 🎥 Demo

![alt text](image.png)


---

## 🏗 System Architecture

```mermaid
flowchart TD
    A["👤 User"] -->|"selects a movie"| B["🎛 Streamlit UI (app.py)"]
    B --> C["📦 movie_dict.pkl<br/>(4,806 movies)"]
    B --> D["📊 similarity.pkl<br/>(4806 x 4806 cosine matrix)"]
    C --> E["🔎 Locate selected movie index"]
    D --> F["📈 Fetch similarity scores"]
    E --> F
    F --> G["🏆 Sort & pick top 5 similar movies"]
    G --> H["🌐 TMDB API<br/>(fetch posters by movie_id)"]
    H --> I["🖼 Display 5 titles + posters"]
```

---

## ⚙️ ML Pipeline

```mermaid
flowchart LR
    A["tmdb_5000_movies.csv"] --> C["Merge on title"]
    B["tmdb_5000_credits.csv"] --> C
    C --> D["Select features:<br/>id, title, overview,<br/>genres, keywords, cast, crew"]
    D --> E["Drop missing values"]
    E --> F["Parse JSON fields<br/>(genres, keywords, cast, crew)"]
    F --> G["Keep top 3 cast +<br/>extract director"]
    G --> H["Merge into single<br/>'tags' field"]
    H --> I["Lowercase + Porter Stemming"]
    I --> J["CountVectorizer<br/>(BoW vectors)"]
    J --> K["Cosine Similarity Matrix"]
    K --> L["Save as movie_dict.pkl<br/>& similarity.pkl"]
```

**Steps:**

1. Load `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`.
2. Merge both datasets on movie title.
3. Keep: `movie_id`, `title`, `overview`, `genres`, `keywords`, `cast`, `crew`.
4. Drop rows with missing values.
5. Parse JSON-formatted `genres`, `keywords`, `cast`, `crew`.
6. Keep the top 3 cast members.
7. Extract the director from crew data.
8. Combine overview + genres + keywords + cast + director → `tags`.
9. Lowercase all tags.
10. Apply Porter stemming.
11. Vectorize tags using `CountVectorizer`.
12. Compute cosine similarity across all movies.
13. Serialize processed data and similarity matrix as `.pkl` files.

---

## 🛠 Tech Stack

| Category | Tools |
|---|---|
| Language | Python |
| Web App | Streamlit |
| Data Handling | Pandas, NumPy |
| ML / NLP | Scikit-learn (`CountVectorizer`, cosine similarity), NLTK (Porter Stemmer) |
| External API | TMDB API (posters) |
| Serialization | Pickle |

---

## 📁 Project Structure

```
movie-recommendation-system/
├── app.py                              # Streamlit app + recommendation logic
├── Movie_Recommandation_System.ipynb   # Data preprocessing & model generation
├── tmdb_5000_movies.csv                # Movie metadata
├── tmdb_5000_credits.csv               # Cast & crew metadata
├── models/
│   ├── movie_dict.pkl                  # Processed movie data (4,806 movies)
│   └── similarity.pkl                  # Precomputed 4806x4806 similarity matrix
├── requirements.txt                    # Python dependencies
└── README.md
```

---

## 💻 Installation

```bash
git clone https://github.com/darshil2032007/movie-recommendation-system.git
cd movie-recommendation-system
pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
streamlit run app.py
```

1. Open the local Streamlit URL shown in the terminal.
2. Select a movie from the dropdown.
3. Click **Recommend**.
4. View the top 5 similar movies with posters.

---

## ⚠️ Limitations

- Content-based only — not personalized to individual user behavior/ratings.
- Recommendations depend solely on metadata quality (overview, genres, keywords, cast, director).
- The selected movie must exist in the processed dataset.
- Poster retrieval requires internet access and a valid TMDB API key.
- The TMDB API key is currently hard-coded in `app.py` — move it to Streamlit secrets or an environment variable before deploying.
- Recommendation quality is bounded by the original TMDB metadata and the chosen vectorization method (`CountVectorizer` vs. TF-IDF).

---

## 🔮 Future Improvements

- [ ] Move TMDB API key to `.env` / Streamlit secrets.
- [ ] Switch to TF-IDF or embeddings (e.g., Sentence-BERT) for richer similarity.
- [ ] Add collaborative filtering using user ratings for hybrid recommendations.
- [ ] Cache TMDB API responses to reduce latency and API calls.
- [ ] Deploy on Streamlit Community Cloud / Docker.

---

<p align="center">Made with 🐍 Python & ❤️</p>