from typing import Dict, Any

class RouterEngine:
    def __init__(self):
        # Available Agent/Model Pool and Capability Matrix (စာတမ်းပါ Model Capability Metadata)
        # cost: per 1k tokens, latency_factor: lower is faster, accuracy_tier: 0.0 to 1.0
        self.agent_pool = {
            "gpt-4o": {
                "model_name": "gpt-4o",
                "cost_per_1k": 0.015,
                "latency_factor": 1.2,
                "accuracy_tier": 0.95,
                "capabilities": ["complex_reasoning", "coding", "financial_analysis"]
            },
            "llama-3-70b": {
                "model_name": "llama-3-70b",
                "cost_per_1k": 0.002,
                "latency_factor": 0.8,
                "accuracy_tier": 0.85,
                "capabilities": ["general_text", "summarization", "extraction"]
            },
            "phi-3-mini": {
                "model_name": "phi-3-mini",
                "cost_per_1k": 0.0001,
                "latency_factor": 0.3,
                "accuracy_tier": 0.65,
                "capabilities": ["simple_tasks", "classification"]
            }
        }

    def route(self, governance_result: Dict[str, Any]) -> str:
        """
        Legacy Interface used by standalone RuntimeOrchestrator pipeline.
        Defaults to selecting the highest tier model if governance allows.
        """
        if isinstance(governance_result, dict) and governance_result.get("status") == "BLOCK":
            return "None (Terminated)"
        return "gpt-4o"

    def select_optimal_agent(self, trust_context: Dict[str, Any], request_data: Dict[str, Any]) -> str:
        """
        Academic-Grade Optimization Router (Mathematical Utility Function Maximization).
        Selects target model m* by maximizing: Utility = (w_acc * Accuracy) - (w_cost * Cost) - (w_lat * Latency)
        """
        task_content = request_data.get("task", "").lower()
        aggregated_trust = trust_context.get("aggregated_trust", 100.0)
        
        # 1. Dynamic Weight Adjustment based on Trust Vector State
        # စနစ်ရဲ့ စုစုပေါင်း Trust Score ကျဆင်းနေချိန်ဆိုလျှင် Accuracy ကို ပိုအလေးပေးပြီး လုံခြုံစိတ်ချရသော မော်ဒယ်ကို ရွေးချယ်မည်
        if aggregated_trust < 75.0:
            w_accuracy = 0.70
            w_cost = 0.15
            w_latency = 0.15
        else:
            # Normal State: Balanced Optimization
            w_accuracy = 0.40
            w_cost = 0.40
            w_latency = 0.20

        best_utility = -float('inf')
        selected_agent = "llama-3-70b" # Default Fallback Agent

        # 2. Match Tasks to Capabilities and Compute Multi-Criteria Utility Scores
        for agent_name, profile in self.agent_pool.items():
            
            # Step A: Domain Match Bonus (မော်ဒယ်ကျွမ်းကျင်မှုနယ်ပယ်နှင့် တိုက်စစ်ခြင်း)
            domain_bonus = 0.10 if any(cap in task_content for cap in profile["capabilities"]) else 0.0
            effective_accuracy = profile["accuracy_tier"] + domain_bonus

            # Step B: Apply Utility Optimization Formula (Section XII Equation)
            # Normalize Cost and Latency values for mathematical synthesis
            normalized_cost = profile["cost_per_1k"] / 0.015  # Scaled against max cost
            normalized_latency = profile["latency_factor"] / 1.2 # Scaled against max latency

            utility_score = (
                (w_accuracy * effective_accuracy) - 
                (w_cost * normalized_cost) - 
                (w_latency * normalized_latency)
            )

            # Step C: Find Maximum Argument (Argmax m*)
            if utility_score > best_utility:
                best_utility = utility_score
                selected_agent = profile["model_name"]

        return selected_agent