# Changelog

All notable changes to the pyWATS core API library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - TBD

### Added
- Complete domain-driven architecture with layered design
- Station configuration and metadata management
- Comprehensive logging support with `enable_debug_logging()`
- Enhanced Product module with full CRUD operations
- Asset management module with equipment tracking
- RootCause ticketing system integration
- Production module for serial number management
- Statistics and analytics capabilities
- Full type hints and Pydantic models
- Timezone-aware datetime handling

### Changed
- Restructured to layered architecture (Facade -> Service -> Repository)
- Improved error handling with custom exception hierarchy
- Enhanced data models with better validation
- Updated API endpoints to match WATS server specs
- Modernized HTTP client using httpx

### Deprecated
- Legacy module structure (will be removed in 3.0.0)

### Fixed
- Timezone handling in date/time fields
- Model serialization edge cases
- Authentication token handling

### Security
- Updated dependencies to address security vulnerabilities
- Improved credential handling

## [1.0.0] - Initial Release

### Added
- Initial release of pyWATS API library
- Basic WATS server communication
- Report submission (UUT/UUR)
- Product and asset management
- Basic query capabilities
