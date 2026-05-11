#' @title Read Province Data
#' @description Load province boundaries for Mozambique
#' @param code_province Province code (optional). If NULL, returns all provinces
#' @param name_province Province name (optional). If NULL, returns all provinces
#' @return An sf object with province boundaries
#' @export
#' @examples
#' \dontrun{
#' # Read all provinces
#' provinces <- read_province()
#' 
#' # Read specific province by code
#' maputo <- read_province(code_province = "01")
#' 
#' # Read specific province by name
#' nampula <- read_province(name_province = "Nampula")
#' }
read_province <- function(code_province = NULL, name_province = NULL) {
  # Download data if needed
  file_path <- download_from_hf("provinces.gpkg")
  
  # Read with sf
  data <- sf::st_read(file_path, quiet = TRUE)
  
  # Filter if code_province specified
  if (!is.null(code_province)) {
    code_str <- sprintf("%02d", as.integer(code_province))
    data <- data[data$CodProv == code_str, ]
  }
  
  # Filter if name_province specified
  if (!is.null(name_province)) {
    data <- data[grepl(name_province, data$Provincia, ignore.case = TRUE), ]
  }
  
  return(data)
}
