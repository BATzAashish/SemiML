import DashboardPage from "./pages/DashboardPage";
import DatasetUploadPage from "./pages/DatasetUploadPage";
import DataUploadTestPage from "./pages/DataUploadTestPage";
import MetaFeaturesTestPage from "./pages/MetaFeaturesTestPage";
import DataAnalysisPage from "./pages/DataAnalysisPage";
import PipelinePage from "./pages/PipelinePage";
import DecisionTracePage from "./pages/DecisionTracePage";
import EvaluationPage from "./pages/EvaluationPage";
import ExplainabilityPage from "./pages/ExplainabilityPage";
import AssistantPage from "./pages/AssistantPage";
import ExperimentsPage from "./pages/ExperimentsPage";
import ConnectionTestPage from "./pages/ConnectionTestPage";

export const appRoutes = [
  { path: "/", label: "Dashboard", element: DashboardPage },
  { path: "/connection-test", label: "Connection Test", element: ConnectionTestPage },
  { path: "/upload", label: "Upload", element: DatasetUploadPage },
  { path: "/data-upload-test", label: "Data Upload Test (M2)", element: DataUploadTestPage },
  { path: "/meta-features-test", label: "Meta-Features Test (M3)", element: MetaFeaturesTestPage },
  { path: "/analysis", label: "Data Analysis", element: DataAnalysisPage },
  { path: "/pipeline", label: "Pipeline", element: PipelinePage },
  { path: "/decision-trace", label: "Decision Trace", element: DecisionTracePage },
  { path: "/evaluation", label: "Evaluation", element: EvaluationPage },
  { path: "/explainability", label: "Explainability", element: ExplainabilityPage },
  { path: "/assistant", label: "AI Assistant", element: AssistantPage },
  { path: "/experiments", label: "History", element: ExperimentsPage },
];
