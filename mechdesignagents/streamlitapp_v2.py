import streamlit as st
import os
from chat_with_designer_expert_multimodal import multimodal_designers_chat
from streamlit_stl import stl_from_file

def main():
    # Set page config
    st.set_page_config(
        page_title="AnK CAD with Multiagent team",
        layout="wide"
    )

    # Initialize session state for prompt if it doesn't exist
    if 'prompt' not in st.session_state:
        st.session_state.prompt = ""

    # Title and description
    st.title("AnK CAD with Multiagent team")
    st.markdown("""
    Generate 3D CAD models by entering the prompt.
    """)

    # Example prompts
    examples = [
        "A box with a through hole in the center.",
        "Create a pipe of outer diameter 50mm and inside diameter 40mm.",
        "Create a circular plate of radius 2mm and thickness 0.125mm with four holes of radius 0.25mm patterned at distance of 1.5mm from the centre along the axes."
    ]

    # Create columns for layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Text input for prompt
        prompt = st.text_input("Let's design", 
                             value=st.session_state.prompt,
                             placeholder="Enter a text prompt here",
                             key="input_prompt")
        
        # Generate button
        if st.button("Generate CAD Model"):
            if prompt:
                with st.spinner("Generating CAD model..."):
                    try:
                        stl_file = multimodal_designers_chat(prompt)
                        # Display the STL file
                        if stl_file and os.path.exists(stl_file):
                            st.subheader("Here is the model!")
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

                            stl_from_file(  file_path=stl_file, 
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
                        else:
                            st.error("Failed to generate CAD model")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter a prompt")

    with col2:
        # Example prompts section
        st.subheader("Example Prompts")
        for example in examples:
            if st.button(example, key=f"example_{example}"):
                st.session_state.prompt = example
                st.rerun()

if __name__ == "__main__":
    main()