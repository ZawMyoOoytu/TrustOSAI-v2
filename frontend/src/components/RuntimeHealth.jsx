export default function RuntimeHealth() {

    const services = [

        "API Gateway",

        "Database",

        "Policy Engine",

        "Memory Engine"

    ];

    return (

        <div>

            {

                services.map((item) => (

                    <div

                        key={item}

                        className="health-item"

                    >

                        🟢 {item} ONLINE

                    </div>

                ))

            }

        </div>

    );

}