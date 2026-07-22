import {useState} from "react";


import {
executeTask
}
from "../api/client";



export default function ReplayButton({

task

}){


const [loading,setLoading]=useState(false);



async function replay(){


try{


setLoading(true);


const result = await executeTask(task);



alert(

"New Execution Created: "

+

result.execution_id

);



}

catch(err){


alert(err.message);


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

"⚡ Replay Execution"

}


</button>


);


}