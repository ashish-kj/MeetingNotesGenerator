import streamlit as st
import requests

st.title("🎙 Meeting Notes Generator")

audio_file = st.file_uploader("Upload your meeting audio (.mp3 or .wav)", type=["mp3", "wav"])

if audio_file:
    st.audio(audio_file)
    if st.button("Generate Notes"):
        # Send the file to the backend
        files = {"file": (audio_file.name, audio_file, audio_file.type)}
        res = requests.post("http://localhost:8000/process/", files=files)
        output = res.json()

        st.subheader("📝 Summary:")
        st.write(output["summary"])

        st.subheader("✅ Action Items:")
        st.write(output["action_items"])

        with st.expander("📄 Full Transcript"):
            st.text_area("Transcript", value=output["transcript"], height=300)