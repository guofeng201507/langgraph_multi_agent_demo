from llm_router import summarize_response_ollama  # Replace with actual module name


def test_local_ollama_summary():
    prompt = """
    Customer called complaining about late delivery and a missing item from their order.
    They were polite but frustrated. Requesting refund or reshipment.
    
    Please respond with maximum length of 20 words
    """

    result = summarize_response_ollama(prompt, expect_json=False)
    print("\n🧪 Test Result:")
    print(result)


if __name__ == "__main__":
    test_local_ollama_summary()
