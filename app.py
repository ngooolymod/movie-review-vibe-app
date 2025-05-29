import streamlit as st
import requests
import openai

# pull your keys from Replit secrets (or os.environ)
TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

def search_movie(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    data = requests.get(url).json()
    results = data.get("results")
    return results[0] if results else None

def generate_summary(statements):
    prompt = f"Summarize the following review statements succinctly:\n\n{statements}"
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        max_tokens=150,
        temperature=0.7
    )
    return resp.choices[0].message.content.strip()

st.title("Vibe-Coded Movie Review App")

movie_title = st.text_input("Enter Movie Title:")
if movie_title:
    movie = search_movie(movie_title)
    if movie:
        st.image(f"https://image.tmdb.org/t/p/w300{movie['poster_path']}", caption=movie['title'])
        st.markdown(f"**Release Date:** {movie['release_date']}")
        st.markdown(f"**Overview:** {movie['overview']}")

        st.header("Scoring")
        col1, col2 = st.columns(2)
        with col1:
            cinematography = st.slider("Cinematography Score", 0, 10, 5)
        with col2:
            pacing = st.slider("Pacing Score", 0, 10, 5)

        st.header("Your Insights")
        statements = st.text_area("Share your thoughts on Cinematography and Pacing")

        st.header("Finalizing")
        weights = st.slider("Cinematography Weight (%)", 0, 100, 50)
        final_score = round(
            (cinematography * (weights/100)) +
            (pacing * ((100-weights)/100)), 2
        )
        st.markdown(f"**Final Score:** {final_score} / 10")

        if st.button("Generate Summary"):
            summary = generate_summary(statements)
            st.markdown("**AI-Generated Summary:**")
            st.write(summary)
    else:
        st.error("Movie not found. Try a different title.")
