# GeoMozR - Geospatial Data for Mozambique

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/R-4.0%2B-blue.svg" alt="R Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
</p>

**GeoMozR** is an R package that provides easy access to geospatial data for Mozambique, including administrative boundaries (11 provinces, 161 districts, 459 admin posts, 11,524 villages) and complete geological data.

Inspired by the [`geobr`](https://github.com/ipeaGIT/geobr) package for Brazil.

---

## 🚀 Installation

```r
# Install from GitHub
remotes::install_github("geolithicamz-hub/geomozr")

# Or using pak
pak::pkg_install("geolithicamz-hub/geomozr")
```

---

## ⚡ Quick Start

```r
library(geomoz)
library(ggplot2)

# Load provinces
provinces <- read_province()
print(paste("Loaded", nrow(provinces), "provinces"))

# Plot with ggplot2
ggplot(provinces) +
  geom_sf(aes(fill = Provincia), color = "white", linewidth = 0.5) +
  scale_fill_viridis_d() +
  theme_minimal() +
  labs(title = "Provinces of Mozambique")

# Load districts from Nampula
nampula_districts <- read_district(name_province = "Nampula")

# Load villages (uses cache for performance)
villages <- read_village(name_province = "Nampula")

# Load geology data
geology <- read_geology(era = "Proterozoic")
```

---

## 📊 Available Data

| Dataset | Records | Function |
|---------|---------|----------|
| **Provinces** | 11 | `read_province()` |
| **Districts** | 161 | `read_district()` |
| **Admin Posts** | 459 | `read_admin_post()` |
| **Villages** | 11,524 | `read_village()` |
| **Geology** | ~50,000 | `read_geology()` |

---

## 🎨 Plotting Examples

### Plot Provinces
```r
plot_provinces(palette = "Set3")
```

### Plot Districts
```r
districts <- read_district(name_province = "Nampula")
plot_districts(districts, title = "Districts of Nampula")
```

### Custom ggplot
```r
library(ggplot2)

provinces <- read_province()
ggplot(provinces) +
  geom_sf(aes(fill = Provincia), color = "black", linewidth = 0.8) +
  scale_fill_viridis_d(option = "plasma") +
  theme_minimal() +
  labs(title = "Mozambique Provinces",
       fill = "Province") +
  theme(legend.position = "right",
        plot.title = element_text(hjust = 0.5, size = 16))
```

---

## 📚 Documentation

- [Full Documentation](https://github.com/geolithicamz-hub/geomozr/blob/main/README.md) - Detailed documentation
- [Examples](https://github.com/geolithicamz-hub/geomozr/tree/main/examples) - Code examples

---

## 🛠️ Development

```bash
git clone https://github.com/geolithicamz-hub/geomozr.git
cd geomozr
R CMD INSTALL .
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

**GeoMozR** - Geospatial data for Mozambique at your fingertips! 🗺️🇲🇿
