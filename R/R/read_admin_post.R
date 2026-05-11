#' @title Read Administrative Post Data
#' @description Load administrative post boundaries for Mozambique
#' @param code_admin_post Admin post code (optional)
#' @param name_admin_post Admin post name (optional)
#' @param name_district District name to filter (optional)
#' @param name_province Province name to filter (optional)
#' @return An sf object with admin post boundaries
#' @export
#' @examples
#' \dontrun{
#' # Read all admin posts
#' posts <- read_admin_post()
#' 
#' # Read admin posts from Nampula province
#' nampula_posts <- read_admin_post(name_province = "Nampula")
#' }
read_admin_post <- function(code_admin_post = NULL,
                            name_admin_post = NULL,
                            name_district = NULL,
                            name_province = NULL) {
  # Download data if needed
  file_path <- download_from_hf("admin_posts.gpkg")
  
  # Read with sf
  data <- sf::st_read(file_path, quiet = TRUE)
  
  # Filter if code specified
  if (!is.null(code_admin_post)) {
    code_str <- sprintf("%03d", as.integer(code_admin_post))
    data <- data[data$CodPosto == code_str, ]
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
