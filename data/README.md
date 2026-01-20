# Data Directory Structure

This directory contains all data files used by the email reports pipeline.

## Directory Structure

```
data/
├── raw/                    # Raw input files
│   ├── dGerentes.xlsx     # Managers data (input)
│   └── resultados_powerbi.xlsx  # Power BI query results (historical)
├── processed/             # Processed data files
├── temp/                  # Temporary files (auto-cleaned)
└── README.md             # This file
```

## Raw Data Files

### dGerentes.xlsx
- **Purpose**: Contains manager information for email distribution
- **Location**: `data/raw/dGerentes.xlsx`
- **Required Columns**:
  - `Equipe`: Team code (integer)
  - `Nome da Equipe`: Manager name (string)
  - `Email`: Manager email address (string)
- **Validation**: Email format validation applied during extraction
- **Processing**: Duplicates removed, null values filtered

### resultados_powerbi.xlsx
- **Purpose**: Historical Power BI query results (reference)
- **Location**: `data/raw/resultados_powerbi.xlsx`
- **Usage**: Reference data, not used by pipeline
- **Format**: Raw Power BI export format

## Processed Data Files

The `data/processed/` directory will contain:
- Transformed data files (if pipeline is modified to save intermediate results)
- Aggregated reports
- Historical processing results

## Temporary Files

The `data/temp/` directory contains:
- Generated Excel reports for email attachments
- Automatically cleaned up after email sending
- No manual intervention required

## Data Flow

1. **Input**: `dGerentes.xlsx` → Managers Extractor
2. **Processing**: Power BI API → Data Transformer
3. **Output**: Temporary Excel files → Email Service → Cleanup

## Best Practices

- **Backup**: Regularly backup `dGerentes.xlsx`
- **Validation**: Ensure email addresses are valid before updates
- **Security**: This directory contains sensitive contact information
- **Monitoring**: Check logs for data quality issues

## File Permissions

- **Read**: Pipeline service account
- **Write**: Pipeline service account (for temp files)
- **Backup**: Administrative access

## Data Quality

The pipeline performs automatic data quality checks:
- Email format validation
- Duplicate detection
- Null value filtering
- Type conversion validation

## Troubleshooting

### Missing Files
If `dGerentes.xlsx` is missing, the pipeline will fail with:
```
FileNotFoundError: Managers file not found: data/raw/dGerentes.xlsx
```

### Invalid Data Format
If columns are missing or incorrectly named:
```
ValueError: Missing required columns: ['Equipe', 'Nome da Equipe', 'Email']
```

### Invalid Emails
If email addresses are invalid:
```
WARNING: Found X invalid email addresses
```

Check the pipeline logs for detailed error information.
