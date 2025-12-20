"""
Tests for agent autonomy and configuration.

Tests AnalyticalRigor, WriteMode, and AgentConfig.
"""

import pytest
from pywats_agent.autonomy import (
    AnalyticalRigor,
    WriteMode,
    AgentConfig,
    PRESETS,
    get_preset,
)


# =============================================================================
# Test AnalyticalRigor Enum
# =============================================================================

class TestAnalyticalRigor:
    """Tests for AnalyticalRigor enum."""
    
    def test_all_levels_defined(self):
        """All rigor levels should be defined."""
        assert AnalyticalRigor.QUICK
        assert AnalyticalRigor.BALANCED
        assert AnalyticalRigor.THOROUGH
        assert AnalyticalRigor.EXHAUSTIVE
    
    def test_values_are_strings(self):
        """Rigor values should be lowercase strings."""
        assert AnalyticalRigor.QUICK.value == "quick"
        assert AnalyticalRigor.BALANCED.value == "balanced"
        assert AnalyticalRigor.THOROUGH.value == "thorough"
        assert AnalyticalRigor.EXHAUSTIVE.value == "exhaustive"
    
    def test_can_create_from_string(self):
        """Should be able to create from string value."""
        assert AnalyticalRigor("quick") == AnalyticalRigor.QUICK
        assert AnalyticalRigor("thorough") == AnalyticalRigor.THOROUGH


# =============================================================================
# Test WriteMode Enum
# =============================================================================

class TestWriteMode:
    """Tests for WriteMode enum."""
    
    def test_all_modes_defined(self):
        """All write modes should be defined."""
        assert WriteMode.BLOCKED
        assert WriteMode.CONFIRM_ALL
        assert WriteMode.CONFIRM_DESTRUCTIVE
    
    def test_values_are_strings(self):
        """Write mode values should be lowercase strings."""
        assert WriteMode.BLOCKED.value == "blocked"
        assert WriteMode.CONFIRM_ALL.value == "confirm_all"
        assert WriteMode.CONFIRM_DESTRUCTIVE.value == "confirm_destructive"


# =============================================================================
# Test AgentConfig
# =============================================================================

class TestAgentConfig:
    """Tests for AgentConfig."""
    
    def test_default_config(self):
        """Should have sensible defaults."""
        config = AgentConfig()
        assert config.rigor == AnalyticalRigor.BALANCED
        assert config.write_mode == WriteMode.BLOCKED
        assert config.max_api_calls_per_question == 10
        assert config.prefer_aggregated_data is True
    
    def test_custom_config(self):
        """Should accept custom values."""
        config = AgentConfig(
            rigor=AnalyticalRigor.EXHAUSTIVE,
            write_mode=WriteMode.CONFIRM_ALL,
            max_api_calls_per_question=20,
        )
        assert config.rigor == AnalyticalRigor.EXHAUSTIVE
        assert config.write_mode == WriteMode.CONFIRM_ALL
        assert config.max_api_calls_per_question == 20


class TestAgentConfigSystemPrompt:
    """Tests for system prompt generation."""
    
    def test_quick_rigor_prompt(self):
        """Quick rigor should generate appropriate instructions."""
        config = AgentConfig(rigor=AnalyticalRigor.QUICK)
        prompt = config.get_system_prompt()
        
        assert "QUICK" in prompt
        assert "fast" in prompt.lower() or "direct" in prompt.lower()
        assert "minimal" in prompt.lower()
    
    def test_balanced_rigor_prompt(self):
        """Balanced rigor should generate appropriate instructions."""
        config = AgentConfig(rigor=AnalyticalRigor.BALANCED)
        prompt = config.get_system_prompt()
        
        assert "BALANCED" in prompt
        assert "appropriate" in prompt.lower() or "reasonable" in prompt.lower()
    
    def test_thorough_rigor_prompt(self):
        """Thorough rigor should generate appropriate instructions."""
        config = AgentConfig(rigor=AnalyticalRigor.THOROUGH)
        prompt = config.get_system_prompt()
        
        assert "THOROUGH" in prompt
        assert "cross-validate" in prompt.lower()
        assert "confidence" in prompt.lower()
    
    def test_exhaustive_rigor_prompt(self):
        """Exhaustive rigor should generate appropriate instructions."""
        config = AgentConfig(rigor=AnalyticalRigor.EXHAUSTIVE)
        prompt = config.get_system_prompt()
        
        assert "EXHAUSTIVE" in prompt
        assert "no stone unturned" in prompt.lower()
        assert "outliers" in prompt.lower() or "edge cases" in prompt.lower()
    
    def test_blocked_write_mode_prompt(self):
        """Blocked write mode should explain restrictions."""
        config = AgentConfig(write_mode=WriteMode.BLOCKED)
        prompt = config.get_system_prompt()
        
        assert "BLOCKED" in prompt
        assert "cannot modify" in prompt.lower() or "cannot" in prompt.lower()
    
    def test_confirm_all_write_mode_prompt(self):
        """Confirm all should require confirmation for everything."""
        config = AgentConfig(write_mode=WriteMode.CONFIRM_ALL)
        prompt = config.get_system_prompt()
        
        assert "CONFIRM ALL" in prompt
        assert "confirmation" in prompt.lower()
        assert "never assume" in prompt.lower()
    
    def test_confirm_destructive_write_mode_prompt(self):
        """Confirm destructive should only confirm deletes."""
        config = AgentConfig(write_mode=WriteMode.CONFIRM_DESTRUCTIVE)
        prompt = config.get_system_prompt()
        
        assert "DESTRUCTIVE" in prompt
        assert "delete" in prompt.lower()
        assert "create" in prompt.lower()


class TestAgentConfigWritePermissions:
    """Tests for write permission checks."""
    
    def test_blocked_mode_blocks_all(self):
        """Blocked mode should block all writes."""
        config = AgentConfig(write_mode=WriteMode.BLOCKED)
        
        assert not config.allows_write("create")
        assert not config.allows_write("update")
        assert not config.allows_write("delete")
    
    def test_confirm_all_allows_with_confirmation(self):
        """Confirm all should allow writes but require confirmation."""
        config = AgentConfig(write_mode=WriteMode.CONFIRM_ALL)
        
        assert config.allows_write("create")
        assert config.allows_write("update")
        assert config.allows_write("delete")
        
        assert config.requires_confirmation("create")
        assert config.requires_confirmation("update")
        assert config.requires_confirmation("delete")
    
    def test_confirm_destructive_only_confirms_deletes(self):
        """Confirm destructive should only confirm destructive ops."""
        config = AgentConfig(write_mode=WriteMode.CONFIRM_DESTRUCTIVE)
        
        assert config.allows_write("create")
        assert config.allows_write("delete")
        
        assert not config.requires_confirmation("create")
        assert not config.requires_confirmation("update")
        assert config.requires_confirmation("delete")
        assert config.requires_confirmation("revoke")


class TestAgentConfigDefaultParameters:
    """Tests for default parameter generation."""
    
    def test_quick_uses_small_samples(self):
        """Quick rigor should use small sample sizes."""
        config = AgentConfig(rigor=AnalyticalRigor.QUICK)
        defaults = config.get_default_parameters()
        
        assert defaults["top_count"] <= 100
        assert defaults["max_results"] <= 100
    
    def test_exhaustive_uses_large_samples(self):
        """Exhaustive rigor should use large sample sizes."""
        config = AgentConfig(rigor=AnalyticalRigor.EXHAUSTIVE)
        defaults = config.get_default_parameters()
        
        assert defaults["top_count"] >= 1000
        assert defaults["max_results"] >= 1000
    
    def test_rigor_affects_sample_size(self):
        """Higher rigor should mean larger samples."""
        quick = AgentConfig(rigor=AnalyticalRigor.QUICK).get_default_parameters()
        balanced = AgentConfig(rigor=AnalyticalRigor.BALANCED).get_default_parameters()
        thorough = AgentConfig(rigor=AnalyticalRigor.THOROUGH).get_default_parameters()
        exhaustive = AgentConfig(rigor=AnalyticalRigor.EXHAUSTIVE).get_default_parameters()
        
        assert quick["top_count"] < balanced["top_count"]
        assert balanced["top_count"] < thorough["top_count"]
        assert thorough["top_count"] < exhaustive["top_count"]


# =============================================================================
# Test Presets
# =============================================================================

class TestPresets:
    """Tests for preset configurations."""
    
    def test_all_presets_defined(self):
        """All expected presets should be defined."""
        assert "viewer" in PRESETS
        assert "quick_check" in PRESETS
        assert "investigation" in PRESETS
        assert "audit" in PRESETS
        assert "admin" in PRESETS
        assert "power_user" in PRESETS
    
    def test_viewer_preset(self):
        """Viewer preset should be read-only."""
        config = get_preset("viewer")
        assert config.write_mode == WriteMode.BLOCKED
    
    def test_quick_check_preset(self):
        """Quick check should be fast and read-only."""
        config = get_preset("quick_check")
        assert config.rigor == AnalyticalRigor.QUICK
        assert config.write_mode == WriteMode.BLOCKED
        assert config.max_api_calls_per_question <= 5
    
    def test_investigation_preset(self):
        """Investigation should be thorough and read-only."""
        config = get_preset("investigation")
        assert config.rigor == AnalyticalRigor.THOROUGH
        assert config.write_mode == WriteMode.BLOCKED
    
    def test_audit_preset(self):
        """Audit should be exhaustive."""
        config = get_preset("audit")
        assert config.rigor == AnalyticalRigor.EXHAUSTIVE
        assert config.write_mode == WriteMode.BLOCKED
    
    def test_admin_preset(self):
        """Admin should allow writes with confirmation."""
        config = get_preset("admin")
        assert config.write_mode == WriteMode.CONFIRM_ALL
    
    def test_get_preset_unknown(self):
        """Unknown preset should raise KeyError."""
        with pytest.raises(KeyError):
            get_preset("unknown_preset")
    
    def test_get_preset_returns_copy(self):
        """get_preset should return a copy, not the original."""
        config1 = get_preset("viewer")
        config2 = get_preset("viewer")
        
        config1.rigor = AnalyticalRigor.EXHAUSTIVE
        assert config2.rigor == AnalyticalRigor.BALANCED


# =============================================================================
# Test AgentContext Integration
# =============================================================================

class TestAgentContextIntegration:
    """Tests for AgentContext with config."""
    
    def test_context_with_config(self):
        """Should accept config in context."""
        from pywats_agent import AgentContext
        
        config = AgentConfig(rigor=AnalyticalRigor.THOROUGH)
        context = AgentContext(
            current_product="TEST-001",
            config=config,
        )
        
        assert context.config is not None
        assert context.config.rigor == AnalyticalRigor.THOROUGH
    
    def test_context_from_dict_with_config(self):
        """Should parse config from dict."""
        from pywats_agent import AgentContext
        
        data = {
            "current_product": "TEST-001",
            "config": {
                "rigor": "thorough",
                "write_mode": "confirm_all",
            }
        }
        
        context = AgentContext.from_dict(data)
        
        assert context.config is not None
        assert context.config.rigor == AnalyticalRigor.THOROUGH
        assert context.config.write_mode == WriteMode.CONFIRM_ALL
    
    def test_system_prompt_includes_config(self):
        """System prompt should include config instructions."""
        from pywats_agent import AgentContext
        
        config = AgentConfig(rigor=AnalyticalRigor.EXHAUSTIVE)
        context = AgentContext(
            current_product="TEST-001",
            config=config,
        )
        
        prompt = context.to_system_prompt()
        
        assert "EXHAUSTIVE" in prompt
        assert "TEST-001" in prompt
    
    def test_context_without_config(self):
        """Should work without config."""
        from pywats_agent import AgentContext
        
        context = AgentContext(current_product="TEST-001")
        prompt = context.to_system_prompt()
        
        assert "TEST-001" in prompt
        # Should not have rigor instructions if no config
        assert "EXHAUSTIVE" not in prompt


# =============================================================================
# Test Imports
# =============================================================================

class TestImports:
    """Test module exports."""
    
    def test_import_from_pywats_agent(self):
        """Should be importable from main package."""
        from pywats_agent import (
            AnalyticalRigor,
            WriteMode,
            AgentConfig,
            PRESETS,
            get_preset,
        )
        
        assert AnalyticalRigor.QUICK
        assert WriteMode.BLOCKED
        assert AgentConfig
        assert "viewer" in PRESETS
        assert callable(get_preset)
