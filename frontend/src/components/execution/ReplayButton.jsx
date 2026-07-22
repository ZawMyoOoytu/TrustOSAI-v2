import {useState} from "react";


export default function ReplayButton({
execution
}){


const [loading,setLoading]=useState(false);



async function replay(){


try{


setLoading(true);



const response = await fetch(

"http://localhost:8000/api/execution/",

{

method:"POST",

headers:{

"Content-Type":
"application/json"

},


body:JSON.stringify({

task:
execution.task

})


}

);



const data =
await response.json();



alert(

`New Execution Created #${data.execution_id}`

);



}

catch(err){


console.error(err);


alert(
"Replay failed"
);


}

finally{


setLoading(false);


}



}



return (

<button

className="replay-btn"

onClick={replay}

disabled={loading}

>


{

loading

?

"Running..."

:

"▶ Replay Execution"

}


</button>


);


}