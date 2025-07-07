import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sentence_transformers import SentenceTransformer
import numpy as np
import matplotlib.pyplot as plt

# Optional: UMAP for visualization (if needed)
# from umap import UMAP

def cluster_transactions(input_csv, output_csv, n_clusters=6):
    # Load data
    df = pd.read_csv(input_csv)

    # Step 1: Embed Descriptions
    model = SentenceTransformer("all-MiniLM-L6-v2")  # Fast, effective model
    embeddings = model.encode(df["Description"].astype(str).tolist())

    # Step 2: (Optional) Normalize embeddings
    scaler = StandardScaler()
    embeddings_scaled = scaler.fit_transform(embeddings)

    # Step 3: KMeans Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(embeddings_scaled)
    df["Cluster"] = clusters

    # Step 4: Save output
    df.to_csv(output_csv, index=False)
    print(f"✅ Saved clustered data to {output_csv}")
    
    # Step 5: Print top 5 descriptions per cluster
    for cluster_id in sorted(df["Cluster"].unique()):
        print(f"\n🔹 Cluster {cluster_id}")
        top = df[df["Cluster"] == cluster_id]["Description"].value_counts().head(5)
        print(top)

    # Optional: UMAP for visualization
    # reducer = UMAP(n_neighbors=15, min_dist=0.1, metric='cosine', random_state=42)
    # embedding_2d = reducer.fit_transform(embeddings_scaled)
    # plt.figure(figsize=(10, 6))
    # plt.scatter(embedding_2d[:, 0], embedding_2d[:, 1], c=clusters, cmap="tab10")
    # plt.title("Transaction Clusters (UMAP)")
    # plt.show()

# Example usage
if __name__ == "__main__":
    cluster_transactions("parsed_td.csv", "clustered_td.csv", n_clusters=6)
