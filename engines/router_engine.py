class RouterEngine:

    def route(
        self,
        governance
    ):

        if governance == "ALLOW":
            return "EXECUTION"

        if governance == "REVIEW":
            return "MANUAL"

        return "DENY"