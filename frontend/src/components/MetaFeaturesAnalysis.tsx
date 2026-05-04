/**
 * Meta-Features Analysis Component
 * Location: frontend/src/components/MetaFeaturesAnalysis.tsx
 * 
 * Component for analyzing dataset meta-features
 */

import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import backendService from "@/services/backend";

interface MetaFeatures {
  dataset_id: string;
  basic_info: any;
  statistical_features: any;
  feature_analysis: any;
  missing_data_analysis: any;
  data_quality: any;
  class_distribution: any;
  feature_types: any;
}

interface DataPreview {
  dataset_id: string;
  rows_shown: number;
  total_rows: number;
  columns: string[];
  data: any[];
}

export default function MetaFeaturesAnalysis() {
  const [selectedDatasetId, setSelectedDatasetId] = useState("");
  const [datasets, setDatasets] = useState<any[]>([]);
  const [metaFeatures, setMetaFeatures] = useState<MetaFeatures | null>(null);
  const [dataPreview, setDataPreview] = useState<DataPreview | null>(null);
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("overview");

  // Load datasets on mount
  React.useEffect(() => {
    loadDatasets();
  }, []);

  const loadDatasets = async () => {
    try {
      const response = await backendService.listDatasets();
      setDatasets(response.datasets || []);
      if (response.datasets && response.datasets.length > 0) {
        setSelectedDatasetId(response.datasets[0].dataset_id);
      }
    } catch (err: any) {
      setError(`Error loading datasets: ${err.message}`);
    }
  };

  const handleAnalyzeDataset = async () => {
    if (!selectedDatasetId) {
      setError("Please select a dataset");
      return;
    }

    setLoading(true);
    setError("");

    try {
      // Get meta-features
      const metaFeaturesResponse = await backendService.extractMetaFeatures(
        selectedDatasetId
      );
      setMetaFeatures(metaFeaturesResponse.meta_features);

      // Get data preview
      const previewResponse = await backendService.getDataPreview(
        selectedDatasetId,
        5
      );
      setDataPreview(previewResponse);

      // Get summary
      const summaryResponse = await backendService.getDatasetSummary(
        selectedDatasetId
      );
      setSummary(summaryResponse.summary);
    } catch (err: any) {
      setError(`Analysis failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 w-full">
      {/* Dataset Selection */}
      <Card>
        <CardHeader>
          <CardTitle>Select Dataset for Analysis</CardTitle>
          <CardDescription>Choose a dataset to analyze its meta-features</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className="flex gap-4">
            <select
              value={selectedDatasetId}
              onChange={(e) => setSelectedDatasetId(e.target.value)}
              disabled={loading}
              className="flex-1 px-3 py-2 border rounded-md"
            >
              <option value="">Select a dataset...</option>
              {datasets.map((dataset) => (
                <option key={dataset.dataset_id} value={dataset.dataset_id}>
                  {dataset.filename} ({dataset.data_metadata?.num_rows} rows)
                </option>
              ))}
            </select>

            <Button onClick={handleAnalyzeDataset} disabled={loading || !selectedDatasetId}>
              {loading ? "Analyzing..." : "Analyze Dataset"}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Analysis Results */}
      {metaFeatures && summary && (
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="statistics">Statistics</TabsTrigger>
            <TabsTrigger value="features">Features</TabsTrigger>
            <TabsTrigger value="preview">Preview</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Dataset Overview</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-muted-foreground">Rows</p>
                    <p className="text-2xl font-bold">
                      {metaFeatures.basic_info.num_rows.toLocaleString()}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Columns</p>
                    <p className="text-2xl font-bold">
                      {metaFeatures.basic_info.num_columns}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Memory Usage</p>
                    <p className="text-2xl font-bold">
                      {metaFeatures.basic_info.memory_usage_mb.toFixed(2)} MB
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Sparsity</p>
                    <p className="text-2xl font-bold">
                      {metaFeatures.basic_info.sparsity.toFixed(2)}%
                    </p>
                  </div>
                </div>

                {/* Data Quality */}
                <div className="mt-6">
                  <h3 className="text-lg font-semibold mb-3">Data Quality Metrics</h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <p className="text-sm text-muted-foreground">Completeness</p>
                      <p className="text-2xl font-bold">
                        {metaFeatures.data_quality.completeness_score.toFixed(1)}%
                      </p>
                    </div>
                    <div className="bg-green-50 p-4 rounded-lg">
                      <p className="text-sm text-muted-foreground">Uniqueness</p>
                      <p className="text-2xl font-bold">
                        {metaFeatures.data_quality.uniqueness_score.toFixed(1)}%
                      </p>
                    </div>
                    <div className="bg-purple-50 p-4 rounded-lg">
                      <p className="text-sm text-muted-foreground">Overall Quality</p>
                      <p className="text-2xl font-bold">
                        {metaFeatures.data_quality.overall_quality_score.toFixed(1)}%
                      </p>
                    </div>
                  </div>
                </div>

                {/* Recommendations */}
                <div className="mt-6">
                  <h3 className="text-lg font-semibold mb-3">Recommendations</h3>
                  <ul className="space-y-2">
                    {summary.recommendations.map((rec: string, idx: number) => (
                      <li key={idx} className="flex items-center gap-2">
                        <Badge variant="outline">✓</Badge>
                        <span className="text-sm">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Modeling Readiness */}
                <div className="mt-6">
                  <Badge
                    variant={summary.ready_for_modeling ? "default" : "secondary"}
                  >
                    {summary.ready_for_modeling
                      ? "✓ Ready for Modeling"
                      : "⚠ Needs Preprocessing"}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Statistics Tab */}
          <TabsContent value="statistics">
            <Card>
              <CardHeader>
                <CardTitle>Statistical Features</CardTitle>
              </CardHeader>
              <CardContent>
                {metaFeatures.statistical_features.numeric_columns_count > 0 ? (
                  <div className="space-y-4">
                    <p className="text-sm text-muted-foreground">
                      Numeric Columns: {metaFeatures.statistical_features.numeric_columns_count}
                    </p>

                    <div className="overflow-x-auto">
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead>Column</TableHead>
                            <TableHead>Mean</TableHead>
                            <TableHead>Std Dev</TableHead>
                            <TableHead>Min</TableHead>
                            <TableHead>Max</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {metaFeatures.statistical_features.numeric_columns.map(
                            (col: string) => (
                              <TableRow key={col}>
                                <TableCell className="font-medium">{col}</TableCell>
                                <TableCell>
                                  {metaFeatures.statistical_features.means[col]?.toFixed(2) || "N/A"}
                                </TableCell>
                                <TableCell>
                                  {metaFeatures.statistical_features.stds[col]?.toFixed(2) || "N/A"}
                                </TableCell>
                                <TableCell>
                                  {metaFeatures.statistical_features.mins[col]?.toFixed(2) || "N/A"}
                                </TableCell>
                                <TableCell>
                                  {metaFeatures.statistical_features.maxs[col]?.toFixed(2) || "N/A"}
                                </TableCell>
                              </TableRow>
                            )
                          )}
                        </TableBody>
                      </Table>
                    </div>
                  </div>
                ) : (
                  <p className="text-muted-foreground">No numeric columns found</p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Features Tab */}
          <TabsContent value="features">
            <Card>
              <CardHeader>
                <CardTitle>Feature Analysis</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <p className="text-sm text-muted-foreground">Numeric Features</p>
                    <p className="text-2xl font-bold">
                      {metaFeatures.feature_analysis.numeric_columns}
                    </p>
                  </div>
                  <div className="bg-orange-50 p-4 rounded-lg">
                    <p className="text-sm text-muted-foreground">Categorical Features</p>
                    <p className="text-2xl font-bold">
                      {metaFeatures.feature_analysis.categorical_columns}
                    </p>
                  </div>
                  <div className="bg-red-50 p-4 rounded-lg">
                    <p className="text-sm text-muted-foreground">Constant Columns</p>
                    <p className="text-2xl font-bold">
                      {metaFeatures.feature_analysis.constant_columns}
                    </p>
                  </div>
                  <div className="bg-green-50 p-4 rounded-lg">
                    <p className="text-sm text-muted-foreground">Duplicate Rows</p>
                    <p className="text-2xl font-bold">
                      {metaFeatures.feature_analysis.duplicate_rows}
                    </p>
                  </div>
                </div>

                {/* Missing Data */}
                <div className="mt-6">
                  <h3 className="text-lg font-semibold mb-3">Missing Data</h3>
                  {metaFeatures.missing_data_analysis.columns_with_missing > 0 ? (
                    <div className="space-y-2">
                      {Object.entries(
                        metaFeatures.missing_data_analysis.missing_by_column as Record<
                          string,
                          any
                        >
                      ).map(([col, info]: [string, any]) => (
                        <div key={col} className="flex justify-between items-center">
                          <span className="text-sm">{col}</span>
                          <Badge variant="outline">
                            {info.missing_percentage}%
                          </Badge>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-sm text-green-600">✓ No missing values</p>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Preview Tab */}
          <TabsContent value="preview">
            {dataPreview && (
              <Card>
                <CardHeader>
                  <CardTitle>Data Preview</CardTitle>
                  <CardDescription>
                    First {dataPreview.rows_shown} rows of {dataPreview.total_rows} total
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="overflow-x-auto">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          {dataPreview.columns.map((col) => (
                            <TableHead key={col}>{col}</TableHead>
                          ))}
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {dataPreview.data.map((row, idx) => (
                          <TableRow key={idx}>
                            {dataPreview.columns.map((col) => (
                              <TableCell key={`${idx}-${col}`}>
                                {typeof row[col] === "object"
                                  ? JSON.stringify(row[col])
                                  : String(row[col] ?? "-")}
                              </TableCell>
                            ))}
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>
        </Tabs>
      )}
    </div>
  );
}
