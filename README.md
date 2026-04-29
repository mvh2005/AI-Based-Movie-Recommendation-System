# 🎬 AI-Based-Movie-Recommendation-System


This project builds a **content-based movie recommender system** using cosine similarity on user ratings data. It suggests movies similar to a given movie based on what other users have rated similarly.


---

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vigneshgit2005/AI-Based-Movie-Recommendation-System.git
   
---

## 📁 Dataset Information

The project uses the following CSV files:

1. **Dataset.csv**  
   Contains user ratings:
   - `user_id`: ID of the user
   - `item_id`: ID of the movie
   - `rating`: Rating given by the user

2. **Movie_Id_Titles.csv**  
   Contains movie titles:
   - `item_id`: Movie ID
   - `title`: Movie name

---

## 📊 Features

- Creates a **User-Movie rating matrix**
- Uses **cosine similarity** to find similar movies
- Provides **top 5 recommended movies** for a given input
- **Visualizes**:
  - Bar chart of recommended movies
  - Heatmap of similarity among top 10 rated movies
- Interactive function to input any movie and get recommendations

---

## 🛠️ How to Run

### 📌 Requirements:
- Python 3.x
- pandas, matplotlib, seaborn, scikit-learn

### 🚀 Steps:
1. Clone or download this repository
2. Place `Dataset.csv` and `Movie_Id_Titles.csv` in the same directory
3. Open and run `Movie_Recommendation_Project.ipynb` in **Jupyter Notebook**

---

## 🧠 Example Output

**Input:**

Enter a movie title: Babe (1995)


**Output:**

🎬 Top 5 movies similar to 'Babe (1995)':

    Back to the Future (1985) — Similarity Score: 0.59

    Raiders of the Lost Ark (1981) — Similarity Score: 0.57

    E.T. the Extra-Terrestrial (1982) — Similarity Score: 0.57

    Princess Bride, The (1987) — Similarity Score: 0.56

    Empire Strikes Back, The (1980) — Similarity Score: 0.56

    

## 📦 Future Improvements

- Add a **Streamlit web app** for live interaction
- Include **user-based recommendations**
- Integrate with a movie poster API for enhanced UI

---

## 🤝 Credits

Built with ❤️ using Python, pandas, scikit-learn, and seaborn.

---


