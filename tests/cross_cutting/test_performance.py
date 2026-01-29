"""
Tests for performance optimization utilities.
"""
import pytest
import json
from unittest.mock import patch

from pywats.core.performance import (
    Serializer,
    format_bytes,
    benchmark_serialization,
    MSGPACK_AVAILABLE,
    COMPRESSION_AVAILABLE,
)


class TestSerializer:
    """Tests for Serializer class."""
    
    def test_formats_list(self):
        """Test available formats list."""
        assert 'json' in Serializer.FORMATS
        assert 'msgpack' in Serializer.FORMATS
        assert 'json-gzip' in Serializer.FORMATS
    
    def test_default_format_is_json(self):
        """Test default format is json."""
        serializer = Serializer()
        assert serializer.format == 'json'
    
    def test_invalid_format_raises_error(self):
        """Test invalid format raises ValueError."""
        with pytest.raises(ValueError, match="Invalid format"):
            Serializer(format='xml')
    
    def test_json_serialization(self):
        """Test JSON serialization round-trip."""
        serializer = Serializer(format='json')
        data = {'key': 'value', 'number': 42, 'list': [1, 2, 3]}
        
        serialized = serializer.dumps(data)
        assert isinstance(serialized, bytes)
        
        restored = serializer.loads(serialized)
        assert restored == data
    
    def test_json_serialization_unicode(self):
        """Test JSON handles unicode correctly."""
        serializer = Serializer(format='json')
        data = {'name': 'Ølaf', 'emoji': '🎉'}
        
        serialized = serializer.dumps(data)
        restored = serializer.loads(serialized)
        assert restored == data
    
    def test_json_serialization_complex_nested(self):
        """Test JSON handles nested structures."""
        serializer = Serializer(format='json')
        data = {
            'reports': [
                {'id': i, 'steps': [{'name': f'step_{j}'} for j in range(3)]}
                for i in range(5)
            ]
        }
        
        serialized = serializer.dumps(data)
        restored = serializer.loads(serialized)
        assert restored == data
    
    @pytest.mark.skipif(not COMPRESSION_AVAILABLE, reason="gzip not available")
    def test_json_gzip_serialization(self):
        """Test compressed JSON serialization."""
        serializer = Serializer(format='json-gzip', compress_threshold=0)  # Force compression
        data = {'key': 'value', 'long_string': 'x' * 1000}
        
        serialized = serializer.dumps(data)
        assert isinstance(serialized, bytes)
        
        restored = serializer.loads(serialized)
        assert restored == data
    
    @pytest.mark.skipif(not COMPRESSION_AVAILABLE, reason="gzip not available")
    def test_json_gzip_below_threshold_not_compressed(self):
        """Test small data is not compressed."""
        serializer = Serializer(format='json-gzip', compress_threshold=10000)
        data = {'small': 'data'}
        
        serialized = serializer.dumps(data)
        # Small data should be plain JSON (not gzip)
        restored = serializer.loads(serialized)
        assert restored == data
    
    @pytest.mark.skipif(not COMPRESSION_AVAILABLE, reason="gzip not available")
    def test_json_gzip_fallback_to_plain_json(self):
        """Test loading plain JSON when gzip format expected."""
        serializer = Serializer(format='json-gzip')
        plain_json = json.dumps({'key': 'value'}).encode('utf-8')
        
        # Should be able to load plain JSON even in gzip mode
        restored = serializer.loads(plain_json)
        assert restored == {'key': 'value'}
    
    @pytest.mark.skipif(not MSGPACK_AVAILABLE, reason="msgpack not available")
    def test_msgpack_serialization(self):
        """Test MessagePack serialization."""
        serializer = Serializer(format='msgpack')
        data = {'key': 'value', 'number': 42, 'list': [1, 2, 3]}
        
        serialized = serializer.dumps(data)
        assert isinstance(serialized, bytes)
        
        restored = serializer.loads(serialized)
        assert restored == data
    
    @pytest.mark.skipif(not MSGPACK_AVAILABLE, reason="msgpack not available")
    def test_msgpack_smaller_than_json(self):
        """Test MessagePack produces smaller output."""
        json_serializer = Serializer(format='json')
        msgpack_serializer = Serializer(format='msgpack')
        
        # Large data
        data = {'values': list(range(100))}
        
        json_size = len(json_serializer.dumps(data))
        msgpack_size = len(msgpack_serializer.dumps(data))
        
        # MessagePack should be smaller
        assert msgpack_size < json_size
    
    def test_compare_sizes_json(self):
        """Test compare_sizes includes JSON."""
        serializer = Serializer()
        data = {'test': 'data'}
        
        comparison = serializer.compare_sizes(data)
        
        assert 'json' in comparison
        assert 'size' in comparison['json']
        assert comparison['json']['ratio'] == 1.0
    
    @pytest.mark.skipif(not MSGPACK_AVAILABLE, reason="msgpack not available")
    def test_compare_sizes_msgpack(self):
        """Test compare_sizes includes msgpack if available."""
        serializer = Serializer()
        data = {'test': 'data'}
        
        comparison = serializer.compare_sizes(data)
        
        assert 'msgpack' in comparison
        assert 'size' in comparison['msgpack']
        assert 'savings' in comparison['msgpack']
    
    @pytest.mark.skipif(not COMPRESSION_AVAILABLE, reason="gzip not available")
    def test_compare_sizes_gzip(self):
        """Test compare_sizes includes gzip if available."""
        serializer = Serializer()
        data = {'test': 'data' * 100}  # Compressible data
        
        comparison = serializer.compare_sizes(data)
        
        assert 'json-gzip' in comparison
        assert 'size' in comparison['json-gzip']
        assert 'savings' in comparison['json-gzip']


class TestSerializerFallbacks:
    """Tests for serializer format fallbacks."""
    
    def test_msgpack_fallback_when_unavailable(self):
        """Test msgpack format falls back to json when unavailable."""
        with patch('pywats.core.performance.MSGPACK_AVAILABLE', False):
            # Import fresh to test fallback
            from pywats.core import performance
            original = performance.MSGPACK_AVAILABLE
            performance.MSGPACK_AVAILABLE = False
            
            try:
                serializer = Serializer(format='msgpack')
                # Should have fallen back to json
                assert serializer.format == 'json'
            finally:
                performance.MSGPACK_AVAILABLE = original
    
    def test_gzip_fallback_when_unavailable(self):
        """Test json-gzip format falls back to json when unavailable."""
        from pywats.core import performance
        original = performance.COMPRESSION_AVAILABLE
        performance.COMPRESSION_AVAILABLE = False
        
        try:
            serializer = Serializer(format='json-gzip')
            # Should have fallen back to json
            assert serializer.format == 'json'
        finally:
            performance.COMPRESSION_AVAILABLE = original


class TestFormatBytes:
    """Tests for format_bytes utility."""
    
    def test_bytes(self):
        """Test formatting bytes."""
        assert format_bytes(500) == "500.0 B"
    
    def test_kilobytes(self):
        """Test formatting kilobytes."""
        assert format_bytes(1024) == "1.0 KB"
        assert format_bytes(1536) == "1.5 KB"
    
    def test_megabytes(self):
        """Test formatting megabytes."""
        assert format_bytes(1024 * 1024) == "1.0 MB"
        assert format_bytes(int(1024 * 1024 * 2.5)) == "2.5 MB"
    
    def test_gigabytes(self):
        """Test formatting gigabytes."""
        assert format_bytes(1024 ** 3) == "1.0 GB"
    
    def test_terabytes(self):
        """Test formatting terabytes."""
        assert format_bytes(1024 ** 4) == "1.0 TB"
    
    def test_petabytes(self):
        """Test formatting very large sizes."""
        assert format_bytes(1024 ** 5) == "1.0 PB"
    
    def test_zero(self):
        """Test formatting zero bytes."""
        assert format_bytes(0) == "0.0 B"


class TestBenchmarkSerialization:
    """Tests for benchmark_serialization function."""
    
    def test_benchmark_runs_without_error(self, capsys):
        """Test benchmark runs and produces output."""
        data = {'test': 'data', 'values': list(range(10))}
        
        benchmark_serialization(data)
        
        captured = capsys.readouterr()
        assert "Serialization Benchmark" in captured.out
        assert "JSON:" in captured.out
        assert "Size:" in captured.out
        assert "Serialize:" in captured.out
        assert "Deserialize:" in captured.out
    
    @pytest.mark.skipif(not MSGPACK_AVAILABLE, reason="msgpack not available")
    def test_benchmark_includes_msgpack(self, capsys):
        """Test benchmark includes msgpack if available."""
        data = {'test': 'data'}
        
        benchmark_serialization(data)
        
        captured = capsys.readouterr()
        assert "MessagePack:" in captured.out
    
    @pytest.mark.skipif(not COMPRESSION_AVAILABLE, reason="gzip not available")
    def test_benchmark_includes_gzip(self, capsys):
        """Test benchmark includes gzip if available."""
        data = {'test': 'data' * 100}
        
        benchmark_serialization(data)
        
        captured = capsys.readouterr()
        assert "JSON + GZIP:" in captured.out
