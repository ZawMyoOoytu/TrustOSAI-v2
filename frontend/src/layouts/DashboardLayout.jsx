import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";


export default function DashboardLayout({children}){


return (

<div className="app-layout">


<Sidebar/>


<div className="main-area">


<Topbar/>


<main>

{children}

</main>


</div>


</div>

);


}