export default function Timeline() {

    const steps = [

        "Request Received",

        "Policy Evaluation",

        "Trust Generated",

        "Decision Generated",

        "Agent Executed",

        "Audit Stored"

    ];

    return (

        <div className="timeline">

            {

                steps.map((item) => (

                    <div

                        key={item}

                        className="timeline-item"

                    >

                        ✓ {item}

                    </div>

                ))

            }

        </div>

    );

}