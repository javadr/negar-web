#!/usr/bin/env python3

import re
import streamlit as st
from redlines import Redlines


# https://stackoverflow.com/questions/16981921
# sys.path.append(Path(__file__).parent.parent.as_posix())
from negar.virastar import PersianEditor  # noqa: E402
from negar.constants import INFO, __version__  # noqa: E402


st.set_page_config(
    page_title="Negar Web",
    page_icon=":sparkles:",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/javadr/negar-gui",
        "Report a bug": "https://github.com/shahinism/python-negar/issues",
        "About": f"# Negar. Version  *{__version__}*!",
    },
)

# Streamlit App Layout
with st.sidebar:
    st.markdown(f"# Negar *{__version__}*")
    comparative_mode = st.checkbox(
        "Comparative Mode",
        key="comparative_mode",
        help="Toggle comparative mode.",
        # on_change=lambda: pass,
    )
# Title and Description
st.title("Negar")
st.markdown("""
Persian Text Editor.
""")
st.markdown(
    "",
    unsafe_allow_html=True,
)  # Render the HTML

# Injecting custom CSS
# Inject CSS to target the text area
st.markdown(
    """
<style>
/* Import Vazirmatn font from Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');

/* Target the textarea inside stTextArea */
div[data-baseweb="textarea"] textarea {
    direction: RTL;
    text-align: right;
    font-family: 'Vazirmatn', sans-serif;
    
}

/* Make the markdown output RTL */
.rtl-text {
    direction: RTL;
    text-align: justify;
    font-family: 'Vazirmatn', sans-serif;
    
}
</style>
""",
    unsafe_allow_html=True,
)

user_input = st.text_area(
    "Input Text:",
    key="rtl_text",
    placeholder="Start typing here...",
    height=300,
)

# Button to Predict
if st.button("Edit"):
    if user_input.strip():
        with st.spinner("Analyzing..."):
            st.subheader("Results:")

            edited_text = []
            for line in user_input.strip().split("\n"):
                line = line.strip()
                run_PE = PersianEditor(line)
                if comparative_mode:
                    edited_text.append(
                        Redlines(
                            re.sub(r"\s*?\n", " <br> ", line),
                            run_PE.cleanup().strip(),
                        ).output_markdown
                        if line
                        else ""
                    )
                else:
                    edited_text.append(run_PE.cleanup())
                # Display Results
            st.markdown(
                f'<p class="rtl-text">{"<br/>".join(edited_text)}</p>',
                unsafe_allow_html=True,
            )  # Render the HTML

    else:
        st.warning("Please enter text before clicking analyze.")
