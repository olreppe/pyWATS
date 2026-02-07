# Vte.DataAccess (skeleton)

Minimal, production-oriented starting point for reading a VTE SQL Server database and composing test runs for upload to WATS.

## Quick start

```csharp
using Microsoft.Extensions.Logging.Abstractions;
using Vte.DataAccess;

var opts = new VteDbOptions
{
    ConnectionString = "Server=...;Database=VTE9_3;Trusted_Connection=True;",
    Schema = "dbo"
};

var repo = new VteRepository(new SqlConnectionFactory(opts), NullLogger<VteRepository>.Instance, opts);

await foreach (var run in repo.StreamTestRunsSinceAsync(DateTime.UtcNow.AddDays(-1)))
{
    // TODO: map to WATS and upload
}
```

## Notes
- Validate column names/types against your deployment using the VTE create scripts.
- This library intentionally keeps SQL explicit and easy to audit.
