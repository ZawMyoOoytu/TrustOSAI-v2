import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import "./Executions.css";

import {
  getExecutions,
  deleteExecution as removeExecution,
} from "../api/execution";



const decisionTypes = [
  "ALL",
  "ALLOW",
  "ALLOW_WITH_MONITORING",
  "REVIEW",
  "BLOCK",
];



export default function Executions() {


  const navigate = useNavigate();


  const [executions, setExecutions] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState(null);



  const [search, setSearch] = useState("");

  const [filter, setFilter] = useState("ALL");





  // =====================================================
  // LOAD EXECUTIONS
  // =====================================================

  const loadExecutions = async()=>{


    try{


      setLoading(true);


      const data = await getExecutions();



      console.log(
        "EXECUTIONS RESPONSE:",
        data
      );



      setExecutions(

        Array.isArray(data)

        ? data

        : data.executions || []

      );



    }

    catch(err){


      console.error(
        "Execution Load Error:",
        err
      );


      setError(
        err.message
      );


    }

    finally{


      setLoading(false);


    }


  };






  useEffect(()=>{


    loadExecutions();


  },[]);








  // =====================================================
  // DELETE EXECUTION
  // =====================================================

  const deleteExecution = async(id)=>{


    const confirmDelete = window.confirm(

      `Delete execution #${id}?`

    );



    if(!confirmDelete)
      return;




    try{


      await removeExecution(id);



      await loadExecutions();



    }

    catch(err){


      console.error(err);



      alert(
        err.message
      );


    }


  };









  // =====================================================
  // FILTER
  // =====================================================


  const filtered = executions.filter((item)=>{


    const task = (

      item.task || ""

    ).toLowerCase();



    const matchSearch = task.includes(

      search.toLowerCase()

    );



    const matchDecision =

      filter === "ALL"

      ||

      item.decision === filter;



    return (

      matchSearch

      &&

      matchDecision

    );


  });









  // =====================================================
  // LOADING
  // =====================================================


  if(loading){


    return (

      <div className="executions-page">

        <h2>
          Loading executions...
        </h2>

      </div>

    );


  }






  // =====================================================
  // ERROR
  // =====================================================


  if(error){


    return (

      <div className="executions-page">


        <h2>

          ❌ {error}

        </h2>


      </div>

    );


  }









  // =====================================================
  // UI
  // =====================================================


  return (


    <div className="executions-page">



      <div className="page-header">


        <h1>
          ⚡ Execution History
        </h1>


        <p>
          AI Governance Runtime Telemetry
        </p>


      </div>









      <div className="toolbar">


        <input

          type="text"

          placeholder="Search executions..."

          value={search}

          onChange={(e)=>
            setSearch(
              e.target.value
            )
          }

        />





        <div className="filters">


          {
            decisionTypes.map((status)=>(


              <button


                key={status}


                className={

                  filter === status

                  ?

                  "active-filter"

                  :

                  ""

                }


                onClick={()=>


                  setFilter(status)

                }


              >

                {status}


              </button>


            ))
          }



        </div>



      </div>









      <div className="execution-table">



        <div className="table-header">


          <span>ID</span>

          <span>Task</span>

          <span>Agent</span>

          <span>Trust</span>

          <span>Decision</span>

          <span>Created</span>

          <span>Actions</span>


        </div>









        {
          filtered.length === 0 ?


          (

            <div className="table-row empty">


              <span>

                No executions found.

              </span>


            </div>


          )


          :



          filtered.map((item)=>(


            <div


              className="table-row"


              key={

                item.execution_id

              }


            >




              <span>

                #{item.execution_id}

              </span>







              <span className="task">

                {item.task || "-"}

              </span>







              <span>

                {item.agent || "-"}

              </span>







              <span className="trust">


                {

                  Math.round(

                    item.trust_score || 0

                  )

                }


              </span>







              <span>


                <DecisionBadge

                  decision={

                    item.decision

                  }

                />


              </span>







              <span>


                {

                  item.created_at

                  ?

                  new Date(

                    item.created_at

                  ).toLocaleString()

                  :

                  "-"

                }


              </span>







              <span className="actions">



                <button


                  className="view-btn"


                  onClick={()=>


                    navigate(

                      `/executions/${item.execution_id}`

                    )


                  }


                >

                  👁 View


                </button>







                <button


                  className="delete-btn"


                  onClick={()=>


                    deleteExecution(

                      item.execution_id

                    )


                  }


                >

                  🗑 Delete


                </button>



              </span>






            </div>


          ))

        }





      </div>





    </div>


  );


}









// =====================================================
// DECISION BADGE
// =====================================================


function DecisionBadge({

  decision

}){


  const badgeClass = decision

    ?

    decision

      .toLowerCase()

      .replace(

        /_/g,

        "-"

      )

    :

    "";



  return (

    <span

      className={

        `badge ${badgeClass}`

      }

    >

      {decision || "-"}


    </span>

  );


}