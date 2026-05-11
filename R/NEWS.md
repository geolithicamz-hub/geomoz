# News

## geomoz 0.1.0

* Initial CRAN release.
* Added functions to read Mozambique administrative boundaries:
  - `read_province()` - Load province boundaries (11 provinces)
  - `read_district()` - Load district boundaries (161 districts)
  - `read_admin_post()` - Load administrative post boundaries (459 posts)
  - `read_village()` - Load village/locality boundaries (11,524 villages)
* Added function to read geological data:
  - `read_geology()` - Load geological units (~50,000 features)
* Added plotting functions:
  - `plot_provinces()` - Create ggplot maps of provinces
  - `plot_districts()` - Create ggplot maps of districts
* Added cache management:
  - `cache_info()` - Display cache information
  - `clear_cache()` - Clear downloaded data cache
* Data is automatically downloaded from Hugging Face and cached locally.
