import { Link } from "react-router-dom";

export default function ExecutionTable({

    executions

}) {

    if (!executions.length) {

        return (

            <div className="empty">

                No executions found.

            </div>

        );

    }

    return (

        <table className="execution-table">

            <thead>

                <tr>

                    <th>ID</th>

                    <th>Task</th>

                    <th>Agent</th>

                    <th>Trust</th>

                    <th>Risk</th>

                    <th>Decision</th>

                    <th>Created</th>

                    <th></th>

                </tr>

            </thead>

            <tbody>

                {

                    executions.map(execution=>(

                        <tr key={execution.execution_id}>

                            <td>

                                #{execution.execution_id}

                            </td>

                            <td>

                                {execution.task}

                            </td>

                            <td>

                                {execution.agent}

                            </td>

                            <td>

                                {execution.trust_score}

                            </td>

                            <td>

                                {execution.risk_score}

                            </td>

                            <td>

                                <span
                                    className={`decision ${execution.decision.toLowerCase()}`}
                                >

                                    {execution.decision}

                                </span>

                            </td>

                            <td>

                                {

                                    new Date(
                                        execution.created_at
                                    ).toLocaleString()

                                }

                            </td>

                            <td>

                                <Link
                                    to={`/executions/${execution.execution_id}`}
                                >

                                    View

                                </Link>

                            </td>

                        </tr>

                    ))

                }

            </tbody>

        </table>

    );

}