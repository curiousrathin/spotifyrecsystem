import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from spotify_recommend import SpotifyRecommender

def set_page_config():
    st.set_page_config(
        page_title="Spotify Song Recommender",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def add_custom_css():
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            background-color: #1DB954;
            color: white;
            border: none;
            padding: 0.75rem;
            border-radius: 20px;
            font-weight: 600;
        }
        .stButton>button:hover {
            background-color: #1ed760;
        }
        .song-card {
            background-color: #282828;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            color: white;
        }
        .metric-container {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        .title-container {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(90deg, #1DB954, #191414);
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
        }
        .recommendation-header {
            background-color: #282828;
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

def create_radar_chart(song_features):
    feature_cols = [
        'danceability_%', 'valence_%', 'energy_%',
        'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%'
    ]
    
    values = song_features[feature_cols].values.tolist()
    values.append(values[0])  # Close the polygon
    
    labels = [col.replace('_%', '').title() for col in feature_cols]
    labels.append(labels[0])  # Close the polygon
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        line=dict(color='#1DB954'),
        fillcolor='rgba(29, 185, 84, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=80, r=80, t=40, b=40)
    )
    
    return fig

def display_song_card(track_name, artist_name, similarity_score=None):
    similarity_text = f"Similarity: {similarity_score:.2%}" if similarity_score is not None else ""
    st.markdown(
        f"""
        <div class="song-card">
            <h3>🎵 {track_name}</h3>
            <p>👤 {artist_name}</p>
            <p>{similarity_text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    set_page_config()
    add_custom_css()
    
    # Header
    st.markdown(
        """
        <div class="title-container">
            <h1>🎵 Spotify Song Recommender</h1>
            <p>Discover new music based on song characteristics</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    try:
        recommender = SpotifyRecommender()
        available_songs = recommender.get_available_songs()
        
        # Create song selection interface
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### 🎼 Select a Song")
            song_list = [f"{song[0]} - {song[1]}" for song in available_songs]
            selected_song = st.selectbox(
                "Search for a song:",
                options=song_list,
                help="Type to search for a song"
            )
            
            if selected_song:
                song_name, artist_name = selected_song.split(" - ", 1)
                
                # Get song features for visualization
                mask = (
                    (recommender.df_frontend['track_name'].str.lower() == song_name.lower()) &
                    (recommender.df_frontend['artist(s)_name'].str.lower() == artist_name.lower())
                )
                song_features = recommender.df_frontend[mask].iloc[0]
                
                # Display song features
                st.markdown("### 📊 Song Characteristics")
                fig = create_radar_chart(song_features)
                st.plotly_chart(fig, use_container_width=True)
                
                # BPM display
                st.markdown(
                    f"""
                    <div class="metric-container">
                        <h4>Tempo (BPM)</h4>
                        <h2>{float(song_features['bpm']):.0f}</h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                if st.button("Get Recommendations 🎵", use_container_width=True):
                    with st.spinner("Finding similar songs..."):
                        recommendations = recommender.get_recommendations(song_name, artist_name)
                        st.session_state.recommendations = recommendations
                        st.session_state.selected_features = song_features
        
        with col2:
            if 'recommendations' in st.session_state:
                st.markdown(
                    """
                    <div class="recommendation-header">
                        <h2>🎯 Recommended Songs</h2>
                        <p>Based on musical characteristics and similarity</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                recommendations = st.session_state.recommendations
                
                if isinstance(recommendations, str):
                    st.error(recommendations)
                else:
                    for _, row in recommendations.iterrows():
                        display_song_card(row['track_name'], row['artist(s)_name'])
                        
    except Exception as e:
        st.error("😕 Oops! Something went wrong...")
        with st.expander("Show error details"):
            st.write(f"Error: {str(e)}")
            st.write("Please check your data files and column names.")

if __name__ == "__main__":
    main()