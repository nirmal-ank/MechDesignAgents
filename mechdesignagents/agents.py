from autogen import ConversableAgent
from autogen import AssistantAgent, UserProxyAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import cadquery
from ocp_vscode import *
import chromadb
import os

config_list = [
    {

        "model": "llama3-70b-8192",
        "api_key":  os.environ["GROQ_API_KEY"],
        "api_type": "groq", 
    },
    {
        "model": 'gemini-pro',
        "api_key": os.environ["GEMINI_API_KEY"],  # Replace with your API key variable
        "api_type": "google",
    },
    {

        "model": "llama3-8b-8192",
        "api_key":  os.environ["GROQ_API_KEY"],
        "api_type": "groq", 
    },
    
]

llm_config = {
    "seed": 25,
    "temperature": 0,
    "config_list": config_list,
    "request_timeout": 600,
    "retry_wait_time": 120,
}

def termination_msg(x):
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

designer = UserProxyAgent(
    name="Designer",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    code_execution_config= {
        "work_dir": "NewCAD1",
        "use_docker": False,
    },
    llm_config={"config_list": config_list},
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
    Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
    description= "The designer who asks questions to create CAD models using CadQuery",
    default_auto_reply="Reply `TERMINATE` if the task is done.",
)

designer_aid  = RetrieveUserProxyAgent(
    name="Designer_Assistant",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    llm_config={"config_list": config_list},
    default_auto_reply="Reply `TERMINATE` if the task is done.",
    code_execution_config=False,
    retrieve_config={
        "task": "code",
        "docs_path":[
            "/home/niel77/MechanicalAgents/data/Examples_small.md",
            ],
        "chunk_token_size" : 500,
        "collection_name" : "groupchat",
        "get_or_create": True,
        "clean_up_tokenization_spaces": True,
    },
)

cad_coder = AssistantAgent(
    "CadQuery Code Writer",
    system_message= '''You are a CadQuery expert specializing in creating CAD models using Python. Follow the exact structure and format provided below to solve design problems and save the CAD models in STL, STEP, and DXF formats. Adhere strictly to the following outline for every response:

1. **Import Libraries:**
   Always include necessary imports, especially `cadquery` and `ocp_vscode` for model visualization.

2. **Define Parameters:**
   Clearly define parameters for the model, such as dimensions and other properties.

3. **Create the CAD Model:**
   Use CadQuery functions to build the CAD model based on the defined parameters.

4. **Save the Model:**
   Save the model in STL, STEP, and DXF formats using `cq.exporters.export`.

5. **Visualize the Model:**
   Use `show()` from the `ocp_vscode` library to visualize the created model.

6. **Example Structure:**
   ```python
   #filename: box.py
   import cadquery as cq
   from ocp_vscode import *  # Always include this for visualization.

   # Step 1: Define Parameters
   height = 60.0
   width = 80.0
   thickness = 10.0

   # Step 2: Create the CAD Model
   box = cq.Workplane("XY").box(height, width, thickness)

   # Step 3: Save the Model
   cq.exporters.export(box, "box.stl")
   cq.exporters.export(box.section(), "box.dxf")
   cq.exporters.export(box, "box.step")

   # Step 4: Visualize the Model
   show(box)  # Always use this to visualize the model.
''',
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    description="CadQuery Code Writer who writes python code to create CAD models following the system message.",
)

reviewer = AssistantAgent(
    name="Code Reviewer",
    is_termination_msg=termination_msg,
    system_message=''' You are a code review expert. Your role is to ensure that the "Creator" agent's response follows the exact structure and format specified. Check the response against the following guidelines:
    Import Libraries: Verify that the necessary imports, including cadquery and ocp_vscode, are included.
    Define Parameters: Ensure all necessary parameters (e.g., dimensions) are defined clearly.
    Create the CAD Model: Confirm that the model is built correctly using the provided parameters.
    Save the Model: Make sure the model is saved in STL, STEP, and DXF formats.
    Visualize the Model: Check if show() is used for visualization.
    If any step is missing, incorrect, or not following the instructions, provide constructive feedback to the "Creator" agent to correct it.
    Reply `TERMINATE` in the end when everything is done. ''' ,
    llm_config=llm_config,
    description="Code Reviewer who can review the python code created to generate CAD models using CadQuery and also visualize using show(model) method.",
    code_execution_config= {
        "work_dir": "NewCAD1",
        "use_docker": False,
    },
)

def reset_agents():
    designer.reset()
    designer_aid.reset()
    cad_coder.reset()
    reviewer.reset()