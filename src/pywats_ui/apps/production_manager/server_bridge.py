"""Bridge between the Qt UI and the async MI service.

Runs async WATS API calls in a background thread and delivers
results back to the Qt event loop via signals.

Connection priority (highest to lowest):
1. Explicit configure(base_url, token)
2. Auto-discover from running pyWATS Client service (IPC)
3. Environment variables (PYWATS_SERVER_URL, PYWATS_API_TOKEN)
"""
from __future__ import annotations

import asyncio
import logging
import os
import traceback
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QObject, QThread, Signal

logger = logging.getLogger(__name__)


class _Worker(QObject):
    """Executes a single async callable in its own event loop."""

    finished = Signal(object)  # result
    error = Signal(str)        # error message

    def __init__(self, coro_factory: Any) -> None:
        super().__init__()
        self._coro_factory = coro_factory

    def run(self) -> None:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(self._coro_factory())
            finally:
                loop.close()
            self.finished.emit(result)
        except Exception as exc:
            logger.error("Worker error: %s\n%s", exc, traceback.format_exc())
            self.error.emit(str(exc))


class ServerBridge(QObject):
    """Manages async WATS API calls from the Qt thread.

    Provides signals for UI updates when server data arrives.
    On construction, attempts auto-discovery from:
      1. Running pyWATS Client service (IPC)
      2. Environment variables
    Falls back to manual configure() if auto-discovery fails.
    """

    # Signals for definition operations
    definitions_loaded = Signal(list)       # List[dict]
    definition_loaded = Signal(dict)        # single definition detail
    definition_copied = Signal(dict)        # copied definition
    definition_updated = Signal(dict)       # updated definition
    xaml_loaded = Signal(dict)              # XAML response
    relations_loaded = Signal(list)         # List[dict]
    media_loaded = Signal(list)             # List[dict] — MI media/documents
    operation_complete = Signal(str)        # success message
    error_occurred = Signal(str)            # error message
    connected = Signal(str)                 # base_url on successful connection

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._base_url: Optional[str] = None
        self._token: Optional[str] = None
        self._threads: List[QThread] = []

    def shutdown(self) -> None:
        """Wait for all running background threads to finish.

        Uses a 3-second graceful timeout, then force-terminates
        any threads that haven't stopped.
        """
        for thread in list(self._threads):
            thread.quit()
            if not thread.wait(3000):  # 3 second timeout
                logger.warning(
                    "Thread did not stop gracefully, force terminating"
                )
                thread.terminate()
                thread.wait(1000)  # Brief wait after terminate
        self._threads.clear()

    def configure(self, base_url: str, token: str) -> None:
        """Set server connection details explicitly."""
        self._base_url = base_url.rstrip("/")
        self._token = token
        self.connected.emit(self._base_url)

    @property
    def is_configured(self) -> bool:
        return self._base_url is not None and self._token is not None

    @property
    def base_url(self) -> Optional[str]:
        return self._base_url

    def auto_connect(self) -> bool:
        """Try to auto-discover credentials from installed pyWATS.

        Checks (in order):
        1. Running pyWATS Client service via IPC
        2. Environment variables PYWATS_SERVER_URL / PYWATS_API_TOKEN

        Returns True if credentials were found and configured.
        """
        # 1. Try IPC discovery from running service
        try:
            from pywats.pywats import pyWATS
            creds = pyWATS._discover_credentials("default")
            if creds and creds.get("base_url") and creds.get("token"):
                self.configure(creds["base_url"], creds["token"])
                logger.info("Auto-connected via service IPC: %s", self._base_url)
                return True
        except Exception as exc:
            logger.debug("IPC discovery failed: %s", exc)

        # 2. Try environment variables
        env_url = os.environ.get("PYWATS_SERVER_URL", "")
        env_token = os.environ.get("PYWATS_API_TOKEN", "")
        if env_url and env_token:
            self.configure(env_url, env_token)
            logger.info("Auto-connected via environment: %s", self._base_url)
            return True

        # 3. Try loading from config file
        try:
            from pywats_client.core.config import ClientConfig
            config = ClientConfig.load_for_instance("default")
            addr, tok = config.get_runtime_credentials()
            if addr and tok:
                self.configure(addr, tok)
                logger.info("Auto-connected via config file: %s", self._base_url)
                return True
        except Exception as exc:
            logger.debug("Config file discovery failed: %s", exc)

        logger.info("Auto-connect failed — manual configuration required")
        return False

    # ----------------------------------------------------------------
    # Public API — each launches a background thread
    # ----------------------------------------------------------------

    def load_definitions(self, is_global: bool = False) -> None:
        """Fetch all definitions from the server."""
        self._run_async(
            lambda: self._fetch_definitions(is_global),
            self.definitions_loaded,
        )

    def load_definition(self, definition_id: str) -> None:
        """Fetch a single definition's detail."""
        self._run_async(
            lambda: self._fetch_definition(definition_id),
            self.definition_loaded,
        )

    def load_xaml(self, definition_id: str) -> None:
        """Fetch XAML content for a definition."""
        self._run_async(
            lambda: self._fetch_xaml(definition_id),
            self.xaml_loaded,
        )

    def load_relations(self, definition_id: str) -> None:
        """Fetch relations for a definition."""
        self._run_async(
            lambda: self._fetch_relations(definition_id),
            self.relations_loaded,
        )

    def save_xaml(self, definition_id: str, xaml: str) -> None:
        """Save XAML content for a definition."""
        self._run_async(
            lambda: self._push_xaml(definition_id, xaml),
            self.operation_complete,
        )

    def copy_definition(self, definition_id: str) -> None:
        """Copy a definition on the server."""
        self._run_async(
            lambda: self._fetch_copy(definition_id),
            self.definition_copied,
        )

    def update_definition_status(self, definition_id: str, new_status: int,
                                    full_definition: Optional[dict] = None) -> None:
        """Change the status of a definition (Draft/Pending/Released/Revoked)."""
        self._run_async(
            lambda: self._push_status(definition_id, new_status, full_definition),
            self.definition_updated,
        )

    def create_relation(self, definition_id: str, entity_schema: str,
                        entity_key: str, entity_value: str) -> None:
        """Create a new relation for a definition."""
        self._run_async(
            lambda: self._push_new_relation(
                definition_id, entity_schema, entity_key, entity_value),
            self.operation_complete,
        )

    def delete_relation(self, relation_payload: dict) -> None:
        """Delete a relation."""
        self._run_async(
            lambda: self._push_delete_relation(relation_payload),
            self.operation_complete,
        )

    # ----------------------------------------------------------------
    # Report submission
    # ----------------------------------------------------------------

    def submit_report(self, report: Any) -> None:
        """Submit a UUT report to the WATS server."""
        self._run_async(
            lambda: self._push_report(report),
            self.operation_complete,
        )

    # ----------------------------------------------------------------
    # Media / document operations (Blob/mi endpoints)
    # ----------------------------------------------------------------

    def load_media(self, definition_id: str) -> None:
        """Fetch media/documents for a definition."""
        self._run_async(
            lambda: self._fetch_media(definition_id),
            self.media_loaded,
        )

    def upload_media(self, definition_id: str, file_path: str) -> None:
        """Upload a media file (PDF) for a definition."""
        self._run_async(
            lambda: self._push_media(definition_id, file_path),
            self.operation_complete,
        )

    def delete_media(self, definition_id: str, media_info: dict) -> None:
        """Delete a media attachment."""
        self._run_async(
            lambda: self._push_delete_media(definition_id, media_info),
            self.operation_complete,
        )

    def download_media(self, definition_id: str, media_info: dict,
                       save_path: str) -> None:
        """Download a media file to a local path."""
        self._run_async(
            lambda: self._fetch_download_media(definition_id, media_info, save_path),
            self.operation_complete,
        )

    # ----------------------------------------------------------------
    # Async implementations
    # ----------------------------------------------------------------

    async def _fetch_definitions(self, is_global: bool) -> list:
        svc = self._create_service()
        defs = await svc.list_definitions(is_global=is_global)
        return [d.model_dump(by_alias=True) for d in defs]

    async def _fetch_definition(self, definition_id: str) -> dict:
        svc = self._create_service()
        defn = await svc.get_definition(definition_id)
        if defn is None:
            return {}
        return defn.model_dump(by_alias=True)

    async def _fetch_xaml(self, definition_id: str) -> dict:
        svc = self._create_service()
        return await svc.get_xaml(definition_id)

    async def _fetch_relations(self, definition_id: str) -> list:
        svc = self._create_service()
        rels = await svc.list_relations(definition_id)
        return [r.model_dump(by_alias=True) for r in rels]

    async def _push_xaml(self, definition_id: str, xaml: str) -> str:
        svc = self._create_service()
        payload = {
            "TestSequenceDefinitionId": definition_id,
            "Definition": xaml,
        }
        await svc.put_xaml(payload)
        return f"XAML saved for {definition_id}"

    async def _fetch_copy(self, definition_id: str) -> dict:
        svc = self._create_service()
        copy = await svc.copy_definition(definition_id)
        if copy is None:
            return {}
        return copy.model_dump(by_alias=True)

    async def _push_status(self, definition_id: str, new_status: int,
                            full_definition: Optional[dict] = None) -> dict:
        svc = self._create_service()
        # The PUT endpoint needs the full definition object, not just id+Status.
        # Merge the new status into the current definition if available.
        if full_definition:
            result = await svc.update_definition(
                definition_id,
                **{k: v for k, v in full_definition.items()
                   if k != "TestSequenceDefinitionId"},
                Status=new_status,
            )
        else:
            result = await svc.update_definition(definition_id, Status=new_status)
        if result is None:
            return {}
        return result.model_dump(by_alias=True)

    async def _push_new_relation(self, definition_id: str, entity_schema: str,
                                 entity_key: str, entity_value: str) -> str:
        svc = self._create_service()
        await svc.create_relation(
            definition_id=definition_id,
            entity_schema=entity_schema,
            entity_name=entity_key,
            entity_key=entity_key,
            entity_value=entity_value,
        )
        return f"Relation created for {definition_id}"

    async def _push_delete_relation(self, relation_payload: dict) -> str:
        svc = self._create_service()
        await svc.delete_relation(relation_payload)
        return "Relation deleted"

    async def _fetch_media(self, definition_id: str) -> list:
        """Fetch MI media list via GET /api/internal/Blob/mi."""
        import httpx
        url = f"{self._base_url}/api/internal/Blob/mi"
        params = {"definitionId": definition_id}
        headers = {
            "Authorization": f"Basic {self._token}",
            "Referer": self._base_url or "",
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, headers=headers)
            if resp.status_code == 200:
                return resp.json()
            logger.error("Fetch media failed: %s", resp.status_code)
            return []

    async def _push_media(self, definition_id: str, file_path: str) -> str:
        """Upload MI media via POST /api/internal/Blob/mi."""
        import httpx
        url = f"{self._base_url}/api/internal/Blob/mi"
        params = {"definitionId": definition_id}
        headers = {
            "Authorization": f"Basic {self._token}",
            "Referer": self._base_url or "",
        }
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            files = {"file": (filename, f, "application/pdf")}
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, params=params, headers=headers,
                                        files=files)
                if resp.status_code in (200, 201, 204):
                    return f"Media uploaded: {filename}"
                raise RuntimeError(f"Upload failed ({resp.status_code}): {resp.text}")

    async def _push_delete_media(self, definition_id: str,
                                 media_info: dict) -> str:
        """Delete MI media via DELETE /api/internal/Blob/mi."""
        import httpx
        url = f"{self._base_url}/api/internal/Blob/mi"
        media_id = media_info.get("Id", media_info.get("BlobId", ""))
        params = {"definitionId": definition_id, "mediaId": media_id}
        headers = {
            "Authorization": f"Basic {self._token}",
            "Referer": self._base_url or "",
        }
        async with httpx.AsyncClient() as client:
            resp = await client.delete(url, params=params, headers=headers)
            if resp.status_code in (200, 204):
                return "Media deleted"
            raise RuntimeError(f"Delete failed ({resp.status_code}): {resp.text}")

    async def _fetch_download_media(self, definition_id: str,
                                    media_info: dict, save_path: str) -> str:
        """Download MI media file to local path."""
        import httpx
        url = f"{self._base_url}/api/internal/Blob/mi"
        media_id = media_info.get("Id", media_info.get("BlobId", ""))
        params = {"definitionId": definition_id, "mediaId": media_id,
                  "download": "true"}
        headers = {
            "Authorization": f"Basic {self._token}",
            "Referer": self._base_url or "",
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, headers=headers)
            if resp.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(resp.content)
                return f"Media downloaded to {save_path}"
            raise RuntimeError(f"Download failed ({resp.status_code}): {resp.text}")

    async def _push_report(self, report: Any) -> str:
        """Submit a UUT report via the report service."""
        import json as _json
        from pywats.core.async_client import AsyncHttpClient
        from pywats.domains.report import AsyncReportRepository, AsyncReportService

        # Debug: dump serialized JSON
        if hasattr(report, 'model_dump'):
            data = report.model_dump(mode="json", by_alias=True, exclude_none=True)
            logger.info("Report JSON:\n%s", _json.dumps(data, indent=2, default=str))

        http_client = AsyncHttpClient(
            base_url=self._base_url or "",
            token=self._token or "",
        )
        repo = AsyncReportRepository(http_client=http_client)
        svc = AsyncReportService(repo)
        report_id = await svc.submit_report(report)
        if report_id:
            return f"Report submitted: {report_id}"
        return "Report submitted (no ID returned)"

    def _create_service(self) -> Any:
        """Create a fresh async MI service instance."""
        from pywats.core.async_client import AsyncHttpClient
        from pywats.domains.manual_inspection import (
            AsyncManualInspectionRepository,
            AsyncManualInspectionService,
        )

        http_client = AsyncHttpClient(
            base_url=self._base_url or "",
            token=self._token or "",
        )
        repo = AsyncManualInspectionRepository(
            http_client=http_client,
            base_url=self._base_url,
        )
        return AsyncManualInspectionService(repo)

    # ----------------------------------------------------------------
    # Thread management
    # ----------------------------------------------------------------

    def _run_async(self, coro_factory: Any, success_signal: Signal) -> None:
        """Run an async callable in a background thread."""
        if not self.is_configured:
            self.error_occurred.emit("Server not configured")
            return

        thread = QThread()
        worker = _Worker(coro_factory)
        worker.moveToThread(thread)

        thread.started.connect(worker.run)
        worker.finished.connect(lambda result: success_signal.emit(result))
        worker.error.connect(self.error_occurred.emit)

        # Cleanup — must use thread.finished to avoid "wait on itself"
        def cleanup() -> None:
            if thread in self._threads:
                self._threads.remove(thread)
            worker.deleteLater()
            thread.deleteLater()

        # When worker done → quit the thread's event loop
        worker.finished.connect(thread.quit)
        worker.error.connect(thread.quit)

        # When thread actually stops → safe to clean up
        thread.finished.connect(cleanup)

        self._threads.append(thread)
        thread.start()
