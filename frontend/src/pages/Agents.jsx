import {
    useEffect,
    useState
}
from "react";


import {

    getAgents,

    createAgent,

    enableAgent,

    disableAgent,

    getAgentStats

}
from "../api/client";


import "./Agents.css";






export default function Agents(){



    const [agents,setAgents] = useState([]);


    const [loading,setLoading] = useState(true);


    const [error,setError] = useState("");



    const [showCreate,setShowCreate] = useState(false);



    const [selectedStats,setSelectedStats] = useState(null);





    const [newAgent,setNewAgent] = useState({

        name:"",

        description:"",

        agent_type:"GENERAL",

        model:"llama-3-70b",

        provider:"local",

        trust_threshold:60,

        risk_level:"MEDIUM"

    });








    // =====================================================
    // LOAD AGENTS
    // =====================================================


    async function loadAgents(){


        try{


            setLoading(true);


            const data = await getAgents();



            setAgents(data);



            setError("");



        }

        catch(err){


            console.error(err);


            setError(

                "Cannot load Agent Registry"

            );


        }

        finally{


            setLoading(false);


        }



    }








    useEffect(()=>{


        loadAgents();



    },[]);









    // =====================================================
    // CREATE AGENT
    // =====================================================


    async function handleCreate(){



        try{


            await createAgent(newAgent);



            setShowCreate(false);



            setNewAgent({

                name:"",

                description:"",

                agent_type:"GENERAL",

                model:"llama-3-70b",

                provider:"local",

                trust_threshold:60,

                risk_level:"MEDIUM"

            });



            loadAgents();



        }

        catch(err){


            alert(

                err.message

            );


        }


    }









    // =====================================================
    // ENABLE / DISABLE
    // =====================================================


    async function toggleStatus(agent){



        try{


            if(agent.status==="ACTIVE"){


                await disableAgent(agent.id);


            }

            else{


                await enableAgent(agent.id);


            }



            loadAgents();



        }

        catch(err){


            alert(

                err.message

            );


        }



    }









    // =====================================================
    // STATS
    // =====================================================


    async function showStats(agent){



        try{


            const stats = await getAgentStats(

                agent.id

            );


            setSelectedStats(stats);



        }

        catch(err){


            alert(

                "Cannot load stats"

            );


        }


    }









    if(loading){


        return (

            <div className="agents-page">


                <h2>

                    Loading Agent Registry...

                </h2>


            </div>

        );


    }








    return (



        <div className="agents-page">







            <div className="page-title">



                <div>


                    <h1>

                        🤖 AI Agent Registry

                    </h1>



                    <p>

                        Manage autonomous AI execution agents

                    </p>


                </div>






                <button

                    className="create-btn"

                    onClick={()=>setShowCreate(true)}

                >

                    + Create Agent


                </button>



            </div>








            {
                error &&

                <div className="error-box">

                    {error}

                </div>

            }









            <div className="agent-grid">





            {


            agents.map(agent=>(



                <div

                    className="agent-card"

                    key={agent.id}


                >







                    <div className="agent-header">



                        <h2>

                            {agent.name}

                        </h2>



                        <span

                        className={

                            agent.status==="ACTIVE"

                            ?

                            "active"

                            :

                            "disabled"

                        }

                        >

                            {agent.status}


                        </span>



                    </div>










                    <div className="agent-info">



                        <p>

                            Type

                            <strong>

                                {agent.agent_type}

                            </strong>


                        </p>





                        <p>

                            Model

                            <strong>

                                {agent.model}

                            </strong>


                        </p>






                        <p>

                            Provider

                            <strong>

                                {agent.provider}

                            </strong>


                        </p>






                        <p>

                            Trust Threshold

                            <strong>

                                {agent.trust_threshold}

                            </strong>


                        </p>







                    </div>









                    <div className="trust-bar">


                        <div


                        style={{

                            width:

                            `${agent.average_trust || 0}%`

                        }}


                        />



                    </div>







                    <div className="card-actions">



                        <button

                            onClick={()=>showStats(agent)}

                        >

                            📊 Stats


                        </button>





                        <button

                        onClick={()=>toggleStatus(agent)}

                        >


                        {

                            agent.status==="ACTIVE"

                            ?

                            "Disable"

                            :

                            "Enable"

                        }


                        </button>




                    </div>







                </div>



            ))



            }





            </div>













            {
            showCreate &&


            <div className="modal">



                <div className="modal-box">


                    <h2>

                        Create New Agent

                    </h2>




                    <input

                    placeholder="Agent Name"

                    value={newAgent.name}

                    onChange={e=>

                        setNewAgent({

                            ...newAgent,

                            name:e.target.value

                        })

                    }

                    />






                    <input

                    placeholder="Model"

                    value={newAgent.model}

                    onChange={e=>

                        setNewAgent({

                            ...newAgent,

                            model:e.target.value

                        })

                    }

                    />







                    <input

                    placeholder="Provider"

                    value={newAgent.provider}

                    onChange={e=>

                        setNewAgent({

                            ...newAgent,

                            provider:e.target.value

                        })

                    }

                    />









                    <button

                    onClick={handleCreate}

                    >

                        Create


                    </button>





                    <button

                    onClick={()=>setShowCreate(false)}

                    >

                        Cancel


                    </button>





                </div>



            </div>


            }









            {
            selectedStats &&


            <div className="modal">


                <div className="modal-box">


                    <h2>

                        Agent Statistics

                    </h2>



                    <p>

                    Agent:

                    {selectedStats.agent_name}

                    </p>



                    <p>

                    Executions:

                    {selectedStats.total_executions}

                    </p>



                    <p>

                    Average Trust:

                    {selectedStats.average_trust}

                    </p>



                    <p>

                    Success Rate:

                    {selectedStats.success_rate}%

                    </p>





                    <button

                    onClick={()=>setSelectedStats(null)}

                    >

                    Close


                    </button>



                </div>



            </div>

            }





        </div>



    );



}