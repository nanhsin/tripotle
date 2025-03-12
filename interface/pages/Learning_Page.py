import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from dotenv import load_dotenv
import pandas as pd
import requests

df = pd.read_csv("../data/billboard_lyrics_1960-2024_difficulty.csv")

# Set page title and layout
st.set_page_config(page_title="English Music Recommender", layout="wide")

# Create three columns for the layout
col1, col2, col3 = st.columns([1, 2, 1])


def filter_level(level):
    """
    Get songs from df according to user's difficulty level
    ------
    input: difficulty level selected by users (str)
    ------
    reture: filtered df
    """
    return df[df["lyrics_difficulty_class"] == level.lower()]



def left_column():
    """
    Renders the left column in the Streamlit application for selecting difficulty level preferences
    and handling song recommendations.
    """
    with col1:
        st.subheader("Set Your Goal!")
        difficulty = st.radio("Choose a difficulty level:", ["Easy", "Medium", "Hard"])
        filtered_songs = filter_level(difficulty)

        if not st.session_state["song_bool"]:

            if st.button("Start Learning!"):
                st.session_state.song_index = filtered_songs.sample(n=1).index.item()
                # st.session_state.song_index = random.randint(0, len(songs) - 1)

                st.session_state["title"] = filtered_songs.loc[st.session_state.song_index]["title"]
                st.session_state["artist"] = filtered_songs.loc[st.session_state.song_index]["artist"]
                st.session_state["lyrics"] = filtered_songs.loc[st.session_state.song_index]["lyrics"]

                st.session_state["song_bool"] = True

                st.rerun()

        else:
            if st.session_state["song_bool"]:

                st.markdown("<br>", unsafe_allow_html=True)
                st.write("#### We'd recommend you...")
                st.write(f"### {st.session_state['title']}")
                st.write(f"##### by {st.session_state['artist']}")

                st.markdown("<br>", unsafe_allow_html=True)
                st.write("Please reload the page for another recommendation.")
                if st.button("Reload"):
                    streamlit_js_eval(js_expressions="parent.window.location.reload()")

def page_middle_column_title():
    """
    Sets the title of the Streamlit page based on the selected song and artist.
    """
    with col2:
        if st.session_state["title"] and st.session_state["artist"]:
            st.subheader(
                f'Let\'s learn from  {st.session_state["title"]} by {st.session_state["artist"]}'
            )
        else:
            st.title("🎵 English Music Recommender")


def middle_column():
    """
    Manages the middle main column in the Streamlit application, handling the lyrics display.
    """
    with col2:
        if st.session_state["lyrics"]:
            # st.write("Lyrics:")
            # st.write(st.session_state["lyrics"], height=200)
            st.text_area("Lyrics:", st.session_state["lyrics"], height=300)
        else:
            st.write(f'Let\'s learn some vocabulary from the lyrics!')


# vocabulary_example_db = {
#                 "romance": {
#                     "definition": """
#                     noun
#                     uk /rəʊˈmaɪns/ /rəʊˌmaɪns/
#                     us /rɒʊˈmaɪns/ /rɒʊˌmaɪns/

#                     a close, usually short relationship of love between two people:
#                     - They got married last year after a whirlwind (= very short and unexpected) romance.
#                     - It was just a holiday romance.
#                     - Office romances are usually a bad idea.
#                     """
#                 },
#                 "damn": {
#                     "definition": """
#                     exclamation
#                     uk /dæm/ us /dæm/

#                     used to express anger or frustration:
#                     - Damn! I forgot my keys.
#                     - I don't give a damn what they think.
#                     """
#                 },
#                 "lover": {
#                     "definition": """
#                     noun
#                     uk /ˈlʌv.ər/ us /ˈlʌv.ɚ/

#                     a partner in a sexual or romantic relationship outside marriage:
#                     - She's been his lover for years.
#                     - He's a lover of fine wine.
#                     """
#                 }
#             }


def get_dictionary(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    word = {}
    try:
        word['partOfSpeech'] = response.json()[0]["meanings"][0]["partOfSpeech"]
    except:
        word['partOfSpeech'] = ""
    try:
        word['phonetics'] = response.json()[0]["phonetics"][0]["text"]
    except:
        word['phonetics'] = ""
    try:
        word['definition'] = response.json()[0]["meanings"][0]["definitions"][0]["definition"]
    except:
        word['definition'] = ""
    return word


def right_column():
    """
    Manages the right column in the Streamlit application, handling the vocabulary search box and display.
    """
    with col3:
        st.subheader("Search Vocabulary")
        search_word = st.text_input("Enter a word to search:", value=st.session_state.vocab_search, key="vocab_search")

        if st.button("Search"):
            if search_word.strip():

                # Look up the word in the vocabulary database
                # word_lower = search_word.lower()
                # if word_lower in vocabulary_example_db:
                #     st.session_state.vocab_definition = vocabulary_example_db[word_lower]["definition"]
                # else:
                #     st.session_state.vocab_definition = f"**'{search_word}'** not found in the vocabulary database."
                word_dict = get_dictionary(search_word.lower())
                if word_dict["definition"] != "":
                    st.session_state.vocab_definition = f"({word_dict['partOfSpeech']})\n\n{word_dict['phonetics']}\n\n{word_dict['definition']}"
                else:
                    st.session_state.vocab_definition = f"**'{search_word}'** not found in the vocabulary database."

                # # Clear the input box after searching
                # st.session_state.vocab_search = ""
            else:
                st.warning("Please enter a word to search.")

        # Display the vocabulary definition (if available)
        if "vocab_definition" in st.session_state:
            st.markdown("#### Definition:")
            st.subheader(st.session_state.vocab_search)
            st.markdown(st.session_state.vocab_definition)
            # Clear the input box after searching
            # st.session_state.vocab_search = ""


def init():
    """
    Initializes the session state variables used in the Streamlit application and
    loads environment variables.
    """
    load_dotenv()

    if "title" not in st.session_state:
        st.session_state["title"] = ""
    if "artist" not in st.session_state:
        st.session_state["artist"] = ""
    if "song_index" not in st.session_state:
        st.session_state["song_index"] = ""
    if "song_bool" not in st.session_state:
        st.session_state["song_bool"] = False
    if "lyrics" not in st.session_state:
        st.session_state["lyrics"] = ""
    if "vocab_search" not in st.session_state:
        st.session_state["vocab_search"] = ""


def main():
    init()
    page_middle_column_title()
    left_column()
    middle_column()
    right_column()


if __name__ == "__main__":
    main()