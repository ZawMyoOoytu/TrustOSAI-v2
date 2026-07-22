import ExecutionHeader from "./ExecutionHeader";
import ExecutionOverview from "./ExecutionOverview";
import GovernanceTimeline from "./GovernanceTimeline";
import AgentOutputViewer from "./AgentOutputViewer";
import TracePanel from "./TracePanel";
import TokenTelemetry from "./TokenTelemetry";
import ExecutionActions from "./ExecutionActions";


export default function ExecutionTrace({ execution }) {

  if (!execution) {
    return (
      <div className="
        rounded-xl 
        border 
        border-slate-700 
        bg-slate-900 
        p-8
        text-center
      ">

        <h2 className="text-xl text-white">
          No Execution Selected
        </h2>

        <p className="text-slate-400 mt-2">
          Select an execution trace to inspect governance telemetry.
        </p>

      </div>
    );
  }


  return (

    <div className="space-y-6">


      {/* Execution Identity */}
      <ExecutionHeader 
        execution={execution}
      />


      {/* Trust / Risk / Runtime */}
      <ExecutionOverview
        execution={execution}
      />


      {/* Governance Decision Flow */}
      <GovernanceTimeline
        execution={execution}
      />


      {/* Agent Response */}
      <AgentOutputViewer
        execution={execution}
      />


      {/* Runtime Trace */}
      <TracePanel
        execution={execution}
      />


      {/* Token / Cost Telemetry */}
      <TokenTelemetry
        execution={execution}
      />


      {/* Actions */}
      <ExecutionActions
        execution={execution}
      />


    </div>

  );
}