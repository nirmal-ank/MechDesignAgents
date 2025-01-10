import gradio as gr
from chat_with_designer_expert_multimodal import multimodal_designers_chat



examples = [
    "A box with a through hole in the center.",
    "Create a pipe of outer diameter 50mm and inside diameter 40mm.",
    "Create a circular plate of radius 2mm and thickness 0.125mm with four holes of radius 0.25mm patterned at distance of 1.5mm from the centre along the axes."
]

title = "AnK CAD with Multiagent team"
description = """
Generate 3D CAD models by entering the prompt.
"""

# Create the Gradio interface
demo = gr.Interface(
    fn=multimodal_designers_chat,
    inputs=gr.Textbox(label="Let's design.", placeholder="Enter a text prompt here"),
    outputs=gr.Model3D(clear_color=[0.678, 0.847, 0.902, 1.0], label="3D CAD Model"),
    examples=examples,
    title=title,
    description=description,
    theme=gr.themes.Soft(), 
)

if __name__ == "__main__":
    demo.launch(share=True)
