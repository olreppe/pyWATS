"""
MES Base Module

Provides base functionality for all MES modules including common REST API methods,
authentication handling, and shared utilities.
"""

from typing import Optional, Dict, Any, TypeVar, Type, Union
import httpx
from datetime import datetime
import json

from ..rest_api.client import WATSClient, get_default_client
from ..rest_api.exceptions import WATSAPIException, handle_response_error
from ..connection import WATSConnection

T = TypeVar('T')


class MESBase:
    """
    Base class for all MES modules providing common functionality.
    
    This class provides:
    - REST API access methods
    - Authentication handling
    - Connection management
    - Common utilities
    """
    
    def __init__(self, connection: Optional[Union[WATSConnection, WATSClient]] = None):
        """
        Initialize MES module.
        
        Args:
            connection: WATS connection or client instance
        """
        if isinstance(connection, WATSConnection):
            self._client = connection.client
        elif isinstance(connection, WATSClient):
            self._client = connection
        else:
            # Use default client
            self._client = get_default_client()
            
        self._admin_credentials = None
    
    @property
    def client(self) -> WATSClient:
        """Get the underlying WATS client."""
        return self._client
    
    def set_admin_credentials(self, username: str, password: str) -> None:
        """
        Set admin credentials for privileged operations.
        
        Args:
            username: Admin username
            password: Admin password
        """
        self._admin_credentials = (username, password)
    
    def is_connected(self) -> bool:
        """
        Check if connected to WATS MES Server.
        
        Returns:
            True if connected, False otherwise
        """
        try:
            # Try to make a simple API call to test connection
            response = self._client.get("/api/App/Version")
            return response.status_code == 200
        except Exception:
            return False
    
    def _rest_get_json(
        self, 
        query: str, 
        use_admin_credentials: bool = False,
        response_type: Optional[Type[T]] = None
    ) -> Union[Dict[str, Any], T]:
        """
        Perform GET request and return JSON response.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            query: API endpoint query
            use_admin_credentials: Use admin credentials if available
            response_type: Optional type to deserialize response to
            
        Returns:
            JSON response or deserialized object
            
        Raises:
            WATSAPIException: On API errors
        """
        headers = {}
        if use_admin_credentials and self._admin_credentials:
            headers['X-Admin-Auth'] = 'true'
        
        response = self._client.get(query, headers=headers)
        
        if response.status_code != 200:
            handle_response_error(response)
        
        json_response = response.json()
        
        if response_type:
            try:
                if hasattr(response_type, 'model_validate'):  # Pydantic v2 model
                    return response_type.model_validate(json_response)  # type: ignore
                elif hasattr(response_type, 'parse_obj'):  # Pydantic v1 model (legacy)
                    return response_type.parse_obj(json_response)  # type: ignore
                else:
                    return response_type(**json_response)
            except Exception:
                # Fallback to direct instantiation
                return response_type(**json_response)
        
        return json_response
    
    def _convert_to_json_serializable(self, obj: Any) -> Any:
        """
        Convert object to JSON serializable format.
        
        Args:
            obj: Object to convert
            
        Returns:
            JSON serializable representation
        """
        if obj is None:
            return None
            
        if hasattr(obj, 'model_dump'):  # Pydantic v2 model
            return obj.model_dump(exclude_none=True, by_alias=True)
        elif hasattr(obj, 'dict'):  # Pydantic v1 model
            return obj.dict(exclude_none=True, by_alias=True)
        elif isinstance(obj, (dict, list, str, int, float, bool)):
            return obj
        else:
            # Try to serialize as dict
            try:
                if hasattr(obj, 'model_validate'):  # Pydantic v2 model
                    return obj.model_dump(exclude_none=True, by_alias=True)  # type: ignore
                elif hasattr(obj, 'parse_obj'):  # Pydantic v1 model (legacy)
                    return obj.dict(exclude_none=True, by_alias=True)  # type: ignore
                else:
                    return obj.__dict__ if hasattr(obj, '__dict__') else str(obj)
            except Exception:
                return str(obj)
    
    def _rest_post_json(
        self,
        query: str,
        obj: Any = None,
        use_admin_credentials: bool = False,
        response_type: Optional[Type[T]] = None
    ) -> Union[Dict[str, Any], T]:
        """
        Perform POST request and return JSON response.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            query: API endpoint query
            obj: Object to serialize and send
            use_admin_credentials: Use admin credentials if available
            response_type: Optional type to deserialize response to
            
        Returns:
            JSON response or deserialized object
            
        Raises:
            WATSAPIException: On API errors
        """
        headers = {}
        if use_admin_credentials and self._admin_credentials:
            headers['X-Admin-Auth'] = 'true'
        
        json_data = None
        if obj is not None:
            json_data = self._convert_to_json_serializable(obj)
        
        response = self._client.post(query, json=json_data, headers=headers)
        
        if response.status_code != 200:
            handle_response_error(response)
        
        json_response = response.json()
        
        if response_type:
            if hasattr(response_type, 'model_validate'):  # Pydantic v2 model
                return response_type.model_validate(json_response)  # type: ignore
            elif hasattr(response_type, 'parse_obj'):  # Pydantic v1 model (legacy)
                return response_type.parse_obj(json_response)  # type: ignore
            else:
                return response_type(**json_response)
        
        return json_response
    
    def _rest_put_json(
        self,
        query: str,
        obj: Any = None,
        use_admin_credentials: bool = False,
        response_type: Optional[Type[T]] = None
    ) -> Union[Dict[str, Any], T]:
        """
        Perform PUT request and return JSON response.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            query: API endpoint query
            obj: Object to serialize and send
            use_admin_credentials: Use admin credentials if available
            response_type: Optional type to deserialize response to
            
        Returns:
            JSON response or deserialized object
            
        Raises:
            WATSAPIException: On API errors
        """
        headers = {}
        if use_admin_credentials and self._admin_credentials:
            headers['X-Admin-Auth'] = 'true'
        
        json_data = None
        if obj is not None:
            json_data = self._convert_to_json_serializable(obj)
        
        response = self._client.put(query, json=json_data, headers=headers)
        
        if response.status_code != 200:
            handle_response_error(response)
        
        json_response = response.json()
        
        if response_type:
            if hasattr(response_type, 'model_validate'):  # Pydantic v2 model
                return response_type.model_validate(json_response)  # type: ignore
            elif hasattr(response_type, 'parse_obj'):  # Pydantic v1 model (legacy)
                return response_type.parse_obj(json_response)  # type: ignore
            else:
                return response_type(**json_response)
        
        return json_response
    
    def _rest_delete_json(
        self,
        query: str,
        obj: Any = None,
        use_admin_credentials: bool = False,
        response_type: Optional[Type[T]] = None
    ) -> Union[Dict[str, Any], T, None]:
        """
        Perform DELETE request and return JSON response.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            query: API endpoint query
            obj: Optional object to serialize and send
            use_admin_credentials: Use admin credentials if available
            response_type: Optional type to deserialize response to
            
        Returns:
            JSON response, deserialized object, or None
            
        Raises:
            WATSAPIException: On API errors
        """
        headers = {}
        if use_admin_credentials and self._admin_credentials:
            headers['X-Admin-Auth'] = 'true'
        
        json_data = None
        if obj is not None:
            json_data = self._convert_to_json_serializable(obj)
        
        response = self._client.delete(query, json=json_data, headers=headers)
        
        if response.status_code == 204:
            return None
        
        if response.status_code != 200:
            handle_response_error(response)
        
        json_response = response.json()
        
        if response_type:
            if hasattr(response_type, 'model_validate'):  # Pydantic v2 model
                return response_type.model_validate(json_response)  # type: ignore
            elif hasattr(response_type, 'parse_obj'):  # Pydantic v1 model (legacy)
                return response_type.parse_obj(json_response)  # type: ignore
            else:
                return response_type(**json_response)
        
        return json_response
    
    def get_mes_server_settings(self) -> Dict[str, Any]:
        """
        Get MES server settings.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Returns:
            MES server settings
        """
        return self._rest_get_json("/api/internal/mes/GetMESServerSettings")
    
    def get_common_user_settings(self) -> Dict[str, Any]:
        """
        Get common user settings.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Returns:
            Common user settings
        """
        return self._rest_get_json("/api/internal/User/GetCommonUserSettings")
    
    def get_key_value(self, key: str) -> Any:
        """
        Get value by key from key-value store.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            key: Key to retrieve
            
        Returns:
            Value associated with key
        """
        data = {"key": key}
        response = self._rest_post_json("/api/internal/KeyValue/GetKeyValue", data)
        return response.get("value")
    
    def update_key_value(self, key: str, value: Any) -> bool:
        """
        Update key-value pair in store.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            key: Key to update
            value: New value
            
        Returns:
            True if successful, False otherwise
        """
        data = {"key": key, "value": value}
        response = self._rest_post_json("/api/internal/KeyValue/UpdateKeyValue", data)
        return response.get("success", False)
    
    def delete_key_value(self, key: str) -> bool:
        """
        Delete key-value pair from store.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            key: Key to delete
            
        Returns:
            True if successful, False otherwise
        """
        data = {"key": key}
        response = self._rest_post_json("/api/internal/KeyValue/DeleteKeyValue", data)
        return response.get("success", False)
    
    def translate(self, text: str, culture_code: Optional[str] = None) -> str:
        """
        Translate text using WATS translation system.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            text: Text to translate
            culture_code: Optional culture code (e.g., "en-US", "nb-NO")
            
        Returns:
            Translated text
        """
        data: Dict[str, Any] = {"text": text}
        if culture_code:
            data["cultureCode"] = culture_code
        
        response = self._rest_post_json("/api/internal/Translation/Translate", data)
        return response.get("translatedText", text)
    
    def translate_array(self, texts: list[str], culture_code: Optional[str] = None) -> list[str]:
        """
        Translate array of texts using WATS translation system.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            texts: List of texts to translate
            culture_code: Optional culture code (e.g., "en-US", "nb-NO")
            
        Returns:
            List of translated texts
        """
        data: Dict[str, Any] = {"texts": texts}
        if culture_code:
            data["cultureCode"] = culture_code
        
        response = self._rest_post_json("/api/internal/Translation/TranslateArray", data)
        return response.get("translatedTexts", texts)
    
    def get_processes(self) -> list[Dict[str, Any]]:
        """
        Get available processes.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Returns:
            List of available processes
        """
        response = self._rest_get_json("/api/internal/process/GetProcesses")
        return response if isinstance(response, list) else response.get("processes", [])
