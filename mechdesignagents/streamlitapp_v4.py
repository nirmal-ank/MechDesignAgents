#This is the best version yet.
import streamlit as st
from streamlit_stl import stl_from_file
import os
from chat_with_designer_expert_multimodal import multimodal_designers_chat

def initialize_session_state():
    # Initialize all session state variables if they don't exist
    if 'prompt' not in st.session_state:
        st.session_state.prompt = ""
    if 'current_stl_path' not in st.session_state:
        st.session_state.current_stl_path = '/home/niel77/MechDesignAgents/mechdesignagents/NewCADs/airplane_wing_naca2412.stl'
    if 'color' not in st.session_state:
        st.session_state.color = "#FF9900"
    if 'material' not in st.session_state:
        st.session_state.material = "material"
    if 'auto_rotate' not in st.session_state:
        st.session_state.auto_rotate = False
    if 'opacity' not in st.session_state:
        st.session_state.opacity = 1.0
    if 'height' not in st.session_state:
        st.session_state.height = 500
    if 'cam_v_angle' not in st.session_state:
        st.session_state.cam_v_angle = 60
    if 'cam_h_angle' not in st.session_state:
        st.session_state.cam_h_angle = -90
    if 'cam_distance' not in st.session_state:
        st.session_state.cam_distance = 0
    if 'max_view_distance' not in st.session_state:
        st.session_state.max_view_distance = 1000

def update_stl_path(new_path):
    st.session_state.current_stl_path = new_path

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    initialize_session_state()

    st.title("AnK CAD")

    col1, col2 = st.columns([2, 1])

    with col1:
        prompt = st.text_input("Let's design", 
                             value=st.session_state.prompt,
                             placeholder="Enter a text prompt here",
                             key="input_prompt")
        
    if st.button("Generate CAD Model"):
        if prompt:
            with st.spinner("Generating CAD model..."):
                stl_file = multimodal_designers_chat(prompt)
                update_stl_path(stl_file)
                st.rerun()  # Rerun to update the UI with new STL

    st.subheader("CAD viewer")
    
    # UI Controls with persistent state
    cols = st.columns(5)
    with cols[0]:
        color = st.color_picker("Pick a color", 
                              value=st.session_state.color, 
                              key='color_picker')
        st.session_state.color = color
        
    with cols[1]:
        material = st.selectbox("Select a material", 
                              ["material", "flat", "wireframe"], 
                              index=["material", "flat", "wireframe"].index(st.session_state.material),
                              key='material_selector')
        st.session_state.material = material
        
    with cols[2]:
        st.write('\n'); st.write('\n')
        auto_rotate = st.toggle("Auto rotation", 
                              value=st.session_state.auto_rotate,
                              key='rotation_toggle')
        st.session_state.auto_rotate = auto_rotate
        
    with cols[3]:
        opacity = st.slider("Opacity", 
                          min_value=0.0, 
                          max_value=1.0, 
                          value=st.session_state.opacity,
                          key='opacity_slider')
        st.session_state.opacity = opacity
        
    with cols[4]:
        height = st.slider("Height", 
                         min_value=50, 
                         max_value=1000, 
                         value=st.session_state.height,
                         key='height_slider')
        st.session_state.height = height

    # Camera controls with persistent state
    cols = st.columns(4)
    with cols[0]:
        cam_v_angle = st.number_input("Camera Vertical Angle", 
                                    value=st.session_state.cam_v_angle,
                                    key='cam_v_angle_input')
        st.session_state.cam_v_angle = cam_v_angle
        
    with cols[1]:
        cam_h_angle = st.number_input("Camera Horizontal Angle", 
                                    value=st.session_state.cam_h_angle,
                                    key='cam_h_angle_input')
        st.session_state.cam_h_angle = cam_h_angle
        
    with cols[2]:
        cam_distance = st.number_input("Camera Distance", 
                                     value=st.session_state.cam_distance,
                                     key='cam_distance_input')
        st.session_state.cam_distance = cam_distance
        
    with cols[3]:
        max_view_distance = st.number_input("Max view distance", 
                                          min_value=1, 
                                          value=st.session_state.max_view_distance,
                                          key='max_view_distance_input')
        st.session_state.max_view_distance = max_view_distance

    examples = [
        "A box with a through hole in the center.",
        "Create a pipe of outer diameter 50mm and inside diameter 40mm.",
        "Create a circular plate of radius 2mm and thickness 0.125mm with four holes of radius 0.25mm patterned at distance of 1.5mm from the centre along the axes."
    ]

    with col2:
        # Example prompts section
        st.subheader("Example Prompts")
        for example in examples:
            if st.button(example, key=f"example_{example}"):
                st.session_state.prompt = example
                st.rerun()

    # STL Viewer with persistent state values
    stl_from_file(
        file_path=st.session_state.current_stl_path,
        color=st.session_state.color,
        material=st.session_state.material,
        auto_rotate=st.session_state.auto_rotate,
        opacity=st.session_state.opacity,
        height=st.session_state.height,
        shininess=100,
        cam_v_angle=st.session_state.cam_v_angle,
        cam_h_angle=st.session_state.cam_h_angle,
        cam_distance=st.session_state.cam_distance,
        max_view_distance=st.session_state.max_view_distance,
        key='stl_viewer'
    )