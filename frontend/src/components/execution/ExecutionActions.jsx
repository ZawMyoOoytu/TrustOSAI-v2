import {
    useState
} from "react";




export default function ExecutionActions({

    execution

}) {



    const [
        error,
        setError
    ] = useState("");








    // =====================================
    // COPY JSON
    // =====================================


    function copyJSON(){


        try{


            navigator.clipboard.writeText(

                JSON.stringify(

                    execution,

                    null,

                    2

                )

            );


            alert(
                "JSON copied successfully"
            );


        }
        catch(err){


            console.error(
                "Copy JSON Error:",
                err
            );


            setError(
                "Failed to copy JSON"
            );


        }


    }









    // =====================================
    // EXPORT JSON
    // =====================================


    function exportJSON(){


        try{


            const blob = new Blob(

                [

                    JSON.stringify(

                        execution,

                        null,

                        2

                    )

                ],

                {

                    type:
                    "application/json"

                }

            );





            const url =

            URL.createObjectURL(blob);







            const link =

            document.createElement("a");







            link.href = url;



            link.download =

            `execution-${execution.execution_id}.json`;







            document.body.appendChild(link);



            link.click();




            document.body.removeChild(link);




            URL.revokeObjectURL(url);



        }



        catch(err){


            console.error(
                "Export JSON Error:",
                err
            );


            setError(
                "Failed to export JSON"
            );


        }


    }











    return (


        <div className="execution-actions">








            {
                error &&


                <div className="error-message">


                    ❌ {error}


                </div>


            }









            <button


                className="action-btn copy"


                onClick={copyJSON}


            >


                📋 Copy JSON


            </button>









            <button


                className="action-btn export"


                onClick={exportJSON}


            >


                📥 Export JSON


            </button>









        </div>


    );


}