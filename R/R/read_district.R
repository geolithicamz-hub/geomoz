#' @title Read District Data
#' @description Load district boundaries for Mozambique
#' @param code_district District code (optional)
#' @param name_district District name (optional)
#' @param name_province Province name to filter districts (optional)
#' @return An sf object with district boundaries
#' @export
#' @examples
#' \dontrun{
#' # Read all districts
#' districts <- read_district()
#' 
#' # Read districts from specific province
#' nampula_districts <- read_district(name_province = "Nampula")
#' }
read_district <- function(code_district = NULL, 
                          name_district = NULL, 
                          name_province = NULL) {
  # Download data if needed
  file_path <- download_from_hf("districts.gpkg")
  
  # Read with sf
  data <- sf::st_read(file_path, quiet = TRUE)
  
  # Filter if code_district specified
  if (!is.null(code_district)) {
    code_str <- sprintf("%02d", as.integer(code_district))
    data <- data[data$CodDist == code_str, ]
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
