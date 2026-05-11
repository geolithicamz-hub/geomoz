#' @title Read Village Data
#' @description Load village/locality boundaries for Mozambique.
#' Note: This dataset is large (11,524 features). Use cache for better performance.
#' @param code_village Village code (optional)
#' @param name_village Village name (optional)
#' @param name_admin_post Admin post name to filter (optional)
#' @param name_district District name to filter (optional)
#' @param name_province Province name to filter (optional)
#' @param use_cache Use cached data if available (default TRUE)
#' @return An sf object with village boundaries
#' @export
#' @examples
#' \dontrun{
#' # Read all villages (uses cache)
#' villages <- read_village()
#' 
#' # Read villages from Nampula
#' nampula_villages <- read_village(name_province = "Nampula")
#' 
#' # Read specific village
#' village <- read_village(name_village = "Cidade de Nampula")
#' }
read_village <- function(code_village = NULL,
                         name_village = NULL,
                         name_admin_post = NULL,
                         name_district = NULL,
                         name_province = NULL,
                         use_cache = TRUE) {
  # Download data if needed
  file_path <- download_from_hf("villages.gpkg", force_download = !use_cache)
  
  # Read with sf
  data <- sf::st_read(file_path, quiet = TRUE)
  
  # Filter if code specified
  if (!is.null(code_village)) {
    code_str <- sprintf("%03d", as.integer(code_village))
    data <- data[data$CodPov == code_str, ]
  }
  
  # Filter if name_village specified
  if (!is.null(name_village)) {
    data <- data[grepl(name_village, data$Povoacao, ignore.case = TRUE), ]
  }
  
  # Filter if name_admin_post specified
  if (!is.null(name_admin_post)) {
    data <- data[grepl(name_admin_post, data$Posto, ignore.case = TRUE), ]
  }
  
  # Filter if name_district specified
  if (!is.null(name_district)) {
    data <- data[grepl(name_district, data$Distrito, ignore.case = TRUE), ]
  }
  
  # Filter if name_province specified
  if (!is.null(name_province)) {
    data <- data[grepl(name_province, data$Provincia, ignore.case = TRUE), ]
  }
  
  return(data)
}
