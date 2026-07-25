import { useState } from "react";


const API = "http://localhost:8000/api";



export default function ReplayButton({

    executionId

}){


    const [
        loading,
        setLoading
    ] = useState(false);




    async function replay(){


        try{


            setLoading(true);



            const response =

            await fetch(

                `${API}/replay/${executionId}`,

                {

                    method:"POST",

                    headers:{

                        "Content-Type":
                        "application/json"

                    }

                }

            );





            if(!response.ok){


                throw new Error(

                    "Replay execution failed"

                );


            }






            const data =

            await response.json();






            alert(

                "Replay Created: "

                +

                (

                    data.replay_result?.execution_id

                    ??

                    data.execution_id

                )

            );



            window.location.reload();



        }


        catch(err){


            console.error(

                "Replay Error",

                err

            );


            alert(

                err.message

            );


        }



        finally{


            setLoading(false);


        }


    }







    return(


        <button


            className="replay-button"


            onClick={replay}


            disabled={loading}


        >


            {


                loading

                ?

                "Running..."

                :

                "🔁 Replay Execution"


            }


        </button>


    );


}