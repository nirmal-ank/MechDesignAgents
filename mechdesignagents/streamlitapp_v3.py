import streamlit as st
import os
from chat_with_designer_expert_multimodal import multimodal_designers_chat
from streamlit_stl import stl_from_file

def initialize_session_state():
    """Initialize all session state variables"""
    if 'prompt' not in st.session_state:
        st.session_state.prompt = ""
    if 'current_stl' not in st.session_state:
        st.session_state.current_stl = None
    if 'viz_settings' not in st.session_state:
        st.session_state.viz_settings = {
            'color': "#FF9900",
            'material': "material",
            'auto_rotate': False,
            'opacity': 1.0,
            'height': 500,
            'cam_v_angle': 60,
            'cam_h_angle': -90,
            'cam_distance': 0,
            'max_view_distance': 1000
        }

def handle_cad_generation(prompt):
    """Handle the CAD generation process"""
    with st.spinner("Generating CAD model..."):
        try:
            stl_file = multimodal_designers_chat(prompt)
            if stl_file and os.path.exists(stl_file):
                st.session_state.current_stl = stl_file
                return True
            else:
                st.error("Failed to generate CAD model")
                return False
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return False

def render_visualization_controls():
    """Render the visualization control panel"""
    cols = st.columns(5)
    with cols[0]:
        st.session_state.viz_settings['color'] = st.color_picker(
            "Pick a color", 
            st.session_state.viz_settings['color']
        )
    with cols[1]:
        st.session_state.viz_settings['material'] = st.selectbox(
            "Select a material", 
            ["material", "flat", "wireframe"]
        )
    with cols[2]:
        st.write('\n'); st.write('\n')
        st.session_state.viz_settings['auto_rotate'] = st.toggle(
            "Auto rotation"
        )
    with cols[3]:
        st.session_state.viz_settings['opacity'] = st.slider(
            "Opacity", 
            min_value=0.0, 
            max_value=1.0, 
            value=st.session_state.viz_settings['opacity']
        )
    with cols[4]:
        st.session_state.viz_settings['height'] = st.slider(
            "Height", 
            min_value=50, 
            max_value=1000, 
            value=st.session_state.viz_settings['height']
        )

    # camera position
    cols = st.columns(4)
    with cols[0]:
        st.session_state.viz_settings['cam_v_angle'] = st.number_input(
            "Camera Vertical Angle", 
            value=st.session_state.viz_settings['cam_v_angle']
        )
    with cols[1]:
        st.session_state.viz_settings['cam_h_angle'] = st.number_input(
            "Camera Horizontal Angle", 
            value=st.session_state.viz_settings['cam_h_angle']
        )
    with cols[2]:
        st.session_state.viz_settings['cam_distance'] = st.number_input(
            "Camera Distance", 
            value=st.session_state.viz_settings['cam_distance']
        )
    with cols[3]:
        st.session_state.viz_settings['max_view_distance'] = st.number_input(
            "Max view distance", 
            min_value=1, 
            value=st.session_state.viz_settings['max_view_distance']
        )

@st.cache_resource(show_spinner=False)
def get_stl_viewer(stl_file, settings):
    """Cache the STL viewer to prevent unnecessary reloading"""
    return stl_from_file(
        file_path=stl_file,
        color=settings['color'],
        material=settings['material'],
        auto_rotate=settings['auto_rotate'],
        opacity=settings['opacity'],
        height=settings['height'],
        shininess=100,
        cam_v_angle=settings['cam_v_angle'],
        cam_h_angle=settings['cam_h_angle'],
        cam_distance=settings['cam_distance'],
        max_view_distance=settings['max_view_distance']
    )

def main():
    # Set page config
    st.set_page_config(
        page_title="AnK CAD with Multiagent team",
        layout="wide"
    )

    # Initialize session state
    initialize_session_state()

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
        prompt = st.text_input(
            "Let's design", 
            value=st.session_state.prompt,
            placeholder="Enter a text prompt here",
            key="input_prompt"
        )
        
        # Generate button
        if st.button("Generate CAD Model"):
            if prompt:
                if handle_cad_generation(prompt):
                    st.session_state.prompt = prompt  # Save successful prompt
            else:
                st.warning("Please enter a prompt")

        # Display visualization if we have an STL file
        if st.session_state.current_stl:
            st.subheader("Here is the model!")
            render_visualization_controls()
            
            try:
                # Use cached STL viewer with current settings
                get_stl_viewer(st.session_state.current_stl, st.session_state.viz_settings)
            except Exception as e:
                st.error(f"Error displaying STL: {str(e)}")

    with col2:
        # Example prompts section
        st.subheader("Example Prompts")
        for example in examples:
            if st.button(example, key=f"example_{example}"):
                st.session_state.prompt = example
                st.rerun()

if __name__ == "__main__":
    main()