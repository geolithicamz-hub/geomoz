#' @title Cache Information
#' @description Display information about the geomoz cache
#' @return Invisible list with cache information
#' @export
#' @examples
#' \dontrun{
#' cache_info()
#' }
cache_info <- function() {
  cache_dir <- get_cache_dir()
  
  if (!dir.exists(cache_dir)) {
    message("Cache directory does not exist yet.")
    return(invisible(list(path = cache_dir, size = 0, files = 0)))
  }
  
  files <- list.files(cache_dir, full.names = TRUE)
  file_info <- file.info(files)
  total_size <- sum(file_info$size, na.rm = TRUE)
  
  message("=== GeoMoz Cache Information ===")
  message("Cache directory: ", cache_dir)
  message("Number of files: ", length(files))
  message("Total size: ", format(total_size, big.mark = ","), " bytes")
  message("=================================")
  
  if (length(files) > 0) {
    message("\nCached files:")
    for (f in files) {
      size <- file.info(f)$size
      mtime <- file.info(f)$mtime
      message(sprintf("  - %s (%s bytes, modified: %s)",
                     basename(f), format(size, big.mark = ","),
                     format(mtime, "%Y-%m-%d %H:%M")))
    }
  }
  
  invisible(list(
    path = cache_dir,
    size = total_size,
    files = length(files),
    file_list = files
  ))
}

#' @title Clear Cache
#' @description Clear the geomoz cache
#' @param older_than Remove files older than this many hours (default NULL = all)
#' @return Invisible logical indicating success
#' @export
#' @examples
#' \dontrun{
#' # Clear all cache
#' clear_cache()
#' 
#' # Clear files older than 48 hours
#' clear_cache(older_than = 48)
#' }
clear_cache <- function(older_than = NULL) {
  cache_dir <- get_cache_dir()
  
  if (!dir.exists(cache_dir)) {
    message("Cache directory does not exist.")
    return(invisible(FALSE))
  }
  
  files <- list.files(cache_dir, full.names = TRUE)
  
  if (length(files) == 0) {
    message("Cache is already empty.")
    return(invisible(TRUE))
  }
  
  if (is.null(older_than)) {
    # Remove all files
    file.remove(files)
    message("Cleared ", length(files), " cached file(s).")
  } else {
    # Remove files older than specified hours
    file_info <- file.info(files)
    file_age <- difftime(Sys.time(), file_info$mtime, units = "hours")
    old_files <- files[file_age > older_than]
    
    if (length(old_files) > 0) {
      file.remove(old_files)
      message("Cleared ", length(old_files), " file(s) older than ", 
              older_than, " hours.")
    } else {
      message("No files older than ", older_than, " hours found.")
    }
  }
  
  invisible(TRUE)
}
