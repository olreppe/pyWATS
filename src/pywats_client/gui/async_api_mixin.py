"""
Async API Mixin - Helper for GUI pages to use AsyncWATS

Provides a clean abstraction for pages to work with either sync or async API,
with automatic detection and proper async handling via AsyncTaskRunner.

Usage:
    class MyPage(BasePage, AsyncAPIMixin):
        def __init__(self, config, parent=None):
            super().__init__(config, parent)
            
        def _on_refresh(self):
            # This will automatically use async if available
            self.run_api_call(
                lambda api: api.asset.get_assets(),
                on_success=self._on_assets_loaded,
                on_error=self._on_error,
                task_name="Loading assets..."
            )
        
        async def _load_assets_async(self):
            # Or explicitly use async
            api = await self.get_async_api()
            return await api.asset.get_assets()
"""

from __future__ import annotations

import asyncio
import logging
from typing import (
    Any, Awaitable, Callable, Optional, TypeVar, Union, TYPE_CHECKING
)

if TYPE_CHECKING:
    from pywats import pyWATS, AsyncWATS
    from ..pages.base import BasePage

logger = logging.getLogger(__name__)

T = TypeVar('T')


class AsyncAPIMixin:
    """
    Mixin that provides async API support for GUI pages.
    
    Features:
    - Auto-detect sync vs async API
    - Unified interface for API calls
    - Automatic async-to-sync bridging via AsyncTaskRunner
    - Error handling with loading states
    
    This mixin should be used with BasePage and assumes:
    - self._facade exists (or will be set)
    - self.run_async() is available from BasePage
    - self.handle_error() is available from ErrorHandlingMixin
    
    Raises TypeError if required methods are not available.
    """
    
    # Type hints for the mixing context
    _facade: Any
    run_async: Callable
    handle_error: Callable
    set_loading: Callable
    
    def _validate_mixin_dependencies(self) -> None:
        """
        Validate that required methods exist.
        
        Raises:
            TypeError: If required methods are missing
        """
        missing = []
        if not hasattr(self, 'run_async') or not callable(getattr(self, 'run_async', None)):
            missing.append('run_async')
        if not hasattr(self, 'handle_error') or not callable(getattr(self, 'handle_error', None)):
            missing.append('handle_error')
        
        if missing:
            raise TypeError(
                f"{self.__class__.__name__} must inherit from BasePage to use AsyncAPIMixin. "
                f"Missing: {', '.join(missing)}"
            )
    
    @property
    def has_api(self) -> bool:
        """Check if API is available"""
        return bool(getattr(self, '_facade', None) and self._facade.has_api)
    
    @property
    def has_async_api(self) -> bool:
        """Check if async API is available"""
        if not self._facade:
            return False
        # Check if facade provides async API
        return hasattr(self._facade, 'async_api') and self._facade.async_api is not None
    
    def get_sync_api(self) -> Optional['pyWATS']:
        """
        Get sync API client (pyWATS).
        
        Returns:
            pyWATS instance or None
        """
        if self._facade and self._facade.has_api:
            return self._facade.api
        return None
    
    def get_async_api_sync(self) -> Optional['AsyncWATS']:
        """
        Get async API client (AsyncWATS) - sync access.
        
        Returns:
            AsyncWATS instance or None
        """
        if self._facade and hasattr(self._facade, 'async_api'):
            return self._facade.async_api
        return None
    
    async def get_async_api(self) -> 'AsyncWATS':
        """
        Get async API client (AsyncWATS) - for use in async context.
        
        Raises:
            RuntimeError: If async API not available
        """
        api = self.get_async_api_sync()
        if api is None:
            raise RuntimeError("Async API not available. Ensure service is connected.")
        return api
    
    def run_api_call(
        self,
        api_call: Union[Callable[['pyWATS'], T], Callable[['AsyncWATS'], Awaitable[T]]],
        on_success: Optional[Callable[[T], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
        task_name: str = "Loading...",
        show_loading: bool = True
    ) -> Optional[str]:
        """
        Run an API call with automatic sync/async handling.
        
        This is the preferred way to make API calls from GUI pages.
        It will:
        1. Use async API if available (non-blocking)
        2. Fall back to sync API in thread if async not available
        3. Show loading indicator
        4. Handle errors gracefully
        
        Args:
            api_call: Function that takes API client and returns result.
                     Can be sync (for pyWATS) or async (for AsyncWATS)
            on_success: Callback with result on success
            on_error: Callback with exception on error
            task_name: Name shown in loading indicator
            show_loading: Whether to show loading indicator
        
        Returns:
            Task ID (can be used to cancel) or None if sync
        
        Example:
            # Simple get call
            self.run_api_call(
                lambda api: api.asset.get_assets(),
                on_success=self._on_assets_loaded
            )
            
            # Async version (if you know it's async)
            self.run_api_call(
                lambda api: api.asset.get_assets(),  # Works for both
                on_success=self._on_assets_loaded
            )
        """
        if not self.has_api:
            if on_error:
                on_error(RuntimeError("Not connected to WATS server"))
            return None
        
        # Validate mixin dependencies on first use
        self._validate_mixin_dependencies()
        
        # Prefer async API
        if self.has_async_api:
            return self._run_async_api_call(
                api_call, on_success, on_error, task_name, show_loading
            )
        else:
            # Fall back to sync API in thread
            return self._run_sync_api_call(
                api_call, on_success, on_error, task_name, show_loading
            )
    
    def _run_async_api_call(
        self,
        api_call: Callable[['AsyncWATS'], Awaitable[T]],
        on_success: Optional[Callable[[T], None]],
        on_error: Optional[Callable[[Exception], None]],
        task_name: str,
        show_loading: bool
    ) -> str:
        """Run API call using async API"""
        api = self.get_async_api_sync()
        
        async def _execute():
            return await api_call(api)
        
        from ..core.async_runner import TaskResult
        
        def _on_complete(result: TaskResult):
            if result.is_success and on_success:
                on_success(result.result)
            elif result.is_error and on_error:
                on_error(result.error)
            elif result.is_error:
                self.handle_error(result.error, task_name)
        
        return self.run_async(
            _execute(),
            name=task_name,
            on_complete=_on_complete,
            show_loading=show_loading
        )
    
    def _run_sync_api_call(
        self,
        api_call: Callable[['pyWATS'], T],
        on_success: Optional[Callable[[T], None]],
        on_error: Optional[Callable[[Exception], None]],
        task_name: str,
        show_loading: bool
    ) -> str:
        """Run sync API call in thread"""
        api = self.get_sync_api()
        
        async def _execute():
            # Run sync call in thread pool
            return await asyncio.to_thread(api_call, api)
        
        from ..core.async_runner import TaskResult
        
        def _on_complete(result: TaskResult):
            if result.is_success and on_success:
                on_success(result.result)
            elif result.is_error and on_error:
                on_error(result.error)
            elif result.is_error:
                self.handle_error(result.error, task_name)
        
        return self.run_async(
            _execute(),
            name=task_name,
            on_complete=_on_complete,
            show_loading=show_loading
        )


class AsyncAPIPageMixin(AsyncAPIMixin):
    """
    Extended mixin with additional helper methods for common patterns.
    """
    
    def require_api(self, action: str = "perform this action") -> bool:
        """
        Check if API is available, show message if not.
        
        Args:
            action: Description of what user is trying to do
        
        Returns:
            True if API is available, False otherwise
        """
        if not self.has_api:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Not Connected",
                f"Please connect to WATS server to {action}."
            )
            return False
        return True
    
    def run_async_parallel(
        self,
        *calls: tuple[Callable, str],
        on_all_complete: Optional[Callable[[list], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None
    ) -> None:
        """
        Run multiple API calls in PARALLEL (all start at once).
        
        Use this when calls are independent and can run concurrently.
        Results are returned in the same order as the calls.
        
        Args:
            *calls: Tuples of (api_call, task_name)
            on_all_complete: Called when all complete with list of results
            on_error: Called if any fails
        
        Example:
            self.run_async_parallel(
                (lambda api: api.asset.get_types(), "Loading types..."),
                (lambda api: api.asset.get_assets(), "Loading assets..."),
                on_all_complete=self._on_data_loaded
            )
        """
        results = [None] * len(calls)  # Pre-allocate to preserve order
        completed = [0]  # Use list to allow mutation in closure
        
        def make_success_handler(idx, total):
            def handler(result):
                results[idx] = result
                completed[0] += 1
                if completed[0] == total and on_all_complete:
                    on_all_complete(results)
            return handler
        
        for idx, (call, name) in enumerate(calls):
            self.run_api_call(
                call,
                on_success=make_success_handler(idx, len(calls)),
                on_error=on_error,
                task_name=name
            )
    
    def run_async_sequence(
        self,
        *calls: tuple[Callable, str],
        on_all_complete: Optional[Callable[[list], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None
    ) -> None:
        """
        Run multiple API calls in SEQUENCE (one after another).
        
        Use this when later calls depend on earlier results,
        or when you need guaranteed ordering.
        
        Args:
            *calls: Tuples of (api_call, task_name)
            on_all_complete: Called when all complete with list of results
            on_error: Called if any fails (stops the sequence)
        
        Example:
            self.run_async_sequence(
                (lambda api: api.product.get_products(), "Loading products..."),
                (lambda api: api.product.get_bom(self._selected_product), "Loading BOM..."),
                on_all_complete=self._on_data_loaded
            )
        """
        if not calls:
            if on_all_complete:
                on_all_complete([])
            return
        
        results = []
        calls_list = list(calls)  # Convert to list for indexing
        
        def run_next(idx: int):
            if idx >= len(calls_list):
                # All done
                if on_all_complete:
                    on_all_complete(results)
                return
            
            call, name = calls_list[idx]
            
            def on_success(result):
                results.append(result)
                # Run next call
                run_next(idx + 1)
            
            def on_err(e):
                if on_error:
                    on_error(e)
                # Stop sequence on error (don't run remaining calls)
            
            self.run_api_call(
                call,
                on_success=on_success,
                on_error=on_err,
                task_name=name
            )
        
        # Start the sequence
        run_next(0)
