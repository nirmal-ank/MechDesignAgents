import streamlit as st
from streamlit_stl import stl_from_file
import os
from chat_with_designer_expert_multimodal import multimodal_designers_chat


if __name__ == "__main__":
    if 'prompt' not in st.session_state:
        st.session_state.prompt = ""
    st.set_page_config(layout="wide")

    st.title("AnK CAD")
    default_file_path='/home/niel77/MechDesignAgents/mechdesignagents/NewCADs/airplane_wing_naca2412.stl'


    col1, col2 = st.columns([2, 1])

    with col1:
        # Text input for prompt
        prompt = st.text_input("Let's design", 
                             value=st.session_state.prompt,
                             placeholder="Enter a text prompt here",
                             key="input_prompt")
    if st.button("Generate CAD Model"):
            if prompt:
                with st.spinner("Generating CAD model..."):
                        stl_file = multimodal_designers_chat(prompt)
                        default_file_path=stl_file  

    st.subheader("CAD viewer")
    cols = st.columns(5)
    with cols[0]:
        color = st.color_picker("Pick a color", "#FF9900", key='color_file')
    with cols[1]:
        material = st.selectbox("Select a material", ["material", "flat", "wireframe"], key='material_file')
    with cols[2]:
        st.write('\n'); st.write('\n')
        auto_rotate = st.toggle("Auto rotation", key='auto_rotate_file')
    with cols[3]:
        opacity = st.slider("Opacity", min_value=0.0, max_value=1.0, value=1.0, key='opacity_file')
    with cols[4]:
        height = st.slider("Height", min_value=50, max_value=1000, value=500, key='height_file')

    # camera position
    cols = st.columns(4)
    with cols[0]:
        cam_v_angle = st.number_input("Camera Vertical Angle", value=60, key='cam_v_angle')
    with cols[1]:
        cam_h_angle = st.number_input("Camera Horizontal Angle", value=-90, key='cam_h_angle')
    with cols[2]:
        cam_distance = st.number_input("Camera Distance", value=0, key='cam_distance')
    with cols[3]:
        max_view_distance = st.number_input("Max view distance", min_value=1, value=1000, key='max_view_distance')

    stl_from_file(  file_path=default_file_path, 
                    color=color,
                    material=material,
                    auto_rotate=auto_rotate,
                    opacity=opacity,
                    height=height,
                    shininess=100,
                    cam_v_angle=cam_v_angle,
                    cam_h_angle=cam_h_angle,
                    cam_distance=cam_distance,
                    max_view_distance=max_view_distance,
                    key='example1')
    