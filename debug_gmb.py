from googleapiclient.discovery import build
import pprint

try:
    # Check mybusinessaccountmanagement for accounts.list
    print("Building mybusinessaccountmanagement service...")
    service_account = build("mybusinessaccountmanagement", "v1")
    print("\nService (Account Management):", service_account)
    print("Dir:", dir(service_account))
    
    if hasattr(service_account, 'accounts'):
        print("\nservice.accounts:", service_account.accounts)
        accounts_resource = service_account.accounts()
        print("Dir(accounts_resource):", dir(accounts_resource))
        
        if hasattr(accounts_resource, 'list'):
            print("\naccounts_resource.list exists in Account Management!")
    
    print("\n--------------------------------\n")

    print("Building mybusinessbusinessinformation service...")
    # We don't need valid credentials just to inspect the service structure
    service = build("mybusinessbusinessinformation", "v1")
    
    print("\nService object:", service)
    print("\nDir(service):", dir(service))
    
    if hasattr(service, 'accounts'):
        print("\nservice.accounts:", service.accounts)
        accounts_resource = service.accounts()
        print("accounts_resource:", accounts_resource)
        print("Dir(accounts_resource):", dir(accounts_resource))
        
        if hasattr(accounts_resource, 'list'):
            print("\naccounts_resource.list exists!")
        else:
            print("\naccounts_resource.list DOES NOT exist!")
    else:
        print("\nservice.accounts DOES NOT exist!")

except Exception as e:
    print(f"\nError: {e}")
