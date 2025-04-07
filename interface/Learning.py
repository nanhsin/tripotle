import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import pandas as pd
import requests
import time

df = pd.read_csv("../data/billboard_lyrics_1960-2024_difficulty.csv")

# # Initialize session state for tracking the current page
# if "current_page" not in st.session_state:
#     st.session_state.current_page = "Learning"

# # Check if the page has changed
# if st.session_state.current_page != "Learning":
#     st.session_state.current_page = "Learning"  # Update the session state
#     st.rerun()  # Trigger a rerun

# Set page title and layout
st.set_page_config(page_title="LyricsMaster", layout="wide")
st.title("🎵 LyricsMaster")

# Create three columns for the layout
# col1, col2, col3 = st.columns([1, 2, 1])
col1, col2 = st.columns([2, 1])


def filter_level(level):
    """
    Get songs from df according to user's difficulty level
    ------
    input: difficulty level selected by users (str)
    ------
    reture: filtered df
    """
    return df[df["lyrics_difficulty_class"] == level.lower()]

def col1_display():
    """
    Renders column 1 in the Streamlit application for selecting difficulty level preferences
    , handling song recommendations, and show lyrics.
    """
    with col1:
        # st.subheader("Set Your Goal!")
        # difficulty = st.radio("Choose a difficulty level:", ["Easy", "Medium", "Hard"])
        # filtered_songs = filter_level(difficulty)
        # subcol1, subcol2 = st.columns([2, 1])

        if not st.session_state["song_bool"]:
            st.subheader("Set Your Goal!")
            difficulty = st.radio("Choose a difficulty level:", ["Easy", "Medium", "Hard"])
            filtered_songs = filter_level(difficulty)

            if st.button("Start Learning!"):
                st.session_state.song_index = filtered_songs.sample(n=1).index.item()
                # st.session_state.song_index = random.randint(0, len(songs) - 1)

                st.session_state["title"] = filtered_songs.loc[st.session_state.song_index]["title"]
                st.session_state["artist"] = filtered_songs.loc[st.session_state.song_index]["artist"]
                st.session_state["lyrics"] = filtered_songs.loc[st.session_state.song_index]["lyrics_ori"]

                st.session_state["song_bool"] = True

                st.rerun()

        else:
            subcol1, subcol2 = st.columns([4, 1])
            if st.session_state["song_bool"]:

                with subcol1:
                    # st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("Let's learn from...")
                    st.markdown(f"## **{st.session_state['title']}** by {st.session_state['artist']}")
                    # st.write(f"##### by {st.session_state['artist']}")

                    # st.markdown("<br>", unsafe_allow_html=True)
                with subcol2:
                    # st.write("For another recommendation:")
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Reload"):
                        streamlit_js_eval(js_expressions="parent.window.location.reload()")

        # Show lyrics
        if st.session_state["lyrics"]:
            # st.write("Lyrics:")
            # st.write(st.session_state["lyrics"], height=200)
            st.text_area("Lyrics:", st.session_state["lyrics"], height=400)
        # else:
        #     st.write(f'Let\'s learn some vocabulary from the lyrics!')

# def left_column():
#     """
#     Renders the left column in the Streamlit application for selecting difficulty level preferences
#     and handling song recommendations.
#     """
#     with col1:
#         st.subheader("Set Your Goal!")
#         difficulty = st.radio("Choose a difficulty level:", ["Easy", "Medium", "Hard"])
#         filtered_songs = filter_level(difficulty)

#         if not st.session_state["song_bool"]:

#             if st.button("Start Learning!"):
#                 st.session_state.song_index = filtered_songs.sample(n=1).index.item()
#                 # st.session_state.song_index = random.randint(0, len(songs) - 1)

#                 st.session_state["title"] = filtered_songs.loc[st.session_state.song_index]["title"]
#                 st.session_state["artist"] = filtered_songs.loc[st.session_state.song_index]["artist"]
#                 st.session_state["lyrics"] = filtered_songs.loc[st.session_state.song_index]["lyrics_ori"]

#                 st.session_state["song_bool"] = True

#                 st.rerun()

#         else:
#             if st.session_state["song_bool"]:

#                 st.markdown("<br>", unsafe_allow_html=True)
#                 st.write("#### We'd recommend you...")
#                 st.write(f"### {st.session_state['title']}")
#                 st.write(f"##### by {st.session_state['artist']}")

#                 st.markdown("<br>", unsafe_allow_html=True)
#                 st.write("Please reload the page for another recommendation.")
#                 if st.button("Reload"):
#                     streamlit_js_eval(js_expressions="parent.window.location.reload()")

# def page_middle_column_title():
#     """
#     Sets the title of the Streamlit page based on the selected song and artist.
#     """
#     with col2:
#         if st.session_state["title"] and st.session_state["artist"]:
#             st.subheader(
#                 f'Let\'s learn from  {st.session_state["title"]} by {st.session_state["artist"]}'
#             )
#         else:
#             st.title("🎵 English Music Recommender")


# def middle_column():
#     """
#     Manages the middle main column in the Streamlit application, handling the lyrics display.
#     """
#     with col2:
#         if st.session_state["lyrics"]:
#             # st.write("Lyrics:")
#             # st.write(st.session_state["lyrics"], height=200)
#             st.text_area("Lyrics:", st.session_state["lyrics"], height=500)
#         else:
#             st.write(f'Let\'s learn some vocabulary from the lyrics!')


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


def save_vocab(word, definition):
    url = "http://localhost:8000/savevocab/"
    if "auth_token" not in st.session_state:
        token = streamlit_js_eval(js_expressions="localStorage.getItem('auth_token')")
        if token:
            st.session_state['auth_token'] = token
            st.session_state['logged_in'] = True
    headers = {"Authorization": f"Token {st.session_state.get('auth_token', '')}"}
    response = requests.post(url, json={"word": word, "definition": definition}, headers=headers)
    if response.status_code == 201:
        return True
    else:
        return False

def col2_display():
    """
    Manages column 2 in the Streamlit application, handling the vocabulary search box and display.
    """
    with col2:
        st.subheader("Search Vocabulary")
        search_word = st.text_input("Enter a word to search:", value=st.session_state.vocab_search, key="vocab_search").strip().lower()

        # Reset vocab_definition
        if not search_word:
            st.session_state.vocab_definition = ""

        if st.button("Search"):
            if search_word:

                word_dict = get_dictionary(search_word)
                if word_dict["definition"] != "":
                    st.session_state.vocab_definition = f"({word_dict['partOfSpeech']})\n\n{word_dict['phonetics']}\n\n{word_dict['definition']}"
                else:
                    st.session_state.vocab_definition = f"**'{search_word}'** not found in the vocabulary database."

            else:
                st.warning("Please enter a word to search.")

        # Display the vocabulary definition (if available)
        if st.session_state.get("vocab_definition"):
            st.markdown("#### Definition:")
            # st.subheader(st.session_state.vocab_search)
            st.subheader(search_word)
            st.markdown(st.session_state.vocab_definition)

            if st.button("Save"):
                save_definition = st.session_state.vocab_definition.replace("\n\n", " ")
                # save_vocab(st.session_state.vocab_search, save_definition)
                save_vocab(search_word, save_definition)

# def right_column():
#     """
#     Manages the right column in the Streamlit application, handling the vocabulary search box and display.
#     """
#     with col3:
#         st.subheader("Search Vocabulary")
#         search_word = st.text_input("Enter a word to search:", value=st.session_state.vocab_search, key="vocab_search")

#         # Reset vocab_definition
#         if not search_word:
#             st.session_state.vocab_definition = ""

#         if st.button("Search"):
#             if search_word.strip():

#                 word_dict = get_dictionary(search_word.lower())
#                 if word_dict["definition"] != "":
#                     st.session_state.vocab_definition = f"({word_dict['partOfSpeech']})\n\n{word_dict['phonetics']}\n\n{word_dict['definition']}"
#                 else:
#                     st.session_state.vocab_definition = f"**'{search_word}'** not found in the vocabulary database."

#             else:
#                 st.warning("Please enter a word to search.")

#         # Display the vocabulary definition (if available)
#         if st.session_state.get("vocab_definition"):
#             st.markdown("#### Definition:")
#             st.subheader(st.session_state.vocab_search)
#             st.markdown(st.session_state.vocab_definition)

#             if st.button("Save"):
#                 save_definition = st.session_state.vocab_definition.replace("\n\n", " ")
#                 save_vocab(st.session_state.vocab_search, save_definition)


def register():
    BASE_URL = "http://127.0.0.1:8000"
    st.subheader("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    password2 = st.text_input("Confirm Password", type="password")
    
    if st.button("Register"):
        data = {"username": username, "password1": password, "password2": password2}
        response = requests.post(f"{BASE_URL}/register/", json=data)
        if response.status_code == 201:
            st.success("Registered successfully! Please log in.")
        else:
            st.error(f"Error: {response.json()}")

def login():
    BASE_URL = "http://127.0.0.1:8000"
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password", help="Enter your password")
    if st.button("Login"):
        data = {"username": username, "password": password}
        response = requests.post(f"{BASE_URL}/login/", json=data)
        if response.status_code == 200:
            token = response.json().get('token')
            streamlit_js_eval(js_expressions="localStorage.setItem('auth_token', '" + token + "')")
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['auth_token'] = token
            st.success(f"Welcome, {username}!")
            url = "http://localhost:8000/savevocab/"
            headers = {"Authorization": f"Token {st.session_state.get('auth_token', '')}"}
            response_vocab = requests.get(url, headers=headers)
            if response_vocab.status_code == 200:
                st.session_state.vocabulary_list = response_vocab.json()
            time.sleep(1)
            st.rerun()
        else:
            st.error("Invalid credentials")

def logout():
    BASE_URL = "http://127.0.0.1:8000"
    st.subheader("Logout")
    if st.button("Logout"):
        response = requests.post(f"{BASE_URL}/logout/")
        if response.status_code == 200:
            streamlit_js_eval(js_expressions="localStorage.removeItem('auth_token')")
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.session_state['auth_token'] = ""

            # st.session_state drop vocabulary_list and reviewed_words
            st.session_state.pop("vocabulary_list", None)
            st.session_state.pop("reviewed_words", None)

            st.success("Logged out successfully")
            time.sleep(1)
            st.rerun()


def init():
    """
    Initializes the session state variables used in the Streamlit application and
    loads environment variables.
    """

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
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""


def main():
    init()
    if not st.session_state["logged_in"]:
        option = st.radio("Choose an option", ("Login", "Register"))
        if option == "Login":
            login()
        elif option == "Register":
            register()
    else:
    # page_middle_column_title()
    # left_column()
        col1_display()
        col2_display()
        logout()
    # middle_column()
    # right_column()


if __name__ == "__main__":
    main()