import streamlit as st

# Add custom CSS to hide the Streamlit footer and hamburger menu
hide_footer_style = """
    <style>
        .viewerBadge_container__1QSob {
            display: none;
        }
        .sidebarCollapserIcon_container__1p5gS {
            display: none;
        }
    </style>
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)



