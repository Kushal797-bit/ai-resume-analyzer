import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
import os

# 1. Load dataset
df = pd.read_csv("../data/UpdatedResumeDataSet.csv")
print(df.head())
print(df["Category"].value_counts())

# 2. Split features/labels
X = df["Resume"]
y = df["Category"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Vectorize resume text
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000,
    ngram_range=(1, 2)
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 4. Train classifier
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train_vec, y_train)

# 5. Evaluate
y_pred = clf.predict(X_test_vec)
print(classification_report(y_test, y_pred))

# 6. Save model + vectorizer
os.makedirs("models", exist_ok=True)
joblib.dump(clf, "models/role_classifier.pkl")
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

print("Model and vectorizer saved to ml/models/")