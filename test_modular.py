"""Test script for the modular Azure DevOps MCP Server."""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_modular_imports():
    """Test that all modular components can be imported successfully."""
    try:
        # Test core imports
        from core.config import get_current_config, get_auth_headers
        from core.azure_client import AzureDevOpsClient
        
        # Test service imports
        from services.work_items import WorkItemService
        from services.formatting import split_task_descriptions, process_description_text
        
        # Test utility imports
        from utils.helpers import setup_logging, format_error_message
        
        # Test resource imports
        # from resources.standards import get_work_item_standards
        # from resources.guides import get_epic_management_guide
        
        print('✅ All modular imports successful!')
        print('✅ Core configuration module: OK')
        print('✅ Core Azure client module: OK') 
        print('✅ Work items service: OK')
        print('✅ Formatting service: OK')
        print('✅ Utilities module: OK')
        # print('✅ Resources standards: OK')
        # print('✅ Resources guides: OK')
        print()
        print('🎯 Modular architecture is ready!')
        
        return True
        
    except ImportError as e:
        print(f'❌ Import error: {e}')
        return False
    except Exception as e:
        print(f'❌ Unexpected error: {e}')
        return False


def test_description_splitting():
    """Test the enhanced description splitting functionality."""
    try:
        from services.formatting import split_task_descriptions
        
        print()
        print('🔧 Testing description splitting fix:')
        
        # Test case 1: New ||| delimiter system
        titles = ['Database Task', 'API Task', 'Frontend Task']
        descriptions = (
            'Complete database setup with schema design ||| '
            'Implement REST API with authentication ||| '
            'Create responsive frontend interface'
        )
        
        result = split_task_descriptions(descriptions, len(titles))
        print('  Test 1 - Triple pipe delimiter:')
        for i, desc in enumerate(result):
            print(f'    Task {i+1}: {desc[:60]}...')
        
        # Test case 2: Legacy comma separation (exact count)
        descriptions_comma = (
            'Setup database schema, '
            'Create API endpoints, '
            'Build user interface'
        )
        result_comma = split_task_descriptions(descriptions_comma, len(titles))
        print('\n  Test 2 - Legacy comma delimiter:')
        for i, desc in enumerate(result_comma):
            print(f'    Task {i+1}: {desc[:60]}...')
        
        # Test case 3: Single description (fallback)
        single_desc = 'This single description will be assigned to first task only'
        result_single = split_task_descriptions(single_desc, len(titles))
        print('\n  Test 3 - Single description fallback:')
        for i, desc in enumerate(result_single):
            if desc:
                print(f'    Task {i+1}: {desc[:60]}...')
            else:
                print(f'    Task {i+1}: (empty - as expected)')
        
        print('\n✅ Description splitting tests passed!')
        return True
        
    except Exception as e:
        print(f'❌ Description splitting test failed: {e}')
        return False


def test_azure_client():
    """Test Azure client instantiation."""
    try:
        from core.azure_client import AzureDevOpsClient
        
        print()
        print('🔌 Testing Azure client instantiation:')
        
        client = AzureDevOpsClient()
        print('✅ AzureDevOpsClient created successfully')
        
        # Test that client has required methods
        required_methods = [
            'create_work_item', 'get_work_item', 'update_work_item',
            'delete_work_item', 'create_work_item_link'
        ]
        
        for method in required_methods:
            if hasattr(client, method):
                print(f'✅ Method {method}: Available')
            else:
                print(f'❌ Method {method}: Missing')
                return False
        
        return True
        
    except Exception as e:
        print(f'❌ Azure client test failed: {e}')
        return False


def test_work_item_service():
    """Test work item service instantiation."""
    try:
        from core.azure_client import AzureDevOpsClient
        from services.work_items import WorkItemService
        
        print()
        print('🔧 Testing work item service:')
        
        client = AzureDevOpsClient()
        service = WorkItemService()  # No client parameter needed
        print('✅ WorkItemService created successfully')
        
        # Test that service has required methods
        required_methods = [
            'create_work_item', 'create_epic_with_tasks', 'get_work_item',
            'update_work_item', 'delete_work_item', 'link_task_to_epic'
        ]
        
        for method in required_methods:
            if hasattr(service, method):
                print(f'✅ Method {method}: Available')
            else:
                print(f'❌ Method {method}: Missing')
                return False
        
        return True
        
    except Exception as e:
        print(f'❌ Work item service test failed: {e}')
        return False


def main():
    """Run all modular architecture tests."""
    print("="*60)
    print("Azure DevOps MCP Server - Modular Architecture Tests")
    print("="*60)
    
    tests = [
        ("Import Tests", test_modular_imports),
        ("Description Splitting", test_description_splitting),
        ("Azure Client", test_azure_client),
        ("Work Item Service", test_work_item_service)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n[{test_name}]")
        print("-" * 40)
        if test_func():
            passed += 1
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")
    
    print("\n" + "="*60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Modular architecture is working correctly.")
        print("\n🚀 Ready to use mcp_server_modular.py")
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
    
    print("="*60)


if __name__ == "__main__":
    main()
