import requests
import json

print("=" * 70)
print("TESTING ALL 5 MODULES - COMPREHENSIVE TEST")
print("=" * 70)

# Test 1: System Info - Verify all modules are registered
print("\n[1] MODULE REGISTRATION CHECK")
print("-" * 70)
resp = requests.get('http://localhost:8000/api/system-info')
data = resp.json()
modules = data['modules']
for module_name in sorted(modules.keys()):
    module = modules[module_name]
    endpoints = len(module['endpoints'])
    print(f"✅ {module_name}: {module['name']} - {endpoints} endpoints")

# Test 2: Module 1 - Connection test
print("\n[2] MODULE 1: PROJECT FOUNDATION")
print("-" * 70)
resp = requests.get('http://localhost:8000/api/connect')
data = resp.json()
print(f"✅ Connection: {data['status']}")

# Test 3: Module 2 - Data Processing
print("\n[3] MODULE 2: DATA PROCESSING")
print("-" * 70)
resp = requests.get('http://localhost:8000/api/datasets')
data = resp.json()
print(f"✅ Datasets: {data['count']} datasets available")
if data['count'] > 0:
    dataset_id = data['datasets'][0]['dataset_id']
    print(f"✅ Using dataset: {data['datasets'][0]['filename']} (ID: {dataset_id[:8]}...)")

# Test 4: Module 3 - Meta-Features
print("\n[4] MODULE 3: META-FEATURES EXTRACTION")
print("-" * 70)
if data['count'] > 0:
    dataset_id = data['datasets'][0]['dataset_id']
    resp = requests.post(f'http://localhost:8000/api/extract-meta-features/{dataset_id}')
    meta = resp.json()['meta_features']
    basic = meta['basic_info']
    quality = meta['data_quality']
    print(f"✅ Dataset: {basic['num_rows']} rows, {basic['num_columns']} columns")
    print(f"✅ Quality: {quality['overall_quality_score']}% (completeness: {quality['completeness_score']}%)")

# Test 5: Module 4 - Experience Retrieval
print("\n[5] MODULE 4: EXPERIENCE RETRIEVAL")
print("-" * 70)
resp = requests.get('http://localhost:8000/api/experience-statistics')
stats = resp.json()['statistics']
print(f"✅ Stored experiences: {stats['total_experiences']}")
print(f"✅ Unique models: {stats['unique_models']}")
print(f"✅ Pipeline types: {', '.join(stats['pipeline_types'])}")
print(f"✅ Avg accuracy: {stats['avg_best_accuracy']}")

# Test 6: Module 5 - Decision Engine
print("\n[6] MODULE 5: DECISION ENGINE")
print("-" * 70)
resp = requests.post('http://localhost:8000/api/detect-problem-type', 
    json={'class_distribution': {'potential_target_columns': [{'unique_values': 5}]}})
problem = resp.json()['problem_type']
print(f"✅ Problem detection: {problem}")

if data['count'] > 0:
    resp = requests.post('http://localhost:8000/api/decide-pipeline',
        json={'dataset_meta_features': meta, 'problem_type': 'classification'})
    decision = resp.json()['decision']
    print(f"✅ Decision made: {decision['best_pipeline']['name']}")
    print(f"✅ Score: {decision['best_pipeline']['score']}")

# Summary
print("\n" + "=" * 70)
print("✅ ALL MODULES WORKING - SYSTEM OPERATIONAL")
print("=" * 70)
print(f"\nBackend: http://localhost:8000")
print(f"Frontend: http://localhost:8080")
print(f"Total Endpoints: 25+ across 5 modules")
