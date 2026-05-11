#' @title GeoMoz Utility Functions
#' @description Internal utility functions for the geomoz package
#' @keywords internal

#' Get cache directory for geomoz
#' @return Path to cache directory
#' @keywords internal
get_cache_dir <- function() {
  cache_dir <- rappdirs::user_cache_dir("geomoz", "geolithica")
  if (!dir.exists(cache_dir)) {
    dir.create(cache_dir, recursive = TRUE, showWarnings = FALSE)
  }
  return(cache_dir)
}

#' Get path to cached file
#' @param filename Name of the file
#' @return Full path to cached file
#' @keywords internal
get_cache_path <- function(filename) {
  file.path(get_cache_dir(), filename)
}

#' Check if file is in cache and not expired
#' @param filename Name of the file
#' @param max_age Maximum age in hours (default 24)
#' @return TRUE if cache is valid, FALSE otherwise
#' @keywords internal
cache_exists <- function(filename, max_age = 24) {
  cache_path <- get_cache_path(filename)
  if (!file.exists(cache_path)) {
    return(FALSE)
  }
  
  # Check if cache is expired
  file_age <- difftime(Sys.time(), file.mtime(cache_path), units = "hours")
  if (file_age > max_age) {
    return(FALSE)
  }
  
  return(TRUE)
}

#' Download file from Hugging Face
#' @param filename Name of the file on Hugging Face
#' @param force_download If TRUE, download even if cache exists
#' @return Path to downloaded file
#' @keywords internal
download_from_hf <- function(filename, force_download = FALSE) {
  cache_path <- get_cache_path(filename)
  
  # Check cache
  if (!force_download && cache_exists(filename)) {
    return(cache_path)
  }
  
  # Build Hugging Face URL
  repo_id <- "geolithicamz/geomoz-data"
  url <- sprintf(
    "https://huggingface.co/datasets/%s/resolve/main/%s",
    repo_id, filename
  )
  
  # Download with httr2
  req <- httr2::request(url)
  req <- httr2::req_options(req, ssl_verifypeer = 0L)
  
  # Download to cache
  tryCatch({
    httr2::req_perform(req, path = cache_path)
    return(cache_path)
  }, error = function(e) {
    # Try alternative method
    download.file(url, cache_path, mode = "wb", quiet = TRUE)
    return(cache_path)
  })
}

#' List available datasets from Hugging Face
#' @return Character vector of available dataset names
#' @keywords internal
list_hf_datasets <- function() {
  datasets <- c(
    "provinces.gpkg",
    "districts.gpkg",
    "admin_posts.gpkg",
    "villages.gpkg",
    "geology.gpkg"
  )
  return(datasets)
}
