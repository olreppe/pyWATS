# Data Models

This directory contains specifications for all data models used in the pyWATS API.

## Structure

Each data model should have its own markdown file describing:

- **Purpose**: What the model represents
- **Properties**: All fields with types and descriptions
- **Relationships**: How it relates to other models
- **Validation Rules**: Any constraints or validation logic
- **Examples**: Sample data instances

## Format

```markdown
# Model Name

## Purpose
Brief description of what this model represents.

## Properties

| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | string | Yes | Unique identifier |
| name | string | Yes | Display name |
| created_at | datetime | Yes | Creation timestamp |

## Relationships
- Belongs to: ParentModel
- Has many: ChildModels

## Validation Rules
- Field constraints
- Business rules

## Example
```json
{
  "id": "uuid-here",
  "name": "Example Name",
  "created_at": "2024-01-01T00:00:00Z"
}
```
```