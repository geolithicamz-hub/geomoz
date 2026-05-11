#' @title Read Geology Data
#' @description Load geological units for Mozambique
#' @param code_geology Geological unit code (optional)
#' @param name_geology Geological unit name/legend (optional)
#' @param era Geological era to filter (optional). Options: "Archean", 
#'   "Proterozoic", "Paleozoic", "Mesozoic", "Cenozoic"
#' @param rock_type Rock type to filter (optional)
#' @return An sf object with geological units
#' @export
#' @examples
#' \dontrun{
#' # Read all geology
#' geology <- read_geology()
#' 
#' # Filter by era
#' proterozoic <- read_geology(era = "Proterozoic")
#' 
#' # Filter by rock type
#' granites <- read_geology(rock_type = "granite")
#' }
read_geology <- function(code_geology = NULL,
                         name_geology = NULL,
                         era = NULL,
                         rock_type = NULL) {
  # Download data if needed
  file_path <- download_from_hf("geology.gpkg")
  
  # Read with sf
  data <- sf::st_read(file_path, quiet = TRUE)
  
  # Filter if code specified
  if (!is.null(code_geology)) {
    data <- data[data$code2006 == code_geology, ]
  }
  
  # Filter if name_geology/legend specified
  if (!is.null(name_geology)) {
    data <- data[grepl(name_geology, data$Legend, ignore.case = TRUE), ]
  }
  
  # Filter if era specified
  if (!is.null(era)) {
    data <- data[grepl(era, data$ERA, ignore.case = TRUE), ]
  }
  
  # Filter if rock_type specified
  if (!is.null(rock_type)) {
    data <- data[grepl(rock_type, data$ROCKTYPE1, ignore.case = TRUE) |
                   grepl(rock_type, data$ROCKTYPE2, ignore.case = TRUE), ]
  }
  
  return(data)
}
