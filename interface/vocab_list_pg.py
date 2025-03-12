import streamlit as st

# Initialize session state for vocabulary list and reviewed words
if "vocabulary_list" not in st.session_state:
    st.session_state.vocabulary_list = [
        {"word": "romance", "definition": "(n.) a close, usually short relationship of love between two people", "save_date": "2025/02/20", "reviewed": False},
        {"word": "damn", "definition": "(exclamation) used to express anger or frustration", "save_date": "2025/02/21", "reviewed": False},
        {"word": "lover", "definition": "(n.) a partner in a sexual or romantic relationship outside marriage", "save_date": "2025/02/22", "reviewed": False},
    ]

if "reviewed_words" not in st.session_state:
    st.session_state.reviewed_words = []

# Function to move reviewed words to the bottom of the list
def move_reviewed_words():
    for word in st.session_state.vocabulary_list:
        if word["reviewed"]:
            st.session_state.reviewed_words.append(word)
            st.session_state.vocabulary_list.remove(word)

# Page title
st.title("English Music Recommender")
st.subheader("Let's review your vocabulary!")

# Display vocabulary list in a table
st.write("### Vocabulary List")

col1, col2, col3, col4 = st.columns([1, 4, 1.5, 1])

with col1:
    st.write("Word")
with col2:
    st.write("Definition")
with col3:
    st.write("Save Date")
with col4:
    st.write("Review")

for word in st.session_state.vocabulary_list:
    with col1:
        st.write(word["word"])
    with col2:
        st.write(word["definition"])
    with col3:
        st.write(word["save_date"])
    with col4:
        if st.button("Review", key=f"review_{word['word']}"):
            word["reviewed"] = True
            st.session_state.vocabulary_list = [w for w in st.session_state.vocabulary_list if not w["reviewed"]]
            st.session_state.reviewed_words.append(word)
            st.experimental_rerun()

# Display reviewed words at the bottom
if st.session_state.reviewed_words:
    st.write("### Reviewed Words")
    for word in st.session_state.reviewed_words:
        col1, col2, col3 = st.columns([1, 4, 1.5])
        with col1:
            st.write(word["word"])
        with col2:
            st.write(word["definition"])
        with col3:
            st.write(word["save_date"])

# Button to save the review
if st.button("Save Review"):
    move_reviewed_words()
    st.success("Review saved! Refreshing the list...")
    st.experimental_rerun()

