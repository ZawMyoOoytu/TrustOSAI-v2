import {
    BrowserRouter,
    Routes,
    Route
} from "react-router-dom";


// ======================================
// Layout
// ======================================

import DashboardLayout from "./layouts/DashboardLayout";



// ======================================
// Pages
// ======================================

import Dashboard from "./pages/Dashboard";

import Executions from "./pages/Executions";

import ExecutionDetail from "./pages/ExecutionDetail";

import Agents from "./pages/Agents";

import Policies from "./pages/Policies";

import Settings from "./pages/Settings";





export default function App(){


    return (

        <BrowserRouter>


            <Routes>




                {/* =================================
                    MAIN DASHBOARD
                ================================= */}


                <Route

                    path="/"

                    element={

                        <DashboardLayout>

                            <Dashboard/>

                        </DashboardLayout>

                    }

                />







                {/* =================================
                    EXECUTION HISTORY
                    Example:

                    /executions

                ================================= */}



                <Route

                    path="/executions"

                    element={

                        <DashboardLayout>

                            <Executions/>

                        </DashboardLayout>

                    }

                />









                {/* =================================
                    EXECUTION TRACE DETAIL

                    Example:

                    /executions/51

                ================================= */}



                <Route

                    path="/executions/:id"

                    element={


                        <DashboardLayout>


                            <ExecutionDetail/>


                        </DashboardLayout>


                    }

                />









                {/* =================================
                    AI AGENT MANAGEMENT
                ================================= */}



                <Route

                    path="/agents"

                    element={


                        <DashboardLayout>


                            <Agents/>


                        </DashboardLayout>


                    }

                />









                {/* =================================
                    POLICY MANAGEMENT
                ================================= */}



                <Route

                    path="/policies"

                    element={


                        <DashboardLayout>


                            <Policies/>


                        </DashboardLayout>


                    }

                />









                {/* =================================
                    SYSTEM SETTINGS
                ================================= */}



                <Route

                    path="/settings"

                    element={


                        <DashboardLayout>


                            <Settings/>


                        </DashboardLayout>


                    }

                />









                {/* =================================
                    404 ERROR PAGE
                ================================= */}



                <Route


                    path="*"


                    element={


                        <DashboardLayout>


                            <div className="not-found">



                                <h1>

                                    ⚠ Page Not Found

                                </h1>



                                <p>

                                    The requested TrustOSAI
                                    resource does not exist.

                                </p>



                            </div>



                        </DashboardLayout>


                    }


                />




            </Routes>



        </BrowserRouter>


    );


}