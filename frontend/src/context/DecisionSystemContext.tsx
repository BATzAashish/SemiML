import { createContext, useContext, useMemo, useState } from "react";

const DecisionSystemContext = createContext(null);

export function DecisionSystemProvider({ children }) {
  const [dataset, setDataset] = useState(null);
  const [problemContext, setProblemContext] = useState({ problemType: "classification", targetColumn: "", priority: "explainability", constraints: "" });
  const [selectedModel, setSelectedModel] = useState("Explainable Gradient Boosting");
  const [pipelineResults, setPipelineResults] = useState(null);

  const value = useMemo(() => ({ dataset, setDataset, problemContext, setProblemContext, selectedModel, setSelectedModel, pipelineResults, setPipelineResults }), [dataset, problemContext, selectedModel, pipelineResults]);
  return <DecisionSystemContext.Provider value={value}>{children}</DecisionSystemContext.Provider>;
}

export const useDecisionSystem = () => useContext(DecisionSystemContext);
