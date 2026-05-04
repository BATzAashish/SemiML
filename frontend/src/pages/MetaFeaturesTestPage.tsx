/**
 * Meta-Features Analysis Test Page
 * Location: frontend/src/pages/MetaFeaturesTestPage.tsx
 * 
 * Page for testing Module 3 functionality
 */

import MetaFeaturesAnalysis from "@/components/MetaFeaturesAnalysis";
import { Card } from "@/components/ui/card";

export default function MetaFeaturesTestPage() {
  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-4xl font-bold">Meta-Features Analysis</h1>
          <p className="text-muted-foreground mt-2">
            Extract and analyze statistical features from your datasets for intelligent pipeline selection
          </p>
        </div>

        {/* Instructions */}
        <Card className="bg-blue-50 border-blue-200 p-4">
          <div className="space-y-2">
            <h3 className="font-semibold text-blue-900">About Module 3: Meta-Features Extraction</h3>
            <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
              <li>Extracts 40+ statistical features from datasets</li>
              <li>Analyzes data quality and completeness</li>
              <li>Identifies feature types (numeric, categorical, datetime)</li>
              <li>Detects missing values and data patterns</li>
              <li>Provides recommendations for data preprocessing</li>
              <li>Determines model readiness</li>
              <li>Enables dataset comparison</li>
            </ul>
          </div>
        </Card>

        {/* Analysis Component */}
        <MetaFeaturesAnalysis />
      </div>
    </div>
  );
}
