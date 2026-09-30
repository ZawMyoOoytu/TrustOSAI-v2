import { useEffect, useState } from "react";
import { getStats } from "../api/execution";


function useDashboard(){

    const [stats, setStats] = useState(null);


    useEffect(()=>{


        console.log("TrustOSAI: Loading stats...");


        async function loadStats(){

            try {

                const data = await getStats();


                console.log(
                    "TrustOSAI Stats Response:",
                    data
                );


                setStats(data);


            } catch(error){


                console.error(
                    "TrustOSAI API Error:",
                    error
                );


            }

        }


        loadStats();


    },[]);



    return {
        stats
    };

}


export default useDashboard;