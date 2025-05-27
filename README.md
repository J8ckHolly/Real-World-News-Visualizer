🌍 Real-World News Globe
This project visualizes real-world news on an interactive 3D globe. The frontend, built with Three.js, TypeScript, and RxJS, allows users to explore global news stories spatially and temporally.

![image](https://github.com/user-attachments/assets/935a4b71-4306-4561-9080-a0d46af915ee)


🧠 How It Works
The system scrapes news articles from Google RSS feeds, then ranks them by relevance using a custom graph-based approach:

Scraping & Parsing: Python scripts gather and process articles using Firecrawl agents and OpenAI APIs.

Text Analysis: Titles are analyzed using an inverse frequency search to detect unique and significant keywords.

Graph Construction: Articles are linked based on keyword similarity to form a weighted graph.

Ranking Algorithm: A custom PageRank-like algorithm with a dampening factor ranks articles by importance.

Data Storage: All structured data is stored in a PostgreSQL database and served to the frontend.

![System Design](https://github.com/user-attachments/assets/598a1974-54ed-43b1-b56c-3d86c9d2d8b3)


🛠️ Technologies Used
Frontend: Three.js, TypeScript, RxJS

Backend: Python, SQL, PostgreSQL

APIs: OpenAI, Firecrawl

Algorithms: Inverse frequency scoring, Graph similarity, PageRank with dampening









