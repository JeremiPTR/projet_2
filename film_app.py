import pandas as pd
import streamlit as st

backgroundColor = "#e5dccf"  # CONFIGURATION ?

col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.write("")

with col2:
    st.image("https://i.imgur.com/GVNLv4m.png")

with col3:
    st.write("")

st.write("Bonne recherche !")

##################################################
# Pourquoi bouton supplémentaire ? - AJOUT PROPOSITION ou NOUVELLE PAGE

if "df" in st.session_state:
    df = st.session_state["df"]
else:
    df = pd.read_csv("dataframe_films.csv")
    st.session_state["df"] = df

if "selected_film_id" in st.session_state:
    film_id = st.session_state["selected_film_id"]
    film = df[df["movie_ID"] == film_id].iloc[0]

    st.markdown(f"## 🎬 {film['frenchTitle']}")
    st.markdown(f"- **Année** : {film['startYear']}")
    st.markdown(f"- **Genres** : {film['genres']}")

    if pd.notna(film["backdrop_path"]):
        image_url = f"https://image.tmdb.org/t/p/w500{film['backdrop_path']}"
        st.image(image_url, use_container_width=True)

    if st.button("🔙 Retour aux résultats"):
        del st.session_state["selected_film_id"]
        st.write("Retour aux résultats...")
        st.stop()

# --- BARRE DE RECHERCHE ---
else:
    st.markdown("")
    recherche_film = st.text_input(
        "Entrez le nom de votre film préféré :", key="film_name"
    )

    if recherche_film:
        resultats = df[
            df["frenchTitle"].str.contains(recherche_film, case=False, na=False)
        ]

        if not resultats.empty:
            st.success(f"{len(resultats)} film(s) trouvé(s) :")
            resultats_dedoublonnes = resultats.drop_duplicates(subset=["movie_ID"])

            for index, row in resultats_dedoublonnes.iterrows():
                with st.container():
                    bouton = st.button(
                        f" {row['frenchTitle']} ({row['startYear']}) - {row['genres']}",
                        key=f"film_{row['movie_ID']}",
                    )
                    if bouton:
                        st.session_state["selected_film_id"] = row["movie_ID"]
                        st.stop()

                    # Présentation visuelle du film
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if pd.notna(row["backdrop_path"]):
                            image_url = (
                                f"https://image.tmdb.org/t/p/w500{row['backdrop_path']}"
                            )
                            st.image(image_url, width=120)
                    with col2:
                        st.markdown(
                            f"""
                            ### {row['frenchTitle']}  
                            - **Année** : {row['startYear']}  
                            - **Genre** : {row['genres']}  
                            """
                        )
                    st.markdown("---")
        else:
            st.error("Aucun film trouvé.")
