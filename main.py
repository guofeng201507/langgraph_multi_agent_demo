from graph import graph

def run():
    user_input = input("User: ")

    state = {
        "user_input": user_input,
        "coordinator_response": {},
        "agent_outputs": {}
    }

    result = graph.invoke(state)

    print("\n--- Final Output ---")
    print(result)

if __name__ == "__main__":
    run()
