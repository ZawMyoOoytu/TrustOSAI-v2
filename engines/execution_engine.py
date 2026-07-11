class ExecutionEngine:

    def execute(
        self,
        route,
        task
    ):

        if route == "DENY":

            return "Execution blocked"

        if route == "MANUAL":

            return "Waiting for approval"

        return "Execution completed successfully"