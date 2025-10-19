# Scripts Directory

Utility scripts used for verification and maintenance of the Rambam Mitzvot Schedule.

## 📋 Script Descriptions

### Verification Scripts
- **`verify_all_sources.py`** - Comprehensive verification of all 613 biblical sources against master list
- **`simple_test_bot.py`** - Local testing utility for bot functionality

### Correction Scripts  
- **`apply_source_corrections.py`** - Original source correction tool with backup and preview
- **`apply_final_corrections.py`** - Final 10 corrections to achieve 100% consistency

### Deployment Scripts
- **`create_lambda_package.bat`** - Windows batch script to create AWS Lambda deployment package

## 🚀 Usage Examples

### Verify All Sources
```bash
python scripts/verify_all_sources.py
```

### Test Bot Locally
```bash 
python scripts/simple_test_bot.py 2025-11-02
```

### Create Lambda Package
```batch
scripts\create_lambda_package.bat
```

## ⚠️ Important Notes

- Always run verification after making changes to the schedule
- Keep backups before applying corrections
- Test locally before deploying to Lambda

---

All scripts are preserved for future maintenance and verification needs.
