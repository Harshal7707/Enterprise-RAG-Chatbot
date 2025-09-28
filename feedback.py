
class FeedbackManager:
    def __init__(self):
        self.feedback_log = []

    def record_feedback(self, question, answer, rating):
        self.feedback_log.append({"q": question, "a": answer, "r": rating})

    def get_feedback(self):
        return self.feedback_log

