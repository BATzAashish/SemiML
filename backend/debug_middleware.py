#!/usr/bin/env python
"""Debug script to check FastAPI middleware configuration"""
import sys
sys.path.insert(0, '/d/Internship project/SemiML/backend')

try:
    from app.main import app
    print("App imported successfully")
    print(f"Number of user_middleware: {len(app.user_middleware)}")
    print(f"User middleware: {app.user_middleware}")
    print(f"Middleware stack: {app.middleware_stack}")
    
    # Try to check the middleware attribute
    if hasattr(app, 'middleware'):
        print(f"App.middleware: {app.middleware}")
    
    # Check Starlette's middleware
    if hasattr(app, 'user_middleware'):
        for i, m in enumerate(app.user_middleware):
            print(f"Middleware {i}: {m} (type: {type(m)}, len: {len(m) if hasattr(m, '__len__') else 'N/A'})")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
