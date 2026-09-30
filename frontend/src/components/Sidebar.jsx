import {Link} from "react-router-dom";


export default function Sidebar(){


return (

<div className="sidebar">


<h2>
⚡ TrustOSAI
</h2>



<nav>


<Link to="/">
Dashboard
</Link>


<Link to="/executions">
Executions
</Link>


<Link to="/agents">
Agents
</Link>


<Link to="/policies">
Policies
</Link>


<Link to="/settings">
Settings
</Link>


</nav>


</div>

);


}