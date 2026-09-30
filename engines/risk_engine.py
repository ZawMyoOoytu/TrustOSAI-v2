import re
import time

from typing import Dict, Any, Tuple



class RiskEngine:

    """
    TrustOSAI Adaptive Risk Evaluation Engine


    Risk Model:

        R(t)=
        wi*Injection
        +
        wm*MaliciousIntent
        +
        wp*PII


    Output:

        Risk Score:
            0   = Safe
            100 = Critical


    """



    def __init__(self):


        self.injection_patterns = [

            r"(?i)ignore previous instructions",

            r"(?i)ignore all instructions",

            r"(?i)system prompt",

            r"(?i)reveal system message",

            r"(?i)bypass restrictions",

            r"(?i)developer mode",

            r"(?i)dan mode",

            r"(?i)act as an unrestricted AI"

        ]



        self.pii_patterns = {


            "email":

                r"[\w\.-]+@[\w\.-]+\.\w+",



            "credit_card":

                r"\b(?:\d[ -]*?){13,16}\b",



            "phone":

                r"\b(?:\+?95|0)9\d{7,9}\b"

        }



        self.malicious_keywords = [

            "exploit",

            "malware",

            "ransomware",

            "hack",

            "ddos",

            "phishing",

            "credential theft",

            "bypass authentication"

        ]





    # =====================================================
    # Simple Interface
    # =====================================================

    def analyze(
        self,
        task: str
    ) -> float:


        _, risk_score, _ = (

            self.analyze_intent(

                {
                    "task": task
                }

            )

        )


        return risk_score





    # =====================================================
    # Detailed Risk Analysis
    # =====================================================

    def analyze_intent(
        self,
        request_data: Dict[str,Any],
        execution_id=None
    ) -> Tuple[float,float,Dict[str,Any]]:


        start_time = time.time()



        task = (

            request_data
            .get(
                "task",
                ""
            )

        )



        injection_hits = 0

        pii_hits = 0

        malicious_hits = 0


        threats = []





        # =================================================
        # Injection Detection
        # =================================================

        for pattern in self.injection_patterns:


            if re.search(
                pattern,
                task
            ):


                injection_hits += 1


                threats.append(

                    "Injection detected: "

                    +

                    pattern

                )





        # =================================================
        # PII Detection
        # =================================================

        for name, pattern in self.pii_patterns.items():


            matches = re.findall(

                pattern,

                task

            )


            if matches:


                pii_hits += len(matches)


                threats.append(

                    f"PII detected: {name}"

                )





        # =================================================
        # Malicious Intent Detection
        # =================================================

        lower_task = task.lower()



        for keyword in self.malicious_keywords:


            if keyword in lower_task:


                malicious_hits += 1


                threats.append(

                    f"Malicious keyword: {keyword}"

                )





        # =================================================
        # Risk Mathematical Model
        # =================================================

        normalized_risk = (

            min(

                injection_hits,

                2

            )

            *

            0.25


            +


            min(

                malicious_hits,

                3

            )

            *

            0.10


            +


            min(

                pii_hits,

                2

            )

            *

            0.10

        )



        normalized_risk = min(

            max(

                normalized_risk,

                0

            ),

            1

        )



        risk_score = round(

            normalized_risk * 100,

            2

        )





        # =================================================
        # Severity
        # =================================================

        if risk_score >= 75:


            severity = "CRITICAL"


        elif risk_score >= 40:


            severity = "MEDIUM"


        else:


            severity = "LOW"





        latency_ms = round(

            (time.time() - start_time)

            *

            1000,

            3

        )





        metadata = {


            "execution_id":

                execution_id,


            "risk_score":

                risk_score,



            "severity":

                severity,



            "threats":

                threats,



            "metrics":

            {

                "injection":

                    injection_hits,


                "pii":

                    pii_hits,


                "malicious_intent":

                    malicious_hits

            },



            # =================================
            # Execution Trace
            # =================================

            "trace":

            {

                "engine":

                    "RiskEngine",


                "execution_id":

                    execution_id,


                "latency_ms":

                    latency_ms,


                "output":

                {

                    "risk_score":

                        risk_score,


                    "severity":

                        severity

                }

            }

        }





        return (

            normalized_risk,

            risk_score,

            metadata

        )