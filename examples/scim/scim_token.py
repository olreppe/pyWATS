"""SCIM Token Generation Example

Demonstrates how to generate a SCIM provisioning token for Azure AD configuration.

The generated token is used to configure Azure Active Directory for automatic
user provisioning to WATS.

Usage:
    python -m examples.scim.scim_token
"""
from pywats import pyWATS


def main():
    # Initialize API client
    api = pyWATS(
        base_url="https://your-wats-server.com",
        token="your-api-token"
    )
    
    # Generate token with 90-day validity (default)
    print("Generating SCIM provisioning token...")
    token = api.scim.get_token(duration_days=90)
    
    if token:
        print("\n=== SCIM Token Generated ===")
        print(f"Token: {token.token[:50]}..." if token.token else "No token")
        print(f"Expires: {token.expires_utc}")
        print(f"Duration: {token.duration_days} days")
        
        print("\n=== Azure AD Configuration ===")
        print("1. Go to Azure AD Enterprise Applications")
        print("2. Select your WATS application")
        print("3. Go to Provisioning")
        print("4. Set Provisioning Mode to 'Automatic'")
        print(f"5. Set Tenant URL to: {api.base_url}/api/SCIM/v2")
        print("6. Copy the token above to 'Secret Token'")
        print("7. Test Connection and Save")
    else:
        print("Failed to generate token")


if __name__ == "__main__":
    main()
