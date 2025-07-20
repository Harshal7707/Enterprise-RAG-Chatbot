class Chatbot:
    def __init__(self, qa_chain):
        self.qa_chain = qa_chain

    def get_response(self, user_input):
        try:
            response = self.qa_chain({"query": user_input})
            return response["result"]
        except Exception as e:
            return f"An error occurred: {str(e)}"
