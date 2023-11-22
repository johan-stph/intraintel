import time


class ChainStub:
    def invoke(self, message):
        print("Function is starting...")
        # Simulate some time-consuming work
        time.sleep(5)
        print("Function is finished.")
        return "answer"
