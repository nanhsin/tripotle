import streamlit as st
import requests
import pandas as pd
from streamlit_js_eval import streamlit_js_eval

# # Handle page automatically refresh when click on navigation tab
# # Initialize session state for tracking the current page
# if "current_page" not in st.session_state:
#     st.session_state.current_page = "Vocabulary List"
# # Check if the page has changed
# if st.session_state.current_page != "Vocabulary List":
#     st.session_state.current_page = "Vocabulary List"  # Update the session state
#     st.rerun()  # Trigger a rerun


# Page title
st.title("🎵 English Music Recommender")
st.subheader("Let's review your vocabulary!")

# Initialize session state for vocabulary list and reviewed words
def initialize_vocab_list():
    if "auth_token" not in st.session_state:
        token = streamlit_js_eval(js_expressions="localStorage.getItem('auth_token')")
        if token:
            st.session_state['auth_token'] = token
            st.session_state['logged_in'] = True
    headers = {"Authorization": f"Token {st.session_state.get('auth_token', '')}"}
    if "vocabulary_list" not in st.session_state:
        url = "http://localhost:8000/savevocab/"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            st.session_state.vocabulary_list = response.json()
        else:
            st.error("Failed to load vocabulary list. Using a default list.")

        # st.session_state.vocabulary_list = [
        #     {"word": "romance", "definition": "(n.) a close, usually short relationship of love between two people", "save_date": "2025/02/20", "reviewed": False},
        #     {"word": "damn", "definition": "(exclamation) used to express anger or frustration", "save_date": "2025/02/21", "reviewed": False},
        #     {"word": "lover", "definition": "(n.) a partner in a sexual or romantic relationship outside marriage", "save_date": "2025/02/22", "reviewed": False},
        # ]

    if "reviewed_words" not in st.session_state:
        st.session_state.reviewed_words = []


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

def show_vocab_list():
    if st.session_state.vocabulary_list:
        vocab_df = pd.DataFrame(st.session_state.vocabulary_list)
        vocab_df["save_date"] = vocab_df["save_date"].str.split("T").str[0]  # Extract only date

        # Render table with review buttons
        for i, row in vocab_df.iterrows():
            col1, col2, col3, col4 = st.columns([1, 4, 1.5, 1])
            with col1:
                st.write(row["word"])
            with col2:
                st.write(row["definition"])
            with col3:
                st.write(row["save_date"])
            with col4:
                if st.button("Review", key=f"review_{row['word']}"):
                    st.session_state.vocabulary_list = [w for w in st.session_state.vocabulary_list if w["word"] != row["word"]]
                    st.session_state.reviewed_words.append(row.to_dict())
                    st.rerun()

    else:
        st.write("No words saved yet.")

    # for word in st.session_state.vocabulary_list:
    #     with col1:
    #         st.write(word["word"])
    #     with col2:
    #         st.write(word["definition"])
    #     with col3:
    #         st.write(word["save_date"].split("T")[0])
    #     with col4:
    #         if st.button("Review", key=f"review_{word['word']}"):
    #             word["reviewed"] = True
    #             st.session_state.vocabulary_list = [w for w in st.session_state.vocabulary_list if not w["reviewed"]]
    #             st.session_state.reviewed_words.append(word)
    #             st.rerun()

# Display reviewed words at the bottom
def show_reviewed_list():
    if st.session_state.reviewed_words:
        st.write("### Reviewed Words")
        for word in st.session_state.reviewed_words:
            col1, col2, col3, col4 = st.columns([1, 4, 1.5, 1])
            with col1:
                st.write(word["word"])
            with col2:
                st.write(word["definition"])
            with col3:
                st.write(word["save_date"].split("T")[0])
            with col4:
                if st.button("Review again", key=f"review_{word['word']}"):
                    word["reviewed"] = False
                    # st.session_state.vocabulary_list = [w for w in st.session_state.vocabulary_list if not w["reviewed"]]
                    st.session_state.reviewed_words.remove(word)
                    st.session_state.vocabulary_list.append(word)
                    st.rerun()

# Function to move reviewed words to the bottom of the list
def move_reviewed_words():
    for word in st.session_state.vocabulary_list:
        if word["reviewed"]:
            st.session_state.reviewed_words.append(word)
            st.session_state.vocabulary_list.remove(word)

# Button to save the review
# def save_review():
    # if st.button("Save Review"):
    #     move_reviewed_words()
    #     st.success("Review saved! Refreshing the list...")
    #     st.rerun()
    # pass



def main():
    initialize_vocab_list()
    show_vocab_list()
    show_reviewed_list()
    # save_review()


if __name__ == "__main__":
    main()