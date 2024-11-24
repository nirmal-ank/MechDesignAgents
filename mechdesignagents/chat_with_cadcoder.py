from agents import *

#for two agent system with just designer and cad coder.

User = UserProxyAgent(
    name="User",
    is_termination_msg=termination_msg,
    human_input_mode="ALWAYS", # Use ALWAYS for human in the loop
    max_consecutive_auto_reply=5, #Change it to limit the number of replies from this agent
    #here we define the coding configuration for executing the code generated by agent 
    code_execution_config= {
        "work_dir": "NewCADs",
        "use_docker": False,
    },
    # llm_config={"config_list": config_list}, #you can also select a particular model from the config list here for llm
    system_message=""" A human designer who asks questions to create CAD models using CadQuery. Interact with Designer Expert
    on how to create the cad model. The Designer Expert's approach to create models needs to be
    approved by this Designer. """,
    description= "The designer who asks questions to create CAD models using CadQuery",
    default_auto_reply="Reply `TERMINATE` if the task is done.",
)

def main():
    """Two agent CAD generation"""
    print("\nTwo agent CAD generation system")
    print("----------------------------------")
    print("Enter 'quit' to exit the program")

    reset_agents()
    
    while True:
        try:
            prompt = input("\nEnter your design problem (or 'quit'if you want to exit): ")
            if prompt.lower() == 'quit':
                print("\nExiting CAD Design Assistant")
                break
            User.initiate_chat(cad_coder, message=prompt)

            
        except KeyboardInterrupt:
            print("\nSession interrupted by user")
            break
        except ValueError as ve:
            print(f"\nError: {str(ve)}")
            print("Please try again with a more detailed prompt")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again or create github issues if the problem persists")

if __name__ == "__main__":
    main()