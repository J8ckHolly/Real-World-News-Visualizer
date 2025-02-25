import feedparser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re 
from PageRankingAlgo import Node, WeightedGraph



def TitleEntries():
    rss_url = "https://news.google.com/rss/search?q=us"
    feed = feedparser.parse(rss_url)

    myarr = []
    count = 0
    # Loop through each entry (RSS item)
    for entry in feed.entries:
        cleaned_title = re.sub(r'[^\x00-\x7F]+', '', entry.title)
        hyphen_index = cleaned_title.rfind(' -')
        if hyphen_index != -1:
            cleaned_title = cleaned_title[:hyphen_index]

        #print(f"Title: {cleaned_title}")
        myarr.append(cleaned_title)
        #print("")
    return myarr

def cosineSimilarity(myArr):
    # List of your titles/articles
    titles = [
        "Elon Musk and Donald Trump Are Not Fixing U.S. Foreign Aid but Destroying It - The New Yorker",
        "Ending USAID programs could undercut Trump's goal of slashing migration to U.S., experts warn - NBC News",
        "Trump's aid freeze sparks mayhem around the world - Reuters",
        # Add other titles here...
    ]

    # Step 1: Vectorize the titles using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
    tfidf_matrix = vectorizer.fit_transform(myArr)

    # Step 2: Compute pairwise cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix)

    # Step 3: Display the cosine similarity matrix
    #print("Cosine Similarity Matrix:")
    #print(cosine_sim)

    # Example: Get the similarity between the first and second article
    #similarity_value = cosine_sim[0, 1]
    #print(f"Similarity between Article 1 and Article 2: {similarity_value}")
    return cosine_sim

def zeroOut(matrix):
    threshold = .06
    Perfect = 0
    Good = 0
    Dropped = 0
    max_value = 0
    
    # Iterate over each row and each value in the row
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] < threshold:
                matrix[i][j] = 0
                Dropped +=1  
            if matrix[i][j] >= 1:
                Perfect +=1
            else:
                matrix[i][j] = round(matrix[i][j], 6)
                if matrix[i][j] > max_value:
                    max_value = matrix[i][j]
                    maxIndex = [i,j]
                Good +=1
    print(f"Perfect: {Perfect}")
    print(f"Good: {Good}")
    print(f"Dropped: {Dropped}")
    print(f"Max Value: {max_value}")
    """
    with open("matrix_output.txt", "w") as file:
        for row in matrix:
            # Convert each row into a string of space-separated values
            file.write(" ".join(map(str, row)) + "\n")
    """
    

titleArr = []
titleArr = TitleEntries()
#print(titleArr)
titles = [
    "Elon Musk and Donald Trump Are Not Fixing U.S. Foreign Aid but Destroying It",
    "Ending USAID programs could undercut Trump's goal of slashing migration to U.S., experts warn",
    "Trump's aid freeze sparks mayhem around the world",
    "How Trump's Foreign Aid Cuts Impact Developing Nations",
    "The Long-Term Effects of Trump's Aid Policy on Global Poverty",
    "US Foreign Aid Under Trump: A Crisis in the Making",
    "The Future of USAID: Trump's Foreign Policy Shifts and Global Diplomacy",
    "Rising Tensions in the Middle East After Trump's Withdrawal from Syria",
    "The Impact of Climate Change on Global Security and International Relations"
]
matrix = cosineSimilarity(titleArr)
zeroOut(matrix)
graph = WeightedGraph()
graph.convert_matrix_to_graph(matrix)
graph.page_ranking_algorithm()
graph.display_graph()
#graph.page_ranking_algorithm()