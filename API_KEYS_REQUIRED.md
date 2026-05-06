"""
API Key Requirements Documentation
This file documents all API keys used in the SemiML project
"""

# ============================================================================
# REQUIRED API KEYS
# ============================================================================

API_KEYS_REQUIRED = {
    # OPTIONAL - For LLM-based reasoning and meta-learning
    "OPENAI_API_KEY": {
        "description": "OpenAI API key for GPT-4 and embeddings",
        "provider": "OpenAI (https://platform.openai.com/api-keys)",
        "usage": "LLM reasoning, embeddings for semantic search",
        "required": False,
        "models": ["gpt-4", "gpt-3.5-turbo", "text-embedding-3-small"],
        "fallback": "HuggingFace embeddings, rule-based reasoning"
    },
    
    "GOOGLE_API_KEY": {
        "description": "Google Generative AI API key for Gemini",
        "provider": "Google AI Studio (https://makersuite.google.com/app/apikey)",
        "usage": "LLM reasoning with Google Gemini Pro",
        "required": False,
        "models": ["gemini-pro"],
        "fallback": "OpenAI or rule-based reasoning"
    },
    
    "ANTHROPIC_API_KEY": {
        "description": "Anthropic API key for Claude",
        "provider": "Anthropic Console (https://console.anthropic.com/)",
        "usage": "LLM reasoning with Claude 3",
        "required": False,
        "models": ["claude-3-opus", "claude-3-sonnet"],
        "fallback": "OpenAI or Gemini or rule-based reasoning"
    },
}

# ============================================================================
# OPTIONAL API KEYS (For monitoring and production)
# ============================================================================

OPTIONAL_API_KEYS = {
    "LANGCHAIN_API_KEY": {
        "description": "LangChain API key for LangChain Hub",
        "usage": "Optional - for prompt versioning and management",
        "required": False,
    },
    
    "PROMETHEUS_METRICS": {
        "description": "Prometheus for metrics collection",
        "usage": "Optional - for advanced monitoring",
        "required": False,
    },
}

# ============================================================================
# CONFIGURATION
# ============================================================================

ENVIRONMENT_SETUP = """
# .env file example

# LLM Integration (Optional - system works without these)
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIzaSyD...
ANTHROPIC_API_KEY=sk-ant-...

# Database
DATABASE_URL=sqlite:///./semiml.db

# Optional
LANGCHAIN_API_KEY=...
ENVIRONMENT=development
"""

# ============================================================================
# SYSTEM BEHAVIOR BY API KEY CONFIGURATION
# ============================================================================

BEHAVIOR_MATRIX = {
    "all_keys_missing": {
        "description": "System uses only rule-based and experience-based reasoning",
        "llm_reasoning": "DISABLED",
        "embeddings": "HuggingFace (local, no API needed)",
        "meta_decision": "Rule + Experience only",
        "status": "OPERATIONAL (reduced features)"
    },
    
    "openai_only": {
        "description": "System uses OpenAI for LLM and embeddings",
        "llm_reasoning": "ENABLED (GPT-4/3.5)",
        "embeddings": "OpenAI text-embedding-3",
        "meta_decision": "Rule + Experience + LLM (OpenAI)",
        "status": "FULL OPERATIONAL"
    },
    
    "google_only": {
        "description": "System uses Google Gemini for LLM",
        "llm_reasoning": "ENABLED (Gemini Pro)",
        "embeddings": "HuggingFace (local)",
        "meta_decision": "Rule + Experience + LLM (Gemini)",
        "status": "OPERATIONAL"
    },
    
    "anthropic_only": {
        "description": "System uses Anthropic Claude for LLM",
        "llm_reasoning": "ENABLED (Claude 3)",
        "embeddings": "HuggingFace (local)",
        "meta_decision": "Rule + Experience + LLM (Claude)",
        "status": "OPERATIONAL"
    },
    
    "multiple_keys": {
        "description": "System uses priority: OpenAI > Google > Anthropic",
        "llm_reasoning": "ENABLED (with fallback)",
        "embeddings": "OpenAI (if available, else HuggingFace)",
        "meta_decision": "Rule + Experience + LLM (best available)",
        "status": "OPTIMAL (with fallback support)"
    }
}

# ============================================================================
# SETUP INSTRUCTIONS
# ============================================================================

SETUP_INSTRUCTIONS = """
### Option 1: No LLM Integration (Default - Works Out of Box)
No setup needed! System operates with:
- Rule-based decision engine
- Experience-based recommendations
- HuggingFace embeddings (local, offline)
- Local outlier detection and statistical analysis

### Option 2: With OpenAI (Recommended)
1. Get API key: https://platform.openai.com/api-keys
2. Create .env file in project root:
   OPENAI_API_KEY=sk-your-key-here
3. Restart backend

### Option 3: With Google Gemini
1. Get API key: https://makersuite.google.com/app/apikey
2. Create .env file:
   GOOGLE_API_KEY=AIzaSyD-your-key-here
3. Restart backend

### Option 4: With Anthropic Claude
1. Get API key: https://console.anthropic.com/
2. Create .env file:
   ANTHROPIC_API_KEY=sk-ant-your-key-here
3. Restart backend

### Check LLM Status
GET /api/llm-status
Response shows which provider is active and others available
"""

if __name__ == "__main__":
    print("SemiML API Key Requirements")
    print("=" * 60)
    print("\nOptional API Keys (System works without them):")
    for key, info in API_KEYS_REQUIRED.items():
        print(f"\n{key}:")
        print(f"  Provider: {info['provider']}")
        print(f"  Usage: {info['usage']}")
        print(f"  Fallback: {info['fallback']}")
    
    print("\n" + "=" * 60)
    print("\nBehavior by Configuration:")
    for config, behavior in BEHAVIOR_MATRIX.items():
        print(f"\n{config}:")
        print(f"  Status: {behavior['status']}")
        print(f"  LLM Reasoning: {behavior['llm_reasoning']}")
