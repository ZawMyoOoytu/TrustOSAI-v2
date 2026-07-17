from typing import Dict, Any, Tuple
from sqlalchemy.orm import Session


class CostEngine:

    def __init__(self):

        # =====================================================
        # Token Pricing Matrix ($ / 1M Tokens)
        # =====================================================

        self.pricing_matrix = {

            "gpt-4o": {

                "input_per_1m": 5.00,

                "output_per_1m": 15.00

            },


            "llama-3-70b": {

                "input_per_1m": 0.59,

                "output_per_1m": 0.79

            },


            "phi-3-mini": {

                "input_per_1m": 0.05,

                "output_per_1m": 0.10

            }

        }



    # =====================================================
    # Main Runtime Interface
    # Used by ExecutionService
    # =====================================================

    def calculate(
        self,
        task: str,
        latency_ms: int = 0,
        db: Session = None
    ) -> Dict[str, Any]:


        # -------------------------------------------------
        # Runtime estimation
        # Replace later with real tokenizer
        # -------------------------------------------------

        prompt_tokens = max(
            len(task.split()),
            1
        )


        completion_tokens = int(
            prompt_tokens * 0.5
        )


        model_name = "gpt-4o"



        input_cost, total_cost, metadata = (
            self.calculate_financial_metrics(

                model_name,

                prompt_tokens,

                completion_tokens

            )
        )



        return {


            "model":

                model_name,


            "prompt_tokens":

                prompt_tokens,


            "completion_tokens":

                completion_tokens,


            "input_cost":

                input_cost,


            "total_cost":

                total_cost,


            "latency_ms":

                latency_ms,


            "metadata":

                metadata

        }





    # =====================================================
    # Legacy Interface
    # =====================================================

    def compute(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int
    ) -> float:


        _, total_cost, _ = (

            self.calculate_financial_metrics(

                model,

                prompt_tokens,

                completion_tokens

            )

        )


        return total_cost





    # =====================================================
    # Academic Financial Auditor
    # =====================================================

    def calculate_financial_metrics(
        self,
        model_name: str,
        prompt_tokens: int,
        completion_tokens: int
    ) -> Tuple[float, float, Dict[str, Any]]:



        rates = self.pricing_matrix.get(

            model_name,

            {

                "input_per_1m": 0.10,

                "output_per_1m": 0.20

            }

        )



        input_cost = (

            prompt_tokens
            /
            1_000_000

        ) * rates["input_per_1m"]



        output_cost = (

            completion_tokens
            /
            1_000_000

        ) * rates["output_per_1m"]



        total_cost = (

            input_cost

            +

            output_cost

        )



        metadata = {


            "target_model_evaluated":

                model_name,


            "token_counts":

            {

                "input":

                    prompt_tokens,


                "output":

                    completion_tokens,


                "aggregate_total":

                    prompt_tokens + completion_tokens

            },



            "financial_breakdown":

            {

                "input_expense_usd":

                    round(input_cost, 8),


                "output_expense_usd":

                    round(output_cost, 8),


                "total_expense_usd":

                    round(total_cost, 8)

            },



            "cost_efficiency_tier":

                (
                    "HIGH"
                    if total_cost < 0.0001
                    else
                    "PREMIUM"
                )

        }



        return (

            input_cost,

            total_cost,

            metadata

        )