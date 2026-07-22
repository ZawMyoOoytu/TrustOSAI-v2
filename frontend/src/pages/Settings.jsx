import {
    useState
}
from "react";


import "./Settings.css";





export default function Settings(){



const [
    apiKey,
    setApiKey
]=useState(
"trustos_live_xxxxxxxxx"
);



const [
    environment,
    setEnvironment
]=useState(
"Production"
);



const [
    model,
    setModel
]=useState(
"llama-3-70b"
);





function saveSettings(){


alert(
"TrustOSAI configuration updated successfully"
);


}






return (



<div className="settings-page">





<div className="page-title">


<h1>

⚙ TrustOSAI Settings

</h1>


<p>

Runtime configuration and governance control

</p>


</div>








{/* Organization */}



<section className="settings-card">


<h2>

🏢 Organization

</h2>




<div className="setting-row">


<label>

Organization Name

</label>


<input

value="TrustOSAI Research Lab"

readOnly

/>


</div>





<div className="setting-row">


<label>

Environment

</label>



<select


value={environment}


onChange={(e)=>

setEnvironment(
e.target.value
)

}



>


<option>

Development

</option>


<option>

Staging

</option>


<option>

Production

</option>



</select>


</div>



</section>









{/* API Configuration */}





<section className="settings-card">


<h2>

🔑 API Configuration

</h2>




<div className="setting-row">


<label>

API Key

</label>


<input


value={apiKey}


onChange={(e)=>

setApiKey(
e.target.value
)

}



/>



</div>



<button className="secondary-btn">

Generate New Key

</button>



</section>









{/* Model Runtime */}





<section className="settings-card">


<h2>

🧠 Model Runtime

</h2>




<div className="setting-row">


<label>

Default AI Model

</label>



<select


value={model}


onChange={(e)=>

setModel(
e.target.value
)

}



>


<option>

llama-3-70b

</option>


<option>

gpt-4.1

</option>


<option>

claude-sonnet

</option>



</select>



</div>






<div className="setting-row">


<label>

Fallback Routing

</label>


<select>


<option>

Enabled

</option>


<option>

Disabled

</option>


</select>



</div>



</section>









{/* Governance */}




<section className="settings-card">


<h2>

🛡 Governance Control

</h2>





<div className="switch-row">


<label>

Automatic Policy Enforcement

</label>



<input

type="checkbox"

defaultChecked

/>



</div>





<div className="switch-row">


<label>

Human Review Required

</label>



<input

type="checkbox"

defaultChecked

/>



</div>




<div className="switch-row">


<label>

Execution Audit Logging

</label>



<input

type="checkbox"

defaultChecked

/>



</div>



</section>









{/* Billing */}



<section className="settings-card">


<h2>

💳 Usage & Billing

</h2>




<div className="billing-grid">



<div>


<h3>

Monthly Executions

</h3>


<strong>

10,000

</strong>


</div>




<div>


<h3>

Current Plan

</h3>


<strong>

Enterprise

</strong>


</div>




<div>


<h3>

Credits Remaining

</h3>


<strong>

8,420

</strong>


</div>



</div>



</section>









<button


className="save-btn"


onClick={saveSettings}


>

Save Configuration

</button>







</div>


);



}