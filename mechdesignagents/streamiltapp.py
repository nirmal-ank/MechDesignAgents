import streamlit as st
from chat_with_designer_expert_multimodal import multimodal_designers_chat

# Function to visualize STL file
def visualize_stl(stl_path):
    st.write("### 3D CAD Model")
    try:
        # Display download button for the STL file
        with open(stl_path, "rb") as stl_file:
            st.download_button(
                label="Download STL File",
                data=stl_file,
                file_name="generated_model.stl",
                mime="application/octet-stream"
            )
        st.write("### Rendered View")
        st.markdown("Use an external viewer like MeshLab or other CAD tools to view the STL file in 3D.")
    except Exception as e:
        st.error(f"Error displaying STL file: {e}")

# Streamlit UI
st.title("AnK CAD with Multiagent Team")
st.write("Generate 3D CAD models by entering the prompt.")

# Input text prompt
prompt = st.text_input("Let's design:", placeholder="Enter a text prompt here")

# Process the input and generate the STL file
if st.button("Generate"):
    if prompt.strip():
        try:
            st.write("Processing your prompt...")
            
            # Call the multimodal_designers_chat function to generate the STL file path
            stl_path = multimodal_designers_chat(prompt)
            
            # Visualize the STL file
            visualize_stl(stl_path)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a prompt before clicking Generate.")

# Examples
st.write("### Examples")
examples = [
    "A box with a through hole in the center.",
    "Create a pipe of outer diameter 50mm and inside diameter 40mm.",
    "Create a circular plate of radius 2mm and thickness 0.125mm with four holes of radius 0.25mm patterned at distance of 1.5mm from the centre along the axes."
]
for example in examples:
    if st.button(f"Use example: {example}"):
        st.experimental_set_query_params(prompt=example)
        st.experimental_rerun()
