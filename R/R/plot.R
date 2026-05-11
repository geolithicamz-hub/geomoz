#' @title Plot Provinces
#' @description Create a ggplot map of Mozambique provinces
#' @param data sf object with province data (optional). If NULL, reads all provinces
#' @param column Column name for coloring (default "Provincia")
#' @param palette Color palette name (default "viridis")
#' @param title Plot title
#' @return A ggplot object
#' @export
#' @examples
#' \dontrun{
#' # Plot all provinces
#' plot_provinces()
#' 
#' # Plot with custom palette
#' plot_provinces(palette = "Set3")
#' 
#' # Plot specific data
#' nampula <- read_province(name_province = "Nampula")
#' plot_provinces(nampula, title = "Nampula Province")
#' }
plot_provinces <- function(data = NULL, 
                           column = "Provincia", 
                           palette = "viridis",
                           title = "Provinces of Mozambique") {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    stop("ggplot2 is required for plotting. Install with: install.packages('ggplot2')")
  }
  
  if (is.null(data)) {
    data <- read_province()
  }
  
  ggplot2::ggplot(data) +
    ggplot2::geom_sf(ggplot2::aes(color = .data[[column]]), linewidth = 0.8) +
    ggplot2::scale_color_viridis_d(option = palette) +
    ggplot2::labs(title = title) +
    ggplot2::theme_minimal() +
    ggplot2::theme(
      legend.position = "right",
      plot.title = ggplot2::element_text(hjust = 0.5, size = 14)
    )
}

#' @title Plot Districts
#' @description Create a ggplot map of districts
#' @param data sf object with district data
#' @param column Column name for coloring (default "Distrito")
#' @param palette Color palette name (default "viridis")
#' @param title Plot title
#' @return A ggplot object
#' @export
#' @examples
#' \dontrun{
#' # Plot districts of Nampula
#' districts <- read_district(name_province = "Nampula")
#' plot_districts(districts, title = "Districts of Nampula")
#' }
plot_districts <- function(data,
                           column = "Distrito",
                           palette = "viridis", 
                           title = "Districts") {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    stop("ggplot2 is required for plotting. Install with: install.packages('ggplot2')")
  }
  
  ggplot2::ggplot(data) +
    ggplot2::geom_sf(ggplot2::aes(fill = .data[[column]]), color = "white", linewidth = 0.3) +
    ggplot2::scale_fill_viridis_d(option = palette) +
    ggplot2::labs(title = title) +
    ggplot2::theme_minimal() +
    ggplot2::theme(
      legend.position = "right",
      plot.title = ggplot2::element_text(hjust = 0.5, size = 14)
    )
}
