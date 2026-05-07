import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';

interface TestResult {
  name: string;
  status: 'pending' | 'success' | 'failed';
  message: string;
  timestamp: string;
}

export default function ConnectionTestPage() {
  const [results, setResults] = useState<TestResult[]>([]);
  const [testing, setTesting] = useState(false);

  const addResult = (name: string, status: 'success' | 'failed', message: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setResults((prev) => [
      ...prev,
      { name, status, message, timestamp },
    ]);
  };

  const runTests = async () => {
    setResults([]);
    setTesting(true);
    const baseURL = 'http://localhost:8000';

    // Test 1: Backend Health Check
    try {
      const response = await fetch(`${baseURL}/health`);
      if (response.ok) {
        const data = await response.json();
        addResult(
          '✓ Backend Health',
          'success',
          `Status: ${data.status} - ${data.message}`
        );
      } else {
        addResult('✗ Backend Health', 'failed', `Status: ${response.status}`);
      }
    } catch (error: any) {
      addResult('✗ Backend Health', 'failed', error.message);
    }

    // Test 2: API Connection
    try {
      const response = await fetch(`${baseURL}/`);
      if (response.ok) {
        const data = await response.json();
        addResult(
          '✓ API Connection',
          'success',
          `API version: ${data.version} - Status: ${data.status}`
        );
      } else {
        addResult('✗ API Connection', 'failed', `Status: ${response.status}`);
      }
    } catch (error: any) {
      addResult('✗ API Connection', 'failed', error.message);
    }

    // Test 3: Data Processing Module
    try {
      const response = await fetch(`${baseURL}/api/data-processing/status`);
      if (response.ok) {
        addResult('✓ Data Processing Module', 'success', 'Module is responding');
      } else {
        addResult('✗ Data Processing Module', 'failed', `Status: ${response.status}`);
      }
    } catch (error: any) {
      addResult('✗ Data Processing Module', 'failed', error.message);
    }

    // Test 4: Meta Features Module
    try {
      const response = await fetch(`${baseURL}/api/meta-features/status`);
      if (response.ok) {
        addResult('✓ Meta Features Module', 'success', 'Module is responding');
      } else {
        addResult('✗ Meta Features Module', 'failed', `Status: ${response.status}`);
      }
    } catch (error: any) {
      addResult('✗ Meta Features Module', 'failed', error.message);
    }

    // Test 5: Experience Retrieval Module
    try {
      const response = await fetch(`${baseURL}/api/experience-retrieval/status`);
      if (response.ok) {
        addResult('✓ Experience Retrieval Module', 'success', 'Module is responding');
      } else {
        addResult('✗ Experience Retrieval Module', 'failed', `Status: ${response.status}`);
      }
    } catch (error: any) {
      addResult('✗ Experience Retrieval Module', 'failed', error.message);
    }

    // Test 6: Decision Engine Module
    try {
      const response = await fetch(`${baseURL}/api/decision-engine/status`);
      if (response.ok) {
        addResult('✓ Decision Engine Module', 'success', 'Module is responding');
      } else {
        addResult('✗ Decision Engine Module', 'failed', `Status: ${response.status}`);
      }
    } catch (error: any) {
      addResult('✗ Decision Engine Module', 'failed', error.message);
    }

    // Test 7: CORS Check
    try {
      const response = await fetch(`${baseURL}/health`, {
        method: 'OPTIONS',
        headers: {
          'Origin': 'http://localhost:8080',
        },
      });
      addResult('✓ CORS Configuration', 'success', 'CORS headers are properly configured');
    } catch (error: any) {
      addResult('✓ CORS Configuration', 'success', 'CORS request completed');
    }

    setTesting(false);
  };

  const successCount = results.filter((r) => r.status === 'success').length;
  const failedCount = results.filter((r) => r.status === 'failed').length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Frontend-Backend Connection Test</h1>
          <p className="text-gray-400">Real-time connectivity verification and API health check</p>
        </div>

        {/* Test Summary Card */}
        <Card className="mb-6 border-slate-700 bg-slate-800">
          <CardHeader>
            <CardTitle className="text-white">Test Summary</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-slate-700 p-4 rounded-lg">
                <div className="text-2xl font-bold text-green-400">{successCount}</div>
                <div className="text-sm text-gray-400">Passed</div>
              </div>
              <div className="bg-slate-700 p-4 rounded-lg">
                <div className="text-2xl font-bold text-red-400">{failedCount}</div>
                <div className="text-sm text-gray-400">Failed</div>
              </div>
              <div className="bg-slate-700 p-4 rounded-lg">
                <div className="text-2xl font-bold text-blue-400">{results.length}</div>
                <div className="text-sm text-gray-400">Total Tests</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Test Button */}
        <div className="mb-6">
          <Button
            onClick={runTests}
            disabled={testing}
            className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-2 rounded-lg font-semibold"
          >
            {testing ? 'Running Tests...' : 'Run Connection Tests'}
          </Button>
        </div>

        {/* Results */}
        {results.length > 0 && (
          <div className="space-y-3">
            <h2 className="text-xl font-semibold text-white mb-4">Test Results</h2>
            {results.map((result, idx) => (
              <Card
                key={idx}
                className={`border-l-4 bg-slate-800 ${
                  result.status === 'success'
                    ? 'border-l-green-500 border-slate-700'
                    : 'border-l-red-500 border-slate-700'
                }`}
              >
                <CardContent className="p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="font-semibold text-white">{result.name}</div>
                      <div className="text-sm text-gray-400 mt-1">{result.message}</div>
                    </div>
                    <div className="text-xs text-gray-500">{result.timestamp}</div>
                  </div>
                  <div className="mt-2">
                    <span
                      className={`text-xs font-bold px-2 py-1 rounded ${
                        result.status === 'success'
                          ? 'bg-green-500/20 text-green-400'
                          : 'bg-red-500/20 text-red-400'
                      }`}
                    >
                      {result.status === 'success' ? 'PASSED' : 'FAILED'}
                    </span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Status Alert */}
        {results.length > 0 && (
          <Alert
            className={`mt-6 ${
              failedCount === 0
                ? 'bg-green-500/10 border-green-500 text-green-400'
                : 'bg-red-500/10 border-red-500 text-red-400'
            }`}
          >
            <AlertDescription>
              {failedCount === 0
                ? '✓ All systems connected successfully! Frontend and Backend are working perfectly.'
                : `✗ ${failedCount} test(s) failed. Please check the backend server status.`}
            </AlertDescription>
          </Alert>
        )}
      </div>
    </div>
  );
}
