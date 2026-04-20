# 🚀 GeoMoz PyPI Publication Guide

This guide explains how to publish the GeoMoz package to PyPI for global distribution.

## 📋 Prerequisites

### Required Accounts
1. **PyPI Account**: Register at https://pypi.org/account/register/
2. **GitHub Access**: Push access to geolithicamz/geomoz repository
3. **Hugging Face**: Dataset already published at geolithicamz/geomoz-data

### Required Tools
```bash
pip install build twine wheel
```

## 🔧 Package Structure

The package is properly structured for PyPI:

```
geomoz/
├── geomoz/                    # Main package
│   ├── __init__.py           # Package initialization
│   ├── read_*.py             # Data reading functions
│   ├── spatial.py             # Spatial operations
│   ├── core.py               # Core functionality
│   └── utils/                # Utilities
│       ├── __init__.py
│       ├── data.py              # Hugging Face integration
│       └── utils.py             # Legacy utilities
├── setup.py                   # Legacy setup
├── pyproject.toml             # Modern build config
├── requirements.txt            # Dependencies
├── MANIFEST.in               # Package manifest
├── LICENSE                   # MIT License
├── README.md                 # Main documentation
├── README_PYPI.md           # PyPI-specific README
└── build_and_publish.py     # Build/publish script
```

## 🏗️ Build Process

### 1. Clean Previous Builds
```bash
python build_and_publish.py build
```

### 2. Test Installation
```bash
python build_and_publish.py test
```

### 3. Build Distribution Files
```bash
python build_and_publish.py build
```

## 📦 Distribution Files

After building, you'll find:
- `dist/geomoz-1.0.0-py3-none-any.whl` - Wheel distribution
- `dist/geomoz-1.0.0.tar.gz` - Source distribution

## 🚀 Publishing to PyPI

### Test Publication (Recommended)
```bash
python build_and_publish.py testpypi
```

### Production Publication
```bash
python build_and_publish.py pypi
```

## 🔐 Authentication

### Method 1: API Token (Recommended)
1. Generate PyPI API token at https://pypi.org/manage/account/token/
2. Set environment variable:
```bash
export TWINE_PASSWORD=pypi-xxxxxx
```

### Method 2: Username/Password
```bash
twine upload dist/* -u __username__ -p __password__
```

## 📋 Pre-Publishing Checklist

### ✅ Code Quality
- [ ] All functions documented with docstrings
- [ ] Type hints implemented
- [ ] Code formatted with black
- [ ] No linting errors (flake8)
- [ ] Tests passing (pytest)

### ✅ Package Structure
- [ ] pyproject.toml properly configured
- [ ] All required dependencies listed
- [ ] Version number updated
- [ ] License file included
- [ ] README files updated

### ✅ Functionality
- [ ] Hugging Face integration working
- [ ] CRS handling automatic
- [ ] Cache system functional
- [ ] All read_* functions working
- [ ] Spatial functions working

## 🧪 Testing After Publication

### Install from PyPI
```bash
# Create fresh environment
python -m venv test_env
source test_env/bin/activate

# Install from PyPI
pip install geomoz

# Test basic functionality
python -c "
import geomoz
provinces = geomoz.read_province()
print(f'Loaded {len(provinces)} provinces')
"
```

### Install with Extras
```bash
# Test complete installation
pip install geomoz[complete]

# Test with visualization
python -c "
import geomoz
import matplotlib.pyplot as plt
provinces = geomoz.read_province()
provinces.plot()
plt.savefig('test.png')
print('Visualization test passed')
"
```

## 🔄 Version Management

### Semantic Versioning
- **Major**: Breaking changes (2.0.0)
- **Minor**: New features (1.1.0)
- **Patch**: Bug fixes (1.0.1)

### Update Process
1. Update version in `pyproject.toml`
2. Update version in `setup.py`
3. Update CHANGELOG.md
4. Commit changes
5. Build and publish

## 📊 Distribution Channels

### Primary: PyPI
- **URL**: https://pypi.org/project/geomoz/
- **Install**: `pip install geomoz`
- **Audience**: General users, developers

### Secondary: GitHub
- **URL**: https://github.com/geolithicamz/geomoz
- **Source**: Development version
- **Issues**: Bug tracking and feature requests

### Data: Hugging Face
- **URL**: https://huggingface.co/geolithicamz/geomoz-data
- **Purpose**: Dataset distribution
- **Integration**: Automatic download and caching

## 🎯 Success Metrics

### Installation Success
```bash
# Track downloads
pip install geomoz
python -c "import geomoz; print('✅ Installation successful')"
```

### Functionality Verification
```python
import geomoz

# Test core functionality
try:
    provinces = geomoz.read_province()
    geology = geomoz.read_geology()
    geo_zambezia = geomoz.geology_by_province(name_province="Zambézia")
    area = geomoz.calculate_area(geo_zambezia)
    
    print("✅ All core functions working")
    print(f"✅ Provinces: {len(provinces)}")
    print(f"✅ Geology units: {len(geology)}")
    print(f"✅ Zambézia geology: {len(geo_zambezia)}")
    print(f"✅ Area calculation: {area['area_km2'].sum():.2f} km²")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

## 🆘 Troubleshooting

### Common Issues

#### Build Errors
```bash
# Missing build tools
pip install --upgrade build wheel setuptools

# Python not found
python3 -m build  # Use python3 explicitly
```

#### Upload Errors
```bash
# Authentication failed
twine check dist/*  # Check package first
twine upload --repository testpypi dist/*  # Try test PyPI first

# File exists error
rm -rf dist/*
python build  # Rebuild
```

#### Import Errors
```bash
# Missing dependencies
pip install -r requirements.txt

# Path issues
python -c "import sys; print(sys.path)"
```

## 📞 Support Resources

### Documentation
- **Main README**: README.md
- **PyPI README**: README_PYPI.md
- **API Docs**: Inline docstrings

### Community
- **Issues**: https://github.com/geolithicamz/geomoz/issues
- **Discussions**: https://github.com/geolithicamz/geomoz/discussions
- **Wiki**: https://github.com/geolithicamz/geomoz/wiki

### Contacts
- **Email**: contact@geolithica.org
- **Organization**: Geolithica

---

## 🎉 Publication Success!

Once published successfully:

1. **Verify**: Check https://pypi.org/project/geomoz/
2. **Announce**: Share with community
3. **Monitor**: Track downloads and issues
4. **Maintain**: Update based on user feedback

**GeoMoz will be available globally via `pip install geomoz`!** 🇲🇿
